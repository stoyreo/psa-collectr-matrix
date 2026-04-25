"""Signal Engine - Rule-based portfolio signals"""
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta

from config import SIGNAL_CONFIG, INSIGHTS_CONFIG

logger = logging.getLogger(__name__)

def compute_liquidity(comps: List[Dict[str, Any]]) -> Tuple[str, float]:
    """Compute liquidity classification based on comp data."""
    comp_count = len(comps)
    high_threshold = SIGNAL_CONFIG["liquidity_thresholds"]["high"]
    medium_threshold = SIGNAL_CONFIG["liquidity_thresholds"]["medium"]
    if comp_count >= high_threshold:
        liquidity_level = "HIGH"
        base_score = 80
    elif comp_count >= medium_threshold:
        liquidity_level = "MEDIUM"
        base_score = 50
    else:
        liquidity_level = "LOW"
        base_score = 20
    recency_comps = sum(1 for c in comps if c.get("sold_date") and isinstance(c.get("sold_date"), type(datetime.now().date())) and (datetime.now().date() - c.get("sold_date")).days <= 30)
    if comp_count > 0:
        recency_pct = recency_comps / comp_count
        recency_bonus = recency_pct * 20
    else:
        recency_bonus = 0
    if comp_count >= 3:
        prices = [c.get("total_price", c.get("sold_price", 0)) for c in comps]
        max_price = max(prices)
        min_price = min(prices)
        if min_price > 0:
            spread_pct = (max_price - min_price) / min_price
            variance_bonus = 10 if spread_pct < 0.15 else (-10 if spread_pct > 0.50 else 0)
        else:
            variance_bonus = 0
    else:
        variance_bonus = 0
    liquidity_score = min(100, max(0, base_score + recency_bonus + variance_bonus))
    return liquidity_level, round(liquidity_score, 1)

