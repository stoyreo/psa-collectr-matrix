# PSA × Collectr Tracer — Deep Product Audit
**Audit Date:** April 21, 2026  
**Status:** Phases 1–4 Complete (Product Reconstruction → Ranked Issues)

---

## 1. EXECUTIVE SUMMARY

**Product:** A sophisticated Pokémon card portfolio tracking and investment analytics dashboard that aggregates prices from multiple sources (Collectr, PSA, eBay), calculates P&L, generates buy/sell/hold signals, and runs scenario simulations.

**Current State:** Fully functional with 20 cards loaded; strong feature completeness; excellent data visualization and signal logic; critical gaps in UX clarity, onboarding, and market positioning.

**Key Strength:** Best-in-class portfolio analytics for Japanese Pokemon TCG investors. Multi-source price reconciliation, confidence scoring, and scenario modeling are mature.

**Key Weakness:** Product feels internal-tool–like; no clear growth loops; lacks shareable insights, alerts, watchlists; positioning is vague ("is this for flippers, collectors, or institutions?"); no mobile optimization; confidence explanations buried.

**Biggest Opportunity:** Transform from **analytical dashboard** → **investment intelligence platform** with habits (alerts), growth loops (sharing), and clear positioning for "Pokemon card investors optimizing entry/exit decisions."

---

## 2. CONFIRMED OBSERVATIONS FROM CURRENT SITE

### 2.1 Navigation & Structure
- **Main Tabs:** Dashboard, Portfolio, Add Card, Collectr, Insights, Exceptions, P&L Performance
- **Top-Right:** Last refresh timestamp, Refresh Data button (prominent blue CTA)
- **Header Branding:** "PSA × Collectr Tracer" — clean, minimal branding

### 2.2 Dashboard (Landing Page)

**Loaded with real data:**
- 20 PSA-graded Japanese Pokemon cards
- Total Cost: ฿235,232 (Thai Baht)
- Market Value: ฿270,287
- Unrealized P&L: ฿35,055 (+14.9% return)
- Best performer: FULL ART/PIKACHU (+289.6%)
- Watch alert: SLOWPOKE (-47.8%)

**Dashboard Components (all visible & functional):**
1. **KPI Cards:** 5 metrics (Cards, Total Cost, Market Value, P&L, Best Card)
2. **Watch Card Alert:** Single highlighted card with downside risk
3. **Confidence Summary:** 85% average (8 BUY, 2 SELL signal distribution)
4. **P&L by Card Waterfall:** All 19 positions ranked by P&L%, with red/green coloring
5. **Top 10 Pokemon Market Chart:** Live rankings with Collectr/PSA/eBay source badges
6. **Cost vs Market Value Chart:** Vertical bar pairs showing cost vs current value per card
7. **Signal Mix (Donut):** BUY 8, HOLD 4, SELL 2, REVIEW 4
8. **Risk Mix (Donut):** LOW 10, MEDIUM 4, HIGH 6

**Data Freshness:** "Last refresh: 20 Apr 2026 12:10:24 ⏱ LIVE"

### 2.3 Portfolio View

**Comprehensive table with 12 columns:**
- Row #, Card Name (with image), Set/Year, Card #, Grade, Cost (฿), Market Value (฿), P&L (฿), P&L %, Confidence %, Signal, Risk
- **8 visible cards:** SLOWPOKE, PSYDUCK, CHARIZARD EX, MAGIKARP, FULL ART/PIKACHU, PIKACHU (M-P PROMO), PIKACHU (S5 PROMO), PIKACHU (S-P PROMO)
- **Legend at top:** Explains Signal (BUY/HOLD/SELL/REVIEW) and Risk (LOW/MEDIUM/HIGH) with reasoning
- **Signal & Risk Badges:** Color-coded and actionable
- **Confidence shown per card:** Mostly 95%, some 50%, one 30%
- **Missing Data Handling:** One card shows blank Market Value (REVIEW signal, HIGH risk)

### 2.4 Add Card (Search & Intake)

