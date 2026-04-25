"""Orchestrates the 3-source parallel fetch for Add Card."""
from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional
import threading

from config import USD_TO_THB

logger = logging.getLogger(__name__)

# ── Persistent Playwright browser for live search ──
_BROWSER_CONTEXT = None
_BROWSER_LOCK = threading.Lock()
_BROWSER_LAST_USED = None
_BROWSER_TIMEOUT = 300  # 5 minutes inactivity timeout

# ── Simple query cache (LRU with TTL) ──
_SEARCH_CACHE = {}
_CACHE_TTL = 300  # 5 minutes (prefix-aware)

# ── In-flight coalescing: if the same query is already running, share its task ──
_INFLIGHT_TASKS: dict = {}  # normalized_query -> asyncio.Task

# Generic terms that explode result sets — treat as "too broad"
_GENERIC_TERMS = {
    "pokemon", "pokémon", "psa", "japanese", "japan", "card", "cards",
    "holo", "rare", "art", "full", "gold", "silver", "promo",
}


def _normalize_query(q: str) -> str:
    """Lowercase, strip, collapse whitespace, sort tokens for cache-friendly keys."""
    if not q:
        return ""
    tokens = re.sub(r'[^\w\s#/-]', ' ', q.lower()).split()
    return " ".join(sorted(tokens))


def _is_too_broad(q: str) -> bool:
    """True if the query is a single generic term that would return unhelpful noise."""
    tokens = [t for t in re.sub(r'[^\w\s]', ' ', q.lower()).split() if t]
    if not tokens:
        return True
    # If every token is generic, the query has no discriminating signal
    return all(t in _GENERIC_TERMS for t in tokens)


async def _fetch_psa_cert_details(cert: str) -> dict:
    """Fetch PSA cert details from cert page using Playwright."""
    try:
        from playwright.async_api import async_playwright

        url = f"https://www.psacard.com/cert/{cert}"

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2000)

                # Extract text content
                text = await page.text_content("body")

                # Extract basic info from page (subject, grade, set, etc)
                # Pattern: "SUBJECT", "Grade: 10", etc.
                subject_match = re.search(r'([A-Z\s\-]+)\n', text[:500])
                grade_match = re.search(r'Grade[:\s]+(\d+)', text)

                subject = subject_match.group(1).strip() if subject_match else "UNKNOWN"
                grade = int(grade_match.group(1)) if grade_match else 9

                # Try to get image
                image_url = None
                og_image = await page.query_selector('meta[property="og:image"]')
                if og_image:
                    image_url = await og_image.get_attribute("content")

                return {
                    "cert": cert,
                    "subject": subject,
                    "grade": grade,
                    "year": 0,
                    "set": "",
                    "card_number": "",
                    "variety": "",
                    "item": f"{subject} PSA {grade}",
                    "psa_estimate": None,
                    "image_url": image_url,
                }
            finally:
                await context.close()
                await browser.close()
    except Exception as e:
        logger.warning(f"PSA cert fetch failed for {cert}: {e}")
        raise ValueError(f"Could not fetch PSA cert {cert}: {e}")


@dataclass
class PreviewCard:
    """Complete card preview for Add Card UI."""
    cert: str
    # identity (from PSA)
    item: str
    year: int
    set_name: str
    card_number: str
    subject: str
    variety: str
    grade: int
    # prices
    collectr_url: Optional[str]
    collectr_price_thb: Optional[float]
    psa_estimate_thb: Optional[float]
    ebay_avg_thb: Optional[float]
    ebay_n_comps: int
    # images
    psa_image_ok: bool
    collectr_image_ok: bool
    image_match_ok: bool
    # signal (computed)
    signal: str
    risk_level: str
    upside_pct: float
    confidence: float
    # errors per source
    errors: dict


async def _fetch_psa_async(cert: str) -> dict:
    """Fetch PSA cert details asynchronously."""
    try:
        result = await _fetch_psa_cert_details(cert)
        return result
    except Exception as e:
        logger.warning(f"PSA fetch failed for {cert}: {e}")
        return {"error": str(e)}


