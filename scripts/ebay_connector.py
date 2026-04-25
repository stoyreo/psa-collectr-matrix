"""eBay Sold Listings Connector — real scrape with demo fallback."""
import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from random import random, gauss, choice
from statistics import median, stdev
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
    _NET_OK = True
except ImportError:
    _NET_OK = False

from config import EBAY_CONFIG, COMP_FILTERS, DEMO_MODE_CONFIG, DATA_SOURCES, OUTLIER_CONFIG

logger = logging.getLogger(__name__)

_EBAY_SOLD_URL = "https://www.ebay.com/sch/i.html"
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
_HTTP_TIMEOUT = 6  # seconds — keep short so live search stays snappy

# Simple in-process response cache (TTL 5 min) to avoid re-scraping for repeat queries
_EBAY_CACHE: dict = {}
_EBAY_CACHE_TTL = 300


def search_ebay_sold(query: str, max_results: int = 30) -> List[Dict[str, Any]]:
    """
    Search eBay for sold listings. Real scrape unless demo_mode is on or network fails.
    Returns list of comp dicts with: title, sold_price, shipping, total_price, sold_date,
    url, thumbnail, grade, is_sample.
    """
    if DATA_SOURCES.get("demo_mode") and not DATA_SOURCES.get("ebay"):
        return _generate_sample_comps(query, max_results)

    # Try real scrape
    if _NET_OK:
        try:
            real = _search_ebay_real(query, max_results)
            if real:
                return real
            logger.info(f"eBay real scrape returned 0 for '{query}' — falling back to demo")
        except Exception as e:
            logger.warning(f"eBay real scrape failed for '{query}': {e} — falling back to demo")

    # Fallback to demo
    return _generate_sample_comps(query, max_results)


