"""Live Refresh - Uses real Collectr prices, all values displayed in THB."""
import sys, logging
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))

from config import CSV_INPUT_PATH, EXCEL_OUTPUT_PATH, LOGGING_CONFIG, USD_TO_THB
from ingest import ingest_collection
from matching import generate_match_key
from collectr_live_prices import COLLECTR_PRICES as _STATIC_PRICES
from excel_writer import write_portfolio_excel

logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOGGING_CONFIG["file"])])
logger = logging.getLogger(__name__)

RATE = USD_TO_THB  # 33.22

def to_thb(val):
    if val is None:
        return None
    return round(val * RATE, 0)

def match_collectr(card, prices_dict):
    """
    Match a portfolio card to a Collectr price entry.

    Priority ladder (the first step that yields a match wins):
      1. Exact normalized-subject + card_number (+ grade if both sides specify it).
      2. Substring subject match, but ONLY if exactly one candidate remains after
         filtering by card_number and grade. This handles benign variants like
         "SNORLAX" vs "SNORLAX-HOLO" without letting "PIKACHU" greedily match
         "FULL ART/PIKACHU" (both share card #001).
      3. No match - return None. We refuse to guess on ambiguous cases so the
         caller falls back to PSA estimate and flags the card for review.

    History: the prior implementation did `subj in d_subj or d_subj in subj`
    with only card_number as a gate. Because PIKACHU #001 (SV Promo) and
    FULL ART/PIKACHU #001 (25th Anniversary) share the same number, iteration
    order caused the plain PIKACHU to inherit the Full Art's URL and price -
    which is how two distinct cards ended up with identical market values on
    the dashboard.
    """
    def _norm(s):
        return "".join(ch for ch in str(s or "").lower() if ch.isalnum())

    c_subj  = _norm(card.get("subject", ""))
    c_num   = str(card.get("card_number", "")).strip()
    c_grade = str(card.get("grade", "")).strip()

    # Candidate set: same card_number, and (if both known) same grade.
    num_matches = []
    for key, data in prices_dict.items():
        if data is None:
            continue
        if str(data.get("card_number", "")).strip() != c_num:
            continue
        d_grade = str(data.get("grade", "")).strip()
        if c_grade and d_grade and d_grade != c_grade:
            continue
        num_matches.append((key, data))

    if not num_matches:
        return None

    # (1) Exact normalized-subject match.
    for _key, data in num_matches:
        if _norm(data.get("subject", "")) == c_subj:
            return data

    # (2) Substring fallback - only if exactly one candidate remains.
    subs = [
        (k, d) for k, d in num_matches
        if _norm(d.get("subject", "")) and (
            _norm(d.get("subject", "")) in c_subj or c_subj in _norm(d.get("subject", ""))
        )
    ]
    if len(subs) == 1:
        return subs[0][1]

    # (3) Ambiguous - refuse to guess.
    if len(subs) > 1:
        logger.warning(
            f"match_collectr: refusing ambiguous match for {card.get('subject')} "
            f"#{c_num} PSA{c_grade} - {len(subs)} candidates: "
            f"{[d.get('subject') for _, d in subs]}"
        )
    return None

def compute_signal_live(card):
    cost = card.get("my_cost")
    mv = card.get("market_value")
    confidence = card.get("confidence", 50)
    source = card.get("collectr_source", "")

    if not cost or mv is None:
        return {"signal": "REVIEW", "risk_level": "HIGH", "confidence": confidence,
                "upside_pct": 0, "liquidity": "UNKNOWN", "trend": "UNKNOWN",
                "explanation": "Missing cost or market value"}

    upside_pct = ((mv - cost) / cost) * 100 if cost > 0 else 0
    liquidity = "MEDIUM" if "Collectr Live" in source else "LOW"

    if confidence < 70:
        signal, risk = "REVIEW", "HIGH"
        explanation = f"Low confidence ({confidence:.0f}%); needs manual verification"
    elif mv >= cost * 1.15 and confidence >= 85:
        signal, risk = "BUY", "LOW"
        explanation = f"Strong position: +{upside_pct:.1f}% gain (MV {mv:,.0f} vs cost {cost:,.0f})"
    elif mv < cost * 0.85:
        signal, risk = "SELL", "HIGH"
        explanation = f"Underwater: {upside_pct:.1f}% loss (MV {mv:,.0f} vs cost {cost:,.0f})"
    elif mv >= cost:
        signal = "HOLD"
        risk = "LOW" if upside_pct > 10 else "MEDIUM"
        explanation = f"Slightly positive: +{upside_pct:.1f}% (MV {mv:,.0f} vs cost {cost:,.0f})"
    else:
        signal, risk = "HOLD", "MEDIUM"
        explanation = f"Slightly underwater: {upside_pct:.1f}% (MV {mv:,.0f} vs cost {cost:,.0f})"

    return {"signal": signal, "risk_level": risk, "confidence": round(confidence, 1),
            "upside_pct": round(upside_pct, 2), "liquidity": liquidity,
            "trend": "STABLE", "explanation": explanation}