async def _fetch_collectr_async(cert: str) -> dict:
    """Fetch Collectr data for a cert (if it exists in registry)."""
    try:
        from collectr_live_fetcher import CARD_REGISTRY, fetch_one_async
        from collectr_connector import get_collectr_url_for_cert

        # Find card in registry by cert
        matching_card = None
        for card in CARD_REGISTRY:
            if card.get("cert") == cert:
                matching_card = card
                break

        if not matching_card or not matching_card.get("url"):
            # Try to resolve URL from cert
            url = get_collectr_url_for_cert(cert)
            if not url:
                logger.info(f"No Collectr listing for cert {cert}")
                return {"collectr_url": None, "collectr_price_thb": None}

            matching_card = {
                "url": url,
                "subject": "UNKNOWN",
                "card_number": "UNKNOWN",
                "grade": 9,  # default
            }

        # Fetch Collectr price
        result = await fetch_one_async(matching_card)
        return result
    except Exception as e:
        logger.warning(f"Collectr fetch failed for {cert}: {e}")
        return {"error": str(e)}


async def _fetch_ebay_async(subject: str, grade: int) -> dict:
    """Fetch eBay comps for a subject+grade."""
    try:
        from ebay_connector import search_ebay_sold, filter_comps, compute_stats

        query = f"{subject} PSA {grade}"
        comps = search_ebay_sold(query, max_results=30)

        # Dummy card dict for filtering
        dummy_card = {"grade": str(grade), "subject": subject}
        filtered = filter_comps(comps, dummy_card)

        if not filtered:
            logger.info(f"No valid eBay comps for {query}")
            return {"ebay_avg_thb": None, "ebay_n_comps": 0, "ebay_comps": []}

        stats = compute_stats(filtered)
        avg_usd = stats.get("avg_price_usd", 0)
        avg_thb = avg_usd * USD_TO_THB if avg_usd else None

        return {
            "ebay_avg_thb": round(avg_thb, 2) if avg_thb else None,
            "ebay_n_comps": len(filtered),
            "ebay_comps": filtered,
        }
    except Exception as e:
        logger.warning(f"eBay fetch failed for {subject}/{grade}: {e}")
        return {"ebay_avg_thb": None, "ebay_n_comps": 0, "ebay_comps": [], "error": str(e)}


async def search(cert: str) -> PreviewCard:
    """Parallel fetch PSA + Collectr + eBay using asyncio.gather."""

    logger.info(f"Starting parallel fetch for cert {cert}")

    # Fetch PSA first (identity is mandatory)
    psa_data = await _fetch_psa_async(cert)
    if psa_data.get("error") or not psa_data.get("subject"):
        raise ValueError(f"PSA cert {cert} not found or fetch failed")

    # Extract identity from PSA
    subject = psa_data.get("subject", "UNKNOWN")
    grade = int(psa_data.get("grade", 9))
    year = int(psa_data.get("year", 0))
    set_name = psa_data.get("set", "")
    card_number = psa_data.get("card_number", "")
    variety = psa_data.get("variety", "")
    item = psa_data.get("item", "")

    # Fetch Collectr and eBay in parallel
    collectr_data, ebay_data = await asyncio.gather(
        _fetch_collectr_async(cert),
        _fetch_ebay_async(subject, grade),
        return_exceptions=True,
    )

    # Handle exceptions
    if isinstance(collectr_data, Exception):
        collectr_data = {"error": str(collectr_data)}
    if isinstance(ebay_data, Exception):
        ebay_data = {"error": str(ebay_data)}

    # Extract data
    collectr_url = collectr_data.get("collectr_url")
    collectr_price_usd = collectr_data.get("collectr_price")
    collectr_price_thb = (collectr_price_usd * USD_TO_THB) if collectr_price_usd else None

    psa_estimate_usd = psa_data.get("psa_estimate")
    psa_estimate_thb = (psa_estimate_usd * USD_TO_THB) if psa_estimate_usd else None

    ebay_avg_thb = ebay_data.get("ebay_avg_thb")
    ebay_n_comps = ebay_data.get("ebay_n_comps", 0)
    ebay_comps = ebay_data.get("ebay_comps", [])

    # Image validation
    psa_image_ok = psa_data.get("image_url") is not None
    collectr_image_ok = collectr_data.get("image_url") is not None
    image_match_ok = False  # Will be validated later in UI

    # Compute signal (without my_cost, shows as REVIEW)
    signal_data = _compute_signal(
        my_cost=None,
        collectr_price_thb=collectr_price_thb,
        psa_estimate_thb=psa_estimate_thb,
        ebay_avg_thb=ebay_avg_thb,
        ebay_comps=ebay_comps,
    )

    return PreviewCard(
        cert=cert,
        item=item,
        year=year,
        set_name=set_name,
        card_number=card_number,
        subject=subject,
        variety=variety,
        grade=grade,
        collectr_url=collectr_url,
        collectr_price_thb=collectr_price_thb,
        psa_estimate_thb=psa_estimate_thb,
        ebay_avg_thb=ebay_avg_thb,
        ebay_n_comps=ebay_n_comps,
        psa_image_ok=psa_image_ok,
        collectr_image_ok=collectr_image_ok,
        image_match_ok=image_match_ok,
        signal=signal_data["signal"],
        risk_level=signal_data["risk_level"],
        upside_pct=signal_data["upside_pct"],
        confidence=signal_data["confidence"],
        errors={
            "psa": psa_data.get("error"),
            "collectr": collectr_data.get("error"),
            "ebay": ebay_data.get("error"),
        },
    )


