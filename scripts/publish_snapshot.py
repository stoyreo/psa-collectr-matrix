"""
PSA x Collectr Tracer — Snapshot Publisher
Generates a JSON snapshot of the portfolio from Portfolio_Master.xlsx + static Collectr prices.
Used for offline fallback when the live backend is unreachable.
"""

import sys
import json
import logging
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))

from refresh_live import live_refresh

logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

SNAPSHOT_PATH = Path(__file__).parent.parent / "cache" / "latest_snapshot.json"
WEB_SNAPSHOT_PATH = Path(__file__).parent.parent / "web" / "public" / "snapshot.json"


def serialize_card(card):
    """Serialize a card for API response (from webapp.py)."""
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

    sig = card.get("signal_data", {})
    mv = card.get("market_value")
    cost = card.get("my_cost")
    pnl = (mv - cost) if (mv and cost) else None
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
    """Build API response from refresh result."""
    portfolio = [serialize_card(c) for c in result.get("portfolio", [])]
    summary = result.get("summary", {})
    insights = result.get("insights", {})
    exceptions = result.get("exceptions", [])
    timestamp = result.get("timestamp", datetime.now().isoformat())

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


def publish_snapshot():
    """Generate snapshot and save to both cache and web/public."""
    try:
        logger.info("Generating snapshot from Portfolio_Master.xlsx + static prices...")
        result = live_refresh(live_prices=None)  # None = use static prices
        payload = build_response(result, data_source="snapshot")

        # Save to cache
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, default=str, indent=2),
            encoding="utf-8",
        )
        logger.info(f"✓ Snapshot saved to {SNAPSHOT_PATH}")

        # Save to web/public for Vercel fallback
        WEB_SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        WEB_SNAPSHOT_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, default=str, indent=2),
            encoding="utf-8",
        )
        logger.info(f"✓ Snapshot saved to {WEB_SNAPSHOT_PATH}")

        return {"status": "success", "path": str(SNAPSHOT_PATH), "cards": len(payload.get("portfolio", []))}
    except Exception as e:
        logger.error(f"Snapshot generation failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    result = publish_snapshot()
    sys.exit(0 if result["status"] == "success" else 1)
