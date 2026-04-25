from pathlib import Path

_ROOT = Path(__file__).parent
_OVERRIDE_DIR = _ROOT / "manual_image_overrides"


def check_manual_override(key: str, kind: str) -> bytes | None:
    """
    Return the bytes of a manually-placed override image, if present.

    Args:
        key:  cert number (for PSA cards) or Collectr product id (for Collectr cards)
        kind: "psa" or "collectr"

    Returns:
        Image bytes (≥500 B) or None if no override.
    """
    if kind == "psa":
        fp = _OVERRIDE_DIR / f"psa_{key}.jpg"
    elif kind == "collectr":
        fp = _OVERRIDE_DIR / f"{key}.webp"
    else:
        return None
    if fp.exists() and fp.stat().st_size > 500:
        return fp.read_bytes()
    return None
