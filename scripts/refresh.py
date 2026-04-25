"""Main Orchestrator - Coordinates full portfolio refresh"""
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from config import CSV_INPUT_PATH, CACHE_COMPS_FILE, LOGGING_CONFIG
from ingest import ingest_collection
from matching import generate_match_key, compute_match_confidence
from ebay_connector import get_ebay_comps
from psa_connector import verify_psa_certs
from signals import compute_signal, generate_insights
from cache_manager import get_cached_comps, set_cached_comps

logging.basicConfig(level=LOGGING_CONFIG["level"], format=LOGGING_CONFIG["format"],
    handlers=[logging.StreamHandler(), logging.FileHandler(LOGGING_CONFIG["file"])])
logger = logging.getLogger(__name__)

def full_refresh(csv_path: Path, workbook_path: Path) -> Dict[str, Any]:
    """Full portfolio refresh pipeline."""
    logger.info("="*70)
    logger.info("STARTING PORTFOLIO REFRESH")
    logger.info(f"CSV Input: {csv_path}")
    logger.info("="*70)
    
    exceptions = []
    portfolio = []
    
    try:
        logger.info("\n[1/7] Ingesting CSV...")
        raw_cards = ingest_collection(csv_path)
        logger.info(f"Ingested {len(raw_cards)} cards")
        
        logger.info("\n[2/7] Normalizing cards and generating match keys...")
        for i, card in enumerate(raw_cards, 1):
            try:
                match_key = generate_match_key(card)
                card["match_key"] = match_key
            except Exception as e:
                msg = f"Row {i}: Failed to generate match key - {e}"
                logger.error(msg)
                exceptions.append({"row": i, "error": msg})
        
        logger.info("\n[3/7] Fetching eBay comps...")
        for i, card in enumerate(raw_cards, 1):
            try:
                match_key = card.get("match_key")
                subject = card.get("subject", "Unknown")
                cached_comps = get_cached_comps(match_key, CACHE_COMPS_FILE)
                if cached_comps:
                    logger.info(f"  {i}. {subject} - Using cached comps ({len(cached_comps)} found)")
                    ebay_data = {"query_used": "CACHED", "comps": cached_comps, "stats": {}, "comp_count": len(cached_comps), "from_cache": True}
                else:
                    logger.info(f"  {i}. {subject} - Searching eBay...")
                    ebay_data = get_ebay_comps(card)
                    set_cached_comps(match_key, ebay_data.get("comps", []), CACHE_COMPS_FILE)
                card["ebay_data"] = ebay_data
                card["ebay_comps"] = ebay_data.get("comps", [])
                card["ebay_stats"] = ebay_data.get("stats", {})
            except Exception as e:
                msg = f"{i}. {card.get('subject')}: Failed to fetch eBay comps - {e}"
                logger.error(msg)
                exceptions.append({"row": i, "error": msg})
                card["ebay_comps"] = []
                card["ebay_stats"] = {}
        
        logger.info("\n[4/7] Computing market values from comps...")
        for i, card in enumerate(raw_cards, 1):
            try:
                comps = card.get("ebay_comps", [])
                if comps:
                    total_prices = [c.get("total_price", c.get("sold_price", 0)) for c in comps]
                    market_value = sorted(total_prices)[len(total_prices) // 2]
                else:
                    market_value = card.get("psa_estimate")
                card["market_value"] = market_value
                card["comp_count"] = len(comps)
            except Exception as e:
                logger.warning(f"{i}. {card.get('subject')}: Failed to compute market value - {e}")
                card["market_value"] = card.get("psa_estimate")
                card["comp_count"] = 0
        
        logger.info("\n[5/7] Computing match confidence...")
        for i, card in enumerate(raw_cards, 1):
            try:
                comps = card.get("ebay_comps", [])
                if comps:
                    confidences = [compute_match_confidence(card, c) for c in comps]
                    card["confidence"] = max(confidences) if confidences else 50
                else:
                    card["confidence"] = 50
            except Exception as e:
                logger.warning(f"{i}. {card.get('subject')}: Failed to compute confidence - {e}")
                card["confidence"] = 50
        
        logger.info("\n[6/7] Computing portfolio signals...")
        for i, card in enumerate(raw_cards, 1):
            try:
                signal_data = compute_signal(card)
                card["signal_data"] = signal_data
                logger.debug(f"  {i}. {card.get('subject')} -> {signal_data['signal']}")
            except Exception as e:
                msg = f"{i}. {card.get('subject')}: Failed to compute signal - {e}"
                logger.error(msg)
                exceptions.append({"row": i, "error": msg})
                card["signal_data"] = {"signal": "REVIEW", "risk_level": "HIGH", "confidence": 0, "upside_pct": 0, "liquidity": "LOW", "trend": "UNKNOWN", "explanation": f"Error: {e}"}
        
        logger.info("\n[7/7] Verifying PSA certificates...")
        try:
            verify_psa_certs(raw_cards)
            logger.info(f"Verified PSA certs for {len(raw_cards)} cards")
        except Exception as e:
            logger.warning(f"Failed to verify some PSA certs: {e}")
        
        logger.info("\n[+] Generating portfolio insights...")
        portfolio = raw_cards
        insights = generate_insights(portfolio)
        
        logger.info("\n[+] Computing summary statistics...")
        summary = compute_summary(portfolio)
        
        logger.info("\n" + "="*70)
        logger.info("REFRESH COMPLETE")
        logger.info(f"Portfolio Size: {len(portfolio)} cards")
        logger.info(f"Total Cost: ${summary.get('total_cost', 0):.2f}")
        logger.info(f"Total Market Value: ${summary.get('total_market_value', 0):.2f}")
        logger.info(f"Total P&L: ${summary.get('total_pnl', 0):+.2f}")
        logger.info("="*70 + "\n")
        
        return {"status": "success", "portfolio": portfolio, "insights": insights, "exceptions": exceptions, "summary": summary, "timestamp": datetime.now().isoformat()}
    
    except Exception as e:
        msg = f"Critical error during refresh: {e}"
        logger.error(msg)
        exceptions.append({"step": "critical", "error": msg})
        return {"status": "error", "portfolio": portfolio, "insights": {}, "exceptions": exceptions, "summary": {}, "timestamp": datetime.now().isoformat()}

def compute_summary(portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute portfolio summary statistics."""
    total_cost = sum(c.get("my_cost", 0) for c in portfolio if c.get("my_cost"))
    total_market_value = sum(c.get("market_value", 0) for c in portfolio if c.get("market_value"))
    total_pnl = total_market_value - total_cost
    if total_cost > 0:
        pnl_pct = (total_pnl / total_cost) * 100
    else:
        pnl_pct = 0
    signals = {}
    for sig in ["BUY", "HOLD", "SELL", "REVIEW"]:
        count = sum(1 for c in portfolio if c.get("signal_data", {}).get("signal") == sig)
        signals[sig] = count
    risk_levels = {}
    for level in ["LOW", "MEDIUM", "HIGH"]:
        count = sum(1 for c in portfolio if c.get("signal_data", {}).get("risk_level") == level)
        risk_levels[level] = count
    liquidity = {}
    for liq in ["HIGH", "MEDIUM", "LOW"]:
        count = sum(1 for c in portfolio if c.get("signal_data", {}).get("liquidity") == liq)
        liquidity[liq] = count
    avg_comps = sum(c.get("comp_count", 0) for c in portfolio) / len(portfolio) if portfolio else 0
    return {
        "card_count": len(portfolio),
        "total_cost": round(total_cost, 2),
        "total_market_value": round(total_market_value, 2),
        "total_pnl": round(total_pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "avg_comps_per_card": round(avg_comps, 1),
        "signal_distribution": signals,
        "risk_distribution": risk_levels,
        "liquidity_distribution": liquidity,
    }

if __name__ == "__main__":
    result = full_refresh(CSV_INPUT_PATH, Path("../output/Pokemon_Portfolio_Intelligence.xlsx"))
    print(f"Status: {result['status']}")
