"""Cache Manager - JSON file-based caching"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import CACHE_CONFIG

logger = logging.getLogger(__name__)

def load_cache(cache_file: Path) -> Dict[str, Any]:
    """Load cache from JSON file."""
    if not cache_file.exists():
        logger.debug(f"Cache file not found: {cache_file}")
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
        logger.debug(f"Loaded cache from {cache_file.name}")
        return cache
    except Exception as e:
        logger.warning(f"Failed to load cache: {e}")
        return {}

def save_cache(data: Dict[str, Any], cache_file: Path) -> None:
    """Save cache to JSON file."""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        logger.debug(f"Saved cache to {cache_file.name}")
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")

def is_stale(cache: Dict[str, Any], key: str, max_age_hours: int = 24) -> bool:
    """Check if a cache entry is stale."""
    if key not in cache:
        return True
    entry = cache[key]
    if "timestamp" not in entry:
        return True
    try:
        timestamp = datetime.fromisoformat(entry["timestamp"])
        age = datetime.now() - timestamp
        is_old = age > timedelta(hours=max_age_hours)
        if is_old:
            logger.debug(f"Cache entry '{key}' is stale ({age.days}d old)")
        return is_old
    except Exception as e:
        logger.warning(f"Failed to check cache age for '{key}': {e}")
        return True

def get_cached_comps(match_key: str, cache_file: Path) -> Optional[List[Dict[str, Any]]]:
    """Get cached comps for a card match key."""
    if not CACHE_CONFIG["enabled"]:
        return None
    cache = load_cache(cache_file)
    if match_key not in cache:
        return None
    if is_stale(cache, match_key, CACHE_CONFIG["comps_max_age_hours"]):
        return None
    entry = cache[match_key]
    return entry.get("comps")

def set_cached_comps(match_key: str, comps: List[Dict[str, Any]], cache_file: Path) -> None:
    """Cache comps for a card match key."""
    if not CACHE_CONFIG["enabled"]:
        return
    cache = load_cache(cache_file)
    cache[match_key] = {"timestamp": datetime.now().isoformat(), "comps": comps}
    save_cache(cache, cache_file)
    logger.debug(f"Cached {len(comps)} comps for {match_key}")

if __name__ == "__main__":
    print("cache_manager module loaded")
