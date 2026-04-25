# Quantitative Investment Matrix — Quick Start

## Access the Dashboard

### Option 1: Web Browser (Recommended)
1. Open your web app: `python webapp.py`
2. Navigate to: **http://localhost:5000/matrix**
3. Dashboard loads with live analysis

### Option 2: API Call
```bash
curl -s http://localhost:5000/api/quantitative-matrix | jq .
```

---

## What You See

### Summary Cards (Top)
- **Total Cards**: 23 analyzed
- **BUY Signal**: 0 cards meet strict BUY criteria
- **HOLD Signal**: 2 cards with good demand but weak underval
- **SELL Signal**: 21 cards trading above market value

### Layer 2: ACTION Engine Table
| Column | Meaning |
|--------|---------|
| Card | Pokémon name |
| Action | BUY / HOLD / SELL |
| Confidence % | 50–95% conviction score |
| Score | 0–10 rating |
| Underval % | Cost vs Market Value |
| Demand | S (top tier) / A / B |
| Liquidity | High / Medium / Low |
| Pop Risk | High / Medium / Low population concentration |
| Reason | One-line decision logic |

**Color Coding:**
- Green = BUY (strong buy signal)
- Blue = HOLD (wait for better entry)
- Red = SELL (exit or reduce position)

### Layer 1: BUY Decision Matrix
Full 10-criteria scoring breakdown:
1. Undervaluation %
2. Demand Strength (tier)
3. Liquidity Profile
4. Icon Tier (rarity/appeal)
5. Population Risk
6. Price Momentum
7. Entry Barrier
8. Visual Premium
9. Catalyst Strength
10. Exit Ease

### Key Drivers & Risk Flags
- **Key Drivers**: What makes a good BUY signal
- **Risk Flags**: Portfolio-level warnings

---

## Portfolio Analysis (Your Data)

Your 23-card portfolio shows:
- **Portfolio Status**: Heavily overvalued (negative undervaluation across most cards)
- **Top Opportunity**: Cards with S-tier Pikachu demand but negative underval
- **Action**: Wait for market correction or exit overvalued positions
- **Thai Market**: Pikachu/Eeveelution cards have slight valuation boost

---

## Interpretation Guide

### BUY Signal (Action ≥ 8, Underval ≥ 20%)
- Card is undervalued by 20%+
- Strong demand (S/A tier)
- Good liquidity
- Low population risk

### HOLD Signal (Score 6–7.9)
- Fundamentals are sound
- But current price doesn't offer >20% upside
- Wait for dip before buying
- Keep on watchlist

### SELL Signal (Score < 6)
- Overvalued relative to market
- High risk / volatile momentum
- OR weak demand / difficult exit
- Consider liquidating

---

## Key Metrics Explained

### Undervaluation %
```
Formula: ((Market Value - Cost) / Cost) * 100

Positive = Undervalued (good entry)
Negative = Overvalued (sell signal)
>30% = Extreme buy opportunity
10–30% = Moderate opportunity
<10% = Weak value play
```

### Demand Tier
- **S**: Pikachu (maximum collectibility + market demand)
- **A**: Mew, Eeveelutions (high appeal)
- **B**: Others (niche demand)

*Thai market adds +0.5 bonus to S/A tiers.*

### Confidence Score
```
Base = BUY Score × 10
+10 if S-tier demand
+5 if strong catalyst (new release/event)
−10 if high population risk (overgraded)
−5 if volatile momentum
```

---

## Use Cases

### 1. Identify Quick Flips
Filter for: Action = BUY, Underval > 30%
→ Cards ready to buy and resell quickly

### 2. Build Long-Term Position
Filter for: Demand = S, Momentum = Uptrend
→ Cards with staying power

### 3. Portfolio Health Check
Look at: SELL count vs BUY count
→ If SELL > BUY, portfolio overheated

### 4. Risk Assessment
Check: Pop Risk = High cards
→ Avoid graded copies if oversupplied

### 5. Thai Market Play
Look for: Pikachu or Eevee variants with good scores
→ Higher demand in Thailand = better exit liquidity

---

## Technical Details

### Files Involved
- `quantitative_matrix.py` — Analysis engine
- `webapp.py` — Flask API routes
- `templates/quantitative_matrix.html` — Dashboard UI
- `My Collection CSV - 19.csv` — Input data

### Data Flow
```
CSV → Python analysis → JSON API → HTML dashboard
```

### Update Frequency
- Dashboard refreshes on every page load
- Always pulls latest CSV data
- No caching (live analysis)

---

## Customization

### Change Scoring Thresholds
Edit `quantitative_matrix.py`:
- Line 95: `if underval_pct > 30:` (undervaluation threshold)
- Line 100: `if demand == 'S':` (demand scoring)
- Line 168: `if buy_score >= 8:` (BUY action threshold)

### Change Demand Tier Mapping
Edit lines 55–65:
```python
s_tier = ['PIKACHU']  # Add more here
a_tier = ['MEW', 'EEVEE']  # A-tier cards
```

### Adjust Thai Market Bonus
Edit line 143:
```python
if any(x in subject.upper() for x in ['PIKACHU', 'EEVEE']):
    score += 0.5  # Change 0.5 to adjust boost
```

### Modify UI Colors
Edit `templates/quantitative_matrix.html` CSS:
- Line 100+: Signal colors (BUY/HOLD/SELL)
- Line 120+: Tier colors (S/A/B)
- Line 150+: Risk colors (High/Medium/Low)

---

## Next Steps

1. **Monitor dashboard daily** — Catch trend reversals early
2. **Log historical scores** — Build backtesting database
3. **Set price alerts** — Auto-notify when underval > 30%
4. **Export weekly reports** — Share with team/advisors
5. **Validate against sales** — Check if BUY signals actually sell

---

Questions? Check `MATRIX_INTEGRATION_SUMMARY.md` for technical details.