def generate_insights_live(portfolio):
    valid = [c for c in portfolio if c.get("market_value") and c.get("my_cost")]
    sorted_by_roi = sorted(valid, key=lambda c: c.get("signal_data", {}).get("upside_pct", 0), reverse=True)
    weak = [c for c in valid if c.get("signal_data", {}).get("upside_pct", 0) < -10]
    high_risk = [c for c in valid if c.get("signal_data", {}).get("risk_level") == "HIGH"]

    sig_counts = {"BUY": 0, "HOLD": 0, "SELL": 0, "REVIEW": 0}
    liq_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    for c in portfolio:
        s = c.get("signal_data", {}).get("signal", "REVIEW")
        sig_counts[s] = sig_counts.get(s, 0) + 1
        l = c.get("signal_data", {}).get("liquidity", "LOW")
        liq_counts[l] = liq_counts.get(l, 0) + 1

    return {
        "top_undervalued": sorted_by_roi[:5],
        "top_gainers": sorted(valid, key=lambda c: c.get("my_cost", 0), reverse=True)[:5],
        "weak_positions": sorted(weak, key=lambda c: c.get("signal_data", {}).get("upside_pct", 0))[:5],
        "high_risk": high_risk[:5],
        "liquidity_summary": liq_counts,
        "signal_allocation": sig_counts,
        "total_portfolio_value": sum(c.get("market_value", 0) for c in valid),
        "total_cost": sum(c.get("my_cost", 0) for c in valid),
    }