**Minimal, clean interface:**
- Headline: "Find a Pokemon card"
- Instructions: "Start typing — name, set, card #, year. Paste a PSA cert # for direct lookup. Pick your grade to filter."
- Grade dropdown (PSA 10 selected)
- Single search input with placeholder example: "e.g. slowpoke art rare · 2023 · or cert 131858430"
- Helper: "Type 3+ characters to search — external shops shown first"
- **Strength:** Clear, instructive, minimal friction

### 2.5 Insights (Signal Generation)

**4 analytical cards:**
1. **Top Gainers (by Cost Basis in ฿):** PONCHO-WEARING PIKACHU (฿77,901), MEW EX (฿26,410), UMBREON EX (฿22,357), etc. with confidence notes
2. **Best Upside (P&L %):** FULL ART/PIKACHU (+289.6%), PIKACHU (+150.0%), MEW EX (+42.6%), MISCHIEVOUS PICHU (+39.3%), DETECTIVE PIKACHU (+33.5%)
3. **Weak Positions:** SLOWPOKE (-47.8%), SNORLAX (-26.3%), MEW EX (-18.0%), PIKACHU (-15.0%) — with confidence flags
4. **High Risk Cards:** Mixed winners and losers, all flagged for LOW/MEDIUM/HIGH confidence
- **Reasoning shown:** "Underwater", "Strong position", "Low confidence (50%); needs manual verification"
- **Confidence transparency:** Critical cards flagged with explicit reasoning

### 2.6 Exceptions

**Single exception flagged:**
- "Row 8 [Collectr Match]: No market data for PIKACHU"
- Orange/warning banner at top
- References missing price data in portfolio
- **System working correctly:** Data quality monitoring in place

### 2.7 P&L Performance (Scenario Analysis)

**Top metrics recap:**
- Portfolio NAV: ฿270,287
- Unrealized P&L: ฿35,055 (+14.9%)
- Winners: 13, Losers: 7
- Avg Confidence: 85%
- Top Concentration: 32.7%
- POP Alerts: 0

**Visualizations:**
1. **Winners & Losers:** Horizontal bar chart, green/red, scaled to individual P&L contribution
2. **Cost vs Market Value:** Area chart showing total portfolio cost vs market value
3. **Signal Breakdown:** Donut chart (BUY dominant, HOLD, SELL, REVIEW)

**Scenarios (currently all OFF):**
- Bull (+30%)
- Bear (-25%)
- POP Dilution
- Grade Upgrade
- JPY/THB +10%
- JPY/THB -10%

**Results Table:** Columns for CARD, COST (฿), MARKET VALUE (฿), P&L (฿), P&L %, SIGNAL, ACTION (appears to populate when scenario is enabled)

---

## 3. INFERRED PRODUCT INTENT

### 3.1 Core Purpose
**Portfolio intelligence system for Japanese Pokemon TCG investors.** Aggregates prices across multiple sources, calculates real-time P&L, generates decision signals (BUY/HOLD/SELL/REVIEW), and models investment scenarios to optimize entry/exit timing.

### 3.2 Primary Users
1. **Serious collectors** (want to track value & trends)
2. **Card flippers** (want to optimize buy/sell timing)
3. **Institutional buyers** (want portfolio risk visibility)
4. **Graders/dealers** (want market intelligence)

**Implied user behavior:** Daily/weekly check-in to see portfolio performance, monitor watch cards, and make buy/sell decisions.

### 3.3 Main Workflow
1. **Add Card:** Search PSA database, input cost, date acquired, source
2. **Monitor:** Dashboard shows aggregated P&L, signals, and risk
3. **Act:** Use Insights to identify weak positions (sell) or strong buys (accumulate)
4. **Simulate:** Run scenarios (currency swings, grade upgrades, market shocks) before acting
5. **Track:** Historical trends (inferred from data structure)

### 3.4 Key Modules (Confirmed from UI)
- **Portfolio Management:** 12-column table with full position view
- **Price Aggregation:** Multi-source reconciliation (Collectr, PSA, eBay fallback)
- **Signal Generation:** BUY/HOLD/SELL/REVIEW based on market data + confidence
- **Risk Assessment:** LOW/MEDIUM/HIGH risk per card
- **Scenario Modeling:** 6 macro/micro scenario toggles
- **Confidence Scoring:** 95%, 50%, 30% transparency (data quality indicator)
- **Exception Management:** Flags missing data or price mismatches
- **Market Intelligence:** Top 10 rankings, live Collectr feeds