def _compute_signal(my_cost: Optional[float], collectr_price_thb: Optional[float],
                    psa_estimate_thb: Optional[float], ebay_avg_thb: Optional[float],
                    ebay_comps: list) -> dict:
    """Compute signal for preview (simplified, without full confidence logic)."""

    # Use best available price as market_value
    market_value = ebay_avg_thb or psa_estimate_thb or collectr_price_thb

    if not market_value:
        return {
            "signal": "REVIEW",
            "risk_level": "HIGH",
            "confidence": 20,
            "upside_pct": 0,
            "liquidity": "LOW",
        }

    if my_cost is None:
        # No cost yet — always show REVIEW
        return {
            "signal": "REVIEW",
            "risk_level": "MEDIUM",
            "confidence": 50 + min(len(ebay_comps), 10) * 5,
            "upside_pct": 0,
            "liquidity": "MEDIUM" if len(ebay_comps) >= 4 else "LOW",
        }

    # Compute upside
    upside_pct = ((market_value - my_cost) / my_cost * 100) if my_cost > 0 else 0

    # Simple signal logic
    liquidity = "HIGH" if len(ebay_comps) >= 8 else "MEDIUM" if len(ebay_comps) >= 4 else "LOW"
    confidence = min(100, 60 + len(ebay_comps) * 5)

    if upside_pct > 15 and liquidity in ["HIGH", "MEDIUM"]:
        signal = "BUY"
        risk_level = "LOW" if liquidity == "HIGH" else "MEDIUM"
    elif upside_pct < -15:
        signal = "SELL"
        risk_level = "HIGH"
    else:
        signal = "HOLD"
        risk_level = "MEDIUM"

    return {
        "signal": signal,
        "risk_level": risk_level,
        "confidence": confidence,
        "upside_pct": upside_pct,
        "liquidity": liquidity,
    }


# ──────────────────────────────────────────────────────────────────────────────
# LIVE SEARCH FUNCTIONS (delta spec)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Candidate:
    """A candidate card from live search."""
    source: str  # "collectr" | "ebay"
    title: str
    subject: str
    set: Optional[str] = None
    card_number: Optional[str] = None
    variety: Optional[str] = None
    year: Optional[int] = None
    grade: Optional[int] = None
    product_id: Optional[str] = None
    url: str = ""
    thumbnail_url: Optional[str] = None
    price_thb: Optional[float] = None
    ebay_n_comps: Optional[int] = None
    owned: bool = False
    owned_count: int = 0
    score: float = 0.0


