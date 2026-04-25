"""Pokemon TCG card-identity connector — backup to flaky eBay scraping.

Two independent free, no-auth sources are queried in priority order:

1. pokemontcg.io  — global English-language coverage, very reliable HTTP API,
                    rate-limited to 1000 req/day without a key (well above
                    Add-Card needs).
2. TCGdex         — strong Japanese-card coverage (api.tcgdex.net /ja/ and
                    /en/ endpoints), CC-BY-NC images.

Both expose the SAME interface:

    search_pokemon_tcg(query: str, max_results: int = 20) -> list[dict]

Each returned dict has the same shape as ebay_connector / collectr_connector
candidates so add_card_service can merge them uniformly:

    {
        "title":      str,            # human-readable card name + set
        "subject":    str,            # card name (e.g. "Charizard ex")
        "set":        str | None,
        "card_number":str | None,
        "year":       int | None,
        "url":        str,            # canonical store/info page
        "thumbnail":  str | None,     # small image
        "source":     "pokemontcg" | "tcgdex",
    }

Network failures degrade gracefully (empty list, warning logged).  All
responses are cached in-process for 5 minutes.
"""
from __future__ import annotations

import logging
import re
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

# ── Tunables ────────────────────────────────────────────────────────────────
_HTTP_TIMEOUT = 5
_CACHE_TTL = 300  # 5 min
_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_POKEMONTCG_URL = "https://api.pokemontcg.io/v2/cards"
_TCGDEX_EN_URL = "https://api.tcgdex.net/v2/en/cards"
_TCGDEX_JA_URL = "https://api.tcgdex.net/v2/ja/cards"

# In-process cache: { (provider, query_norm) -> (timestamp, list[dict]) }
_CACHE: dict[tuple[str, str], tuple[float, list[dict]]] = {}


# ── Helpers ─────────────────────────────────────────────────────────────────
def _norm_query(q: str) -> str:
    """Lowercase, collapse whitespace; used for cache key only."""
    return " ".join((q or "").lower().split())


def _cache_get(provider: str, q: str) -> list[dict] | None:
    key = (provider, _norm_query(q))
    if key in _CACHE:
        ts, payload = _CACHE[key]
        if time.time() - ts < _CACHE_TTL:
            return payload
        _CACHE.pop(key, None)
    return None


def _cache_put(provider: str, q: str, payload: list[dict]) -> None:
    _CACHE[(provider, _norm_query(q))] = (time.time(), payload)


def _is_japanese(text: str) -> bool:
    """True if text contains hiragana/katakana/kanji."""
    if not text:
        return False
    return bool(re.search(r"[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]", text))


# ── Provider 1: pokemontcg.io ───────────────────────────────────────────────
def _search_pokemontcg(query: str, max_results: int = 20) -> list[dict]:
    """Hit https://api.pokemontcg.io/v2/cards with a Lucene-style q= filter."""
    cached = _cache_get("pokemontcg", query)
    if cached is not None:
        return cached[:max_results]

    # Build a tolerant search clause: name match OR subjects match.
    # The API supports wildcard '*' on string fields.
    raw = (query or "").strip()
    if not raw:
        return []

    # Strip generic words like "PSA 10", "japanese", etc., they confuse name search.
    cleaned = re.sub(
        r"\b(psa\s*\d+|japanese|japan|pokemon|pokémon|holo|rare|art|full|gold|silver|promo|grade|card|cards)\b",
        "",
        raw,
        flags=re.IGNORECASE,
    ).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)

    if not cleaned:
        return []  # nothing distinctive left to search on

    # Use wildcard match on name; quote any phrase containing whitespace.
    name_term = f'"*{cleaned}*"' if " " in cleaned else f"*{cleaned}*"
    q = f"name:{name_term}"

    params = {"q": q, "pageSize": min(max(1, max_results), 50)}

    try:
        resp = requests.get(
            _POKEMONTCG_URL,
            params=params,
            headers={"User-Agent": _UA, "Accept": "application/json"},
            timeout=_HTTP_TIMEOUT,
        )
        if resp.status_code != 200:
            logger.warning(
                f"pokemontcg.io returned {resp.status_code} for '{query}'"
            )
            return []
        data = resp.json().get("data", [])
    except Exception as e:
        logger.warning(f"pokemontcg.io fetch failed for '{query}': {e}")
        return []

    out: list[dict] = []
    for card in data[:max_results]:
        try:
            name = card.get("name", "") or ""
            set_obj = card.get("set", {}) or {}
            set_name = set_obj.get("name") or ""
            card_number = card.get("number") or ""
            year = None
            release = set_obj.get("releaseDate") or ""
            m = re.match(r"(\d{4})", release)
            if m:
                year = int(m.group(1))
            images = card.get("images", {}) or {}
            thumb = images.get("small") or images.get("large")
            url = card.get("tcgplayer", {}).get("url") or images.get("large") or ""

            title = (
                f"{name} - {set_name} #{card_number}"
                if set_name and card_number
                else name
            )

            out.append(
                {
                    "title": title,
                    "subject": name,
                    "set": set_name or None,
                    "card_number": card_number or None,
                    "year": year,
                    "url": url,
                    "thumbnail": thumb,
                    "source": "pokemontcg",
                }
            )
        except Exception as e:
            logger.debug(f"pokemontcg.io row parse failed: {e}")

    _cache_put("pokemontcg", query, out)
    logger.info(f"pokemontcg.io returned {len(out)} results for '{query}'")
    return out