def live_refresh(live_prices=None):
    """
    Full portfolio refresh.
    live_prices: dict from collectr_live_fetcher (keyed by card key).
                 Pass None to fall back to the static snapshot.
    """
    prices_dict = live_prices if live_prices is not None else _STATIC_PRICES
    data_source = "Playwright live fetch" if live_prices is not None else "Static snapshot"

    logger.info("=" * 70)
    logger.info(f"LIVE REFRESH - Collectr Prices (THB @ {RATE} THB/USD) | {data_source}")
    logger.info("=" * 70)

    raw_cards = ingest_collection(CSV_INPUT_PATH)
    logger.info(f"Ingested {len(raw_cards)} cards")
    exceptions = []

    for card in raw_cards:
        card["match_key"] = generate_match_key(card)

    # Convert CSV cost fields USD -> THB
    for card in raw_cards:
        if card.get("my_cost"):
            card["my_cost_usd"] = card["my_cost"]
            card["my_cost"] = to_thb(card["my_cost"])
        if card.get("psa_estimate"):
            card["psa_estimate_usd"] = card["psa_estimate"]
            card["psa_estimate"] = to_thb(card["psa_estimate"])

    # Match Collectr & convert prices to THB
    matched = 0
    for i, card in enumerate(raw_cards, 1):
        collectr = match_collectr(card, prices_dict)
        if collectr and collectr.get("collectr_graded"):
            usd_price = collectr["collectr_graded"]
            thb_price = to_thb(usd_price)
            card["collectr_price_usd"] = usd_price
            card["collectr_price"] = thb_price
            card["collectr_ungraded"] = to_thb(collectr.get("collectr_ungraded"))
            card["collectr_url"] = collectr.get("collectr_url")
            card["collectr_source"] = collectr.get("source", "Collectr Live")
            card["collectr_psa8"]  = to_thb(collectr.get("collectr_psa8"))
            card["collectr_psa9"]  = to_thb(collectr.get("collectr_psa9"))
            card["collectr_psa10"] = to_thb(collectr.get("collectr_psa10"))
            card["image_url"]    = collectr.get("image_url")
            card["market_value"] = thb_price
            card["confidence"] = 95 if collectr.get("source") == "Collectr Live" else 70
            matched += 1
            logger.info(f"  {i}. {card['subject']} -> ${usd_price} -> THB {thb_price:,.0f} ({collectr.get('source')})")
        else:
            card["collectr_price"] = None
            card["market_value"] = card.get("psa_estimate")
            card["confidence"] = 50 if card.get("psa_estimate") else 30

            # PSA scraper may have returned an image_url for this card (keyed by card_number+subject)
            psa_match = match_collectr(card, prices_dict)
            if psa_match and psa_match.get("image_url") and psa_match.get("source") == "PSA Cert":
                card["image_url"]       = psa_match["image_url"]
                card["collectr_source"] = "PSA Cert"
                mv_str = f"PSA Est THB {card['market_value']:,.0f}" if card.get("market_value") else "NO PRICE"
                logger.warning(f"  {i}. {card['subject']} -> PSA Cert image ✓ | {mv_str}")
            else:
                card["collectr_source"] = "Not available"
                if card.get("market_value"):
                    logger.warning(f"  {i}. {card['subject']} -> PSA Est THB {card['market_value']:,.0f} (fallback, no image)")
                else:
                    logger.warning(f"  {i}. {card['subject']} -> NO MARKET DATA")
                    exceptions.append({"row": i, "error": f"No market data for {card['subject']}", "step": "Collectr Match"})

    logger.info(f"Collectr matched: {matched}/{len(raw_cards)}")

    for card in raw_cards:
        card["ebay_comps"] = []
        card["ebay_stats"] = {}
        card["comp_count"] = 0
        card["signal_data"] = compute_signal_live(card)

    insights = generate_insights_live(raw_cards)

    total_cost = sum(c.get("my_cost", 0) for c in raw_cards if c.get("my_cost"))
    total_mv   = sum(c.get("market_value", 0) for c in raw_cards if c.get("market_value"))
    total_pnl  = total_mv - total_cost
    pnl_pct    = (total_pnl / total_cost * 100) if total_cost > 0 else 0

    sig_dist = {s: sum(1 for c in raw_cards if c.get("signal_data", {}).get("signal") == s)
                for s in ["BUY","HOLD","SELL","REVIEW"]}
    risk_dist = {r: sum(1 for c in raw_cards if c.get("signal_data", {}).get("risk_level") == r)
                 for r in ["LOW","MEDIUM","HIGH"]}
    liq_dist  = {l: sum(1 for c in raw_cards if c.get("signal_data", {}).get("liquidity") == l)
                 for l in ["HIGH","MEDIUM","LOW","UNKNOWN"]}

    summary = {
        "card_count": len(raw_cards),
        "total_cost": round(total_cost, 2),
        "total_market_value": round(total_mv, 2),
        "total_pnl": round(total_pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "avg_comps_per_card": 0,
        "signal_distribution": sig_dist,
        "risk_distribution": risk_dist,
        "liquidity_distribution": liq_dist,
        "currency": "THB",
        "exchange_rate": RATE,
        "data_source": data_source,
    }

    logger.info(f"Portfolio: {len(raw_cards)} cards | Cost: THB {total_cost:,.0f} | "
                f"MV: THB {total_mv:,.0f} | P&L: THB {total_pnl:+,.0f} ({pnl_pct:+.1f}%)")
    logger.info(f"Signals: {sig_dist}")

    result = {
        "status": "success",
        "portfolio": raw_cards,
        "insights": insights,
        "exceptions": exceptions,
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
        "data_source": data_source,
    }

    write_portfolio_excel(result, EXCEL_OUTPUT_PATH)
    logger.info(f"Workbook: {EXCEL_OUTPUT_PATH}")
    return result

if __name__ == "__main__":
    live_refresh()