async def _get_persistent_browser():
    """Lazily initialize and return persistent Playwright browser."""
    global _BROWSER_CONTEXT, _BROWSER_LAST_USED

    with _BROWSER_LOCK:
        _BROWSER_LAST_USED = time.time()

        if _BROWSER_CONTEXT is not None:
            return _BROWSER_CONTEXT

        try:
            from playwright.async_api import async_playwright
            pw = await async_playwright().start()
            browser = await pw.chromium.launch(headless=True)
            _BROWSER_CONTEXT = browser
            logger.info("Persistent Playwright browser initialized")
            return _BROWSER_CONTEXT
        except Exception as e:
            logger.error(f"Failed to initialize persistent browser: {e}")
            raise


def _search_local_registry(query: str) -> list[Candidate]:
    """
    Fast local fallback: fuzzy-match query against CARD_REGISTRY by subject/card_number.
    Returns instantly — no network. Used as primary source so UI never feels "dead".
    """
    try:
        from collectr_live_fetcher import CARD_REGISTRY
    except Exception:
        return []

    q_tokens = [t for t in re.sub(r'[^\w\s]', ' ', query.lower()).split() if t]
    if not q_tokens:
        return []

    results = []
    for card in CARD_REGISTRY:
        subject = (card.get("subject") or "").lower()
        card_num = str(card.get("card_number") or "")
        haystack = f"{subject} {card_num}".lower()

        # Score: count matching tokens (any-token substring match)
        match_count = sum(1 for t in q_tokens if t in haystack)
        if match_count == 0:
            continue

        url = card.get("url") or ""
        product_id = None
        if url:
            m = re.search(r'/product/(\d+)', url)
            if m:
                product_id = m.group(1)

        # Use our own /card-img proxy so thumbnails work from cached images
        thumb = f"/card-img/{product_id}" if product_id else None

        results.append(Candidate(
            source="local",
            title=f"{card.get('subject')} #{card_num} PSA {card.get('grade')}",
            subject=card.get("subject"),
            card_number=card_num,
            grade=card.get("grade"),
            product_id=product_id,
            url=url,
            thumbnail_url=thumb,
            score=match_count * 50.0,  # local matches outrank weak web matches
        ))

    return results


async def _search_collectr(query: str, timeout: float = 2.0) -> list[Candidate]:
    """
    Search Collectr using Playwright.
    Navigate to search URL, scrape result tiles.
    """
    try:
        from playwright.async_api import async_playwright

        browser = await _get_persistent_browser()
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()

        try:
            search_url = f"https://app.getcollectr.com/search?q={query}"
            try:
                await asyncio.wait_for(
                    page.goto(search_url, wait_until="domcontentloaded"),
                    timeout=timeout
                )
            except (asyncio.TimeoutError, Exception):
                return []  # Page never loaded — likely auth wall

            # Bail fast if redirected to login (Collectr is gated)
            current_url = page.url or ""
            if "login" in current_url.lower() or "signin" in current_url.lower():
                logger.debug("Collectr redirected to login — skipping")
                return []

            # Wait briefly for results; if not present, give up (don't burn full budget)
            try:
                await asyncio.wait_for(
                    page.wait_for_selector('[data-testid="product-tile"]', timeout=int(timeout * 500)),
                    timeout=timeout * 0.5
                )
            except Exception:
                return []  # No results selector — gracefully bail

            # Extract result tiles
            results = []
            tiles = await page.query_selector_all('[data-testid="product-tile"]')

            for tile in tiles:
                try:
                    # Extract title, price, URL, image
                    title_elem = await tile.query_selector('h3, [class*="title"]')
                    price_elem = await tile.query_selector('[class*="price"]')
                    link_elem = await tile.query_selector('a[href*="/product/"]')
                    img_elem = await tile.query_selector('img')

                    title = await title_elem.text_content() if title_elem else ""
                    price_text = await price_elem.text_content() if price_elem else None
                    url = await link_elem.get_attribute("href") if link_elem else ""
                    thumbnail = await img_elem.get_attribute("src") if img_elem else None

                    # Parse price from text like "$123.45"
                    price_thb = None
                    if price_text:
                        price_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)', price_text)
                        if price_match:
                            price_usd = float(price_match.group(1).replace(',', ''))
                            price_thb = round(price_usd * USD_TO_THB, 2)

                    # Extract product ID from URL
                    product_id = None
                    if url:
                        pid_match = re.search(r'/product/(\d+)', url)
                        if pid_match:
                            product_id = pid_match.group(1)
                        if not url.startswith('http'):
                            url = f"https://app.getcollectr.com{url}"

                    # Parse card details from title
                    subject, set_name, card_number, variety, year, grade = _parse_card_title(title)

                    candidate = Candidate(
                        source="collectr",
                        title=title.strip() if title else "",
                        subject=subject,
                        set=set_name,
                        card_number=card_number,
                        variety=variety,
                        year=year,
                        grade=grade,
                        product_id=product_id,
                        url=url,
                        thumbnail_url=thumbnail,
                        price_thb=price_thb,
                    )
                    results.append(candidate)
                except Exception as e:
                    logger.debug(f"Error parsing Collectr tile: {e}")
                    continue

            logger.info(f"Collectr search returned {len(results)} results for '{query}'")
            return results
        finally:
            await context.close()
    except asyncio.TimeoutError:
        logger.warning(f"Collectr search timed out for '{query}'")
        return []
    except Exception as e:
        logger.warning(f"Collectr search failed for '{query}': {e}")
        return []