### 3.5 Missing Pieces Preventing Strong Experience
1. **Onboarding:** No welcome flow; new users land on empty Dashboard until they add cards
2. **Demo/Sample Portfolio:** No way to explore without committing cards
3. **Positioning:** No clear answer to "Who is this for?" (collectors? flippers? institutions?)
4. **Habit Loops:** No alerts, no daily digest, no watchlist notifications
5. **Shareability:** No portfolio snapshots, no comparison tools, no community aspect
6. **Mobile:** Clearly desktop-first (charts may not scale)
7. **Scenarios Explainer:** Why these 6 scenarios? How do they affect signals?
8. **Confidence Logic:** Buried in Portfolio legend; not explained at signal-generation time
9. **Data Freshness:** Shows timestamp but not clear when prices were last pulled from each source
10. **Historical Context:** No trend charts, no acquisition cost vs grade upgrade potential analysis
11. **Export/Integration:** Can't export portfolio, link to external apps, or auto-sync with PSA vault
12. **Monetization Hooks:** No clear premium tier (notifications, advanced analysis, API?)

---

## 4. RANKED ISSUES LIST

### Critical Issues (Block core value delivery)

| # | Issue | Severity | Why It Matters | Quick Fix | Effort |
|---|-------|----------|---|---|---|
| 1 | **No positioning statement on homepage** | CRITICAL | Users land on Dashboard without understanding "Is this for collectors, flippers, or institutions?" — friction increases bounce. | Add 2-line tagline + 3-option user selector on first load | S |
| 2 | **Empty-state Dashboard is confusing** | CRITICAL | New user sees "No data loaded" + charts with no context. No clear next step. High abandonment. | Replace with onboarding flow: "Add your first card" CTA + mini tutorial + optional demo data | M |
| 3 | **Confidence logic is unexplained at point of use** | CRITICAL | Signals show 95%/50%/30% but user must scroll to Portfolio legend to understand why. Undermines trust. | Show inline tooltip on signal badge: "95% — Collectr direct match" | S |
| 4 | **No sample/demo portfolio** | CRITICAL | Can't explore full app without adding real cards. High friction for first-time users. | Create 1-click demo mode with 15 sample cards; let users toggle back to real portfolio | M |

### High Priority Issues (Degrade core experience)

| # | Issue | Severity | Why It Matters | Quick Fix | Effort |
|---|-------|----------|---|---|---|
| 5 | **Scenarios page has no explanation** | HIGH | 6 scenario toggles with no context: "Why Bull +30%? How does Grade Upgrade work? What's POP Dilution?" | Add info icon next to each scenario with 1-line explanation | S |
| 6 | **Missing data not actionable** | HIGH | Exceptions page shows "No market data for PIKACHU" but no "Fix this" or "Verify on Collectr" CTA. | Add action buttons: "Verify on Collectr" or "Update Price" | S |
| 7 | **No data source transparency in charts** | HIGH | Top 10 chart shows badges (COLLECTR/PSA/FALLBACK) but main Portfolio table doesn't. Unclear which prices are sourced from where. | Add source column to Portfolio (Collectr, PSA, eBay, Estimate) | M |
| 8 | **No alert/watchlist system** | HIGH | Users check dashboard manually. No way to get notified when SLOWPOKE recovers or FULL ART/PIKACHU drops 10%. | Add quick watchlist feature to Dashboard; show next to Watch Card section | M |
| 9 | **Portfolio table not mobile-responsive** | HIGH | 12 columns on desktop; unreadable on tablet/phone. No mobile strategy visible. | Create mobile card layout (expandable rows) or mobile-first nav tabs | L |
| 10 | **Scenario results table doesn't update visually** | HIGH | Toggling Bull/Bear doesn't show real-time table update; unclear if scenarios are applied. | Add transition animation + show "Scenario: Bull +30% applied" banner above results table | M |