def compute_trend(comps: List[Dict[str, Any]]) -> Tuple[str, float]:
    """Compute price trend from comp data."""
    if len(comps) < 4:
        return "INSUFFICIENT_DATA", 0.0
    sorted_comps = sorted(comps, key=lambda c: c.get("sold_date") or datetime.now().date())
    split_idx = len(sorted_comps) // 2
    older_comps = sorted_comps[:split_idx]
    recent_comps = sorted_comps[split_idx:]
    older_prices = [c.get("total_price", c.get("sold_price", 0)) for c in older_comps if c.get("total_price") or c.get("sold_price")]
    recent_prices = [c.get("total_price", c.get("sold_price", 0)) for c in recent_comps if c.get("total_price") or c.get("sold_price")]
    if not older_prices or not recent_prices:
        return "INSUFFICIENT_DATA", 0.0
    older_median = sorted(older_prices)[len(older_prices) // 2]
    recent_median = sorted(recent_prices)[len(recent_prices) // 2]
    if older_median <= 0:
        return "UNKNOWN", 0.0
    trend_pct = (recent_median - older_median) / older_median
    trend_score = trend_pct * 100
    trend_threshold = SIGNAL_CONFIG["trend_threshold"]
    trend = "UP" if trend_pct > trend_threshold else ("DOWN" if trend_pct < -trend_threshold else "STABLE")
    return trend, round(trend_score, 1)

def compute_signal(card: Dict[str, Any]) -> Dict[str, Any]:
    """Compute portfolio signal (BUY/HOLD/SELL/REVIEW) for a card."""
    my_cost = card.get("my_cost")
    market_value = card.get("market_value")
    confidence = card.get("confidence", 50)
    comps = card.get("ebay_comps", [])
    if not my_cost or market_value is None:
        return {"signal": "REVIEW", "risk_level": "HIGH", "confidence": confidence, "upside_pct": 0, "liquidity": "LOW", "trend": "UNKNOWN", "explanation": "Missing cost or market value data"}
    if my_cost > 0:
        upside_pct = ((market_value - my_cost) / my_cost) * 100
    else:
        upside_pct = 0
    liquidity_level, liquidity_score = compute_liquidity(comps)
    trend_dir, trend_score = compute_trend(comps)
    buy_threshold = SIGNAL_CONFIG["buy_upside_multiplier"]
    sell_threshold = SIGNAL_CONFIG["sell_downside_multiplier"]
    review_confidence = SIGNAL_CONFIG["review_confidence_threshold"]
    buy_confidence = SIGNAL_CONFIG["buy_confidence_threshold"]
    sell_confidence = SIGNAL_CONFIG["sell_confidence_threshold"]
    signal = "HOLD"
    explanation = ""
    if market_value < (my_cost * sell_threshold):
        signal = "SELL"
        explanation = f"Underwater: {upside_pct:.1f}% loss ({market_value:.0f} vs cost {my_cost:.0f})"
    elif trend_dir == "DOWN" and confidence >= sell_confidence:
        signal = "SELL"
        explanation = f"Weakening trend: prices down {trend_score:.1f}%"
    if signal != "SELL":
        if (market_value > (my_cost * buy_threshold) and liquidity_level in ["HIGH", "MEDIUM"] and confidence >= buy_confidence):
            signal = "BUY"
            explanation = f"Strong position: {upside_pct:.1f}% gain with {liquidity_level} liquidity"
        elif confidence < review_confidence:
            signal = "REVIEW"
            explanation = f"Low confidence ({confidence:.0f}%); needs research"
    if signal == "HOLD":
        if liquidity_level == "LOW":
            explanation = f"Illiquid position ({len(comps)} comps); holding for liquidity development"
        elif abs(upside_pct) < 5:
            explanation = f"Position near cost ({upside_pct:+.1f}%); stable"
        else:
            explanation = f"Mixed signal: {upside_pct:+.1f}% position with {liquidity_level} liquidity"
    risk_level = assess_risk(card, signal, upside_pct, liquidity_level, confidence)
    return {"signal": signal, "risk_level": risk_level, "confidence": round(confidence, 1), "upside_pct": round(upside_pct, 2), "liquidity": liquidity_level, "trend": trend_dir, "explanation": explanation}

def assess_risk(card: Dict[str, Any], signal: str, upside_pct: float, liquidity_level: str, confidence: float) -> str:
    """Assess risk level for a position."""
    if upside_pct < -20:
        return "HIGH"
    if liquidity_level == "LOW" and abs(upside_pct) > 50:
        return "HIGH"
    if confidence < 60:
        return "HIGH"
    if upside_pct > 20 and liquidity_level in ["HIGH", "MEDIUM"] and confidence >= 80:
        return "LOW"
    if 0 < upside_pct < 20 and liquidity_level in ["HIGH", "MEDIUM"]:
        return "LOW"
    return "MEDIUM"

def generate_insights(portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate portfolio insights and recommendations."""
    valid_cards = [c for c in portfolio if c.get("market_value") is not None]
    if not valid_cards:
        return {"top_undervalued": [], "top_gainers": [], "weak_positions": [], "high_risk": [], "liquidity_summary": {}, "signal_allocation": {}}
    sorted_by_upside = sorted([c for c in valid_cards if c.get("signal_data", {}).get("upside_pct") is not None], key=lambda c: float(c.get("signal_data", {}).get("upside_pct") or 0), reverse=True)
    top_undervalued = sorted_by_upside[:INSIGHTS_CONFIG["top_undervalued_count"]]
    top_gainers = sorted(valid_cards, key=lambda c: float(c.get("my_cost") or 0), reverse=True)[:INSIGHTS_CONFIG["top_gainers_count"]]
    weak = [c for c in valid_cards if c.get("signal_data", {}).get("upside_pct") and c.get("signal_data", {}).get("upside_pct") < -10]
    weak_positions = sorted(weak, key=lambda c: float(c.get("signal_data", {}).get("upside_pct") or 0))[:INSIGHTS_CONFIG["weak_positions_count"]]
    high_risk = [c for c in valid_cards if c.get("signal_data", {}).get("risk_level") == "HIGH"]
    high_risk = sorted(high_risk, key=lambda c: abs(float(c.get("signal_data", {}).get("upside_pct") or 0)), reverse=True)[:INSIGHTS_CONFIG["weak_positions_count"]]
    liquidity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for card in valid_cards:
        liq = card.get("signal_data", {}).get("liquidity", "LOW")
        if liq in liquidity_counts:
            liquidity_counts[liq] += 1
    signal_counts = {"BUY": 0, "HOLD": 0, "SELL": 0, "REVIEW": 0}
    for card in valid_cards:
        sig = card.get("signal_data", {}).get("signal", "REVIEW")
        if sig in signal_counts:
            signal_counts[sig] += 1
    return {
        "top_undervalued": top_undervalued,
        "top_gainers": top_gainers,
        "weak_positions": weak_positions,
        "high_risk": high_risk,
        "liquidity_summary": liquidity_counts,
        "signal_allocation": signal_counts,
        "total_portfolio_value": sum(float(c.get("market_value") or 0) for c in valid_cards),
        "total_cost": sum(float(c.get("my_cost") or 0) for c in valid_cards),
    }

if __name__ == "__main__":
    print("signals module loaded")
