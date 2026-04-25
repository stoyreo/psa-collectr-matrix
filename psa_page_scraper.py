"""
PSA Cert Detail Page Scraper (Tier 3)
Loads https://www.psacard.com/cert/{cert} directly and extracts the card image from the DOM.
Uses sync Playwright with optimized CSS selectors and HTTP download with proper headers.
"""

import re
from pathlib import Path
from typing import Optional

import requests


_CACHE_DIR = Path(__file__).resolve().parent / "cache" / "images"


def fetch_psa_page_image(cert: str, cache_dir: Path = None) -> Optional[bytes]:
    """
    Scrape https://www.psacard.com/cert/<cert> via Playwright and return the card image bytes.

    Args:
        cert: Certificate number (e.g., "136143757")
        cache_dir: Cache directory path. Defaults to project cache/images/

    Returns:
        Image bytes on success, None on failure. Never raises.
    """
    if cache_dir is None:
        cache_dir = _CACHE_DIR

    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"psa_page_{cert}.jpg"

    # Check cache first
    if cache_path.exists() and cache_path.stat().st_size >= 500:
        print(f"[PSA Page] Cache hit: psa_page_{cert}.jpg ({cache_path.stat().st_size} bytes)")
        return cache_path.read_bytes()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(f"[PSA Page] ERROR: playwright not installed — run: python -m pip install playwright")
        return None

    url = f"https://www.psacard.com/cert/{cert}"

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()

            try:
                # Load the page with 30s timeout
                page.goto(url, wait_until="domcontentloaded", timeout=30000)

                # Try 3 CSS selectors in order
                selectors = [
                    "img.cert-card-front",           # Tier 1: specific card front class
                    "img[data-testid='cert-image']", # Tier 2: data-testid attribute
                    ".cert-preview img",              # Tier 3: preview section
                ]

                image_url = None
                for selector in selectors:
                    try:
                        elem = page.query_selector(selector)
                        if elem:
                            src = elem.get_attribute("src")
                            if src and src.startswith("http"):
                                print(f"[PSA Page] Found image via '{selector}': {src[:80]}")
                                image_url = src
                                break
                    except Exception:
                        pass

                # If no specific selector matched, fallback to finding any large image
                if not image_url:
                    try:
                        best = page.evaluate("""
                            () => {
                                const imgs = [...document.querySelectorAll('img')];
                                let best = null, bestArea = 0;
                                for (const img of imgs) {
                                    const area = img.naturalWidth * img.naturalHeight;
                                    if (area > 50000 && img.src && img.src.startsWith('http')) {
                                        bestArea = area;
                                        best = img.src;
                                    }
                                }
                                return best;
                            }
                        """)
                        if best:
                            print(f"[PSA Page] Found image via fallback (largest): {best[:80]}")
                            image_url = best
                    except Exception as e:
                        print(f"[PSA Page] Fallback selector failed: {e}")

                if not image_url:
                    print(f"[PSA Page] No image URL found for cert {cert}")
                    browser.close()
                    return None

                # Download the image via HTTP with Referer header
                try:
                    headers = {
                        "Referer": url,
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    }
                    response = requests.get(image_url, headers=headers, timeout=10)

                    if response.status_code != 200:
                        print(f"[PSA Page] HTTP {response.status_code} downloading {image_url[:80]}")
                        browser.close()
                        return None

                    img_bytes = response.content
                    if len(img_bytes) < 500:
                        print(f"[PSA Page] Image too small ({len(img_bytes)} bytes) for cert {cert}")
                        browser.close()
                        return None

                    # Cache it
                    cache_path.write_bytes(img_bytes)
                    print(f"[PSA Page] Downloaded and cached: psa_page_{cert}.jpg ({len(img_bytes)} bytes)")
                    browser.close()
                    return img_bytes

                except requests.RequestException as e:
                    print(f"[PSA Page] Download failed: {e}")
                    browser.close()
                    return None

            except Exception as e:
                print(f"[PSA Page] Page load error: {e}")
                browser.close()
                return None

    except Exception as e:
        print(f"[PSA Page] Browser error: {e}")
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python psa_page_scraper.py <cert_number>")
        sys.exit(1)

    cert = sys.argv[1]
    result = fetch_psa_page_image(cert)

    if result:
        cache_path = _CACHE_DIR / f"psa_page_{cert}.jpg"
        print(f"\nSuccess: {cache_path}")
    else:
        print(f"\nFailed to fetch image for cert {cert}")
        sys.exit(1)
