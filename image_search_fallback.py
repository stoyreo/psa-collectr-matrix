"""
Tier 4: Image Search Fallback with Smart Matching
Fallback image fetcher for PSA-graded cards when Collectr & PSA CloudFront fail.
Uses DuckDuckGo image search + multi-layer validation (keyword, size/aspect, slab signature, optional LLM).
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional
import requests
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

# DuckDuckGo endpoints
DDG_SEARCH = "https://duckduckgo.com/"
DDG_IMAGES = "https://duckduckgo.com/i.js"

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def _get_vqd_token(query: str) -> Optional[str]:
    """Extract vqd token from DuckDuckGo search page."""
    try:
        r = requests.get(
            DDG_SEARCH,
            params={"q": query, "iax": "images", "ia": "images"},
            headers={"User-Agent": DEFAULT_USER_AGENT},
            timeout=10,
        )
        match = re.search(r'vqd=["\']([^"\']+)', r.text)
        if match:
            return match.group(1)
    except Exception as e:
        logger.debug(f"[IMG Search] vqd token fetch failed: {e}")
    return None


def _build_query(label: str, card_num: str, set_hint: str) -> str:
    """Build DuckDuckGo query: {label} #{card_num} {set_hint} PSA 10 Pokemon."""
    parts = [label, f"#{card_num}", set_hint, "PSA 10", "Pokemon"]
    # Strip duplicates, uppercase-normalize
    seen = set()
    unique = []
    for p in parts:
        p_upper = p.upper().strip()
        if p_upper and p_upper not in seen:
            unique.append(p_upper)
            seen.add(p_upper)
    return " ".join(unique)


def _keyword_score(title: str, image_url: str, label: str, card_num: str, set_hint: str) -> int:
    """
    Layer 1: keyword score (0-4).
    Counts hits for: pokemon name, set hint, "psa", card number.
    """
    combined = (title + " " + image_url).lower()
    score = 0

    # (a) Pokemon name (lowercased label, any word if multi-word)
    label_words = label.lower().split()
    if any(w in combined for w in label_words):
        score += 1

    # (b) Any word from set_hint
    set_words = set_hint.lower().split()
    if any(w in combined for w in set_words):
        score += 1

    # (c) "psa"
    if "psa" in combined:
        score += 1

    # (d) Card number or #card_number
    if card_num in combined or f"#{card_num}" in combined:
        score += 1

    return score


def _validate_image_bytes(img_bytes: bytes, label: str, card_num: str) -> tuple[Optional[Image.Image], bool]:
    """
    Layer 2: size & aspect validation.
    Returns (PIL.Image, passed_layer2) tuple.
    """
    # Check minimum size
    if len(img_bytes) < 500:
        logger.debug(f"[IMG Search] Image too small ({len(img_bytes)} B)")
        return None, False

    # Parse image
    try:
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        logger.debug(f"[IMG Search] Cannot parse image: {e}")
        return None, False

    w, h = img.size

    # Check dimensions
    if w < 150 or h < 150:
        logger.debug(f"[IMG Search] Image too small ({w}x{h})")
        return None, False

    # Check aspect ratio (0.5–0.85)
    aspect = w / h
    if not (0.5 <= aspect <= 0.85):
        logger.debug(f"[IMG Search] Aspect ratio {aspect:.2f} outside 0.5–0.85")
        return None, False

    return img, True


def _check_slab_signature(img: Image.Image) -> bool:
    """
    Layer 3: PSA slab signature check.
    Look at top 15% horizontal band; red dominance (R > 150, R > G+30, R > B+30).
    """
    w, h = img.size
    band_height = max(1, int(h * 0.15))
    top_band = img.crop((0, 0, w, band_height))

    # Calculate mean RGB
    px = top_band.load()
    r_sum = g_sum = b_sum = 0
    count = 0
    for y in range(top_band.height):
        for x in range(top_band.width):
            r, g, b = px[x, y][:3]
            r_sum += r
            g_sum += g
            b_sum += b
            count += 1

    if count == 0:
        return False

    mean_r = r_sum / count
    mean_g = g_sum / count
    mean_b = b_sum / count

    # Red dominance check
    is_red_dominant = (
        mean_r > 150 and
        mean_r > mean_g + 30 and
        mean_r > mean_b + 30
    )
    return is_red_dominant


def _llm_vision_check(img_bytes: bytes, label: str, card_num: str) -> Optional[bool]:
    """
    Layer 4: Optional LLM vision tiebreak (Claude).
    Only if ENABLE_LLM_IMAGE_CHECK=1 and ANTHROPIC_API_KEY set.
    Returns True (accept), False (reject), or None (skip/error).
    """
    if os.environ.get("ENABLE_LLM_IMAGE_CHECK") != "1":
        return None

    try:
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return None

        # Encode image as base64
        import base64
        b64 = base64.b64encode(img_bytes).decode("utf-8")

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"Is this image a PSA-graded Pokémon card matching '{label}' #{card_num}? Reply YES or NO only.",
                        },
                    ],
                }
            ],
        )
        response_text = message.content[0].text.strip().upper()
        return "YES" in response_text

    except Exception as e:
        logger.debug(f"[IMG Search] LLM vision check failed (non-blocking): {e}")
        return None


