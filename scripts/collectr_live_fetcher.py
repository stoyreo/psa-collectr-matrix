"""
Collectr Live Price Fetcher
Fetches real-time PSA graded prices from Collectr using playwright.
Runs 5 pages concurrently — all 19 cards in ~15 seconds.
"""

import re
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# Disk-cache directory — relative to this script's parent (project root)
_CACHE_DIR = Path(__file__).resolve().parent.parent / "cache" / "images"

logger = logging.getLogger(__name__)

# ── Card registry: all 19 cards with their Collectr URLs & target grade ──────
CARD_REGISTRY = [
    {"key": "slowpoke_sv1v_082_psa8_artrare",                      "subject": "SLOWPOKE",               "card_number": "082", "grade": 8,  "url": "https://app.getcollectr.com/explore/product/10010852"},
    {"key": "psyduck_sv2a_175_psa10_artrare",                      "subject": "PSYDUCK",                "card_number": "175", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10012098"},
    {"key": "charizardex_sv4a_349_psa10_specialartrare",           "subject": "CHARIZARD EX",           "card_number": "349", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10013016"},
    {"key": "magikarp_sv1a_080_psa10_artrare",                     "subject": "MAGIKARP",               "card_number": "080", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10011603"},
    {"key": "fullartpikachu_25thanniversarycollection_001_psa10_", "subject": "FULL ART/PIKACHU",       "card_number": "001", "grade": 10, "url": "https://app.getcollectr.com/explore/product/577896"},
    {"key": "pikachu_mp_020_psa10_mcdonalds",                      "subject": "PIKACHU",                "card_number": "020", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10030009"},
    {"key": "pikachu_sv_001_psa10_scarletvioletpreorder",          "subject": "PIKACHU",                "card_number": "001", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10009523"},
    {"key": "mewex_sv2a_205_psa10_specialartrare",                 "subject": "MEW EX",                 "card_number": "205", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10012128"},
    {"key": "detectivepikachu_svp_098_psa10_detectivepikachureturnspreorder", "subject": "DETECTIVE PIKACHU", "card_number": "098", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10012662"},
    {"key": "sylveonex_sv8a_212_psa10_specialartrare",             "subject": "SYLVEON EX",             "card_number": "212", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10023355"},
    {"key": "snorlaxholo_sunmoondoubleblaze_076_psa10_",           "subject": "SNORLAX",                "card_number": "076", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10004913"},
    {"key": "snorlax_sv2a_181_psa10_artrare",                      "subject": "SNORLAX",                "card_number": "181", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10012104"},
    {"key": "pikachu_spromo_208_psa10_yunagabaxpokemoncardgamecampaign", "subject": "PIKACHU",          "card_number": "208", "grade": 10, "url": "https://app.getcollectr.com/explore/product/250510"},
    {"key": "snorlax_topsun_143_psa8_greenback",                   "subject": "SNORLAX",                "card_number": "143", "grade": 8,  "url": "https://app.getcollectr.com/explore/product/10026716"},
    {"key": "umbreonex_sv8a_217_psa10_specialartrare",             "subject": "UMBREON EX",             "card_number": "217", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10023360"},
    {"key": "ponchowearingpikachu_xypromo_203_psa10_pikachumegacampaign", "subject": "PONCHO-WEARING PIKACHU", "card_number": "203", "grade": 10, "url": "https://app.getcollectr.com/explore/product/10010048"},
    # Cards without Collectr URL — skip live fetch, use PSA estimate fallback
    {"key": "pikachu_svp_242_psa10_illustrationcontest2024",       "subject": "PIKACHU",                "card_number": "242", "grade": 10, "url": None},
    {"key": "pikachu_asia25th_003_psa10_goldenboxjapanese",        "subject": "PIKACHU",                "card_number": "003", "grade": 10, "url": None},
    {"key": "mischievouspichu_spromo_214_psa10_graniphpurchasecampaign", "subject": "MISCHIEVOUS PICHU","card_number": "214", "grade": 10, "url": None},
]


def _parse_prices(text: str, target_grade: int) -> dict:
    """
    Parse PSA prices from Collectr page innerText.
    Page text pattern:
        PSA 10
        ($76)
        PSA 9
        ($19)
        PSA 8
        ($12)
    """
    grade_prices = {}
    # Match "PSA 10\n($76)" or "PSA 10\n\n($76)"
    for m in re.finditer(r'PSA\s+(\d+)\s*\n+\(\$([0-9,]+(?:\.\d+)?)\)', text):
        grade = int(m.group(1))
        price = float(m.group(2).replace(',', ''))
        grade_prices[grade] = price

    # Ungraded: first "$X.XX" in the text (appears in card header before chart)
    ungraded = None
    um = re.search(r'\$(\d+(?:\.\d{1,2})?)\n', text)
    if um:
        ungraded = float(um.group(1))

    graded_for_target = grade_prices.get(target_grade)

    return {
        "collectr_ungraded": ungraded,
        "collectr_graded":   graded_for_target,
        "collectr_psa10":    grade_prices.get(10),
        "collectr_psa9":     grade_prices.get(9),
        "collectr_psa8":     grade_prices.get(8),
    }


async def _fetch_one(browser, semaphore, card: dict, timeout_ms: int = 20000) -> dict:
    """Fetch a single Collectr product page and extract prices."""
    key     = card["key"]
    url     = card["url"]
    grade   = card["grade"]
    subject = card["subject"]

    if not url:
        logger.info(f"  SKIP {subject} — no Collectr URL")
        return {"key": key, "status": "no_url", "data": None}

    async with semaphore:
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()
        try:
            # Intercept CDN image response during page load
            _captured_img = [None]
            async def _on_resp(resp):
                if 'public.getcollectr.com/public-assets/products' in resp.url and resp.ok:
                    try: _captured_img[0] = await resp.body()
                    except Exception: pass
            page.on('response', _on_resp)

            await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

            # Wait until PSA price section appears in the DOM
            await page.wait_for_function(
                "document.body.innerText.includes('PSA 10') || document.body.innerText.includes('PSA 8')",
                timeout=timeout_ms,
            )

            text = await page.evaluate("document.body.innerText")
            prices = _parse_prices(text, grade)

            # Derive product ID from URL and build both CDN + local route URLs
            # Local route /card-img/<pid> is served by webapp.py from disk cache
            product_id_match = re.search(r'/product/(\d+)$', url)
            image_url = None    # local route — used by frontend
            cdn_url   = None    # external CDN — used for downloading to disk
            pid       = None
            if product_id_match:
                pid     = product_id_match.group(1)
                cdn_url = (
                    f"https://public.getcollectr.com/public-assets/products/product_{pid}.webp"
                    "?optimizer=image&format=webp&width=1200&quality=80&strip=metadata"
                )
                image_url = f"/card-img/{pid}"  # served locally by Flask

                # ── Capture image from page responses (CDN blocks direct requests) ──
                try:
                    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    img_path = _CACHE_DIR / f"{pid}.webp"
                    if img_path.exists():
                        logger.info(f"  IMG cached: {pid}.webp (already on disk)")
                    elif _captured_img[0]:
                        img_path.write_bytes(_captured_img[0])
                        logger.info(f"  IMG intercepted+saved: {pid}.webp")
                    else:
                        logger.warning(f"  IMG not captured for {pid} (no CDN response intercepted)")
                        image_url = None
                except Exception as _img_err:
                    logger.warning(f"  IMG error for {pid}: {_img_err}")
                    image_url = None

            graded = prices.get("collectr_graded")
            logger.info(f"  OK  {subject} PSA{grade} -> ${graded} (PSA10=${prices.get('collectr_psa10')}, PSA9={prices.get('collectr_psa9')}, PSA8={prices.get('collectr_psa8')}, img={'ok' if image_url else 'none'})")

            return {
                "key":    key,
                "status": "success",
                "data": {
                    **prices,
                    "collectr_url":    url,
                    "image_url":       image_url,   # /card-img/<pid> local route
                    "source":          "Collectr Live",
                    "fetched":         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "subject":         subject,
                    "card_number":     card["card_number"],
                    "grade":           str(grade),
                },
            }

        except Exception as e:
            logger.warning(f"  FAIL {subject}: {e}")
            return {"key": key, "status": "error", "error": str(e), "data": None}
        finally:
            await context.close()


async def fetch_all_live_prices(concurrency: int = 5) -> dict:
    """
    Fetch live prices for all 19 cards concurrently.
    - Cards with Collectr URL  -> Collectr live prices + CDN image
    - Cards without Collectr URL -> PSA cert page scrape for image; PSA estimate for price
    Returns a dict keyed by card key.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise RuntimeError("playwright not installed — run: python -m pip install playwright && python -m playwright install chromium")

    # ── Step 1: Collectr live prices ─────────────────────────────────────
    logger.info(f"[Collectr Live] Fetching {len(CARD_REGISTRY)} cards (concurrency={concurrency})…")

    results = {}
    semaphore = asyncio.Semaphore(concurrency)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        tasks = [_fetch_one(browser, semaphore, card) for card in CARD_REGISTRY]
        outcomes = await asyncio.gather(*tasks, return_exceptions=True)
        await browser.close()

    for outcome in outcomes:
        if isinstance(outcome, Exception):
            logger.error(f"Unhandled exception: {outcome}")
            continue
        key  = outcome["key"]
        data = outcome.get("data")
        if data:
            results[key] = data
        else:
            results[key] = None  # will fall back to PSA estimate in refresh_live

    ok    = sum(1 for v in results.values() if v)
    total = len(CARD_REGISTRY)
    logger.info(f"[Collectr Live] Done: {ok}/{total} Collectr cards fetched")

    # ── Step 2: PSA cert scrape for exception cards (no Collectr URL) ────
    try:
        from psa_scraper import fetch_psa_exception_data, PSA_EXCEPTION_REGISTRY
        logger.info(f"[PSA Scraper] Fetching images for {len(PSA_EXCEPTION_REGISTRY)} exception cards…")
        psa_results = await fetch_psa_exception_data(concurrency=3)
        for key, psa in psa_results.items():
            if psa and psa.get("image_url"):
                # Store image_url so refresh_live can pick it up
                results[key] = {
                    "image_url":     psa["image_url"],
                    "collectr_url":  None,
                    "source":        "PSA Cert",
                    "subject":       psa.get("subject", ""),
                    "card_number":   psa.get("card_number", ""),
                    # price fields — will use PSA estimate from CSV
                    "collectr_graded":  None,
                    "collectr_psa10":   None,
                    "collectr_psa9":    None,
                    "collectr_psa8":    None,
                    "collectr_ungraded": None,
                }
                logger.info(f"  PSA image stored for {psa.get('subject')} #{psa.get('card_number')}")
            else:
                logger.warning(f"  No PSA image for key={key}")
    except Exception as e:
        logger.warning(f"[PSA Scraper] Skipped (exception cards will use PSA estimate only): {e}")

    return results


def fetch_live_prices_sync(concurrency: int = 5) -> dict:
    """Synchronous wrapper — safe to call from Flask."""
    return asyncio.run(fetch_all_live_prices(concurrency))

if __name__ == "__main__":
    import sys
    logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")
    prices = fetch_live_prices_sync()
    total_graded = sum(
        p["collectr_graded"] for p in prices.values()
        if p and p.get("collectr_graded")
    )
    print(f"\nLive portfolio value: ${total_graded:,.2f}")
    found = sum(1 for p in prices.values() if p and p.get("source") == "Collectr Live")
    print(f"Cards with live data: {found}/{len(CARD_REGISTRY)}")