async def _search_ebay(query: str, timeout: float = 5.0) -> list[Candidate]:
    """
    Search eBay sold listings using ebay_connector.
    """
    try:
        from ebay_connector import search_ebay_sold

        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        comps = await asyncio.wait_for(
            loop.run_in_executor(None, search_ebay_sold, query, 20),
            timeout=timeout
        )

        results = []
        for comp in comps:
            title = comp.get("title", "")
            price_usd = comp.get("total_price") or comp.get("sold_price")
            price_thb = round(price_usd * USD_TO_THB, 2) if price_usd else None

            # Parse card details from title
            subject, set_name, card_number, variety, year, grade = _parse_card_title(title)

            candidate = Candidate(
                source="ebay",
                title=title,
                subject=subject,
                set=set_name,
                card_number=card_number,
                variety=variety,
                year=year,
                grade=grade,
                url=comp.get("url", ""),
                thumbnail_url=comp.get("thumbnail"),
                price_thb=price_thb,
                ebay_n_comps=1,  # Each comp is one listing
            )
            results.append(candidate)

        logger.info(f"eBay search returned {len(results)} results for '{query}'")
        return results
    except asyncio.TimeoutError:
        logger.warning(f"eBay search timed out for '{query}'")
        return []
    except Exception as e:
        logger.warning(f"eBay search failed for '{query}': {e}")
        return []


async def _search_pokemon_tcg(query: str, timeout: float = 3.0) -> list[Candidate]:
    """
    Reliable identity + thumbnail source backed by pokemontcg.io and TCGdex.
    Used as a primary backup when eBay is blocked/slow or Collectr times out.
    Returns Candidate objects with source='pokemontcg' or 'tcgdex'.
    """
    try:
        from pokemon_tcg_connector import search_pokemon_tcg

        loop = asyncio.get_event_loop()
        rows = await asyncio.wait_for(
            loop.run_in_executor(None, search_pokemon_tcg, query, 20),
            timeout=timeout,
        )

        results: list[Candidate] = []
        for row in rows or []:
            title = row.get("title", "") or ""
            # Pokemon TCG APIs don't expose PSA grade — treat as ungraded identity.
            # _parse_card_title still gives us year/variety heuristics if present.
            _subject, _set_name, _card_number, variety, _year, grade = _parse_card_title(title)

            results.append(
                Candidate(
                    source=row.get("source", "pokemontcg"),
                    title=title,
                    subject=row.get("subject") or _subject or "",
                    set=row.get("set") or _set_name,
                    card_number=row.get("card_number") or _card_number,
                    variety=variety,
                    year=row.get("year") or _year,
                    grade=grade,  # usually None — ungraded identity only
                    url=row.get("url", "") or "",
                    thumbnail_url=row.get("thumbnail"),
                    price_thb=None,  # this source has no PSA-graded prices
                )
            )

        logger.info(f"Pokemon TCG search returned {len(results)} results for '{query}'")
        return results
    except asyncio.TimeoutError:
        logger.warning(f"Pokemon TCG search timed out for '{query}'")
        return []
    except Exception as e:
        logger.warning(f"Pokemon TCG search failed for '{query}': {e}")
        return []


