# P&L Tab Refactor: Before & After Comparison

---

## KPI Strip Comparison

### BEFORE (7 KPIs)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Portfolio NAV │ Unrealized P&L │ 30-day Return │ 90-day Volatility │ Sharpe... │
│     0 THB     │   0 THB / 0%   │     0%        │       0%          │   0.00    │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Concentration HHI │ POP Alerts                                                   │
│       0.000       │     0                                                        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Data Sources:**
- Portfolio NAV: hardcoded `pnlPortfolio` array
- Unrealized P&L: pnlPortfolio values
- 30-day Return: computed from price_history (not in Portfolio tab)
- 90-day Volatility: hardcoded vol_90d field
- Sharpe Ratio: (ret30 - 2) / vol90
- Concentration HHI: Herfindahl-Hirschman Index (sum of squared weights)
- POP Alerts: count where pop_growth_90d > 10

### AFTER (7 KPIs)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ Portfolio NAV │ Unrealized P&L │ Winners │ Losers │ Avg Confidence │ Top Conc... │
│     0 THB     │   0 THB / 0%   │    0    │   0    │      0%        │    0%      │
├──────────────────────────────────────────────────────────────────────────────────┤
│ POP Alerts    │ reconciles with Portfolio ✓                                      │
│      0        │                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Data Sources (All from `_portCards`):**
- Portfolio NAV: `∑ market_value` (same as Portfolio tab)
- Unrealized P&L: `∑ (market_value - my_cost)` (same as Portfolio tab)
- **Winners:** count where `market_value > my_cost` ✨ NEW
- **Losers:** count where `market_value < my_cost` ✨ NEW
- **Avg Confidence:** mean of `confidence` field ✨ NEW
- **Top Concentration:** `max(market_value) / ∑ market_value * 100` ✨ NEW
- POP Alerts: count where `pop_growth > 10` (same as before)

---

## Chart Panel Comparison

### Panel 1: Key Movers → Winners & Losers

| Aspect | Before | After |
|--------|--------|-------|
| **Chart Type** | Bar (vertical) | Bar (horizontal) |
| **Library** | Chart.js | Chart.js |
| **Data** | Top 10 P&L % movers | Top 5 gainers (green) + Top 5 losers (red) |
| **Sorting** | By \|pnl_pct\| | By \|pnl ฿\| |
| **Toggle** | Top 10 / Show All | None (always 5+5) |
| **Interactivity** | None | Clickable bars → Portfolio |
| **Updates** | On init | On init + scenario changes |

### Panel 2: Risk vs Return → Cost vs Market Value

| Aspect | Before | After |
|--------|--------|-------|
| **Chart Type** | Scatter | Bubble |
| **Library** | ECharts | Chart.js |
| **X-axis** | 90-day Volatility % | Cost (฿) |
| **Y-axis** | P&L % | Market Value (฿) |
| **Bubble Size** | Cost THB | Market Value (฿) |
| **Colors** | Signal (4 colors) | Signal (4 colors) |
| **Data Source** | pnlPortfolio | _portCards |
| **Interactivity** | Tooltip | Tooltip + Clickable → Portfolio |
| **Updates** | On init | On init + scenario changes |

### Panel 3: Grade Premium Heatmap → Signal Breakdown

| Aspect | Before | After |
|--------|--------|-------|
| **Chart Type** | Heatmap | Donut |
| **Library** | ECharts | Chart.js |
| **Dimensions** | Grade x Character | Signal only |
| **Data** | Grade premium % raw | Card count per signal |
| **Colors** | Green gradient | Signal palette (4 colors) |
| **Data Source** | pnlPortfolio | _portCards |
| **Interactivity** | Tooltip | Tooltip + Legend |
| **Updates** | On init | On init + portfolio changes |

---

## Lower Section: Scenarios & Forecasts

### Before: Three Sections

```
┌─────────────────────────────────────────────────────────────────┐
│ SCENARIO TOGGLES       │ MONTE CARLO FORECAST                  │
│ ─────────────────────  │ ─────────────────────────────────────  │
│ Bull (+30%)            │ [Line chart: p10 band + p50 median]    │
│ Bear (-25%)            │ [Shows 12-month simulation paths]      │
│ POP Dilution           │                                       │
│ Grade Upgrade          │ WATERFALL CONTRIBUTION                │
│ JPY/THB +10%           │ ─────────────────────────────────────  │
│ JPY/THB -10%           │ [Bar chart: top 8 cards' contrib]      │
│ Liquidity Shock        │                                       │
│ [Reset All button]     │                                       │
├─────────────────────────────────────────────────────────────────┤
│ RECOMMENDATION TABLE                                            │
│ ─────────────────────────────────────────────────────────────  │
│ Card | P&L% | EV(12m) | Conf | Action                          │
│ [8 rows of forecast-based recommendations]                     │
└─────────────────────────────────────────────────────────────────┘
```

