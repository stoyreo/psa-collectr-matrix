# Pokémon Card Investment Matrix — Integration Summary

## What Was Added

### 1. **Quantitative Matrix Module** (`quantitative_matrix.py`)
- Reads CSV portfolio data from `My Collection CSV - 19.csv`
- Calculates **10-criteria BUY decision matrix** for each card
- Generates **ACTION engine** (BUY/HOLD/SELL + confidence scores)
- Includes Thai market adjustments (Pikachu + Eeveelution boost)

### 2. **Flask API Endpoints** (added to `webapp.py`)
- **`GET /api/quantitative-matrix`** — Returns matrix analysis as JSON
- **`GET /matrix`** — Renders interactive dashboard

### 3. **Dashboard UI** (`templates/quantitative_matrix.html`)
- Clean, responsive design (gradient background, card-based layout)
- **Summary cards**: Total cards, BUY/HOLD/SELL signal counts
- **Layer 2 table**: Action engine with filtering
- **Layer 1 table**: Full 10-criteria decision matrix
- **Key drivers**: Top BUY catalysts
- **Risk flags**: Portfolio-level warnings

---

## How to Access

### Local Web App
1. Start the Flask app: `python webapp.py`
2. Open browser: **http://localhost:5000/matrix**
3. Dashboard loads automatically with latest portfolio analysis

### API (for integration)
```bash
curl http://localhost:5000/api/quantitative-matrix
```

Returns JSON structure:
```json
{
  "timestamp": "2026-04-24T...",
  "matrix": [
    {
      "card": "PIKACHU",
      "undervaluation_pct": 6.6,
      "demand": "S",
      "action": "HOLD",
      "confidence": 75.0,
      "buy_score": 6.0,
      ...
    }
  ],
  "summary": {
    "total_cards": 27,
    "buy_count": 5,
    "hold_count": 12,
    "sell_count": 10
  },
  "key_buy_drivers": [...],
  "risk_flags": [...]
}
```

---

## Matrix Scoring Logic

### Layer 1: BUY Score (0–10)
| Criterion | Points | Threshold |
|-----------|--------|-----------|
| Undervaluation | +2 | >30% |
| S-Tier Demand | +2 | Pikachu, Mew |
| High Liquidity | +1.5 | Proven market |
| High Visual Premium | +1 | Full Art / EX |
| Strong Catalyst | +1 | New release / event |
| Easy Exit | +1 | Quick secondary market |
| Thai Market Bonus | +0.5 | Pikachu / Eevee |
| **Penalties** | | |
| High Population Risk | -1 | Grade 10 oversupply |
| Volatile Momentum | -0.5 | Unpredictable trends |

### Layer 2: Action Rules
- **BUY**: Score ≥8 AND Undervaluation ≥20% AND Liquidity ≥Medium
- **HOLD**: Score 6–7.9 (good demand but weak underval)
- **SELL**: Score <6 (high risk + weak momentum)

### Confidence Score (0–100%)
```
Base = BUY Score × 10
+ 10 if S-tier demand
+ 5 if strong catalyst
− 10 if high population risk
− 5 if volatile momentum
```

---

## Files Modified

| File | Change |
|------|--------|
| `webapp.py` | Added `/api/quantitative-matrix` and `/matrix` routes |
| `templates/quantitative_matrix.html` | New dashboard (created) |
| `quantitative_matrix.py` | New analysis engine (created) |

---

## Features

✓ Real-time CSV parsing (no manual data entry)
✓ Deterministic scoring (same input = same output)
✓ Thai market adjustments built-in
✓ Interactive filtering (by action: BUY/HOLD/SELL)
✓ Responsive design (mobile + desktop)
✓ JSON API for programmatic access
✓ Color-coded signals (green=BUY, blue=HOLD, red=SELL)
✓ Confidence bars with visual indicators
✓ Risk tier badges (High/Medium/Low)

---

## Next Steps (Optional)

1. **Export to PDF**: Add report generation (pypdf + jinja2 templates)
2. **Historical tracking**: Log scores over time, identify trend reversals
3. **Slack alerts**: Post BUY signals to team channel
4. **Email digest**: Weekly matrix summary to subscribers
5. **Mobile app**: React Native for on-the-go portfolio review
6. **A/B test criteria**: Backtest different weightings against actual sales

---

## Questions?

- Matrix logic: Check `quantitative_matrix.py` lines 50–140
- Styling: Edit CSS in `templates/quantitative_matrix.html` (lines 1–200)
- Scoring tuning: Adjust thresholds in `calculate_buy_score()` function
