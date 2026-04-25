"""
PSA Cert Scraper
Fetches card images and grade confirmation from psacard.com cert pages.
Used as fallback for cards without a Collectr listing.

Cert page: https://www.psacard.com/cert/{cert_number}
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Disk-cache directory — relative to this script's parent (project root)
_CACHE_DIR = Path(__file__).resolve().parent.parent / "cache" / "images"

# Cards without Collectr URLs — scraped from PSA cert pages instead
PSA_EXCEPTION_REGISTRY = [
    {
        "key":         "pikachu_svp_242_psa10_illustrationcontest2024",
        "subject":     "PIKACHU",
        "card_number": "242",
        "variety":     "ILLUSTRATION CONTEST 2024",
        "grade":       10,
        "cert":        "136143757",
        "psa_est_usd": None,   # no PSA estimate in CSV
    },
    {
        "key":         "pikachu_asia25th_003_psa10_goldenboxjapanese",
        "subject":     "PIKACHU",
        "card_number": "003",
        "variety":     "GOLDEN BOX-JAPANESE",
        "grade":       10,
        "cert":        "133726675",
        "psa_est_usd": 78.21,
    },
    {
        "key":         "mischievouspichu_spromo_214_psa10_graniphpurchasecampaign",
        "subject":     "MISCHIEVOUS PICHU",
        "card_number": "214",
        "variety":     "GRANIPH PURCHASE CAMPAIGN",
        "grade":       10,
        "cert":        "124559934",
        "psa_est_usd": 109.98,
    },
]

PSA_CERT_BASE = "https://www.psacard.com/cert/{cert}"


async def _scrape_cert_image(page, cert: str, timeout_ms: int = 20000) -> Optional[str]:
    """
    Load a PSA cert page and extract the card image URL.
    PSA renders the card image in a large viewer — we grab the largest img src.
    """
    url = PSA_CERT_BASE.format(cert=cert)
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        # Wait for images to load
        await page.wait_for_timeout(3000)

        # Strategy 1: og:image meta tag (most reliable)
        og = await page.evaluate("""
            () => {
                const m = document.querySelector('meta[property="og:image"]');
                return m ? m.content : null;
            }
        """)
        if og and og.startswith("http"):
            logger.info(f"    Image (og:image): {og[:80]}")
            return og

        # Strategy 2: find the largest image on the page (card viewer)
        best = await page.evaluate("""
            () => {
                const imgs = [...document.querySelectorAll('img')];
                let best = null, bestArea = 0;
                for (const img of imgs) {
                    const area = img.naturalWidth * img.naturalHeight;
                    if (area > bestArea && img.src && img.src.startsWith('http')) {
                        bestArea = area;
                        best = { src: img.src, w: img.naturalWidth, h: img.naturalHeight };
                    }
                }
                return best;
            }
        """)
        if best and best.get("src"):
            logger.info(f"    Image (largest {best['w']}x{best['h']}): {best['src'][:80]}")
            return best["src"]

        # Strategy 3: look for CloudFront cert image pattern in page source
        content = await page.content()
        cf_matches = re.findall(
            r'https://d\w+\.cloudfront\.net/cert/[^"\'> ]+(?:\.jpg|\.png|\.webp)',
            content
        )
        if cf_matches:
            logger.info(f"    Image (cloudfront): {cf_matches[0][:80]}")
            return cf_matches[0]

        # Strategy 4: any image containing the cert number
        cert_img = await page.evaluate(f"""
            () => {{
                const imgs = [...document.querySelectorAll('img')];
                const certImg = imgs.find(i => i.src.includes('{cert}'));
                return certImg ? certImg.src : null;
            }}
        """)
        if cert_img:
            logger.info(f"    Image (cert-match): {cert_img[:80]}")
            return cert_img

        logger.warning(f"    No image found for cert {cert}")
        return None

    except Exception as e:
        logger.warning(f"    PSA cert fetch error ({cert}): {e}")
        return None


async def _scrape_one(browser, semaphore, card: dict, timeout_ms: int = 20000) -> dict:
    """Scrape a single PSA cert page."""
    async with semaphore:
        ctx  = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = await ctx.new_page()
        try:
            logger.info(f"  PSA scrape: {card['subject']} #{card['card_number']} cert={card['cert']}")
            image_url = await _scrape_cert_image(page, card["cert"], timeout_ms)

            # ── Download image using in-context browser request ──────────────
            if image_url:
                cert = card["cert"]
                _CACHE_DIR.mkdir(parents=True, exist_ok=True)
                # Always save as psa_{cert}.jpg — matches webapp /psa-img/<cert> route
                img_path = _CACHE_DIR / f"psa_{cert}.jpg"
                if not img_path.exists():
                    try:
                        img_resp = await ctx.request.get(image_url)
                        if img_resp.ok:
                            img_path.write_bytes(await img_resp.body())
                            logger.info(f"  IMG saved: psa_{cert}.jpg")
                        else:
                            logger.warning(f"  IMG fetch {img_resp.status}: cert {cert}")
                    except Exception as _img_err:
                        logger.warning(f"  IMG error for cert {cert}: {_img_err}")
                else:
                    logger.info(f"  IMG cached: psa_{cert}.jpg (already on disk)")

            # Return local route URL — webapp serves it from disk cache
            local_url = f"/psa-img/{card['cert']}" if image_url else None

            return {
                "key":          card["key"],
                "status":       "success" if image_url else "no_image",
                "image_url":    local_url,       # local Flask route
                "image_url_ext": image_url,      # original external URL (for reference)
                "cert":         card["cert"],
                "subject":      card["subject"],
                "card_number":  card["card_number"],
                "psa_est_usd":  card.get("psa_est_usd"),
            }
        except Exception as e:
            logger.warning(f"  PSA scrape failed ({card['subject']}): {e}")
            return {
                "key":    card["key"],
                "status": "error",
                "error":  str(e),
                "image_url": None,
            }
        finally:
            await ctx.close()


async def fetch_psa_exception_data(concurrency: int = 3) -> dict:
    """
    Scrape PSA cert pages for all exception cards (those without Collectr URLs).
    Returns a dict keyed by card key with image_url and metadata.
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise RuntimeError("playwright not installed")

    logger.info(f"[PSA Scraper] Fetching {len(PSA_EXCEPTION_REGISTRY)} exception cards…")

    results = {}
    semaphore = asyncio.Semaphore(concurrency)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        tasks = [_scrape_one(browser, semaphore, card) for card in PSA_EXCEPTION_REGISTRY]
        outcomes = await asyncio.gather(*tasks, return_exceptions=True)
        await browser.close()

    for outcome in outcomes:
        if isinstance(outcome, Exception):
            logger.error(f"[PSA Scraper] Unhandled: {outcome}")
            continue
        results[outcome["key"]] = outcome

    ok = sum(1 for v in results.values() if v.get("image_url"))
    logger.info(f"[PSA Scraper] Done: {ok}/{len(PSA_EXCEPTION_REGISTRY)} images retrieved")
    return results


def fetch_psa_exceptions_sync(concurrency: int = 3) -> dict:
    """Synchronous wrapper — safe to call from Flask."""
    return asyncio.run(fetch_psa_exception_data(concurrency))

if __name__ == "__main__":
    logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")
    results = fetch_psa_exceptions_sync()
    for key, v in results.items():
        img = v.get("image_url", "—")
        print(f"{v.get('subject')} #{v.get('card_number')}: {img}")