### After: Two Sections

```
┌─────────────────────────────────────────────────────────────────┐
│ SCENARIO TOGGLES       │ ACTION TABLE (Portfolio-ordered)       │
│ ─────────────────────  │ ─────────────────────────────────────  │
│ Bull (+30%)            │ Card │ Cost │ MV │ P&L │ P&L% │ Sig.. │
│ Bear (-25%)            │ [Each row mirrors Portfolio columns]  │
│ POP Dilution           │ [19 rows = full portfolio view]       │
│ Grade Upgrade          │                                       │
│ JPY/THB +10%           │ ✨ Click any row → highlights in      │
│ JPY/THB -10%           │    Portfolio tab                      │
│ Liquidity Shock        │                                       │
│ [Reset All button]     │                                       │
│                        │                                       │
│ [Scenario Impact]      │ ✨ Shows NAV & P&L delta from base   │
│ NAV: +X ฿              │    when scenarios are active         │
│ P&L: +X ฿              │                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Scenario Behavior Comparison

### Before: Monte Carlo Forecast
- **Logic:** 10,000 simulation paths over 12 months
- **Inputs:** vol_90d, drift_90d, pop_growth_90d (hardcoded in pnlPortfolio)
- **Outputs:** p10/p50/p90 confidence bands
- **Use Case:** "What could happen if I hold these cards for a year?"
- **Problem:** Disconnected from actual Portfolio data; mock price history

### After: Deterministic Scenario Impact
- **Logic:** Multiplies market_value by fixed factors
- **Inputs:** Portfolio market_value + signal
- **Outputs:** Delta from baseline NAV & P&L
- **Transforms Applied:**
  ```
  Bull:              value *= 1.30
  Bear:              value *= 0.75
  POP Dilution:      value *= 0.85
  Grade Upgrade:     value *= 1.08  (if grade < 10)
  JPY/THB +10%:      value *= 1.10
  JPY/THB -10%:      value *= 0.90
  Liquidity Shock:   value *= 0.85
  ```
- **Use Case:** "What if the market does X?" (instant, transparent what-ifs)
- **Advantage:** Auditable, deterministic, tied to live portfolio data

---

## Recommendation Table Comparison

### Before: Forecast-based

| Column | Source | Logic |
|--------|--------|-------|
| Card | pnlPortfolio | Card name |
| P&L% | pnlPortfolio | Hardcoded pnl_pct |
| EV(12m) | Monte Carlo | 12-month p50 change |
| Conf | Hardcoded | 75% constant |
| Action | EV + Confidence | BUY if EV > cost*15%, SELL if EV < -cost*10%, UPGRADE if POP growth > 15% |

### After: Signal-based

| Column | Source | Logic |
|--------|--------|-------|
| Card | _portCards | From Portfolio |
| Cost | _portCards | my_cost |
| Market Value | _portCards | market_value (scenario-adjusted) |
| P&L (฿) | Computed | market_value - cost |
| P&L % | Computed | (pnl / cost) * 100 |
| Signal | _portCards | BUY/HOLD/SELL/REVIEW (from Portfolio) |
| Action | _portCards.signal | Same as signal (can be extended with risk + confidence logic) |

---

## Data Source Changes

### BEFORE: Dual Data Architecture

```
┌─────────────────────────────────────────┐
│ Portfolio Tab                           │
│ ├─ _portCards array                     │
│ ├─ 19 real cards from JSON              │
│ └─ Rendered in portfolio-body table     │
├─────────────────────────────────────────┤
│ P&L Tab                                 │
│ ├─ window.pnlPortfolio array            │
│ ├─ 19 mock cards (hardcoded)            │
│ ├─ Different field names (vol_90d, etc) │
│ └─ Separate computations                │
└─────────────────────────────────────────┘
```

**Problem:** Out of sync, different data, hard to reconcile

### AFTER: Single Source of Truth

```
┌─────────────────────────────────────────┐
│ Portfolio Tab                           │
│ ├─ _portCards array (shared)            │
│ ├─ 19 real cards from JSON              │
│ └─ Rendered in portfolio-body table     │
│                  ▲                       │
│                  │ (same data)           │
│                  │                       │
│ P&L Tab                                 │
│ ├─ getPortfolioCards() → _portCards     │
│ ├─ All charts read from same array      │
│ └─ All metrics reconcile exactly        │
└─────────────────────────────────────────┘
```

**Benefit:** Always in sync, single source, fully reconciled

---

## Code Changes Summary

### Removed (~141 LOC)
```javascript
// Functions removed from pnlApp:
- drawPnL()          // 15 LOC - old top-10 bar chart
- drawScatter()      // 13 LOC - vol vs pnl scatter
- drawHeatmap()      // 23 LOC - grade premium heatmap
- monte()            // 35 LOC - Monte Carlo simulation
- cholesky()         // 12 LOC - matrix decomposition
- corrMatrix()       // 8 LOC - correlation matrix
- drawMC()           // 11 LOC - MC visualization
- drawWaterfall()    // 13 LOC - contribution waterfall
- updateRec()        // 11 LOC - old recommendations
```

### Added (~160 LOC)
```javascript
// Functions added to pnlApp:
+ getPortfolioCards()      // 1 LOC - read _portCards
+ applyScenario(card)      // 10 LOC - deterministic transforms (8 + 2 new)
+ drawWinnersLosers()      // 30 LOC - top 5 gainers/losers bar
+ drawCostValue()          // 35 LOC - cost vs market-value bubble
+ drawSignals()            // 25 LOC - signal breakdown donut
+ updateScenarioImpact()   // 18 LOC - delta readout
+ updateActionTable()      // 30 LOC - portfolio-ordered action table
+ goToCard(card)           // 13 LOC - cross-tab navigation
```

**Net result:** More functionality, better aligned with portfolio data, less speculative forecasting

---

## UI/UX Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Reconciliation** | No visual cue | Banner shows "reconciles with Portfolio ✓" |
| **Navigation** | No cross-linking | Click card → highlights in Portfolio |
| **Scenario Impact** | Hidden in legend | Explicit delta display |
| **Data Currency** | Manual refresh | Live from Portfolio |
| **Card Visibility** | Partial (top 10) | Full portfolio in action table |
| **Interactivity** | Tooltip only | Tooltip + clickable elements |
| **Clarity** | Forecast-focused | Snapshot + what-if scenarios |

---

## Compliance Checklist

✅ **Single source of truth:** `_portCards` shared between Portfolio and P&L tabs  
✅ **1:1 consistency:** NAV, P&L, alerts match exactly  
✅ **Clickable cards:** All chart elements and table rows click → Portfolio with highlight  
✅ **Removed metrics:** No 30-day Return, 90-day Volatility, or Sharpe Ratio  
✅ **New metrics:** Winners, Losers, Avg Confidence %, Top Concentration %  
✅ **Kept metrics:** Portfolio NAV, Unrealized P&L, POP Alerts  
✅ **New panels:** Winners & Losers, Cost vs Market Value, Signal Breakdown  
✅ **Scenarios:** Deterministic transforms with visible impact  
✅ **Action table:** Mirrors Portfolio structure, full card list  
✅ **Banner:** Clarified to "Snapshot mode" with reconciliation checkmark  
✅ **No new CSS/libs:** Only existing colors and Chart.js  
✅ **IDs preserved:** All referenced IDs kept, old IDs removed  

---

## Testing the Changes

### Quick Validation Steps
1. Load Portfolio with Refresh Data (19 cards appear)
2. Switch to P&L tab
   - Verify: NAV ≠ 0, Unrealized P&L ≠ 0
   - Verify: Winners + Losers = 19 (total cards)
   - Verify: Avg Confidence is a percentage (0-100)
   - Verify: Top Concentration is a percentage (0-100)
3. Click a Winners & Losers bar → Portfolio tab highlights that card
4. Click a Cost vs Value bubble → Portfolio tab highlights that card
5. Click an Action Table row → Portfolio tab highlights that card
6. Toggle Bull scenario
   - Verify: NAV increases ~30%
   - Verify: Scenario Impact panel appears showing positive delta
   - Verify: Action Table values update
7. Click Reset All
   - Verify: All toggles uncheck, Impact panel hides, values revert

### Verification
- [ ] All KPIs non-zero with 19-card portfolio
- [ ] No JavaScript console errors
- [ ] Charts render without visual artifacts
- [ ] Navigation is smooth (not laggy)
- [ ] Scenarios apply correctly (all 7 toggles work)
- [ ] Impact numbers are sensible (e.g., Bull → +30% NAV)