def _parse_card_title(title: str) -> tuple:
    """
    Parse card details from a title string.
    Returns (subject, set, card_number, variety, year, grade)
    """
    subject = None
    set_name = None
    card_number = None
    variety = None
    year = None
    grade = None

    if not title:
        return subject, set_name, card_number, variety, year, grade

    title_lower = title.lower()

    # Extract grade (PSA 8, PSA 9, PSA 10)
    grade_match = re.search(r'psa\s+(\d+)', title_lower)
    if grade_match:
        grade = int(grade_match.group(1))

    # Extract year (4 digits)
    year_match = re.search(r'\b(19|20)\d{2}\b', title)
    if year_match:
        year = int(year_match.group(0))

    # Extract card number (#NNN or NNN)
    card_match = re.search(r'#?(\d{1,3})\b', title)
    if card_match:
        card_number = card_match.group(1)

    # Extract set (e.g., SV2a, Pokemon 151, etc.)
    set_match = re.search(r'\b(SV\d+[a-z]?|pokemon\s*\d+|[a-z]+\s*edition)\b', title_lower, re.IGNORECASE)
    if set_match:
        set_name = set_match.group(1).upper()

    # Extract variety (Art Rare, SAR, SIR, Special Art, Full Art, etc.)
    variety_patterns = [
        r'art\s+rare', r'special\s+art(?:\s+rare)?', r'full\s+art',
        r'\bsar\b', r'\bsir\b', r'\brar\b', r'character\s+rare',
        r'trainer\s+gallery'
    ]
    for pattern in variety_patterns:
        if re.search(pattern, title_lower):
            variety = re.findall(pattern, title_lower)[0].upper()
            break

    # Extract subject (first meaningful word, often before card number/set)
    # Simple heuristic: first capitalized word or after set
    words = title.split()
    for word in words:
        if word and word[0].isupper() and not re.match(r'^[\d\(\)]', word):
            if not re.match(r'^(PSA|Pokemon|Set|Card)', word, re.IGNORECASE):
                subject = word
                break

    if not subject:
        subject = title.split()[0] if title.split() else None

    return subject, set_name, card_number, variety, year, grade


def _merge_and_dedupe(collectr: list[Candidate], ebay: list[Candidate]) -> list[Candidate]:
    """
    Merge Collectr and eBay results, dedupe by (subject, card_number, grade).
    Prefer Collectr's identity but carry eBay price data.
    """
    # Build a dict keyed on (subject, card_number, grade)
    merged = {}

    for cand in collectr:
        key = (cand.subject, cand.card_number, cand.grade)
        if key not in merged:
            merged[key] = cand

    for cand in ebay:
        key = (cand.subject, cand.card_number, cand.grade)
        if key in merged:
            # Merge: prefer Collectr identity but keep eBay price
            existing = merged[key]
            existing.ebay_n_comps = cand.ebay_n_comps
            # Keep Collectr's price if available, else use eBay's
            if not existing.price_thb and cand.price_thb:
                existing.price_thb = cand.price_thb
        else:
            merged[key] = cand

    return list(merged.values())


def _annotate_owned(candidates: list[Candidate]) -> list[Candidate]:
    """
    Check each candidate against master workbook.
    Add 'owned' and 'owned_count' if it matches an existing row.
    """
    try:
        from master_workbook import list_cards

        master_cards = list_cards()

        # Build lookup dict: (subject, card_number, grade) -> count
        owned_map = {}
        for card in master_cards:
            key = (card.get("Subject"), card.get("Card Number"), card.get("Grade"))
            owned_map[key] = owned_map.get(key, 0) + 1

        for cand in candidates:
            key = (cand.subject, cand.card_number, cand.grade)
            if key in owned_map:
                cand.owned = True
                cand.owned_count = owned_map[key]

        return candidates
    except Exception as e:
        logger.warning(f"Failed to annotate owned cards: {e}")
        return candidates