def _search_ebay_real(query: str, max_results: int = 30) -> List[Dict[str, Any]]:
    """Real eBay sold-listings scrape via the public search page."""
    import time as _time

    # Cache lookup
    ck = (query.lower().strip(), max_results)
    cached = _EBAY_CACHE.get(ck)
    if cached and (_time.time() - cached[0]) < _EBAY_CACHE_TTL:
        return cached[1]

    params = {
        "_nkw": query,
        "_sacat": "0",
        "LH_Sold": "1",
        "LH_Complete": "1",
        "_ipg": str(min(max(max_results, 10), 60)),
    }
    url = f"{_EBAY_SOLD_URL}?{'&'.join(k+'='+quote_plus(v) for k,v in params.items())}"

    resp = requests.get(url, headers={"User-Agent": _UA, "Accept-Language": "en-US,en;q=0.9"},
                        timeout=_HTTP_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results: List[Dict[str, Any]] = []
    items = soup.select("li.s-item, div.s-item")
    for it in items:
        try:
            title_el = it.select_one(".s-item__title")
            price_el = it.select_one(".s-item__price")
            ship_el  = it.select_one(".s-item__shipping, .s-item__logisticsCost")
            link_el  = it.select_one("a.s-item__link")
            img_el   = it.select_one(".s-item__image img, img.s-item__image-img")
            date_el  = it.select_one(".s-item__title--tagblock .POSITIVE, .s-item__caption--row")

            title = (title_el.get_text(strip=True) if title_el else "").strip()
            if not title or title.lower() in ("shop on ebay", ""):
                continue

            price = _parse_price(price_el.get_text() if price_el else "")
            if price is None:
                continue
            shipping = _parse_price(ship_el.get_text() if ship_el else "") or 0.0
            href = link_el.get("href", "") if link_el else ""
            thumb = None
            if img_el:
                thumb = img_el.get("src") or img_el.get("data-src")

            sold_date = _parse_sold_date(date_el.get_text() if date_el else "")
            grade = _extract_grade_from_title(title)

            results.append({
                "title": title,
                "sold_date": sold_date,
                "sold_price": round(price, 2),
                "shipping": round(shipping, 2),
                "total_price": round(price + shipping, 2),
                "currency": "USD",
                "url": href,
                "thumbnail": thumb,
                "grade": grade,
                "grade_confidence": 95.0 if grade else 50.0,
                "is_sample": False,
            })
            if len(results) >= max_results:
                break
        except Exception as e:
            logger.debug(f"skip eBay tile: {e}")
            continue

    logger.info(f"eBay REAL scrape: {len(results)} results for '{query}'")
    _EBAY_CACHE[ck] = (_time.time(), results)
    return results


def _parse_price(txt: str) -> Optional[float]:
    if not txt:
        return None
    # Handle "$123.45", "$100.00 to $200.00", "US $123.45", etc.
    m = re.search(r'(\d[\d,]*\.?\d*)', txt.replace(",", ""))
    if not m:
        # Try with comma preserved as thousands separator
        m2 = re.search(r'([\d,]+\.\d{2})', txt)
        if m2:
            try: return float(m2.group(1).replace(",", ""))
            except: return None
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


def _parse_sold_date(txt: str):
    """Parse eBay's 'Sold Mar 15, 2024' tag into a date. Returns None on failure."""
    if not txt:
        return None
    m = re.search(r'Sold\s+([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', txt)
    if not m:
        return None
    try:
        return datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%b %d %Y").date()
    except Exception:
        try:
            return datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%B %d %Y").date()
        except Exception:
            return None


def _extract_grade_from_title(title: str) -> Optional[str]:
    m = re.search(r'PSA\s*(\d{1,2})', title, re.IGNORECASE)
    return m.group(1) if m else None


def _generate_sample_comps(query: str, count: int = 12) -> List[Dict[str, Any]]:
    """Generate realistic sample eBay comps for demo mode / fallback."""
    comps = []
    base_price = 100.0
    for i in range(count):
        variance_pct = DEMO_MODE_CONFIG["base_variance"]
        price_variance = gauss(0, variance_pct / 2)
        price = base_price * (1 + price_variance)
        shipping_pct = random() * 0.15
        shipping = price * shipping_pct
        date_bucket = random()
        if date_bucket < DEMO_MODE_CONFIG["recency_mix"]["last_7_days"]:
            days_ago = int(random() * 7)
        elif date_bucket < (DEMO_MODE_CONFIG["recency_mix"]["last_7_days"] + DEMO_MODE_CONFIG["recency_mix"]["last_30_days"]):
            days_ago = 7 + int(random() * 23)
        elif date_bucket < (DEMO_MODE_CONFIG["recency_mix"]["last_7_days"] + DEMO_MODE_CONFIG["recency_mix"]["last_30_days"] + DEMO_MODE_CONFIG["recency_mix"]["last_90_days"]):
            days_ago = 30 + int(random() * 60)
        else:
            days_ago = 90 + int(random() * 100)
        sold_date = datetime.now().date() - timedelta(days=days_ago)
        if "psa 8" in query.lower():
            grade, gc = "8", 85 + random() * 10
        elif "psa 9" in query.lower():
            grade, gc = "9", 85 + random() * 10
        elif "psa 10" in query.lower():
            grade, gc = "10", 85 + random() * 10
        else:
            grade, gc = choice(["8", "9", "10"]), 60 + random() * 25
        comps.append({
            "title": f"DEMO: {query} - Sold {sold_date.strftime('%Y-%m-%d')}",
            "sold_date": sold_date,
            "sold_price": round(price, 2),
            "shipping": round(shipping, 2),
            "total_price": round(price + shipping, 2),
            "currency": "USD",
            "url": f"https://www.ebay.com/itm/demo-{i}",
            "thumbnail": None,
            "grade": grade,
            "grade_confidence": round(gc, 1),
            "is_sample": True,
        })
    logger.debug(f"Generated {len(comps)} sample comps for: {query}")
    return comps


def filter_comps(comps: List[Dict[str, Any]], card: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filter out invalid/inappropriate comps from list."""
    filtered = []
    portfolio_grade = str(card.get("grade", "")).strip()
    grade_tolerance = COMP_FILTERS["grade_tolerance"]
    for comp in comps:
        title_lower = comp.get("title", "").lower()
        reasons = []
        for keyword in COMP_FILTERS["bundle_keywords"]:
            if keyword in title_lower:
                reasons.append(f"bundle_keyword: {keyword}"); break
        for keyword in COMP_FILTERS["fake_keywords"]:
            if keyword in title_lower:
                reasons.append(f"fake_keyword: {keyword}"); break
        for keyword in COMP_FILTERS["damaged_keywords"]:
            if keyword in title_lower:
                reasons.append(f"damaged_keyword: {keyword}"); break
        if "japanese" not in title_lower:
            reasons.append("not_japanese")
        comp_grade = comp.get("grade")
        if comp_grade and portfolio_grade:
            try:
                if abs(int(portfolio_grade) - int(comp_grade)) > grade_tolerance:
                    reasons.append(f"grade_mismatch: {comp_grade} vs {portfolio_grade}")
            except ValueError:
                pass
        if not reasons:
            filtered.append(comp)
    logger.info(f"Filtered {len(comps)} comps -> {len(filtered)} valid comps")
    return filtered


def compute_stats(comps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute pricing statistics from comps."""
    if not comps:
        return {"min": None, "median": None, "max": None, "avg": None, "count": 0,
                "avg_shipping": 0.0, "variance": None, "stdev": None, "recency_score": 0, "trend": "UNKNOWN"}
    prices = [c.get("total_price", c.get("sold_price", 0)) for c in comps]
    shipping = [c.get("shipping", 0) for c in comps]
    sold_dates = [c.get("sold_date") for c in comps if c.get("sold_date")]
    min_price = min(prices); max_price = max(prices)
    median_price = median(prices); avg_price = sum(prices) / len(prices)
    avg_shipping = sum(shipping) / len(shipping) if shipping else 0.0
    variance = sum((p - avg_price) ** 2 for p in prices) / len(prices) if len(prices) > 1 else 0
    std_dev = stdev(prices) if len(prices) > 1 else 0
    if sold_dates:
        cutoff_date = datetime.now().date() - timedelta(days=30)
        recent_count = sum(1 for d in sold_dates if d and d >= cutoff_date)
        recency_score = min(100, int((recent_count / len(sold_dates)) * 100))
    else:
        recency_score = 0
    if len(comps) >= 4:
        sorted_comps = sorted(comps, key=lambda c: c.get("sold_date") or datetime.now().date())
        mid = len(sorted_comps) // 2
        older = [c.get("total_price", c.get("sold_price", 0)) for c in sorted_comps[:mid]]
        recent = [c.get("total_price", c.get("sold_price", 0)) for c in sorted_comps[mid:]]
        older_median = median(older) if older else 0
        recent_median = median(recent) if recent else 0
        if older_median > 0:
            pc = (recent_median - older_median) / older_median
            trend = "UP" if pc > 0.10 else ("DOWN" if pc < -0.10 else "STABLE")
        else:
            trend = "UNKNOWN"
    else:
        trend = "INSUFFICIENT_DATA"
    return {"min": round(min_price, 2), "median": round(median_price, 2),
            "max": round(max_price, 2), "avg": round(avg_price, 2),
            "count": len(comps), "avg_shipping": round(avg_shipping, 2),
            "variance": round(variance, 2), "stdev": round(std_dev, 2),
            "recency_score": recency_score, "trend": trend}


def flag_outliers(comps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flag statistical outliers using IQR method."""
    if len(comps) < OUTLIER_CONFIG["min_data_points"]:
        for comp in comps: comp["is_outlier"] = False
        return comps
    prices = [c.get("total_price", c.get("sold_price", 0)) for c in comps]
    prices_sorted = sorted(prices); n = len(prices_sorted)
    q1 = prices_sorted[n // 4]; q3 = prices_sorted[(3 * n) // 4]
    iqr = q3 - q1; mult = OUTLIER_CONFIG["iqr_multiplier"]
    lower, upper = q1 - mult*iqr, q3 + mult*iqr
    for comp in comps:
        p = comp.get("total_price", comp.get("sold_price", 0))
        comp["is_outlier"] = p < lower or p > upper
    logger.debug(f"Outlier bounds: [{lower:.2f}, {upper:.2f}]")
    return comps


def get_ebay_comps(card: Dict[str, Any]) -> Dict[str, Any]:
    """Full pipeline: search, filter, compute stats, flag outliers."""
    from matching import build_ebay_search_query
    query = build_ebay_search_query(card)
    logger.info(f"Searching eBay for: {card.get('subject')} - Query: {query}")
    raw_comps = search_ebay_sold(query, max_results=EBAY_CONFIG["max_results"])
    filtered_comps = filter_comps(raw_comps, card)
    flagged_comps = flag_outliers(filtered_comps)
    stats = compute_stats(flagged_comps)
    return {"query_used": query, "comps": flagged_comps, "stats": stats, "comp_count": len(flagged_comps)}


if __name__ == "__main__":
    print("ebay_connector module loaded")
