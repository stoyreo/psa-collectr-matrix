"""
Configuration for Pokémon TCG Portfolio Intelligence System.
Central hub for all system parameters, thresholds, and settings.
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure directories exist
CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Input/Output Files
CSV_INPUT_PATH = DATA_DIR / "My Collection CSV - 19.csv"
EXCEL_OUTPUT_PATH = OUTPUT_DIR / "Pokemon_Portfolio_Intelligence.xlsx"
CACHE_COMPS_FILE = CACHE_DIR / "comps_cache.json"
CACHE_METADATA_FILE = CACHE_DIR / "metadata_cache.json"

# ============================================================================
# CONFIDENCE THRESHOLDS (0-100)
# ============================================================================
CONFIDENCE_THRESHOLDS = {
    "exact": 90,
    "strong": 85,
    "moderate": 70,
    "weak": 50,
}

MATCH_CONFIDENCE_BANDS = {
    "EXACT": (90, 100),
    "STRONG": (85, 89),
    "MODERATE": (70, 84),
    "WEAK": (50, 69),
    "REJECT": (0, 49),
}

# ============================================================================
# eBay SEARCH PARAMETERS
# ============================================================================
EBAY_CONFIG = {
    "target_comp_count": (10, 30),
    "max_results": 60,
    "search_only_sold": True,
    "include_completed": True,
    "remove_duplicates": True,
    "timeout_seconds": 10,
}

COMP_FILTERS = {
    "bundle_keywords": ["lot", "bundle", "x2", "x3", "x4", "x5", "playset", "set of"],
    "fake_keywords": ["custom", "fake", "reproduction", "reprint", "artist"],
    "damaged_keywords": ["damaged", "torn", "water damage", "crease", "stain"],
    "grade_tolerance": 0,
}

# ============================================================================
# CURRENCY SETTINGS
# ============================================================================
CURRENCY = {
    "primary": "THB",
    "display_options": ["USD", "THB"],
    "default_display": "THB",
    "exchange_rates": {
        "USD_to_THB": 33.22,
    }
}

# Convenience accessor
USD_TO_THB = CURRENCY["exchange_rates"]["USD_to_THB"]

# ============================================================================
# DATA SOURCES
# ============================================================================
DATA_SOURCES = {
    "ebay": True,
    "collectr": False,
    "psa": True,
    "demo_mode": False,
}

DEMO_MODE_CONFIG = {
    "enabled": True,
    "base_variance": 0.15,
    "grade_mult": {
        8: 0.7,
        9: 0.85,
        10: 1.0,
    },
    "sample_comp_count": 12,
    "recency_mix": {
        "last_7_days": 0.3,
        "last_30_days": 0.5,
        "last_90_days": 0.15,
        "older": 0.05,
    }
}

# ============================================================================
# SIGNAL THRESHOLDS
# ============================================================================
SIGNAL_CONFIG = {
    "buy_upside_multiplier": 1.15,
    "buy_confidence_threshold": 85,
    "sell_downside_multiplier": 0.85,
    "sell_confidence_threshold": 70,
    "review_confidence_threshold": 80,
    "liquidity_thresholds": {
        "high": 8,
        "medium": 4,
        "low": 0,
    },
    "trend_recency_split": 0.5,
    "trend_threshold": 0.10,
}

# ============================================================================
# OUTLIER DETECTION
# ============================================================================
OUTLIER_CONFIG = {
    "method": "iqr",
    "iqr_multiplier": 1.5,
    "min_data_points": 3,
}

# ============================================================================
# DATA NORMALIZATION
# ============================================================================
NORMALIZATION = {
    "null_values": ["-", "N/A", "NA", "", "null", "none"],
    "date_format": "%m/%d/%Y",
    "decimal_places": 2,
}

# ============================================================================
# REPORTING & INSIGHTS
# ============================================================================
INSIGHTS_CONFIG = {
    "top_undervalued_count": 5,
    "top_gainers_count": 5,
    "weak_positions_count": 5,
    "illiquid_threshold": 4,
}

# ============================================================================
# CACHE SETTINGS
# ============================================================================
CACHE_CONFIG = {
    "comps_max_age_hours": 24,
    "metadata_max_age_hours": 72,
    "enabled": True,
}

# ============================================================================
# LOGGING
# ============================================================================
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
    "file": OUTPUT_DIR / "portfolio_refresh.log",
}

# ============================================================================
# EXCEL EXPORT SETTINGS
# ============================================================================
EXCEL_CONFIG = {
    "sheet_names": [
        "DASHBOARD",
        "PORTFOLIO",
        "EBAY_COMPS",
        "COLLECTR_MAP",
        "PSA_MAP",
        "INSIGHTS",
        "EXCEPTIONS",
        "TARGETS",
        "ALERT_LOG",
        "CONFIG",
    ],
    "colors": {
        "header_bg": "1B2A4A",
        "header_text": "FFFFFF",
        "row_alt": "F5F6F8",
        "row_normal": "FFFFFF",
        "positive": "4CAF50",
        "negative": "F44336",
        "neutral": "2196F3",
    },
    "currency_format": "฿#,##0",
    "percent_format": "0.0%",
    "date_format": "mm/dd/yyyy",
    "default_width": 12,
    "auto_width": True,
    "freeze_rows": 1,
}

# ============================================================================
# PORTFOLIO COLUMNS
# ============================================================================
PORTFOLIO_COLUMNS = [
    "Status",
    "Subject",
    "Grade",
    "Set Code",
    "Card #",
    "Variety",
    "Year",
    "My Cost (THB)",
    "PSA Estimate (THB)",
    "Market Value (THB)",
    "P&L (THB)",
    "P&L %",
    "Confidence %",
    "Liquidity",
    "Trend",
    "Risk Level",
    "Signal",
    "Match Key",
    "Cert Number",
    "Date Acquired",
    "Days Held",
]

EBAY_COMPS_COLUMNS = [
    "Match Key",
    "Comp Title",
    "Sold Date",
    "Sold Price (THB)",
    "Shipping (THB)",
    "Total Price (THB)",
    "Currency",
    "Comp URL",
    "Is Outlier",
    "Grade Confidence",
    "Notes",
]

PSA_MAP_COLUMNS = [
    "Subject",
    "Cert Number",
    "Grade",
    "Set",
    "Card #",
    "Variety",
    "Year",
    "Status",
]

INSIGHTS_COLUMNS = [
    "Category",
    "Subject",
    "Grade",
    "Set Code",
    "Card #",
    "My Cost (THB)",
    "Market Value (THB)",
    "P&L (THB)",
    "P&L %",
    "Explanation",
]

def get_config_summary() -> dict:
    """Return a dictionary of all config values for Excel export."""
    return {
        "CSV Input Path": str(CSV_INPUT_PATH),
        "Excel Output Path": str(EXCEL_OUTPUT_PATH),
        "Cache Directory": str(CACHE_DIR),
        "Demo Mode": DATA_SOURCES["demo_mode"],
        "eBay Target Comps": f"{EBAY_CONFIG['target_comp_count'][0]}-{EBAY_CONFIG['target_comp_count'][1]}",
        "Exact Match Confidence": CONFIDENCE_THRESHOLDS["exact"],
        "Strong Match Confidence": CONFIDENCE_THRESHOLDS["strong"],
        "Buy Signal Upside": f"{(SIGNAL_CONFIG['buy_upside_multiplier'] - 1) * 100:.0f}%",
        "Sell Signal Downside": f"{(1 - SIGNAL_CONFIG['sell_downside_multiplier']) * 100:.0f}%",
        "High Liquidity Threshold": SIGNAL_CONFIG["liquidity_thresholds"]["high"],
        "Medium Liquidity Threshold": SIGNAL_CONFIG["liquidity_thresholds"]["medium"],
        "Primary Currency": CURRENCY["primary"],
        "USD to THB Rate": CURRENCY["exchange_rates"]["USD_to_THB"],
        "Cache Enabled": CACHE_CONFIG["enabled"],
        "Cache Age (hours)": CACHE_CONFIG["comps_max_age_hours"],
    }

if __name__ == "__main__":
    print("Configuration loaded successfully.")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Cache Dir: {CACHE_DIR}")
    print(f"Output Dir: {OUTPUT_DIR}")
    print(f"CSV Input: {CSV_INPUT_PATH}")
