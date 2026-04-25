# Haiku Prompt — Redesign P&L Performance tab (1:1 with Portfolio)

Paste the block below to Haiku. It is self-contained and targets the single HTML file that powers the web app.

---

You are editing a single file:
`C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer\templates\index.html`

Goal: redesign the "P&L Performance" tab (tab panel `id="tab-pnl-performance"`, lines ~1039–1082, plus its JS object `pnlApp` around line 2253+ and the tab switch hook at line 2540) so it is intuitive and 1:1 consistent with the Portfolio tab (`id="tab-portfolio"`, lines 724–820).

## Non-negotiable rules

1. **Single source of truth.** The P&L tab must read from the SAME in-memory portfolio array that renders `portfolio-body`. Do not fetch separately, do not keep a parallel copy. If Portfolio shows 19 rows totaling X THB cost and Y THB market value, the P&L tab's NAV and Unrealized P&L must equal Y and (Y-X) exactly. Add a visible "reconciles with Portfolio ✓" micro-label next to the KPI strip.
2. **Click-through everywhere.** Every card shown anywhere on the P&L tab (mover bars, scatter dots, donut segments, action rows) must be CLICKABLE and, on click, switch to the Portfolio tab and scroll/highlight that card's row (match by `subject` + `card_number` + `grade`). Reuse `switchTab()` from line 1171.
3. **Delete time-series metrics we don't collect.** Remove `30-day Return`, `90-day Volatility`, `Sharpe Ratio`. Replace with snapshot metrics:
   - Winners count (P&L > 0)
   - Losers count (P&L < 0)
   - Avg Confidence %
   - Top Concentration % (largest card's market value / NAV)
4. **Keep:** Portfolio NAV, Unrealized P&L (฿ and %), POP Alerts.
5. **Replace the three empty panels** with ones that render from the shared portfolio array:
   - **Winners & Losers** horizontal bar chart: top 5 P&L gainers (green) above, top 5 losers (red) below, sorted by `|P&L ฿|`. Bars clickable.
   - **Cost vs Market Value** scatter: x = `my_cost`, y = `market_value`, bubble size = `market_value`, color by `signal` (BUY/HOLD/SELL/REVIEW using `--green`/`--blue`/`--red`/`--orange`). Dots clickable.
   - **Signal Breakdown** donut: count of cards per signal, with THB market value shown in the tooltip. Segments clickable → Portfolio tab filtered to that signal (add a simple filter on `#portfolio-table` if one doesn't exist; otherwise highlight matching rows).
6. **Scenarios panel** (Bull/Bear/POP Dilution/Grade Upgrade/JPY±10%/Liquidity Shock): keep toggles but apply a deterministic transform to the shared portfolio array and re-render a small "Scenario Impact" readout showing the delta vs baseline NAV and P&L. No Monte Carlo, no fake confidence intervals. Show the formula used for each toggle in a tooltip so the user can audit it.
7. **Replace** the Monte Carlo + Waterfall + Recommendation section with one **Action Table** that mirrors Portfolio's row order and columns (Subject, Grade, Cost, Market Value, P&L, P&L%, Signal) PLUS a computed "Suggested Action" column derived only from Signal + Risk + Confidence (BUY/HOLD/SELL/REVIEW → same palette). Clicking a row jumps to that card in Portfolio.
8. **Digital Twin banner:** keep, but clarify to "Snapshot mode — all numbers reconcile with your Portfolio tab. Scenarios apply model-based transforms; not financial advice."
9. **Visual style:** reuse existing CSS vars (`--navy`, `--accent`, `--green`, `--red`, `--blue`, `--orange`, `--card`, `--border`, `--radius`, `--shadow`). Do not introduce new colors or fonts. Match spacing and card styling of the Portfolio panel.
10. **Preserve IDs** referenced elsewhere in the JS (`kpi-nav`, `kpi-pnl`, `kpi-pnl-pct`, `kpi-alerts`). For removed KPIs, also remove their JS writers in `pnlApp` to avoid dead code. Everything else in the file must remain untouched.

## Deliverable

A single Edit/Write pass on `templates/index.html`. After the edit, open the file and confirm:
- `pnlApp` reads from the same array as the Portfolio render path
- All three new panels render from that array
- Clicking anywhere on the P&L tab routes to Portfolio tab
- No references to Sharpe / Volatility / 30-day remain
- No new CSS colors or external libraries added (Chart.js already present may be reused)

Report back with: (a) the diff summary, (b) before/after of the KPI strip, (c) which JS functions in `pnlApp` you removed.