def fetch_via_image_search(
    label: str,
    cert: str,
    set_hint: str,
    card_num: str,
    cache_dir: Path,
) -> Optional[bytes]:
    """
    Search for a matching card image online, validate, cache, return bytes.

    Args:
        label: Human card label (e.g., "PIKACHU")
        cert: PSA cert number (e.g., "136143757")
        set_hint: Set identifier (e.g., "ILLUSTRATION CONTEST 2024")
        card_num: Card number (e.g., "242")
        cache_dir: Directory to cache images

    Returns:
        Image bytes (JPG) or None if all layers fail.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"psa_{cert}.jpg"

    # Check cache first
    if cache_path.exists() and cache_path.stat().st_size > 500:
        logger.debug(f"[IMG Search] Cache hit for cert {cert}")
        return cache_path.read_bytes()

    query = _build_query(label, card_num, set_hint)
    logger.info(f"[IMG Search] Starting search for cert {cert}: {query}")

    # Get vqd token
    vqd = _get_vqd_token(query)
    if not vqd:
        logger.warning(f"[IMG Search] Could not get vqd token")
        return None

    # Fetch results from DuckDuckGo
    try:
        r = requests.get(
            DDG_IMAGES,
            params={"q": query, "o": "json", "vqd": vqd},
            headers={"User-Agent": DEFAULT_USER_AGENT},
            timeout=10,
        )
        results = r.json().get("results", [])
    except Exception as e:
        logger.warning(f"[IMG Search] DuckDuckGo fetch failed: {e}")
        return None

    if not results:
        logger.warning(f"[IMG Search] No results from DuckDuckGo")
        return None

    logger.debug(f"[IMG Search] Got {len(results)} candidates")

    # Layer 1: keyword scoring + Layer 2: size/aspect validation
    candidates = []
    for idx, result in enumerate(results[:10]):  # Top 10
        title = result.get("title", "")
        image_url = result.get("image", "")
        deep_url = result.get("deep_url", "")

        score = _keyword_score(title, image_url, label, card_num, set_hint)
        if score < 2:
            logger.debug(f"[IMG Search]   Candidate {idx+1}: REJECT (score {score}/4)")
            continue

        # Download image
        try:
            img_r = requests.get(image_url, timeout=10)
            img_bytes = img_r.content
        except Exception as e:
            logger.debug(f"[IMG Search]   Candidate {idx+1}: SKIP (download failed: {e})")
            continue

        # Validate bytes and dimensions
        pil_img, passed_layer2 = _validate_image_bytes(img_bytes, label, card_num)
        if not passed_layer2:
            logger.debug(f"[IMG Search]   Candidate {idx+1}: REJECT (Layer 2 failed)")
            continue

        # Layer 3: slab signature
        has_slab = _check_slab_signature(pil_img)
        logger.debug(
            f"[IMG Search]   Candidate {idx+1}: score={score}/4, slab={has_slab}, "
            f"size={pil_img.width}x{pil_img.height}, {image_url[:60]}"
        )

        candidates.append({
            "score": score,
            "slab": has_slab,
            "image_url": image_url,
            "img_bytes": img_bytes,
            "index": idx + 1,
        })

    if not candidates:
        logger.warning(f"[IMG Search] No valid candidates (all failed Layer 2)")
        return None

    # Sort by: slab (True first), then score (desc)
    candidates.sort(key=lambda x: (-x["slab"], -x["score"]))

    # Layer 4: LLM tiebreak for top candidates with same score+slab
    winner = candidates[0]
    if len(candidates) > 1:
        top_score = candidates[0]["score"]
        top_slab = candidates[0]["slab"]
        tied = [c for c in candidates if c["score"] == top_score and c["slab"] == top_slab]

        if len(tied) >= 2:
            logger.debug(f"[IMG Search] {len(tied)} candidates tied (score={top_score}, slab={top_slab}) — checking LLM")
            for candidate in tied:
                llm_result = _llm_vision_check(candidate["img_bytes"], label, card_num)
                if llm_result is True:
                    logger.info(f"[IMG Search] LLM accepted candidate {candidate['index']}")
                    winner = candidate
                    break
                elif llm_result is False:
                    logger.debug(f"[IMG Search] LLM rejected candidate {candidate['index']}")

    # Cache and return
    try:
        cache_path.write_bytes(winner["img_bytes"])
        logger.info(
            f"[IMG Search] Accepted candidate {winner['index']}/{len(results)} "
            f"(score {winner['score']}/4, slab={winner['slab']}): {winner['image_url'][:70]}"
        )
        return winner["img_bytes"]
    except Exception as e:
        logger.error(f"[IMG Search] Failed to cache image: {e}")
        return None


if __name__ == "__main__":
    """Self-test: run the three known-bad cards."""
    import sys

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
    )

    test_cards = [
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

    cache_dir = Path(__file__).parent / "cache" / "images"
    print(f"\nRunning self-test with cache_dir={cache_dir}\n")

    for card in test_cards:
        print(f"Testing cert={card['cert']} ({card['label']} #{card['card_num']}):")
        result = fetch_via_image_search(
            label=card["label"],
            cert=card["cert"],
            set_hint=card["set_hint"],
            card_num=card["card_num"],
            cache_dir=cache_dir,
        )
        if result:
            print(f"  SUCCESS: {len(result)} bytes cached\n")
        else:
            print(f"  FAILED: returned None\n")