def _score_and_rank(candidates: list[Candidate], query: str) -> list[Candidate]:
    """
    Score each candidate based on query match and source reliability.
    Returns sorted list (highest score first).
    """
    query_lower = query.lower()
    query_tokens = set(query_lower.split())

    for cand in candidates:
        score = 0.0

        # Subject match (40 points)
        if cand.subject and query_lower in cand.subject.lower():
            score += 40

        # All query tokens found in title (25 points)
        title_lower = cand.title.lower()
        if query_tokens.issubset(set(title_lower.split())):
            score += 25

        # Source preference:
        #   Collectr  → rich price + Thai-market signal (15 pts)
        #   PokemonTCG/TCGdex → reliable identity + image (10 pts)
        #   eBay      → price enrichment only (default 0)
        if cand.source == "collectr":
            score += 15
        elif cand.source in ("pokemontcg", "tcgdex"):
            score += 10

        # Has PSA grade in title (10 points)
        if cand.grade and f"psa {cand.grade}" in title_lower:
            score += 10

        # Year match (5 points)
        if cand.year and str(cand.year) in query:
            score += 5

        # No price penalty (-20 points), but skip the penalty for
        # identity-only sources where price is known to be unavailable.
        if cand.price_thb is None and cand.source not in ("pokemontcg", "tcgdex"):
            score -= 20

        # Already owned penalty (-30 points)
        if cand.owned:
            score -= 30

        cand.score = score

    # Sort by score (descending)
    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates


def _candidates_to_dicts(candidates: list) -> list[dict]:
    return [
        {
            "source": c.source, "title": c.title, "subject": c.subject,
            "set": c.set, "card_number": c.card_number, "variety": c.variety,
            "year": c.year, "grade": c.grade, "product_id": c.product_id,
            "url": c.url, "thumbnail_url": c.thumbnail_url,
            "price_thb": c.price_thb, "ebay_n_comps": c.ebay_n_comps,
            "owned": c.owned, "owned_count": c.owned_count, "score": c.score,
        }
        for c in candidates
    ]


async def _live_search_impl(query: str, limit: int = 20) -> list[dict]:
    """Actual search work — wrapped by `live_search` for caching/coalescing."""
    # 1) Local-first: instant fuzzy match against CARD_REGISTRY
    local_results = _search_local_registry(query)

    # 2) Web sources in parallel, with hard wall-clock cap.
    #    Pokemon TCG (pokemontcg.io + TCGdex) is our reliable backup to
    #    eBay — it's free, no-auth, and rarely blocked.  It supplies card
    #    identity + thumbnails even when eBay/Collectr are unavailable.
    web_results: list = []
    try:
        collectr_task = asyncio.create_task(_search_collectr(query, timeout=2.0))
        ebay_task = asyncio.create_task(_search_ebay(query, timeout=3.0))
        pokemon_tcg_task = asyncio.create_task(_search_pokemon_tcg(query, timeout=3.0))

        # Wait at most 3s total; whichever sources finished contribute, the rest are dropped
        done, pending = await asyncio.wait(
            {collectr_task, ebay_task, pokemon_tcg_task}, timeout=3.0
        )
        for t in pending:
            t.cancel()
        for t in done:
            try:
                r = t.result()
                if isinstance(r, list):
                    web_results.extend(r)
            except Exception as e:
                logger.debug(f"web source error: {e}")
    except Exception as e:
        logger.warning(f"web search wave failed: {e}")

    # 3) Merge, annotate, rank.
    #    Identity sources (collectr + pokemontcg + tcgdex + local) are merged
    #    into the primary bucket; eBay rows only enrich price/comp counts.
    identity_sources = {"collectr", "pokemontcg", "tcgdex"}
    candidates = _merge_and_dedupe(
        local_results + [c for c in web_results if c.source in identity_sources],
        [c for c in web_results if c.source == "ebay"],
    )
    candidates = _annotate_owned(candidates)
    candidates = _score_and_rank(candidates, query)

    return _candidates_to_dicts(candidates[:limit])


