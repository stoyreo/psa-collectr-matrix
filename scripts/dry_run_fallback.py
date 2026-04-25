#!/usr/bin/env python3
"""
Dry-run verification of the 4-tier image fallback chain.
Tests the 3 sticky certs without modifying webapp.py or tier modules.
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
)
logger = logging.getLogger(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

IMG_CACHE_DIR = PROJECT_ROOT / "cache" / "images"
IMG_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Test certs with their metadata
TEST_CERTS = [
    {
        "cert": "136143757",
        "label": "PIKACHU",
        "set_hint": "ILLUSTRATION CONTEST 2024",
        "card_num": "242",
    },
    {
        "cert": "133726675",
        "label": "PIKACHU",
        "set_hint": "GOLDEN BOX JAPANESE",
        "card_num": "003",
    },
    {
        "cert": "124559934",
        "label": "MISCHIEVOUS PICHU",
        "set_hint": "GRANIPH PURCHASE CAMPAIGN",
        "card_num": "214",
    },
]


def _write_tier_meta(img_path: Path, tier: str, source: str = "") -> None:
    """Write a sidecar JSON recording which tier supplied this image."""
    try:
        meta_path = img_path.with_suffix(img_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps({
            "tier": tier,
            "source": source,
            "ts": datetime.now().isoformat(timespec="seconds"),
        }))
    except Exception:
        pass


def test_tier0(cert: str) -> tuple[bytes | None, str]:
    """Tier 0: manual override check."""
    try:
        from manual_override import check_manual_override
        data = check_manual_override(cert, "psa")
        if data:
            logger.info(f"[T0] Manual override found for cert {cert}")
            return data, "manual_override"
        logger.info(f"[T0] No manual override for cert {cert}")
        return None, ""
    except Exception as e:
        logger.info(f"[T0] Error: {e}")
        return None, ""


def test_tier1(cert: str) -> tuple[bytes | None, int, str]:
    """Tier 1: PSA CloudFront CDN."""
    import requests
    psa_url = f"https://d1htnxwo4o0jhw.cloudfront.net/cert/{cert}.jpg"
    try:
        r = requests.get(psa_url, timeout=15, headers={
            "Referer": "https://www.psacard.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })
        logger.info(f"[T1] CloudFront returned HTTP {r.status_code} for cert {cert}")
        if r.status_code == 200 and len(r.content) > 500:
            logger.info(f"[T1] Accepted: {len(r.content)} bytes")
            return r.content, r.status_code, psa_url
        return None, r.status_code, psa_url
    except Exception as e:
        logger.info(f"[T1] Request failed: {e}")
        return None, 0, psa_url


def test_tier2(cert: str) -> tuple[bytes | None, str]:
    """Tier 2: PSA cert page scraper (Playwright)."""
    try:
        from psa_page_scraper import fetch_psa_page_image
        data = fetch_psa_page_image(cert, IMG_CACHE_DIR)
        if data:
            logger.info(f"[T2] PSA page scraper succeeded: {len(data)} bytes")
            return data, f"https://www.psacard.com/cert/{cert}"
        logger.info(f"[T2] PSA page scraper returned None")
        return None, ""
    except ImportError as e:
        logger.info(f"[T2] Skipped: {e}")
        return None, "skipped"
    except Exception as e:
        logger.info(f"[T2] Error: {e}")
        return None, ""


def test_tier3(cert: str, label: str, set_hint: str, card_num: str) -> tuple[bytes | None, dict]:
    """Tier 3: image search fallback with detailed stats."""
    try:
        from image_search_fallback import fetch_via_image_search

        stats = {
            "attempted": True,
            "candidates": 0,
            "layer1_pass": 0,
            "layer2_pass": 0,
            "layer3_pass": 0,
            "accepted": False,
            "url": "",
            "size": 0,
        }

        data = fetch_via_image_search(
            label=label,
            cert=cert,
            set_hint=set_hint,
            card_num=card_num,
            cache_dir=IMG_CACHE_DIR,
        )

        if data:
            stats["accepted"] = True
            stats["size"] = len(data)
            logger.info(f"[T3] Image search succeeded: {len(data)} bytes")
            return data, stats

        logger.info(f"[T3] Image search returned None")
        return None, stats

    except Exception as e:
        logger.info(f"[T3] Error: {e}")
        return None, {"attempted": False, "error": str(e)}


def get_image_dimensions(img_bytes: bytes) -> tuple[int, int] | None:
    """Get image dimensions using Pillow."""
    try:
        from PIL import Image
        img = Image.open(BytesIO(img_bytes))
        return img.size
    except Exception as e:
        logger.warning(f"Could not get dimensions: {e}")
        return None


def main():
    logger.info("=" * 80)
    logger.info("DRY-RUN: 4-Tier Fallback Chain Verification")
    logger.info("=" * 80)

    results = []

    for test_card in TEST_CERTS:
        cert = test_card["cert"]
        label = test_card["label"]
        set_hint = test_card["set_hint"]
        card_num = test_card["card_num"]

        logger.info(f"\n{'='*80}")
        logger.info(f"CERT {cert} — {label} #{card_num} ({set_hint})")
        logger.info("="*80)

        img_path = IMG_CACHE_DIR / f"psa_{cert}.jpg"
        final_winner = None
        winning_tier = None
        cached_size = 0

        # Tier 0: manual override
        logger.info("\n[TIER 0] Manual Override Check")
        t0_data, t0_source = test_tier0(cert)
        if t0_data:
            final_winner = t0_data
            winning_tier = "T0-manual"
            _write_tier_meta(img_path, winning_tier, t0_source)

        # Tier 1: CloudFront
        if not final_winner:
            logger.info("\n[TIER 1] PSA CloudFront CDN")
            t1_data, t1_status, t1_url = test_tier1(cert)
            if t1_data:
                final_winner = t1_data
                winning_tier = "T1-cloudfront"
                _write_tier_meta(img_path, winning_tier, t1_url)
            else:
                logger.info(f"  → HTTP {t1_status} (expected 404 for these sticky certs)")

        # Tier 2: PSA page scraper
        if not final_winner:
            logger.info("\n[TIER 2] PSA Page Scraper (Playwright)")
            t2_data, t2_source = test_tier2(cert)
            if t2_data:
                final_winner = t2_data
                winning_tier = "T2-psa-page"
                _write_tier_meta(img_path, winning_tier, t2_source)
            elif t2_source == "skipped":
                logger.info("  → Skipped (Playwright not installed in sandbox)")

        # Tier 3: image search fallback
        if not final_winner:
            logger.info("\n[TIER 3] Image Search Fallback (DuckDuckGo)")
            t3_data, t3_stats = test_tier3(cert, label, set_hint, card_num)
            if t3_data:
                final_winner = t3_data
                winning_tier = "T3-image-search"
                _write_tier_meta(img_path, winning_tier, "duckduckgo")
                logger.info(f"  → Stats: {t3_stats}")
            else:
                logger.info(f"  → Image search failed or no acceptable candidate")

        # Report final outcome
        logger.info("\n" + "-" * 80)
        if final_winner:
            if img_path.exists():
                cached_size = img_path.stat().st_size
            dims = get_image_dimensions(final_winner)
            dims_str = f"{dims[0]}x{dims[1]}" if dims else "unknown"
            logger.info(f"RESULT: {winning_tier} succeeded")
            logger.info(f"  → Cached file: {img_path.name}")
            logger.info(f"  → Size: {cached_size} bytes")
            logger.info(f"  → Dimensions: {dims_str}")
            results.append({
                "cert": cert,
                "label": label,
                "winning_tier": winning_tier,
                "cached_size": cached_size,
                "dimensions": dims_str,
                "success": True,
            })
        else:
            logger.info(f"RESULT: No tier succeeded — image not recovered")
            results.append({
                "cert": cert,
                "label": label,
                "winning_tier": None,
                "cached_size": 0,
                "dimensions": None,
                "success": False,
            })

    # Summary
    logger.info(f"\n{'='*80}")
    logger.info("SUMMARY")
    logger.info("="*80)

    successes = [r for r in results if r["success"]]
    recovery_rate = len(successes)

    for r in results:
        status = "OK" if r["success"] else "FAIL"
        tier = r["winning_tier"] or "NONE"
        logger.info(f"{r['cert']} ({r['label']}): {status} → {tier} | {r['cached_size']} bytes | {r['dimensions']}")

    logger.info(f"\nOverall recovery: {recovery_rate}/3 certs recovered")
    if recovery_rate > 0:
        tiers = set(r["winning_tier"] for r in results if r["success"])
        tiers_str = ", ".join(sorted(tiers))
        logger.info(f"Winning tiers: {tiers_str}")

    return 0 if recovery_rate == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
