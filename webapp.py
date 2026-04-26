"""
PSA x Collectr Tracer — Web App Server
Flask backend: serves portfolio data, triggers live refresh via Playwright.
"""

import os
import sys
import re
import json
import time
import logging
import asyncio
import threading
from pathlib import Path
from datetime import datetime
from threading import Lock

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from refresh_live import live_refresh

# Support PyInstaller launcher overriding template folder via env var
_tmpl_folder = os.environ.get("FLASK_TEMPLATE_FOLDER") or str(Path(__file__).parent / "templates")
app = Flask(__name__, template_folder=_tmpl_folder)
app.logger.setLevel(logging.INFO)

# ── Phase C: Enable CORS for Vercel Frontend ─────────────────────────────────
# Allow both the canonical Vercel domain AND every preview/branch deployment
# (matrix, tracer, *-techcraftlab.vercel.app, etc.) plus localhost for dev.
CORS(app, resources={
    r"/api/*": {
        # Use a regex string (flask-cors compiles it) to cover every
        # psa-collectr-*.vercel.app deployment (matrix, tracer, previews).
        "origins": [
            r"https://psa-collectr-[a-z0-9\-]+\.vercel\.app",
            "http://localhost:3000",
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-Tracer-Key", "ngrok-skip-browser-warning"],
        "supports_credentials": True,
    }
})

# ── Phase C: API Authentication Middleware ────────────────────────────────────
@app.before_request
def check_api_auth():
    """Validate X-Tracer-Key header for all /api/* POST requests."""
    if request.path.startswith('/api/') and request.method in ['POST', 'PUT', 'DELETE']:
        expected_key = os.environ.get('TRACER_API_KEY', '')
        provided_key = request.headers.get('X-Tracer-Key', '')

        if not expected_key:
            app.logger.warning('[AUTH] TRACER_API_KEY not set in environment')
            return jsonify({"error": "Server error: API key not configured"}), 500

        if provided_key != expected_key:
            app.logger.warning(f'[AUTH] Invalid or missing X-Tracer-Key from {request.remote_addr}')
            return jsonify({"error": "Unauthorized: Invalid or missing API key"}), 401

# ── In-memory cache ──────────────────────────────────────────────────────────
_cache = {"data": None, "timestamp": None}
_lock = Lock()

SIGNAL_COLORS = {
    "BUY":    "#4CAF50",
    "HOLD":   "#2196F3",
    "SELL":   "#F44336",
    "REVIEW": "#FF9800",
}

RISK_COLORS = {
    "LOW":    "#4CAF50",
    "MEDIUM": "#FF9800",
    "HIGH":   "#F44336",
}

def serialize_card(card):
    sig  = card.get("signal_data", {})
    mv   = card.get("market_value")
    cost = card.get("my_cost")
    pnl  = (mv - cost) if (mv and cost) else None
    pnl_pct = (pnl / cost * 100) if (pnl is not None and cost) else None

    return {
        "subject":         card.get("subject", ""),
        "grade":           card.get("grade", ""),
        "set_code":        card.get("set", card.get("set_code", "")),
        "card_number":     card.get("card_number", ""),
        "variety":         card.get("variety", ""),
        "year":            card.get("year", ""),
        "cert_number":     str(card.get("cert_number", "")),
        "date_acquired":   str(card.get("date_acquired", "") or ""),
        "my_cost":         cost,
        "psa_estimate":    card.get("psa_estimate"),
        "market_value":    mv,
        "pnl":             round(pnl, 0) if pnl is not None else None,
        "pnl_pct":         round(pnl_pct, 1) if pnl_pct is not None else None,
        "signal":          sig.get("signal", "REVIEW"),
        "risk_level":      sig.get("risk_level", "HIGH"),
        "confidence":      sig.get("confidence", 0),
        "liquidity":       sig.get("liquidity", "UNKNOWN"),
        "upside_pct":      sig.get("upside_pct", 0),
        "explanation":     sig.get("explanation", ""),
        "collectr_price":  card.get("collectr_price"),
        "collectr_url":    card.get("collectr_url"),
        "collectr_source": card.get("collectr_source", ""),
        "collectr_psa8":   card.get("collectr_psa8"),
        "collectr_psa9":   card.get("collectr_psa9"),
        "collectr_psa10":  card.get("collectr_psa10"),
        "source":          card.get("source", ""),
        "my_notes":        card.get("my_notes", ""),
        "image_url":       card.get("image_url", ""),
        "signal_color":    SIGNAL_COLORS.get(sig.get("signal", "REVIEW"), "#FF9800"),
        "risk_color":      RISK_COLORS.get(sig.get("risk_level", "HIGH"), "#F44336"),
    }


def build_response(result, data_source="snapshot"):
    portfolio  = [serialize_card(c) for c in result.get("portfolio", [])]
    summary    = result.get("summary", {})
    insights   = result.get("insights", {})
    exceptions = result.get("exceptions", [])
    timestamp  = result.get("timestamp", datetime.now().isoformat())

    try:
        dt = datetime.fromisoformat(timestamp)
        ts_display = dt.strftime("%d %b %Y  %H:%M:%S")
    except Exception:
        ts_display = timestamp

    return {
        "status":      "success",
        "timestamp":   timestamp,
        "ts_display":  ts_display,
        "data_source": data_source,
        "summary":     summary,
        "portfolio":   portfolio,
        "insights":    insights,
        "exceptions":  exceptions,
    }


# ── Claude Haiku AI Portfolio Summary ────────────────────────────────────────

def generate_ai_summary(portfolio, summary):
    """Call Claude Haiku to produce a punchy, emotional investment briefing."""
    try:
        import anthropic, os
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return "⚠️ ANTHROPIC_API_KEY not set — add it to your environment to enable AI insights."

        buys    = [c for c in portfolio if c.get("signal") == "BUY"]
        sells   = [c for c in portfolio if c.get("signal") == "SELL"]
        holds   = [c for c in portfolio if c.get("signal") == "HOLD"]
        reviews = [c for c in portfolio if c.get("signal") == "REVIEW"]

        def fmt_cards(lst):
            return ", ".join(
                f"{c['subject']} PSA{c['grade']} ({c['pnl_pct']:+.1f}%)"
                for c in lst if c.get("pnl_pct") is not None
            ) or "None"

        pnl     = summary.get("total_pnl", 0)
        pnl_pct = summary.get("pnl_pct", 0)
        cost    = summary.get("total_cost", 0)
        mv      = summary.get("total_market_value", 0)

        top_gain = sorted([c for c in portfolio if c.get("pnl_pct")], key=lambda x: x["pnl_pct"], reverse=True)[:3]
        top_loss = sorted([c for c in portfolio if c.get("pnl_pct")], key=lambda x: x["pnl_pct"])[:3]

        context = f"""
PORTFOLIO SNAPSHOT — Thai Pokemon Card Collector (values in THB ฿)
• {len(portfolio)} PSA-graded Japanese cards
• Cost basis: ฿{cost:,.0f} | Market value: ฿{mv:,.0f}
• Total P&L: ฿{pnl:+,.0f} ({pnl_pct:+.1f}%)

SIGNALS:
• 🟢 BUY  ({len(buys)}):    {fmt_cards(buys)}
• 🔴 SELL ({len(sells)}):   {fmt_cards(sells)}
• 🔵 HOLD ({len(holds)}):   {fmt_cards(holds[:6])}
• 🟠 REVIEW ({len(reviews)}): {fmt_cards(reviews)}

TOP GAINERS: {fmt_cards(top_gain)}
BIGGEST LOSERS: {fmt_cards(top_loss)}
"""

        prompt = f"""You are a sharp, emotionally intelligent Pokemon card investment advisor for a collector in Thailand.
Analyze this portfolio and write a concise briefing. Follow these rules exactly:

1. LINE 1: One powerful headline — the single most urgent truth about this portfolio right now (emoji + bold statement)
2. Then 6-9 bullet points, each 1-2 lines. Mix of: what's working, what's bleeding, what to act on NOW
3. Use specific card names. Be direct. Use emojis: 🚨💰📉🔥⚡🎯💎⏳🧊
4. Make it personal — address the collector as "you"
5. LAST 2 lines: "BOTTOM LINE:" then one clear sentence on what to do this week

Keep total length tight — under 350 words. No headers. Just flow.

{context}"""

        client  = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        return f"⚠️ AI summary error: {e}"


# ── Card image disk cache ─────────────────────────────────────────────────────
# Strategy: download once from Collectr CDN at startup, serve from local disk.
# Falls back to PSA CloudFront cert images if Collectr CDN fails for any card.

_IMG_CACHE_DIR = Path(__file__).parent / "cache" / "images"
_SNAPSHOT_PATH = Path(__file__).parent / "cache" / "latest_snapshot.json"

# ── Startup snapshot restore ──────────────────────────────────────────────────
try:
    if _SNAPSHOT_PATH.exists():
        _cache["data"] = json.loads(
            _SNAPSHOT_PATH.read_text(encoding="utf-8")
        )
        _cache["timestamp"] = _cache["data"].get("timestamp")
        app.logger.info(
            f"[BOOT] Restored snapshot from {_SNAPSHOT_PATH.name} "
            f"(timestamp={_cache['timestamp']})"
        )
except Exception as e:
    app.logger.warning(f"[BOOT] Snapshot restore failed: {e}")

# Collectr product IDs → human label
_COLLECTR_PRODUCTS = {
    "10010852": "SLOWPOKE",
    "10012098": "PSYDUCK",
    "10013016": "CHARIZARD EX",
    "10011603": "MAGIKARP",
    "577896":   "FULL ART/PIKACHU",
    "10030009": "PIKACHU McDONALD'S",
    "10009523": "PIKACHU SV PRE-ORDER",
    "10012128": "MEW EX",
    "10012662": "DETECTIVE PIKACHU",
    "10023355": "SYLVEON EX",
    "10004913": "SNORLAX-HOLO",
    "10012104": "SNORLAX",
    "250510":   "PIKACHU YU NAGABA",
    "10026716": "SNORLAX GREEN BACK",
    "10023360": "UMBREON EX",
    "10010048": "PONCHO-WEARING PIKACHU",
}

# PSA cert numbers — used as fallback when Collectr CDN fails
_PSA_CERT_FALLBACKS = {
    "10010852": "131858430",
    "10012098": "102808568",
    "10013016": "129722527",
    "10011603": "105922889",
    "577896":   "137306655",
    "10030009": "131827338",
    "10009523": "124286500",
    "10012128": "111987130",
    "10012662": "87561186",
    "10023355": "139017599",
    "10004913": "131215747",
    "10012104": "139442643",
    "250510":   "123698796",
    "10026716": "111230748",
    "10023360": "110351015",
    "10010048": "119421425",
}

# Exception cards (no Collectr URL) — served directly from PSA cert images
_PSA_EXCEPTION_CERTS = {
    "136143757": "PIKACHU ILLUS CONTEST 2024",
    "133726675": "PIKACHU GOLDEN BOX",
    "124559934": "MISCHIEVOUS PICHU",
}

# Richer metadata used by the Tier 3 image-search fallback.
# Keyed by cert → (set_hint, card_num, pokemon_name)
_PSA_CERT_METADATA = {
    "136143757": ("ILLUSTRATION CONTEST 2024", "242", "PIKACHU"),
    "133726675": ("GOLDEN BOX JAPANESE",       "003", "PIKACHU"),
    "124559934": ("GRANIPH PURCHASE CAMPAIGN", "214", "MISCHIEVOUS PICHU"),
}


def _write_tier_meta(img_path: Path, tier: str, source: str = "") -> None:
    """Write a small sidecar JSON recording which tier supplied this image."""
    try:
        meta_path = img_path.with_suffix(img_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps({
            "tier": tier,
            "source": source,
            "ts": datetime.now().isoformat(timespec="seconds"),
        }))
    except Exception:
        pass


def _fetch_psa_cert_image(cert: str) -> bytes | None:
    """
    Fetch card image for a PSA cert, trying tiers in order:
      T0 manual override  →  T1 CloudFront CDN  →  T2 PSA cert page (Playwright)
         →  T3 DuckDuckGo image search with smart matching

    First tier to return bytes wins. Result is cached and a .meta.json sidecar
    records which tier supplied it.
    """
    import requests as _req
    _IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    img_path = _IMG_CACHE_DIR / f"psa_{cert}.jpg"
    if img_path.exists() and img_path.stat().st_size > 500:
        return img_path.read_bytes()

    cert_label = _PSA_EXCEPTION_CERTS.get(cert, cert)

    # ── Tier 0: manual override ───────────────────────────────────────────
    try:
        from manual_override import check_manual_override
        data = check_manual_override(cert, "psa")
        if data:
            img_path.write_bytes(data)
            _write_tier_meta(img_path, "T0-manual", "manual_image_overrides/")
            app.logger.info(f"[IMG][T0] Manual override used for cert {cert} ({cert_label})")
            return data
    except Exception as e:
        app.logger.warning(f"[IMG][T0] manual_override unavailable: {e}")

    # ── Tier 1: PSA CloudFront CDN ────────────────────────────────────────
    psa_url = f"https://d1htnxwo4o0jhw.cloudfront.net/cert/{cert}.jpg"
    try:
        r = _req.get(psa_url, timeout=15, headers={
            "Referer": "https://www.psacard.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        if r.status_code == 200 and len(r.content) > 500:
            img_path.write_bytes(r.content)
            _write_tier_meta(img_path, "T1-cloudfront", psa_url)
            app.logger.info(f"[IMG][T1] CloudFront cached: cert {cert}")
            return r.content
        app.logger.warning(f"[IMG][T1] CloudFront {r.status_code} for cert {cert} — trying T2")
    except Exception as e:
        app.logger.warning(f"[IMG][T1] CloudFront failed cert {cert}: {e} — trying T2")

    # ── Tier 2: PSA cert page scrape (Playwright) ─────────────────────────
    try:
        from psa_page_scraper import fetch_psa_page_image
        data = fetch_psa_page_image(cert, _IMG_CACHE_DIR)
        if data:
            img_path.write_bytes(data)
            _write_tier_meta(img_path, "T2-psa-page", f"https://www.psacard.com/cert/{cert}")
            app.logger.info(f"[IMG][T2] PSA page scrape cached: cert {cert}")
            return data
        app.logger.warning(f"[IMG][T2] PSA page returned no image for cert {cert} — trying T3")
    except Exception as e:
        app.logger.warning(f"[IMG][T2] PSA page scraper failed cert {cert}: {e} — trying T3")

    # ── Tier 3: image search fallback ─────────────────────────────────────
    try:
        from image_search_fallback import fetch_via_image_search
        # Derive set_hint & card_num from the label/cert_key registry
        set_hint, card_num, pokemon_name = _PSA_CERT_METADATA.get(
            cert, ("", "", cert_label)
        )
        data = fetch_via_image_search(
            label=pokemon_name,
            cert=cert,
            set_hint=set_hint,
            card_num=card_num,
            cache_dir=_IMG_CACHE_DIR,
        )
        if data:
            # image_search_fallback caches to psa_<cert>.jpg, so the bytes
            # are already on disk in the expected place.
            if img_path.exists() and img_path.stat().st_size > 500:
                _write_tier_meta(img_path, "T3-image-search", "duckduckgo")
                app.logger.info(f"[IMG][T3] Image-search match cached: cert {cert}")
                return data
        app.logger.warning(f"[IMG][T3] Image-search found no acceptable match for cert {cert}")
    except Exception as e:
        app.logger.warning(f"[IMG][T3] Image-search fallback failed cert {cert}: {e}")

    app.logger.error(f"[IMG] All tiers exhausted for cert {cert} ({cert_label}) — no image available")
    return None


def _fetch_collectr_image(product_id: str) -> bytes | None:
    """
    Download a Collectr product image to disk.
    Tier 0 manual override → Collectr CDN → PSA cert fallback chain.
    """
    import requests as _req
    _IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    img_path = _IMG_CACHE_DIR / f"{product_id}.webp"
    if img_path.exists() and img_path.stat().st_size > 500:
        return img_path.read_bytes()
    label = _COLLECTR_PRODUCTS.get(product_id, product_id)

    # Tier 0: manual override (zero-network escape hatch)
    try:
        from manual_override import check_manual_override
        data = check_manual_override(product_id, "collectr")
        if data:
            img_path.write_bytes(data)
            _write_tier_meta(img_path, "T0-manual", "manual_image_overrides/")
            app.logger.info(f"[IMG][T0] Manual override used for {label} ({product_id})")
            return data
    except Exception as e:
        app.logger.warning(f"[IMG][T0] manual_override unavailable: {e}")

    cdn_url = (
        f"https://public.getcollectr.com/public-assets/products/"
        f"product_{product_id}.webp"
        f"?optimizer=image&format=webp&width=400&quality=80&strip=metadata"
    )
    try:
        r = _req.get(cdn_url, timeout=15, headers={
            "Referer": "https://app.getcollectr.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        if r.status_code == 200 and len(r.content) > 500:
            img_path.write_bytes(r.content)
            app.logger.info(f"[IMG] Collectr cached: {label}")
            return r.content
        app.logger.warning(f"[IMG] Collectr CDN {r.status_code} for {label} — trying PSA fallback")
    except Exception as e:
        app.logger.warning(f"[IMG] Collectr failed for {label}: {e} — trying PSA fallback")
    cert = _PSA_CERT_FALLBACKS.get(product_id)
    if cert:
        return _fetch_psa_cert_image(cert)
    return None


def validate_and_fetch_all() -> dict:
    """
    Validate all 19 card images. Re-fetch any missing or corrupt ones.
    Returns { id: 'ok' | 'fetched' | 'failed' } for each card.
    """
    report = {}
    for pid, label in _COLLECTR_PRODUCTS.items():
        img_path = _IMG_CACHE_DIR / f"{pid}.webp"
        if img_path.exists() and img_path.stat().st_size > 500:
            report[pid] = "ok"
        else:
            app.logger.info(f"[IMG] Fetching: {label}")
            report[pid] = "fetched" if _fetch_collectr_image(pid) else "failed"
    for cert, label in _PSA_EXCEPTION_CERTS.items():
        img_path = _IMG_CACHE_DIR / f"psa_{cert}.jpg"
        if img_path.exists() and img_path.stat().st_size > 500:
            report[cert] = "ok"
        else:
            app.logger.info(f"[IMG] Fetching PSA: {label}")
            report[cert] = "fetched" if _fetch_psa_cert_image(cert) else "failed"
    ok = sum(1 for v in report.values() if v in ("ok", "fetched"))
    app.logger.info(f"[IMG] Validation complete: {ok}/{len(report)} images ready")
    return report


def _prefetch_images_bg():
    """
    Background startup task: populate the image cache via Playwright live fetch.
    Cold HTTP to Collectr CDN returns 403 for most cards; the only reliable method
    is to use the browser's in-context cookies when visiting each product page.
    Skips if ALL images are already cached (e.g. after a previous run).
    """
    import time as _t
    _t.sleep(3)

    # Count how many images are already on disk
    _IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = sum(
        1 for pid in _COLLECTR_PRODUCTS
        if (_IMG_CACHE_DIR / f"{pid}.webp").exists()
        and (_IMG_CACHE_DIR / f"{pid}.webp").stat().st_size > 500
    )
    cached += sum(
        1 for cert in _PSA_EXCEPTION_CERTS
        if (_IMG_CACHE_DIR / f"psa_{cert}.jpg").exists()
        and (_IMG_CACHE_DIR / f"psa_{cert}.jpg").stat().st_size > 500
    )
    total = len(_COLLECTR_PRODUCTS) + len(_PSA_EXCEPTION_CERTS)
    # Note: _PSA_EXCEPTION_CERTS cards always fail (404 from PSA) — only check if Collectr images are cached
    required_cached = len(_COLLECTR_PRODUCTS)

    if cached >= required_cached:
        app.logger.info(f"[IMG] All {total} images already cached — skipping prefetch.")
        return

    app.logger.info(f"[IMG] {cached}/{total} images cached. Launching Playwright to fetch missing ones...")
    try:
        from collectr_live_fetcher import fetch_live_prices_sync
        fetch_live_prices_sync(concurrency=5)
        app.logger.info("[IMG] Background image prefetch complete.")
    except Exception as e:
        app.logger.warning(f"[IMG] Background prefetch failed: {e}")


threading.Thread(target=_prefetch_images_bg, daemon=True).start()


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    # Ensure master workbook exists and sync CSV on first run
    try:
        from master_workbook import ensure_master_exists, MASTER_PATH
        from csv_master_sync import run as run_csv_sync
        import os

        ensure_master_exists()

        # Check if CSV is newer than master
        csv_glob_path = Path(__file__).parent / "My Collection CSV - *.csv"
        csv_files = sorted(Path(__file__).parent.glob("My Collection CSV - *.csv"))
        if csv_files:
            csv_path = csv_files[-1]
            if csv_path.stat().st_mtime > MASTER_PATH.stat().st_mtime:
                app.logger.info("CSV is newer than master — syncing...")
                result = run_csv_sync()
                app.logger.info(f"CSV sync result: {result}")
    except Exception as e:
        app.logger.warning(f"Master workbook init failed: {e}")

    return render_template("index.html")


# ── Market Outperformers multi-source helpers ────────────────────────────────
_BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/121.0.0.0 Safari/537.36")

def _http_get(url: str, timeout: int = 12) -> str:
    """Best-effort HTTP GET returning decoded text. Raises on error."""
    import urllib.request
    req = urllib.request.Request(url, headers={
        "User-Agent": _BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    # handle gzip if server returned it despite no Accept-Encoding
    if data[:2] == b"\x1f\x8b":
        import gzip
        data = gzip.decompress(data)
    return data.decode("utf-8", errors="ignore")


def _fetch_pokemontcg_io(limit: int = 10) -> list:
    """Primary API: pokemontcg.io free tier. Returns ranked rows by CardMarket trend price."""
    import urllib.parse, json as _json
    params = urllib.parse.urlencode({
        "q": "supertype:Pokémon",
        "orderBy": "-cardmarket.prices.trendPrice",
        "pageSize": str(limit * 2),
        "select": "id,name,number,set,rarity,images,cardmarket,tcgplayer",
    })
    html = _http_get(f"https://api.pokemontcg.io/v2/cards?{params}")
    payload = _json.loads(html)
    out = []
    for c in (payload.get("data") or [])[:limit]:
        cm = (c.get("cardmarket") or {}).get("prices") or {}
        tp = ((c.get("tcgplayer") or {}).get("prices") or {})
        tp_hi = 0
        for variant in tp.values():
            if isinstance(variant, dict):
                v = variant.get("market") or variant.get("mid") or 0
                if v and v > tp_hi:
                    tp_hi = v
        out.append({
            "source":    "tcgapi",
            "name":      c.get("name") or "",
            "number":    c.get("number"),
            "set":       (c.get("set") or {}).get("name"),
            "rarity":    c.get("rarity"),
            "image":     (c.get("images") or {}).get("small"),
            "price":     cm.get("trendPrice") or tp_hi or None,
            "ccy":       "EUR" if cm.get("trendPrice") else ("USD" if tp_hi else None),
            "price_eur": cm.get("trendPrice"),
            "price_usd": tp_hi or None,
            "url":       (c.get("cardmarket") or {}).get("url") or (c.get("tcgplayer") or {}).get("url"),
        })
    return out


def _fetch_snkr(limit: int = 10) -> list:
    """Scrape snkrdunk.com Pokemon trading cards listing page.
    snkrdunk renders SSR HTML with product cards; we extract name + JPY price via regex.
    If the site format changes, this silently returns [] and the caller falls back."""
    import re
    try:
        html = _http_get("https://snkrdunk.com/en/brands/pokemon/trading-cards", timeout=15)
    except Exception as e:
        app.logger.info(f"SNKR fetch failed: {e}")
        return []
    items = []
    # Pattern 1: Nuxt-style product cards — <a href="/en/products/..."> ... name ... ¥price
    for m in re.finditer(
        r'href="(/en/products/[^"#?]+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<>{]{3,120})\s*(?:</[^>]+>\s*)*[\s\S]{0,600}?¥\s*([0-9,]+)',
        html
    ):
        path, name, price = m.groups()
        name = re.sub(r'\s+', ' ', name).strip()
        if not name or any(x in name.lower() for x in ("login", "register", "sign up", "trademark")):
            continue
        try:
            p_jpy = float(price.replace(",", ""))
        except ValueError:
            continue
        if p_jpy < 100:  # noise
            continue
        items.append({
            "source": "snkr",
            "name": name,
            "price": p_jpy,
            "ccy": "JPY",
            "price_jpy": p_jpy,
            "url": "https://snkrdunk.com" + path,
            "image": None,
        })
        if len(items) >= limit:
            break
    # Pattern 2: JSON in __NUXT__ / __NEXT_DATA__
    if not items:
        for m in re.finditer(
            r'"name"\s*:\s*"([^"]{3,120})"[\s\S]{0,200}?"(?:minPrice|price)"\s*:\s*"?([0-9]+)"?',
            html
        ):
            name, price = m.groups()
            try:
                p = float(price)
            except ValueError:
                continue
            if p < 100:
                continue
            items.append({
                "source": "snkr",
                "name": name.strip(),
                "price": p,
                "ccy": "JPY",
                "price_jpy": p,
                "url": "https://snkrdunk.com/en/brands/pokemon/trading-cards",
                "image": None,
            })
            if len(items) >= limit:
                break
    return items


def _fetch_pricecharting(limit: int = 10) -> list:
    """Scrape PriceCharting Pokemon cards highest-value table.
    Uses the 'sort by loose-price descending' page — purely public HTML."""
    import re
    try:
        html = _http_get(
            "https://www.pricecharting.com/console/pokemon-cards?sort=highest-price&condition=",
            timeout=15,
        )
    except Exception:
        # Fallback to general category page
        try:
            html = _http_get("https://www.pricecharting.com/category/pokemon-cards", timeout=15)
        except Exception as e:
            app.logger.info(f"PriceCharting fetch failed: {e}")
            return []
    items = []
    # PriceCharting rows: <a href="/game/..." class="...">Name</a> ... <td class="price ...">$123.45</td>
    for m in re.finditer(
        r'<a\s+href="(/game/[^"]+)"[^>]*>\s*([^<]{3,140})\s*</a>[\s\S]{0,800}?\$([0-9][\d,]*\.?\d*)',
        html
    ):
        path, name, price = m.groups()
        name = re.sub(r'\s+', ' ', name).strip()
        try:
            p = float(price.replace(",", ""))
        except ValueError:
            continue
        if p < 5:
            continue
        items.append({
            "source": "pricechart",
            "name": name,
            "price": p,
            "ccy": "USD",
            "price_usd": p,
            "url": "https://www.pricecharting.com" + path,
            "image": None,
        })
        if len(items) >= limit:
            break
    return items


def _fetch_ebay(limit: int = 10) -> list:
    """Scrape eBay Pokemon sold-listings sorted by price (highest) — public search HTML."""
    import re
    url = ("https://www.ebay.com/sch/i.html?"
           "_nkw=pokemon+card&_sop=16&LH_Sold=1&LH_Complete=1&_ipg=60")
    try:
        html = _http_get(url, timeout=15)
    except Exception as e:
        app.logger.info(f"eBay fetch failed: {e}")
        return []
    items = []
    # Each sold listing has: class="s-item__title" ... and class="s-item__price"
    for m in re.finditer(
        r'class="s-item__title"[^>]*>\s*(?:<span[^>]*>New Listing</span>)?\s*'
        r'(?:<span[^>]*>)?([^<]{5,200}?)</(?:span|div|h3)>'
        r'[\s\S]{0,900}?class="s-item__price"[^>]*>\s*(?:<span[^>]*>)?'
        r'\$([0-9][\d,]*\.?\d*)',
        html
    ):
        name, price = m.groups()
        name = re.sub(r'\s+', ' ', name).strip()
        if not name or "Shop on eBay" in name or len(name) < 5:
            continue
        try:
            p = float(price.replace(",", ""))
        except ValueError:
            continue
        if p < 20:  # exclude low-priced noise
            continue
        # try to locate the item URL near the title
        link = None
        lm = re.search(re.escape(name[:40]) + r'[\s\S]{0,600}?href="(https://www\.ebay\.com/itm/[^"]+)"', html)
        if lm:
            link = lm.group(1)
        items.append({
            "source": "ebay",
            "name": name,
            "price": p,
            "ccy": "USD",
            "price_usd": p,
            "url": link or url,
            "image": None,
        })
        if len(items) >= limit:
            break
    return items


def _merge_outperformers(sources: dict, limit: int = 10) -> list:
    """Merge per-source rows into a unified ranking.

    Scoring: USD-normalized price, weighted by number of sources it appears in.
    Cards matching across multiple sources rank higher than single-source outliers.
    """
    import re
    # Very rough FX just to place everything on a comparable scale for ranking
    fx = {"USD": 1.0, "EUR": 1.08, "JPY": 1/150.0, "THB": 1/36.0}

    def _key(name: str) -> str:
        return re.sub(r'[^a-z0-9]', '', (name or "").lower())[:32]

    bucket = {}   # key -> merged row
    for src_name, rows in sources.items():
        for r in rows or []:
            k = _key(r.get("name"))
            if not k:
                continue
            price_usd = None
            try:
                p = float(r.get("price") or 0)
                price_usd = p * fx.get(r.get("ccy") or "USD", 1.0)
            except (ValueError, TypeError):
                price_usd = None
            if k not in bucket:
                bucket[k] = {
                    "name": r.get("name"),
                    "set": r.get("set"),
                    "number": r.get("number"),
                    "rarity": r.get("rarity"),
                    "image": r.get("image"),
                    "sources": [],
                    "urls": {},
                    "prices": {},
                    "price_usd_max": 0.0,
                }
            row = bucket[k]
            if src_name not in row["sources"]:
                row["sources"].append(src_name)
            row["urls"][src_name] = r.get("url")
            row["prices"][src_name] = {"price": r.get("price"), "ccy": r.get("ccy")}
            if price_usd and price_usd > row["price_usd_max"]:
                row["price_usd_max"] = price_usd
            # fill missing metadata from any source
            for fld in ("set", "number", "rarity", "image"):
                if not row.get(fld) and r.get(fld):
                    row[fld] = r.get(fld)

    # Rank: primary by source-count (diversity), secondary by USD-max price
    ranked = sorted(
        bucket.values(),
        key=lambda x: (len(x["sources"]), x["price_usd_max"]),
        reverse=True,
    )
    return ranked[:limit]


@app.route("/api/market-outperformers")
def api_market_outperformers():
    """Overall Pokemon TCG top-10 outperformers merged across public sources.

    Sources attempted (graceful fallback on error):
      - pokemontcg.io  (CardMarket + TCGPlayer prices — primary, always tried)
      - snkrdunk.com   (Asian market JPY pricing — scraped)
      - pricecharting.com (USD loose/graded — scraped)
      - ebay.com       (sold-listings high→low — scraped)
    Cached 24h in cache/market_outperformers.json.
    """
    import json as _json, time as _time
    cache_dir = Path(__file__).parent / "cache"
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / "market_outperformers.json"
    # 24h cache
    force = (request.args.get("force") or "").lower() in ("1", "true", "yes")
    try:
        if (not force) and cache_file.exists() and (_time.time() - cache_file.stat().st_mtime) < 86400:
            return jsonify(_json.loads(cache_file.read_text(encoding="utf-8")))
    except Exception:
        pass

    sources = {}
    connected = []
    errors = {}

    # Run each source inside its own try/except so one failure does not kill the endpoint
    for src_name, fn in (
        ("tcgapi",      _fetch_pokemontcg_io),
        ("snkr",        _fetch_snkr),
        ("pricechart",  _fetch_pricecharting),
        ("ebay",        _fetch_ebay),
    ):
        try:
            rows = fn(limit=15) or []
            sources[src_name] = rows
            if rows:
                connected.append(src_name)
        except Exception as e:
            errors[src_name] = str(e)[:180]
            sources[src_name] = []
            app.logger.info(f"outperformers source {src_name} failed: {e}")

    merged = _merge_outperformers(sources, limit=10)

    # If the merged list is empty (all scrapers failed AND tcgapi was blocked),
    # fall back to whatever single source did return data, flattened.
    if not merged:
        for src_name in ("tcgapi", "snkr", "pricechart", "ebay"):
            if sources.get(src_name):
                fallback = []
                for r in sources[src_name][:10]:
                    fallback.append({
                        "name": r.get("name"),
                        "set": r.get("set"),
                        "number": r.get("number"),
                        "rarity": r.get("rarity"),
                        "image": r.get("image"),
                        "sources": [src_name],
                        "urls": {src_name: r.get("url")},
                        "prices": {src_name: {"price": r.get("price"), "ccy": r.get("ccy")}},
                        "price_usd_max": 0.0,
                    })
                merged = fallback
                break

    result = {
        "status":     "success" if merged else "error",
        "updated_at": datetime.now().isoformat(),
        "connected":  connected,
        "errors":     errors,
        "rows":       merged,
        "counts":     {k: len(v) for k, v in sources.items()},
        "note":       "Merged ranking: tcgapi + snkr + pricechart + ebay. Cards appearing in more sources rank higher.",
    }
    try:
        cache_file.write_text(_json.dumps(result, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return jsonify(result)


@app.route("/api/status")
def api_status():
    with _lock:
        if _cache["data"] is None:
            return jsonify(status="empty", message="No data yet — click Refresh.")
        return jsonify(_cache["data"])


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    with _lock:
        try:
            app.logger.info("Refresh triggered…")

            # Step 1: Sync CSV into master workbook
            try:
                from csv_master_sync import run as run_csv_sync
                sync_result = run_csv_sync()
                app.logger.info(f"CSV sync: {sync_result}")
            except Exception as se:
                app.logger.warning(f"CSV sync failed: {se}")

            # Step 2: Fetch live prices
            live_prices = None
            data_source = "snapshot"
            try:
                from collectr_live_fetcher import fetch_live_prices_sync
                live_prices = fetch_live_prices_sync(concurrency=5)
                fetched = sum(1 for v in live_prices.values() if v)
                app.logger.info(f"Live fetch complete: {fetched}/19 cards")
                data_source = "live"
            except Exception as fe:
                app.logger.warning(f"Live fetch failed ({fe}) — falling back to static snapshot")

            # Step 3: Compute analytics
            result = live_refresh(live_prices=live_prices)
            payload = build_response(result, data_source=data_source)
            _cache["data"] = payload
            _cache["timestamp"] = payload["timestamp"]

            _SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
            _SNAPSHOT_PATH.write_text(
                json.dumps(_cache["data"], ensure_ascii=False, default=str),
                encoding="utf-8",
            )

            return jsonify(payload)
        except Exception as e:
            app.logger.error(f"Refresh error: {e}", exc_info=True)
            return jsonify(status="error", message=str(e)), 500


@app.route("/api/health")
def api_health():
    """Health check endpoint for monitoring Flask + tunnel status."""
    try:
        from pathlib import Path
        master_path = Path(__file__).parent / "Portfolio_Master.xlsx"
        excel_locked = False

        # Check if Excel is locked by trying to open it
        if master_path.exists():
            try:
                import openpyxl
                wb = openpyxl.load_workbook(str(master_path), data_only=True)
                wb.close()
            except Exception:
                excel_locked = True

        ngrok_domain = request.headers.get("Host", "unknown")

        return jsonify({
            "flask": "ok",
            "excel_lock": excel_locked,
            "ngrok_domain": ngrok_domain,
            "ts": datetime.now().isoformat(),
        })
    except Exception as e:
        app.logger.warning(f"Health check error: {e}")
        return jsonify({"flask": "error", "message": str(e)}), 500

# ── Add Card Routes ──────────────────────────────────────────────────────────

@app.route("/api/add-card/search", methods=["POST"])
def api_add_card_search():
    """Search for a card by PSA cert number."""
    data = request.get_json() or {}
    cert = (data.get("cert") or "").strip()

    if not re.match(r"^\d{6,10}$", cert):
        return jsonify(status="error", message="Cert must be 6-10 digits"), 400

    try:
        from add_card_service import search
        preview = asyncio.run(search(cert))
        from dataclasses import asdict
        return jsonify(status="ok", preview=asdict(preview))
    except Exception as e:
        app.logger.error(f"Add Card search failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/add-card/save", methods=["POST"])
def api_add_card_save():
    """Save a new card to master workbook."""
    try:
        data = request.get_json() or {}
        preview = data.get("preview") or {}
        my_info = data.get("my_info") or {}

        from master_workbook import append_card

        row = {
            "Item Status": my_info.get("item_status", "Active"),
            "Item": preview.get("item", ""),
            "Cert Number": preview.get("cert", ""),
            "Grade Issuer": "PSA",
            "Grade": preview.get("grade", ""),
            "Autograph Grade": "-",
            "Year": preview.get("year", ""),
            "Set": preview.get("set_name", ""),
            "Card Number": preview.get("card_number", ""),
            "Subject": preview.get("subject", ""),
            "Variety": preview.get("variety", ""),
            "Serial": "-",
            "Category": "-",
            "My Cost": my_info.get("my_cost"),
            "PSA Estimate": preview.get("psa_estimate_thb"),
            "Gain/Loss": "",
            "My Value": "",
            "Date Acquired": my_info.get("date_acquired"),
            "Source": my_info.get("source", ""),
            "My Notes": my_info.get("notes", ""),
            "Vault Status": "Unvaulted",
            "Vaulted Date": "-",
            "Days Vaulted": "-",
            "Listing Status": "-",
            "Listing Date": "-",
            "Listing Price": "-",
            "Sold Status": "-",
            "Sold On": "-",
            "Sold Date": "-",
            "Sold Price": "-",
            "Sold Fees": "-",
            "Sold Proceeds": "-",
            "Payment Date": "-",
            "collectr_url": preview.get("collectr_url"),
            "collectr_price_thb": preview.get("collectr_price_thb"),
            "ebay_avg_thb": preview.get("ebay_avg_thb"),
            "ebay_n_comps": preview.get("ebay_n_comps", 0),
            "image_match_ok": preview.get("image_match_ok", False),
            "last_updated": datetime.now().isoformat(),
        }

        new_row_idx = append_card(row, source="add-card")
        return jsonify(status="ok", master_row=new_row_idx)
    except Exception as e:
        app.logger.error(f"Add Card save failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/add-card/live-search", methods=["POST"])
def api_live_search():
    """
    Live search across Collectr + eBay.
    Body: {"query": str}
    Returns: {"status": "ok", "results": [Candidate, ...], "took_ms": int}
    """
    data = request.get_json() or {}
    query = (data.get("query") or "").strip()

    if len(query) < 2:
        return jsonify(status="ok", results=[], took_ms=0)

    # Cert fast-path guard (frontend should handle, but defend in depth)
    if re.match(r"^\d{6,10}$", query):
        return jsonify(status="cert_detected", results=[], took_ms=0)

    try:
        from add_card_service import live_search
        t0 = time.time()
        # limit bumped to 40 so the enlarged single-grade column has more to display
        results = asyncio.run(live_search(query, limit=40))
        took_ms = int((time.time() - t0) * 1000)
        return jsonify(status="ok", results=results, took_ms=took_ms)
    except Exception as e:
        app.logger.error(f"Live search failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/add-card/search-by-candidate", methods=["POST"])
def api_search_by_candidate():
    """
    Handle clicking on a search result candidate.
    Performs 3-source merge (PSA + Collectr + eBay) and returns PreviewCard.

    Body: {
      "product_id": str | null,
      "url": str,
      "title": str,
      "subject": str,
      "card_number": str,
      "grade": int | null
    }
    """
    data = request.get_json() or {}
    product_id = data.get("product_id")
    url = data.get("url", "")
    title = data.get("title", "")

    if not (product_id or url):
        return jsonify(status="error", message="Missing product_id or url"), 400

    try:
        from add_card_service import search_by_candidate_impl
        t0 = time.time()
        preview = asyncio.run(search_by_candidate_impl(product_id, url, title))
        from dataclasses import asdict
        took_ms = int((time.time() - t0) * 1000)
        return jsonify(
            status="ok",
            preview=asdict(preview),
            took_ms=took_ms
        )
    except Exception as e:
        app.logger.error(f"Search by candidate failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/csv-sync", methods=["POST"])
def api_csv_sync():
    """Manually trigger CSV->Master sync."""
    try:
        from csv_master_sync import run as run_csv_sync
        summary = run_csv_sync()
        return jsonify(status="ok", **summary)
    except Exception as e:
        app.logger.error(f"CSV sync error: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/add-card/image-validate/<cert>")
def api_image_validate(cert):
    """Validate images and compare PSA vs Collectr."""
    if not re.match(r"^\d+$", cert):
        return jsonify(status="error", message="Invalid cert"), 400

    try:
        psa_data = _fetch_psa_cert_image(cert)
        collectr_data = None
        try:
            from collectr_live_fetcher import CARD_REGISTRY
            for card in CARD_REGISTRY:
                if card.get("cert") == cert and card.get("url"):
                    product_id = card["url"].split("/")[-1]
                    collectr_data = _fetch_collectr_image(product_id)
                    break
        except Exception:
            pass

        psa_ok = psa_data is not None and len(psa_data) > 500
        collectr_ok = collectr_data is not None and len(collectr_data) > 500

        image_match_ok = False
        if psa_ok and collectr_ok:
            try:
                import imagehash
                from PIL import Image
                from io import BytesIO

                psa_img = Image.open(BytesIO(psa_data))
                collectr_img = Image.open(BytesIO(collectr_data))

                psa_hash = imagehash.average_hash(psa_img)
                collectr_hash = imagehash.average_hash(collectr_img)
                distance = psa_hash - collectr_hash
                image_match_ok = distance < 10
            except Exception as e:
                app.logger.warning(f"Image hash comparison failed: {e}")
                image_match_ok = True

        return jsonify(
            status="ok",
            psa_ok=psa_ok,
            collectr_ok=collectr_ok,
            image_match=image_match_ok,
        )
    except Exception as e:
        app.logger.error(f"Image validation error: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500



@app.route("/card-img/<product_id>")
def card_img(product_id):
    """Serve Collectr card image from local disk cache."""
    if not re.match(r"^\d+$", product_id):
        return "Invalid product ID", 400
    img_path = _IMG_CACHE_DIR / f"{product_id}.webp"
    data = (
        img_path.read_bytes()
        if img_path.exists() and img_path.stat().st_size > 500
        else _fetch_collectr_image(product_id)
    )
    if data:
        return data, 200, {
            "Content-Type": "image/webp",
            "Cache-Control": "public, max-age=604800",
        }
    return "Image not available", 404


@app.route("/psa-img/<cert>")
def psa_img(cert):
    """Serve PSA cert card image from local disk cache."""
    if not re.match(r"^\d+$", cert):
        return "Invalid cert", 400
    img_path = _IMG_CACHE_DIR / f"psa_{cert}.jpg"
    data = (
        img_path.read_bytes()
        if img_path.exists() and img_path.stat().st_size > 500
        else _fetch_psa_cert_image(cert)
    )
    if data:
        return data, 200, {
            "Content-Type": "image/jpeg",
            "Cache-Control": "public, max-age=604800",
        }
    return "PSA image not available", 404


@app.route("/api/validate-images")
def api_validate_images():
    """Validate all card images."""
    report = validate_and_fetch_all()
    ok = sum(1 for v in report.values() if v in ("ok", "fetched"))
    failed = [k for k, v in report.items() if v == "failed"]
    return jsonify(
        status="ok",
        total=len(report),
        ready=ok,
        failed=failed,
        details=report,
    )


@app.route("/portfolio_pnl_v2.html")
def portfolio_pnl_dashboard():
    """Serve the standalone P&L Performance dashboard HTML (embedded in the P&L Performance tab)."""
    from flask import send_from_directory, abort
    # File lives alongside webapp.py (source) or next to the .exe (onedir frozen build).
    # launcher.py sets cwd to EXE_DIR in the frozen case, so cwd is always correct.
    candidates = [Path.cwd(), Path(__file__).resolve().parent]
    for d in candidates:
        fp = d / "portfolio_pnl_v2.html"
        if fp.is_file():
            return send_from_directory(str(d), "portfolio_pnl_v2.html")
    abort(404, description="portfolio_pnl_v2.html not found")


@app.route("/api/ai-summary", methods=["POST"])
def api_ai_summary():
    try:
        payload = request.get_json(force=True) or {}
        portfolio = payload.get("portfolio", [])
        summary = payload.get("summary", {})
        text = generate_ai_summary(portfolio, summary)
        return jsonify(status="success", text=text)
    except Exception as e:
        app.logger.error(f"AI summary error: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/quantitative-matrix")
def api_quantitative_matrix():
    try:
        from scripts.quantitative_matrix import parse_csv, analyze_cards
        csv_path = Path(__file__).parent / "My Collection CSV - 19.csv"
        cards = parse_csv(str(csv_path))
        result = analyze_cards(cards)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Quantitative matrix error: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/matrix")
def matrix_dashboard():
    return render_template("quantitative_matrix.html")


if __name__ == "__main__":
    print("=" * 60)
    print("  PSA x Collectr Tracer — Web App")
    print("  http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)
# end of webapp.py