async def live_search(query: str, limit: int = 20) -> list[dict]:
    """
    Parallel Collectr + eBay + Pokemon-TCG (pokemontcg.io + TCGdex) + local
    search with:
      - prefix-aware cache (normalized tokens, 5min TTL)
      - in-flight coalescing (duplicate concurrent queries share one task)
      - too-broad guard (single generic terms like pokemon return [])
      - hard 3s wall-clock cap on web sources, partial results allowed
      - local CARD_REGISTRY fallback so user always sees something
      - pokemon-tcg identity backup so thumbnails render even when eBay is
        blocked or Collectr login-redirects
    """
    global _SEARCH_CACHE, _INFLIGHT_TASKS

    if _is_too_broad(query):
        logger.info(f"Query '{query}' too broad - refusing")
        return []

    norm_key = _normalize_query(query)

    # Cache hit
    if norm_key in _SEARCH_CACHE:
        cached_ts, cached_results = _SEARCH_CACHE[norm_key]
        if time.time() - cached_ts < _CACHE_TTL:
            logger.info(f"Cache hit for '{query}' (key='{norm_key}')")
            return cached_results

    # In-flight coalescing
    if norm_key in _INFLIGHT_TASKS:
        existing = _INFLIGHT_TASKS[norm_key]
        if not existing.done():
            logger.info(f"Coalescing '{query}' onto in-flight task")
            try:
                return await existing
            except Exception:
                return []

    task = asyncio.create_task(_live_search_impl(query, limit))
    _INFLIGHT_TASKS[norm_key] = task
    try:
        result = await task
        _SEARCH_CACHE[norm_key] = (time.time(), result)
        logger.info(f"Live search for '{query}' returned {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"Live search failed for '{query}': {e}", exc_info=True)
        return []
    finally:
        _INFLIGHT_TASKS.pop(norm_key, None)


async def search_by_candidate_impl(
    product_id: Optional[str],
    url: str,
    title: str
) -> PreviewCard:
    """
    Handle clicking on a search result candidate.
    Fetch Collectr and eBay data to build a complete PreviewCard.

    For cards without a cert, we create a synthetic cert number from the URL/product_id
    to represent the Collectr listing.
    """
    try:
        # Parse card info from title and URL
        subject, set_name, card_number, variety, year, grade = _parse_card_title(title)

        # If product_id provided, construct Collectr fetch
        collectr_url = None
        collectr_price_thb = None
        psa_estimate_thb = None

        if product_id:
            collectr_url = f"https://app.getcollectr.com/explore/product/{product_id}"
            logger.info(f"Candidate has product_id {product_id}, would fetch Collectr")

        # Fetch eBay comps if we have subject + grade
        ebay_avg_thb = None
        ebay_n_comps = 0

        if subject and grade:
            ebay_data = await _fetch_ebay_async(subject, grade)
            ebay_avg_thb = ebay_data.get("ebay_avg_thb")
            ebay_n_comps = ebay_data.get("ebay_n_comps", 0)

        # Compute signal
        signal_data = _compute_signal(
            my_cost=None,
            collectr_price_thb=collectr_price_thb,
            psa_estimate_thb=psa_estimate_thb,
            ebay_avg_thb=ebay_avg_thb,
            ebay_comps=[],
        )

        # Create synthetic cert from product_id (for tracking)
        cert = product_id or f"CAND_{int(time.time())}"

        return PreviewCard(
            cert=cert,
            item=title,
            year=year or 0,
            set_name=set_name or "",
            card_number=card_number or "",
            subject=subject or "UNKNOWN",
            variety=variety or "",
            grade=grade or 9,
            collectr_url=collectr_url,
            collectr_price_thb=collectr_price_thb,
            psa_estimate_thb=psa_estimate_thb,
            ebay_avg_thb=ebay_avg_thb,
            ebay_n_comps=ebay_n_comps,
            psa_image_ok=False,
            collectr_image_ok=False,
            image_match_ok=False,
            signal=signal_data["signal"],
            risk_level=signal_data["risk_level"],
            upside_pct=signal_data["upside_pct"],
            confidence=signal_data["confidence"],
            errors={
                "psa": None,
                "collectr": None,
                "ebay": None,
            },
        )
    except Exception as e:
        logger.error(f"search_by_candidate_impl failed: {e}", exc_info=True)
        raise