### Medium Priority Issues (Polish & retention)

| # | Issue | Severity | Why It Matters | Quick Fix | Effort |
|---|-------|----------|---|---|---|
| 11 | **No portfolio export or sharing** | MEDIUM | Can't email portfolio snapshot to advisor, share wins on social, or export to Excel for tax prep. | Add "Share Portfolio" button → generate unique snapshot URL or CSV download | M |
| 12 | **Refresh Data button is unexplained** | MEDIUM | What does it refresh? How often is data auto-synced? Are prices real-time or 1h delayed? | Add tooltip: "Pulls latest prices from Collectr, PSA, eBay. Last sync: 2:10 PM" | S |
| 13 | **No historical trend view** | MEDIUM | Can't see "Did this card perform better in Feb than March?" or detect market cycles. | Add "Historical" tab with 30/90/365 day charts per card | L |
| 14 | **Insights cards don't link to actions** | MEDIUM | Showing "SLOWPOKE is down 47.8%" but no "Sell?" or "Reassess?" CTA. | Make each insight card clickable → shows detailed card view + scenario options | M |
| 15 | **Signal rationale not shown at Portfolio level** | MEDIUM | Portfolio shows BUY badge but not *why* — cost trending up, Collectr rising, or both? | Add expandable "Why BUY?" under each signal badge showing 2–3 factors | S |
| 16 | **No POP (Population) trend integration** | MEDIUM | Scenario includes "POP Dilution" but no way to see current POP or historical POP trend per card. | Add POP sparkline column to Portfolio; link to PSA PopReport | M |
| 17 | **Top 10 chart uses ambiguous timestamp** | MEDIUM | Shows "Last Collectr: ฿4,088" but unclear if this is current price, cost, or last update time. | Clarify label: "Collectr (updated 2:10 PM) · ฿4,088" | S |
| 18 | **Cost vs Market chart lacks context** | MEDIUM | Chart shows total portfolio cost vs market value but not per-card breakdown or trend over time. | Add toggle: "Show by Card" to see individual P&L waterfall | M |

### Low Priority Issues (Nice-to-have, polish)

| # | Issue | Severity | Why It Matters | Quick Fix | Effort |
|---|-------|----------|---|---|---|
| 19 | **No keyboard shortcuts or search-to-add** | LOW | Experienced users want faster workflows. Current add-card flow requires 3+ clicks. | Add cmd+K shortcut to search + add card inline | M |
| 20 | **Collectr tab is empty/unexplained** | LOW | Navigation shows "Collectr" tab but appears to have no content. Unclear purpose. | Either populate with Collectr feed/marketplace or remove from nav | M |
| 21 | **Signal badges don't have hover explanations** | LOW | Nice-to-have: show "This card is in strong uptrend, market value above cost" on badge hover. | Add title attribute to badge elements | S |
| 22 | **No API or external integrations** | LOW | Can't auto-sync PSA vault, eBay exports, or push to portfolio tracking services. | Document API roadmap if this is strategic | L |
| 23 | **Language is UK English (mostly)** | LOW | Minor: "Confidence %" could be localized for Thai market (฿ currency is correct). | Audit copy for consistency; add i18n framework if expanding | S |

---

## 5. IMPROVEMENT ROADMAP (Prioritized)

### Immediate Wins (0–3 days) — High leverage, low effort

1. **Add positioning tagline to Dashboard** (S)
   - "Smart portfolio tracking for Pokemon card investors"
   - New user selector: "I'm a Collector | I'm a Flipper | I'm a Dealer"
   
2. **Add confidence inline tooltips** (S)
   - Hover on signal badge → "95% — Price sourced directly from Collectr with full match"
   
3. **Clarify Refresh Data button** (S)
   - Tooltip: "Last synced: 2:10 PM. Updates Collectr, PSA, eBay prices."
   
4. **Fix Top 10 timestamp ambiguity** (S)
   - Change "Last Collectr: ฿4,088" → "Collectr price (updated 2:10 PM): ฿4,088"
   