# ── Provider 2: TCGdex (Japanese-friendly) ──────────────────────────────────
def _search_tcgdex(query: str, max_results: int = 20) -> list[dict]:
    """Hit api.tcgdex.net.  Picks /ja/ when query is Japanese script,
    /en/ otherwise."""
    cached = _cache_get("tcgdex", query)
    if cached is not None:
        return cached[:max_results]

    raw = (query or "").strip()
    if not raw:
        return []

    base_url = _TCGDEX_JA_URL if _is_japanese(raw) else _TCGDEX_EN_URL

    # TCGdex supports `name=like:foo` for partial matches in v2.
    params = {"name": f"like:{raw}"}

    try:
        resp = requests.get(
            base_url,
            params=params,
            headers={"User-Agent": _UA, "Accept": "application/json"},
            timeout=_HTTP_TIMEOUT,
        )
        if resp.status_code != 200:
            logger.warning(
                f"tcgdex returned {resp.status_code} for '{query}'"
            )
            return []
        data = resp.json()
        if not isinstance(data, list):
            return []
    except Exception as e:
        logger.warning(f"tcgdex fetch failed for '{query}': {e}")
        return []

    out: list[dict] = []
    for card in data[:max_results]:
        try:
            name = card.get("name") or ""
            cid = card.get("id") or ""
            image_base = card.get("image") or ""
            # TCGdex image URLs need /low.png (or /high.png) appended
            thumb = f"{image_base}/low.png" if image_base else None
            full_url = (
                f"https://www.tcgdex.net/{'ja' if _is_japanese(raw) else 'en'}/cards/{cid}"
                if cid
                else ""
            )

            # set + number are encoded in the id (e.g. "swsh3-136") — split for display
            set_part, _, num_part = cid.partition("-")
            out.append(
                {
                    "title": f"{name} - {set_part.upper()} #{num_part}" if set_part else name,
                    "subject": name,
                    "set": set_part.upper() or None,
                    "card_number": num_part or None,
                    "year": None,
                    "url": full_url,
                    "thumbnail": thumb,
                    "source": "tcgdex",
                }
            )
        except Exception as e:
            logger.debug(f"tcgdex row parse failed: {e}")

    _cache_put("tcgdex", query, out)
    logger.info(f"tcgdex returned {len(out)} results for '{query}'")
    return out


# ── Public entry point ──────────────────────────────────────────────────────
def search_pokemon_tcg(query: str, max_results: int = 20) -> list[dict]:
    """
    Primary entry: try pokemontcg.io first, fall back to TCGdex if the first
    returns nothing.  For Japanese-script queries TCGdex is tried first.

    Always returns a list (possibly empty); never raises.
    """
    if not query or not query.strip():
        return []

    if _is_japanese(query):
        primary, secondary = _search_tcgdex, _search_pokemontcg
    else:
        primary, secondary = _search_pokemontcg, _search_tcgdex

    try:
        results = primary(query, max_results)
    except Exception as e:
        logger.warning(f"primary pokemon-tcg source failed: {e}")
        results = []

    if results:
        return results

    try:
        return secondary(query, max_results)
    except Exception as e:
        logger.warning(f"secondary pokemon-tcg source failed: {e}")
        return []


__all__ = ["search_pokemon_tcg"]
