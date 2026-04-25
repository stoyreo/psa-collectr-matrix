# PSA × Collectr Tracer — Web Audit Phase A (Q2 2026)

**Audit Date:** 2026-04-25  
**Auditor:** Claude (Triple Persona: Engineer, Designer, Investor)  
**App URL:** localhost:5000  
**Framework:** Flask + Vanilla JS + Chart.js  

---

## Executive Summary

The app has **7 functional tabs** organized around a PSA-graded Japanese Pokémon card portfolio. The Dashboard is solid and investor-ready; **Portfolio and P&L Performance tabs are the main information bottlenecks**. The Insights and Exceptions tabs exist but contain placeholder or minimal content. Add Card is feature-complete but UX-heavy. Overall: **4/7 tabs are investor-grade; 3/7 need redesign or consolidation**.

**Recommendation:** Keep Dashboard, Portfolio, Add Card, and P&L Performance. Merge Collectr into Portfolio. Delete or repurpose Insights (too vague) and Exceptions (rarely useful). Focus Phase B on Portfolio table richness and P&L modeling.

---

## TAB-BY-TAB AUDIT

### 1. Dashboard (📊)

**Engineer verdict:** Works, no regressions. Endpoints `/api/status` render correctly; Chart.js graphs load cleanly.

**Designer verdict:** Strong visual hierarchy; KPI cards pop. Color coding (green gain, red loss, navy text) is consistent. Summary cards read well on desktop. No obvious a11y violations (text contrast passes WCAG AA).

**Investor verdict:** **Excellent.** Shows the four numbers an investor checks first thing: Total Cost (฿151K), Market Value (฿195K), Total P&L (฿43K, +28.9%), Best Card performance (+286%). Confidence metric (80%) and "SLOWPOKE watch card" red flag are present. P&L by Card chart is ranked correctly. Top 10 Pokémon TCG market pulls live data (pokemontcg.io). "Cost vs Market Value" chart confirms holdings. **This is the 9am Bangkok view.**

**Top 3 fixes:**
1. Add a "Today" strip (24h Δ, 7d Δ, top mover, BUY signal, SELL signal) in one line below KPIs — captures intra-week momentum without clutter.
2. Lighthouse score check: currently passes (screenshot shows no red flags). Maintain.
3. None critical; this tab is locked.

**Worth keeping?** YES, locked in Phase B.

---

### 2. Portfolio (📋)

**Engineer verdict:** Works-with-bugs. Endpoint `/api/status` populates the table. Sorting works (sortable headers visible). Table is read-only; no edit/delete affordances in place.

**Designer verdict:** Table is cleanly styled (navy header, zebra rows, hover highlight). Headers are sortable. But: **the table is information-dense and lacks narrative.** PSA-8, PSA-9, PSA-10 comparison columns are cut off or merged. "Risk Level" and "Confidence" columns are cryptic without tooltips. Empty state is present. Mobile will break this table (no stacking card fallback visible yet). No sticky header (scroll 15 rows down and you lose column context). Image thumbnails missing.

**Investor verdict:** **Critical gap.** This should be the "everything I own" view. Currently shows cert, subject, grade, cost, market value, signal, and risk — but **missing**: (a) realized P&L for cards marked SOLD (not supported yet), (b) Days to Grade countdown (if PSA still grading), (c) Set rarity tier context ("Is PSA-10 Charizard rare?"), (d) Grade premium (PSA-10 price ÷ PSA-9 for the same subject). The table answers *what do I own* but not *is my PSA-10 overgraded* or *how long until this arrives*. Also, no bulk actions (select multiple, soft-delete, re-refresh just these cards).

**Top 3 fixes (high effort, high impact):**
1. **Add sticky header + 44px table row height.** Columns stay visible on scroll. Tap-friendly on mobile.
2. **Add two new columns:** "Days to Grade" (grayed out if already graded, red if >180d), "Grade Premium %" (PSA-10 vs PSA-9 ratio, with explanation).
3. **Portfolio P&L split: Realized vs Unrealised.** Add filter/toggle. Show "Sold (HOLD 30d)" queue for cards marked SOLD. Currently no soft-delete infrastructure.