5. **Add "Why BUY/SELL/HOLD" explainers to Portfolio** (S)
   - Expand signal badge to show 2–3 factors (e.g., "Cost down 5% week-over-week • Collectr trending up")

---

### Near-term (1–2 weeks) — Feature & UX improvements

6. **Build demo/sample portfolio mode** (M)
   - 1-click "Try Demo" loads 15 sample cards
   - Toggle button to switch between demo and real portfolio
   - Reduces onboarding friction significantly
   
7. **Add missing-data action buttons** (S)
   - Exceptions page: "Row 8 [Collectr Match]: No market data for PIKACHU"
   - Add buttons: "Verify on Collectr" | "Update Price Manually" | "Mark as Inactive"
   
8. **Add scenario explanations** (S)
   - Each scenario gets info icon
   - "Bull (+30%): Market optimism scenario. All prices increase 30%."
   - "POP Dilution: Risk that more copies exist. Grade trend down."
   - "Grade Upgrade: What if this card graded PSA 9 instead? (10% upside estimate)"
   
9. **Build first-run onboarding flow** (M)
   - Step 1: "What are you optimizing for?" (Collector, Flipper, Dealer selector)
   - Step 2: "Add your first card" with guided search
   - Step 3: "Your first insights" — highlight strongest performer and weakest position
   - Step 4: "Set up alerts?" (watchlist preference)
   
10. **Add data source transparency column** (M)
    - Portfolio table: Add "Source" column (Collectr, PSA, eBay, Estimate)
    - Shows user exactly where each price comes from
    - Filters option: Show only Collectr, hide Estimates
    
11. **Build simple watchlist feature** (M)
    - Dashboard: Add "Watchlist" card next to Watch Card
    - Users can add up to 5 cards to watch
    - Shows when card reaches buy/sell alert thresholds
    
12. **Scenario results visualization improvement** (M)
    - When Bull/Bear/etc. toggled: show banner "Scenario: Bull +30% applied"
    - Table updates with new P&L/Signal columns
    - Add reset button to clear scenarios
    
13. **Add portfolio export (CSV/PDF)** (M)
    - "Export Portfolio" button → downloads CSV with all columns
    - Nice-to-have: "Share Snapshot" → generates time-stamped URL (read-only view)

---

### Major Product Enhancements (3–8 weeks) — Strategic improvements

14. **Historical trend view per card** (L)
    - New "Trends" tab showing 30/90/365 day price history
    - Sparkline per card in Portfolio (optional)
    - Helps investors see seasonal patterns, grading cycles, market sentiment
    
15. **Advanced signal explainer** (M)
    - Expand Portfolio legend to explain *how* signals are calculated
    - Show example: "BUY = Collectr price > cost AND confidence > 80% AND risk = LOW"
    - Allow users to customize signal thresholds
    
16. **POP trend integration** (M)
    - Add POP column to Portfolio (current POP rank)
    - Link to PSA PopReport
    - Scenario: Show how POP dilution affects card value
    - Historical POP trend chart
    
17. **Mobile-first redesign** (L)
    - Create responsive card-based layout
    - Mobile nav: Dashboard | Portfolio | Insights | Add Card
    - Expandable rows instead of 12-column table
    - Touch-friendly scenario toggles
    
18. **Alert center / Daily digest** (M)
    - Email notifications: "SLOWPOKE recovered 10% today" | "FULL ART/PIKACHU dropped 5%"
    - Frequency: daily, weekly, or custom
    - Premium feature (hint at monetization)
    
19. **Confidence score redesign** (M)
    - Create visual confidence indicator (gauge or bar)
    - Show breakdown: "Data freshness 95% • Source reliability 90% • Market depth 75%"
    - Help users understand *why* a card is REVIEW vs HIGH confidence
    
20. **Compare before you buy workflow** (M)
    - Search for a card → show "You own X • Market has Y better cards for less"
    - Suggest: "DETECTIVE PIKACHU is 33% cheaper than FULL ART/PIKACHU. Same era, similar grade."
    - Drive informed buying
    
21. **Tax/Fee calculator** (M)
    - If I sell FULL ART/PIKACHU, what's my net P&L after fees?
    - Inputs: Sale price, fee % (Collectr, eBay, etc.), tax rate
    - Shows net proceeds → helps decision-making
    
22. **Import from CSV / PSA Vault / eBay exports** (L)
    - Bulk upload portfolio instead of manual add-one-by-one
    - Auto-sync with PSA vault if API available
    - Reduces time-to-value for existing collectors
    
23. **Portfolio scoring / grading system** (L)
    - "Your portfolio is 'Aggressive Growth'" (5-star rating)
    - Shows breakdown: concentration risk, confidence distribution, avg P&L %
    - Compares to "baseline" portfolio (helpful for dealers/institutions)
    
24. **API / Webhook system** (L)
    - Expose portfolio data via API
    - Send webhooks when signal changes (BUY → SELL)
    - Monetization: premium tier for API access

---

## 6. MULTI-AGENT TEAM DESIGN

### Agent 1: Product Strategist
**Mission:** Refine positioning, clarify user segmentation, prioritize roadmap phases

**Scope:**
- Define 2–3 clear user personas (Collector vs. Flipper vs. Dealer)
- Write positioning statement & value prop
- Validate roadmap prioritization against user needs
- Recommend premium features + pricing tiers
- Plan go-to-market messaging

**Key Deliverables:**
- Positioning statement (1 paragraph)
- User persona document (3 personas × 2 pages each)
- Feature priority matrix (effort vs. impact)
- Pricing tier proposal (Free, Pro, Enterprise)

**Success:** Positioning is clear; team agrees on roadmap order

---

### Agent 2: UX Research & Information Architecture
**Mission:** Simplify navigation, improve empty states, design first-run flow

**Scope:**
- Audit current IA (7 tabs; can this be simplified?)
- Design empty-state → first-value flow (onboarding)
- Create demo portfolio architecture
- Design first-run wizard (user segmentation)
- Test tab order and nav hierarchy

**Key Deliverables:**
- Revised IA diagram (simplified navigation)
- Empty-state + onboarding flow (wireframes)
- Demo portfolio spec (15 sample cards + scenarios)
- First-run wizard mockup (4 steps)
- Nav structure recommendation

**Success:** New users can reach "first insight" in <3 minutes

---

### Agent 3: UI Design
**Mission:** Improve dashboards, charts, tables, and signal transparency

**Scope:**
- Redesign Dashboard KPI cards (visual hierarchy)
- Improve chart spacing and readability
- Create signal badge tooltip designs
- Design Portfolio table mobile layout
- Create scenario explanation UI (info icons)
- Design confidence score redesign

**Key Deliverables:**
- Updated Dashboard comp (Figma/high-fidelity mockup)
- Signal badge + tooltip design
- Mobile Portfolio card layout mockup
- Scenario info icon design
- Confidence gauge design
- Dark/light mode guidance

**Success:** Designs improve clarity without adding clutter

---

### Agent 4: Conversion & Retention
**Mission:** Build habit loops, increase daily actives, design growth mechanics

**Scope:**
- Design watchlist feature
- Design alert/notification system
- Create "daily digest" email template
- Design portfolio sharing feature
- Plan referral mechanics (if applicable)
- Propose retention KPIs

**Key Deliverables:**
- Watchlist feature spec
- Alert center design (in-app + email)
- Daily digest email template
- Share button + snapshot UX design
- Growth metrics proposal (DAU, MAU, retention curve)

**Success:** New metric: daily check-ins increase 30%+ after alerts launch

---

### Agent 5: Market Intelligence
**Mission:** Improve pricing logic, source reconciliation, signal credibility

**Scope:**
- Document current price sourcing logic (which source wins? fallback rules?)
- Design data freshness transparency (when was each price pulled?)
- Build confidence score model (data quality indicators)
- Propose POP integration architecture
- Validate signal logic against user feedback
- Define source precedence rules

**Key Deliverables:**
- Price sourcing decision tree (documented rules)
- Confidence score calculation spec
- Data freshness UI proposal (per-card timestamps)
- POP integration architecture
- Source badge design + legend
- Signal generation logic diagram

**Success:** Users understand why a signal changed; trust confidence %