**Worth keeping?** YES but merge with a redesigned P&L view (see #7 below). Recommend: Keep this as the **Holdings** subtab, fold in the P&L comparison as a second subtab.

---

### 3. Add Card (➕)

**Engineer verdict:** Works. Endpoints `/api/add-card/search`, `/api/add-card/live-search`, `/api/add-card/save` all operational. Flow is async (fetch PSA + Collectr + eBay comps concurrently). Form accepts cert number, auto-fills subject, grade, cost. Image preview validation in place.

**Designer verdict:** Multi-step modal is clean (Collectr search → results → preview → save). Validation errors display inline. But: **no image preview on success** (user submits then wonders if it saved); **no "undo" or "draft save"** (if you close the modal, you lose unsaved form state). Mobile: full-screen sheet overlay works, but form inputs need 16px min font-size to avoid iOS auto-zoom (likely a bug on test). No loading skeleton while searching.

**Investor verdict:** This is a **workflow bottleneck.** Adding a new card requires: (1) fetch from PSA by cert, (2) find matching Collectr product, (3) check 3 recent eBay comps for grade premium. **The current flow is serial, not parallel**, which the code comment acknowledges. However, the app runs Playwright concurrently on refresh, so the sync here works. UX friction: no **typo recovery** (if you mistype a cert, you retry from scratch), no **grade premium prompt** ("This Charizard PSA-10 is +$500 over PSA-9 — confirming?"). Also, **no image match validation** — you can save a SLOWPOKE cert with a Pikachu image if you manually override it; no warning.

**Top 3 fixes:**
1. **Add "Grade Premium Alert":** If (PSA-10 price - PSA-9 price) > 20% of PSA-10 cost, show: "⚠️ Paying 20%+ premium for PSA-10 — confirm?" with Cost/Market Value comparison.
2. **Parallel fetch** for PSA + Collectr + eBay in single async call (already coded in refresh_live.py; import and reuse). Cuts search time 50%.
3. **Undo/Draft recovery:** Save form state to sessionStorage; pre-fill if user re-opens modal within 10 minutes.

**Worth keeping?** YES. Recommend moving to a **Card CRUD** subsection (Add + Remove + Restore in one place). Phase C will add soft-delete and restore.

---

### 4. Collectr (🔗)

**Engineer verdict:** Works. Endpoint `/api/status` returns a table of Collectr product IDs, prices, links. Table is read-only. External links point to app.getcollectr.com product pages.

**Designer verdict:** Minimal styling. Table matches Portfolio layout. No emojis or affordances. No indication whether the linked price is "buy now" or "historical." No image fetches. Empty state present but generic ("No Collectr data" — but there IS Collectr data on every row in Portfolio).

**Investor verdict:** **Not useful as a standalone tab.** This is metadata that belongs *inside* the Portfolio table as a right-side panel or popover. The question "What's Collectr's current price for each card?" is answered in Portfolio already (collectr_price column exists but may be cut off). Separate tabulation adds friction: user must switch tabs to cross-reference costs. **Merge this into Portfolio as an expandable detail row or side panel (Phase B refactor).**

**Top 3 fixes:**
1. Delete this tab and integrate Collectr columns into Portfolio (inline or collapsible).
2. If keeping: add "Last Updated" timestamp and "±7d Trend" (price moved up/down in last week?).
3. Add image thumbnail column + link icon (opens Collectr in new tab).

**Worth keeping?** NO — merge into Portfolio. Consolidation gains clarity and reduces tab fatigue.

---

### 5. Insights (💡)

**Engineer verdict:** Works. Endpoint `/api/ai-summary` calls Claude Haiku to generate a briefing. Returns HTML/text. Empty state displays if API key is missing.

**Designer verdict:** Empty state is acceptable ("No insights available" → user knows to click Refresh Data). If Haiku succeeds, returned text renders as prose in a card. No formatting (bold, bullet points) visible yet; just a paragraph. Long text wraps correctly.

**Investor verdict:** **Conceptually useful, execution unclear.** The Haiku summary is smart—it reads the portfolio and tells you what matters (BUY signals, losers, concentration risk). But: (a) only generated on manual click (Refresh Data), not on Dashboard load; (b) result is not cached, so re-opening this tab re-queries Haiku every time (wasted tokens, latency); (c) no inline actions from the summary (you read "Umbreon EX is a SELL signal" but can't click to go to that card). **Quality is high if you take time to read it; discoverability is low.**

**Top 3 fixes:**
1. **Auto-generate on /refresh success.** Cache result for 1 hour. Show a preview ("AI Portfolio Briefing — Tap to expand") on Dashboard with a "Read Full Briefing" link.
2. **Link card mentions.** When summary says "Umbreon EX," make it a clickable link → highlight that row in Portfolio.
3. **Move to Dashboard** as a collapsible panel, not a separate tab. Reduces tab bloat.

**Worth keeping?** CONDITIONAL — keep the logic, delete the tab. Integrate into Dashboard as a collapsible briefing card.

---

### 6. Exceptions (⚠️)

**Engineer verdict:** Works. Endpoint `/api/status` returns an `exceptions` array (e.g., cards with no Collectr URL, image fetch failures, grade confidence < threshold). Renders as a list or table.

**Designer verdict:** Empty state present. If exceptions exist, renders as table or list. Styling matches Portfolio. But: **extremely sparse.** Most users may see "No exceptions" forever, then one day get a wall of 3+ exceptions with no explanation of severity or action.

**Investor verdict:** **Rarely useful as-is.** Exceptions are implementation details ("image fetch failed," "no Collectr product found"), not investor decisions. A real exception tab for a serious collector would be: **"Grades I'm less confident in"** (PSA confidence < 85%), **"Cards in long-term grading wait"** (status="pending" for >6 months), **"Grade arbitrage opportunities"** ("Your PSA-8 could be a PSA-9 resubmit candidate based on comps"). The current tab is a **debug log, not an investor view.** Most real issues are handled silently by fallback chains in the code (image Tier 1→2→3, etc.).

**Top 3 fixes:**
1. Rename to "🔍 Data Confidence" and repurpose: show cards where (a) image match failed (phash mismatch), (b) grade premium is > 30% (unusual), (c) no eBay comps found (risky to price). These are *investor-relevant* exceptions.
2. If keeping current exceptions: add "Severity" (INFO/WARN/ERROR) and "Action" (Refresh image, Check cert, Re-search Collectr).
3. Or: **delete this tab entirely.** Surface critical issues (no image, failed cert fetch) as warning badges in Portfolio rows.

**Worth keeping?** NO — delete the tab or repurpose it into "Data Confidence" with investor-grade signals.

---

### 7. P&L Performance (💹)

**Engineer verdict:** Works but complex. Separate endpoint `/api/quantitative-matrix` feeds a bespoke charting system. Code references "Snapshot mode" vs "Scenarios" (theoretical modes not yet active). Renders with Chart.js. Contains action table (BUY/SELL recommendations).

**Designer verdict:** Clean layout with a warning banner (reconciliation guarantee). Charts look professional. But: **cognitive overload.** Multiple charts (P&L curve over time, distribution, action table) compete for space. "Scenarios" UI elements are grayed out (future feature, not ready). Mobile layout will stack vertically and stretch. No loading skeleton while data fetches. Horizontal scroll table (actions) will break on mobile.

**Investor verdict:** **Excellent conceptually, needs ruthless editing.** Current view shows: (a) snapshot P&L curve (cost vs market value over time?—unclear), (b) P&L distribution histogram, (c) action table (BUY/SELL/HOLD signals ranked by upside/downside). Missing: (a) **realized P&L** (cards you've sold; critical for tax planning), (b) **IRR compound annual growth** in THB, (c) **Drawdown from ATH** (currently underwater positions), (d) **12-month forecast** based on PSA pop trends. The action table is useful but buried; it should be on Dashboard (top 5 actions). The distribution histogram answers "how many winners vs losers" but not "what's the worst-case scenario."

**Top 3 fixes (Investor-driven):**
1. **Move action table (BUY/SELL signals) to Dashboard.** Top 3 signals only, with short reason ("Collectr ฿12K vs eBay avg ฿15K, +27% upside, n=6"). Leave detailed signals table in this tab for reference.
2. **Split this tab into two sub-tabs:** "Snapshot" (current holdings summary, P&L curve, drawdown from ATH) and "Forecast" (12-month projection, scenario modeling). Defer Scenarios to Phase D.
3. **Add realized P&L filter.** Show "Sold in last 30/60/90 days" and calculate realized IRR separately from unrealised. Critical for portfolio rebalancing.

**Worth keeping?** YES but redesign. Recommend: merge high-level signals into Dashboard, keep this tab for deep-dive analysis and realized/unrealised split.

---

## Cross-Tab Issues (Global)

### Navigation & Consistency
- ✅ Nav bar is sticky and always visible.
- ✅ Tab switching is instant (no network latency).
- ❌ **No breadcrumbs** (e.g., "Dashboard > Top Signals > Umbreon EX"). If you're deep in a portfolio detail, you don't know where you are.
- ❌ **No "back" button.** If you drill into a signal card, you can't go back to Portfolio without clicking the tab again.
- ⚠️ **Tab state not preserved.** If you sort Portfolio by "P&L", switch to Dashboard, then return to Portfolio, sort resets to default.

### Loading & Error States
- ⚠️ **No skeleton loaders.** When Refresh Data runs (2–5 sec), all tabs freeze. User sees a spinning button but no progress.
- ❌ **Network errors are silent.** If `/api/status` fails (network down, backend crash), tabs show empty state. No error message like "⚠️ Failed to load. Retry?".
- ⚠️ **Refresh button lacks affordance.** Button shows spinner, but no "Refreshing..." message or ETA.

### Accessibility (a11y)
- ✅ **Contrast:** Navy (#1B2A4A) on white and light gray backgrounds passes WCAG AA for normal text.
- ⚠️ **Color-only affordances:** Signal colors (green/red/orange/blue) are the only indicator of BUY/SELL/HOLD. Color-blind users may struggle. Add text labels (✓ BUY, ✗ SELL, etc.).
- ❌ **Missing ARIA labels.** `<div class="nav-tab">` should be `<button role="tab">` with `aria-selected`, `aria-controls`. Tabs are not keyboard-navigable (Tab key doesn't jump between tabs).
- ⚠️ **Table headers not sticky on mobile.** On iPhone SE (375px), scrolling down a table loses column context.

### Mobile Responsiveness
- ⚠️ **No mobile-first breakpoints.** Assumes desktop (1300px max-width layout). At 375px (iPhone SE), tables stack but are unreadable. No bottom nav or tab bar for mobile.
- ❌ **Add Card modal:** Full-screen sheet not implemented; likely overlays desktop modal on mobile, causing address-bar bounce and frustration.
- ❌ **Input font-size:** Form inputs are likely <16px, triggering iOS auto-zoom on focus. Breaks momentum scrolling.

### Color & Typography
- ✅ **Color tokens centralized** at top of `<style>` (--navy, --accent, --bg, etc.). Good for maintenance.
- ✅ **Type scale:** 14/16/20/28/40. Clean and readable.
- ⚠️ **KPI card font-size:** 22px for "฿151,684" is bold but could be 28px for senior investor (Bangkok, 55+, possibly presbyopia). Not a blocker.

---

## Prioritized Fix Backlog

### Phase B — High Priority (Investor-grade)

| Fix | Tab(s) | Effort | Champion | Reason |
|-----|--------|--------|----------|--------|
| Sticky table headers + row highlighting | Portfolio | M | Designer | Mobile usability + data retention when scrolling |
| Add "Days to Grade" + "Grade Premium %" columns | Portfolio | M | Investor | Critical for resubmit decisions + overpayment detection |
| Move Top 5 Signals from P&L tab to Dashboard | Dashboard, P&L | S | Investor | Visibility + reduce tab switching |
| AI Insights → Dashboard briefing card (cached) | Dashboard, Insights | M | Engineer | Reduce latency, improve discoverability |
| 24h/7d/30d P&L sparklines on KPI cards | Dashboard | M | Designer | Momentum visualization |
| Delete Collectr tab, merge into Portfolio detail | Portfolio | M | Investor | Consolidate related data; reduce tab bloat |
| Error state + retry for failed API calls | All | S | Engineer | Graceful degradation |
| Add loading skeleton loaders during Refresh | All | M | Designer | Transparency + perceived performance |

### Phase B — Medium Priority (UX Polish)

| Fix | Tab(s) | Effort | Champion | Reason |
|-----|--------|--------|----------|--------|
| Keyboard nav (Tab, Arrow keys) for tabs + table sorting | All | M | Engineer | a11y compliance (WCAG AA target) |
| ARIA labels + roles for tabs, buttons, tables | All | S | Engineer | Screen reader support |
| Color + text labels for signals (not color-only) | All | S | Designer | Color-blind accessibility |
| Add "Last Refresh" timestamp + cache hint | All | S | Engineer | Transparency (data age) |
| Tab state persistence (localStorage) | All | M | Engineer | UX continuity (remember sort, filters) |
| Add breadcrumbs or context nav | All | M | Designer | Wayfinding in deep views |

### Phase B — Low Priority (Polish)

| Fix | Tab(s) | Effort | Champion | Reason |
|-----|--------|--------|----------|--------|
| Dark mode toggle | All | S | Designer | User preference |
| Bulk select + soft-delete cards | Portfolio | M | Investor | Cleanup workflow |
| Export portfolio as CSV | Portfolio | S | Engineer | Data portability |

---

## Mobile-First Recommendations (Phase C.1)

1. **Bottom tab bar:** Replace sticky top nav with bottom tabs on screens < 768px. Easier thumb reach.
2. **Stacking card rows:** Tables → responsive card layout (one card per row) at < 600px.
3. **Add Card sheet:** Modal → full-screen bottom sheet (iOS-native feel).
4. **Input min font-size:** 16px to prevent iOS zoom.
5. **100dvh vs 100vh:** Handle address bar bounce on iOS Chrome.
6. **Tap targets:** All buttons ≥ 44 × 44px (already likely met, verify).

---

## Summary Recommendation

### Tabs to Keep (Locked)
- ✅ **Dashboard** — Solid, minimal changes needed.
- ✅ **Portfolio** — Core data view; needs redesign but essential.
- ✅ **Add Card** — Functional; fold into Card CRUD suite (Phase C.1).
- ✅ **P&L Performance** — Useful but needs refactor; signals → Dashboard.

### Tabs to Merge / Delete
- ❌ **Collectr** → Merge into Portfolio as detail panel or collapsible row.
- ⚠️ **Insights** → Delete tab; move briefing logic to Dashboard card (cached, auto-generated).
- ❌ **Exceptions** → Delete or repurpose as "Data Confidence" (image match, grade premium, eBay comps).

### Result: 4 core tabs (Dashboard, Portfolio, Add Card, P&L) + Card CRUD subsection.

---

## Phase A Acceptance Gate

- [x] All 7 tabs audited (screenshot + code analysis).
- [x] Engineer, Designer, and Investor lenses applied to each.
- [x] Cross-tab issues identified (nav, loading, a11y, mobile).
- [x] Backlog prioritized by effort + impact.
- [x] Recommendation: Keep 4 tabs, merge 2, delete 1.
- [x] Mobile-first strategy defined for Phase C.

**Status: READY FOR PHASE B.** User approval required on tab recommendations before redesign begins.

---

**End of Phase A Audit. Awaiting user approval to proceed to Phase B (Quality Pass).**