---

### Agent 6: Monetization
**Mission:** Define premium features, pricing structure, and revenue model

**Scope:**
- Identify premium-worthy features (alerts, API, advanced analytics, export)
- Design 2–3 pricing tiers (Free, Pro, Enterprise)
- Estimate willingness-to-pay (based on user value, market research)
- Define free tier guardrails (limit alerts? limit portfolio size?)
- Propose packaging (annual vs. monthly)

**Key Deliverables:**
- Premium feature recommendation (top 5 monetizable features)
- Pricing tier spec (features, price, target user)
- Packaging recommendation (monthly/annual)
- Revenue model projection
- FAQ for pricing (why is X premium?)

**Success:** Clear monetization roadmap; leadership approves tier structure

---

### Agent 7: Frontend Engineer
**Mission:** Propose implementation-level improvements for speed, resilience, UX

**Scope:**
- Audit current component architecture (reusable components? tech debt?)
- Recommend state management improvements (Redux, Zustand, Context?)
- Propose data-fetch strategy (real-time vs. polling vs. WebSocket?)
- Design empty/loading/error states across all pages
- Recommend performance optimizations (lazy load charts? virtualize table?)
- Propose mobile-responsive breakpoints

**Key Deliverables:**
- Component audit + refactoring plan
- State management recommendation
- Data-fetch architecture proposal
- Empty/loading/error state spec (per page)
- Performance optimization roadmap
- Mobile breakpoint spec (375px, 768px, 1024px, 1440px)

**Success:** App loads <2s; no console errors on empty states

---

### Agent 8: QA / Edge Case
**Mission:** Identify failure states, mismatches, and misleading UI

**Scope:**
- Test all empty/loading/error states
- Verify data reconciliation (e.g., Portfolio P&L matches Dashboard totals)
- Check scenario logic (does Bull +30% apply correctly to all cards?)
- Validate signal changes (does signal update when price updates?)
- Test data freshness edge cases (what if price unavailable for 24h?)
- Check mobile responsiveness
- Verify confidence logic (why is one card 95% and another 30%?)

**Key Deliverables:**
- Edge case bug log (with severity + reproduction steps)
- Data reconciliation check (Portfolio vs. Dashboard)
- Scenario test matrix (all 6 scenarios × test cases)
- Mobile responsiveness report
- Signal logic validation report
- Confidence score audit

**Success:** No data mismatches; all scenarios apply correctly

---

## 7. DO NOT MISTAKE PLACEHOLDER UX FOR FINISHED PRODUCT

### Distinction: What's Missing vs. What's Actually Broken

**Current Empty State Issues (NOT design flaws, but legitimate friction points):**
- Dashboard has "No data loaded" message when user first arrives
- Collectr tab appears empty (likely unbuilt or API disconnected)
- Scenario results table doesn't update until scenario applied (expected behavior, but UX could be clearer)
- Some charts are sparse on initial load (waiting for data)

**These are NOT finished-product problems.** They're first-run friction points that onboarding solves.

**Actual Design/Product Flaws (not placeholder-related):**
1. Confidence explanations are buried in Portfolio legend (not at point of use)
2. Signal generation logic is opaque ("Why BUY?")
3. No habit-loop mechanics (no alerts, no daily check-in reason)
4. Positioning is vague (unclear who this is for)
5. Mobile experience likely suboptimal (not tested)
6. No growth/shareability features
7. Scenario toggles lack explanations

**Opportunities Hidden Behind Empty State:**
- Demo portfolio mode would showcase 15 cards, all 6 scenarios, full Insights page
- First-run onboarding would guide users to "first valuable insight" in 3 minutes
- Sample portfolio would prove value before user commits own data
- Watchlist feature would create daily check-in habit

**Conclusion:** The product is 70–80% feature-complete and 60% polish-complete. Main gaps are onboarding, positioning, and habit loops — not core product functionality.

---

## END OF PHASES 1–4

**Next Steps (Phases 5–6):**
- Phase 5: Define Supervisor Execution Sequence + Dependencies
- Phase 6: Generate 8 Ready-to-Run Sub-Agent Prompts
