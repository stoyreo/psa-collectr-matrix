# PSA × Collectr Tracer — Execution Plan
**Phases 5–6: Supervisor Sequence + Ready-to-Run Prompts**

---

## PHASE 5: SUPERVISOR EXECUTION SEQUENCE

### Execution Strategy
**Critical Path:** Product Strategist → UX Research → UI Design + Frontend → QA  
**Parallel Tracks:** Monetization + Market Intelligence (independent of design)  
**Total Duration:** 3–4 weeks (compressed timeline)  
**Handoff Points:** Each agent delivers → next agent consumes + builds on output

---

### Wave 1: Foundation (Days 1–3) — Run in Parallel
**Goal:** Establish positioning, user segmentation, and information architecture  
**Why first:** Everything downstream depends on these decisions

#### Step 1A: Product Strategist
**Owner:** Product Strategist Agent  
**Objective:** Define positioning, user personas, feature priority matrix, pricing tiers  
**Inputs:** Product Audit (Phases 1–4), observed user workflows, roadmap issues list  
**Outputs:** 
- Positioning statement (1 paragraph)
- 3 user personas (Collector, Flipper, Dealer) with goals/pain points
- Feature priority matrix (effort × impact)
- Pricing tier proposal (Free, Pro, Enterprise with feature allocation)
- Go-to-market messaging

**Success Metric:** Leadership approves positioning; team agrees on user prioritization

**Dependencies:** None (Wave 1 start)

---

#### Step 1B: UX Research & Information Architecture
**Owner:** UX Research Agent  
**Objective:** Simplify navigation, design onboarding flow, spec demo portfolio  
**Inputs:** Product Audit, current 7-tab navigation, empty-state pain points  
**Outputs:**
- Revised IA diagram (proposed tab consolidation or reorganization)
- Empty-state flow diagram (→ first-run onboarding)
- Onboarding wizard wireframes (4 steps: segmentation → add card → first insight → alerts)
- Demo portfolio specification (15 sample cards, 3 scenarios enabled)
- Mobile IA proposal (responsive breakpoints)

**Success Metric:** New users can reach "first valuable insight" in <3 min; demo shows full app value

**Dependencies:** None (Wave 1 start); inputs from Product Strategist helpful but not blocking

---

### Wave 2: Strategy & Market Logic (Days 3–5) — Run in Parallel
**Goal:** Define monetization tiers, price sourcing logic, confidence scoring  
**Why after Wave 1:** Positioning + user personas inform which features to monetize

#### Step 2A: Monetization Agent
**Owner:** Monetization Agent  
**Objective:** Define premium features, pricing tiers, revenue model  
**Inputs:** Feature priority matrix from Product Strategist, roadmap (Phases 1–4)  
**Outputs:**
- Premium feature recommendation (top 5: alerts, API, advanced analytics, export, historical trends)
- Pricing tier spec (Free 0–20 cards, Pro $9.99/mo + alerts, Enterprise custom)
- Annual vs. monthly packaging recommendation
- Revenue model projection (% assumed adoption × willingness-to-pay)
- Freemium guardrails (what do free users not get?)
- FAQ for pricing

**Success Metric:** Leadership approves tier structure; can articulate why each feature is premium

**Dependencies:** Product Strategist (positioning + user segments)

---

#### Step 2B: Market Intelligence Agent
**Owner:** Market Intelligence Agent  
**Objective:** Document price sourcing, confidence scoring logic, data freshness strategy  
**Inputs:** Current app logic (Portfolio, Insights, signals), audit findings on confidence gaps  
**Outputs:**
- Price sourcing decision tree (which source wins? fallback rules? When to mark REVIEW?)
- Confidence score calculation model (formula: data freshness × source reliability × market depth)
- Data freshness transparency spec (per-card timestamp + sync history)
- Source precedence documentation (Collectr > PSA estimate > eBay avg)
- Signal generation logic diagram (how BUY/HOLD/SELL determined)
- POP integration architecture (current POP + historical trend proposal)
- Edge case handling spec (what if price missing for 24h? Show stale price or REVIEW?)

**Success Metric:** Users understand *why* a signal changed; confidence % is transparent + auditable

**Dependencies:** None (but inputs from Product Strategist + UX Research helpful for prioritization)

---

### Wave 3: Design & Implementation (Days 5–15) — Can run in parallel after Wave 1
**Goal:** Create UI/frontend architecture for improvements  
**Why after Wave 1:** IA + positioning guide all design decisions

#### Step 3A: UI Design Agent
**Owner:** UI Design Agent  
**Objective:** Redesign Dashboard, signals, confidence, scenarios, mobile layout  
**Inputs:** IA from UX Research, feature priority from Product Strategist, audit issues  
**Outputs:**
- Updated Dashboard comp (Figma/mockup) with:
  - Positioning tagline at top
  - Demo portfolio toggle
  - Improved KPI card hierarchy
  - Watchlist widget
  - Watch Card alert
- Signal badge redesign with tooltip (shows "95% — Collectr direct match")
- Confidence score visual (gauge or bar chart showing data freshness × reliability)
- Scenario explainer UI (info icons + modal explanations for all 6 scenarios)
- Mobile card layout mockup (expandable rows, touch-friendly toggles)
- Portfolio table responsive design (show/hide columns, mobile-first)
- Alert center UI mockup (email + in-app notifications)
- Sharing/export button design
- Dark mode color spec (if applicable)

**Success Metric:** Designs improve clarity without adding visual clutter; mobile prototype shows full functionality on 375px viewport

**Dependencies:** UX Research (IA), Product Strategist (positioning)

---

#### Step 3B: Frontend Engineer Agent
**Owner:** Frontend Engineer Agent  
**Objective:** Propose component architecture, state management, data-fetch strategy, performance  
**Inputs:** Current tech stack (inferred: React + charts library), IA from UX Research, feature list  
**Outputs:**
- Component architecture audit + refactoring plan (extract reusable signal badge, card widget, etc.)
- State management recommendation (Redux, Zustand, Context for portfolio state)
- Data-fetch strategy (polling interval for prices? Real-time WebSocket? Hybrid?)
- Empty/loading/error state spec per page (with code examples)
- Performance optimization roadmap (lazy load charts, virtualize table, bundle splitting)
- Mobile breakpoint spec (375px, 768px, 1024px, 1440px)
- Responsive design implementation guide (CSS Grid fallbacks, flexbox strategy)
- Asset optimization (image loading, chart rendering)
- Testing strategy for scenarios (unit tests for Bull/Bear/POP dilution logic)

**Success Metric:** App loads <2s; no console errors on empty states; table scrolls smoothly with 20+ cards

**Dependencies:** UX Research (IA), UI Design (mockups guide component structure)

---

#### Step 3C: Conversion & Retention Agent
**Owner:** Conversion & Retention Agent  
**Objective:** Design habit loops, alerts, watchlist, sharing  
**Inputs:** User personas from Product Strategist, IA from UX Research, monetization tiers  
**Outputs:**
- Watchlist feature spec (add up to 5 cards, set alert thresholds, Dashboard widget)
- Alert center design:
  - In-app toast notifications (card up/down 10%, signal change)
  - Email digest (daily/weekly summary of wins/losses)
  - Email notification templates (design + copy)
  - Alert frequency preference UI
- Portfolio sharing feature spec:
  - "Share Portfolio" button → unique snapshot URL (read-only view)
  - Snapshot URL TTL (24h? Permanent?)
  - Social share buttons (Twitter, email)
- Growth metrics & KPIs (DAU, retention curve, alert engagement rate)
- Retention levers for free tier (alerts limited to 2 cards? Or unlimited?)
- Referral mechanic proposal (if applicable: "Invite friend to PSA Tracer")

**Success Metric:** Daily check-ins increase 30%+ after alerts launch; sharing doubles portfolio referrals

**Dependencies:** Product Strategist (user personas), Monetization Agent (alert tier limits)

---

### Wave 4: Validation (Days 15–21) — Run after Wave 3
**Goal:** Test all features, validate data reconciliation, identify bugs  
**Why last:** QA tests implementations from Wave 3

#### Step 4: QA / Edge Cases Agent
**Owner:** QA / Edge Cases Agent  
**Objective:** Identify failure states, data mismatches, edge cases  
**Inputs:** All deliverables from Waves 1–3 (UI mockups, code, features)  
**Outputs:**
- Edge case bug log (with severity + reproduction steps):
  - What if price missing for 24h? (should show REVIEW signal, not crash)
  - What if user toggles Bull + Grade Upgrade + JPY/THB +10% simultaneously? (all apply correctly)
  - What if Portfolio has 0 cards? (empty state shows, not error)
  - Mobile: Can user expand card details on touch? (no false positives)
  - Scenarios: Do results table update in real-time? (or delay?)
- Data reconciliation report:
  - Portfolio P&L totals = Dashboard P&L? (must match)
  - Scenario results: Does Bull +30% apply to all 20 cards? (verify each)
  - Top 10 chart: Are rankings correct? (cross-check with Portfolio)
- Confidence score audit:
  - Why is one card 95% and another 30%? (verify logic matches Market Intelligence spec)
  - Does confidence update when price updates? (should be real-time)
- Mobile responsiveness checklist (375px, 768px tested)
- Signal logic validation (BUY threshold met? Then signal should be BUY, not HOLD)
- Accessibility audit (WCAG 2.1 AA: colors, contrast, keyboard nav)

**Success Metric:** No data mismatches between Dashboard and Portfolio; all scenarios apply correctly; mobile loads all features; confidence scoring is auditable

**Dependencies:** All other agents (tests their work)

---

### Critical Path Analysis

```
Wave 1 (Days 1–3):
├─ Product Strategist ─→ [Positioning, Personas, Priority Matrix]
└─ UX Research ────────→ [IA, Onboarding Flow, Mobile Spec]
                 ↓
Wave 2 (Days 3–5, can start before Wave 1 ends):
├─ Monetization ──────→ [Premium Tiers, Revenue Model]
└─ Market Intelligence ─→ [Confidence Logic, Price Sourcing, Data Freshness]
                 ↓
Wave 3 (Days 5–15, can start on Day 3):
├─ UI Design ─────────→ [Mockups, Responsive Design, Components]
├─ Frontend Engineer ──→ [Architecture, Components, State Mgmt]
└─ Conversion & Retention ─→ [Alerts, Watchlist, Sharing]
                 ↓
Wave 4 (Days 15–21):
└─ QA / Edge Cases ───→ [Bug Log, Data Validation, Mobile Testing]
```

**Critical Path Duration:** 21 days (3 weeks)  
**Parallel Opportunity:** Waves 1 & 2 can overlap; Wave 3 can start Day 3  
**Milestone 1 (Day 5):** IA + Positioning approved → unblock Wave 3  
**Milestone 2 (Day 15):** UI + Frontend specs ready → unblock QA  
**Milestone 3 (Day 21):** QA sign-off → ready for development sprint

---

## PHASE 6: READY-TO-RUN AGENT PROMPTS

### How to Use These Prompts
1. Copy each prompt below
2. Create a new Cowork session per agent (or queue them)
3. Paste prompt into chat
4. Agent will produce deliverables in strict format
5. Supervisor (you) collects outputs → coordinates Wave 2 onward

---

### Prompt 1: Product Strategist Agent

```
MISSION: Clarify PSA × Collectr Tracer positioning and user strategy.

CONTEXT:
You're auditing a Pokemon card portfolio tracking dashboard 
(https://celebrity-wool-zus-confident.trycloudflare.com/). 
It's feature-complete but lacks clear positioning: users don't know 
if this tool is for collectors, flippers, or institutions.

The app includes:
- Portfolio management (20 cards, real P&L data)
- Multi-source price aggregation (Collectr, PSA, eBay)
- BUY/HOLD/SELL/REVIEW signals with confidence scoring
- 6 scenario models (Bull/Bear/POP Dilution/Grade Upgrade/JPY-THB shifts)
- Insights (top gainers, weak positions, high-risk cards)

DELIVERABLES (output in this exact format):

## POSITIONING STATEMENT
[1 paragraph: who this is for, what problem it solves, why it's different]

## USER PERSONAS
Create 3 personas (500 words each):
1. Collector (casual, wants to track value + trends)
2. Flipper (active trader, wants buy/sell timing signals)
3. Dealer/Institution (high-volume, wants portfolio risk visibility)

For each persona include:
- Goals
- Pain points
- Decision-making style
- Willingness-to-pay

## FEATURE PRIORITY MATRIX
Rank top 20 roadmap items by:
- Effort (S/M/L)
- Impact on user value (1–5)
- Impact on retention (1–5)
- Impact on monetization (1–5)

Format as table: Feature | Effort | User Impact | Retention | Monetization | Priority Score

## PRICING TIER PROPOSAL
Define 3 tiers:
- Free: What's included? User limits?
- Pro ($X/month): Premium features list
- Enterprise: Custom pricing, features

Justify why each feature is premium.

## GO-TO-MARKET MESSAGING
Write 3 positioning statements (one per persona):
- "For collectors who want to..."
- "For flippers who want to..."
- "For dealers who want to..."

END OUTPUT
```

---

### Prompt 2: UX Research & Information Architecture Agent

```
MISSION: Design onboarding, simplify navigation, specify demo portfolio.

CONTEXT:
PSA × Collectr Tracer is a Pokemon card portfolio tracker with 7 tabs 
(Dashboard, Portfolio, Add Card, Collectr, Insights, Exceptions, P&L Performance).
New users land on empty Dashboard with no guidance. Need to:
- Reduce time-to-first-insight
- Create demo mode
- Improve mobile responsiveness

DELIVERABLES (output in this exact format):

## REVISED INFORMATION ARCHITECTURE
Current: 7 tabs. Proposed structure (ASCII diagram):
- Should tabs stay? Consolidate? Reorder?
- Mobile nav structure (how does this look on 375px?)

## FIRST-RUN ONBOARDING FLOW
Design 4-step wizard:
1. User Segmentation: "I'm a Collector | Flipper | Dealer"
2. Add First Card: Guided search + cost input
3. First Insight: Show strongest performer + weakest position
4. Setup Alerts: Watchlist preference

For each step:
- Wireframe (ASCII or description)
- Copy (headline + helper text)
- Next action

## DEMO PORTFOLIO SPECIFICATION
Build a sample portfolio with 15 cards that showcases:
- Winners (3 cards with +50% to +300% gains)
- Losers (2 cards with -25% to -50% losses)
- Weak Confidence (2 cards with 50% or 30% confidence flagged REVIEW)
- Full range of signals (BUY, HOLD, SELL, REVIEW)
- Multiple scenarios enabled (show Bull +30% impact)

Provide CSV format:
Card Name | PSA Grade | Cost ฿ | Market Value ฿ | Signal | Confidence | Risk

## EMPTY-STATE FLOW DIAGRAM
Show: First-time user arrives → empty Dashboard → 3 paths:
- "Add my cards" → Add Card search
- "Try Demo" → Demo Portfolio loads
- "Learn more" → Help/FAQ

## MOBILE INFORMATION ARCHITECTURE
Propose responsive breakpoints:
- 375px (iPhone): [nav structure]
- 768px (iPad): [nav structure]
- 1024px (desktop): [nav structure]

For each: show tab order, hidden elements, expandable sections.

END OUTPUT
```

---

### Prompt 3: UI Design Agent

```
MISSION: Redesign Dashboard, signals, scenarios, and mobile layouts.

CONTEXT:
PSA × Collectr Tracer needs UX polish:
- Confidence logic (95%/50%/30%) is unexplained
- Scenarios (6 toggles) lack explanations
- Dashboard doesn't show positioning
- Mobile layout untested
- Signal badges need tooltips

DELIVERABLES (output in this exact format):

## DASHBOARD REDESIGN SPEC
Current Dashboard includes: KPI cards, Watch Card alert, confidence summary, 
P&L chart, Top 10 market chart, Cost vs Value chart, Signal Mix, Risk Mix.

Propose:
- Where does positioning tagline appear?
- How does "Try Demo" toggle integrate?
- Watchlist widget position + design
- Improved KPI card hierarchy (typography, spacing)
- Mobile-first layout (what's hidden on <768px?)

## SIGNAL BADGE TOOLTIP DESIGN
When user hovers on BUY/HOLD/SELL/REVIEW badge:
- Show 1-line explanation: "95% — Price sourced directly from Collectr"
- Or: "SELL — Market value below cost, downtrend"
- Design: modal tooltip, in-line note, or popover?

## CONFIDENCE SCORE REDESIGN
Current: 95%, 50%, 30% percentages.
Proposed: Visual confidence indicator (gauge, bar, or icon)
- Show breakdown: Data Freshness 95% | Source Reliability 90% | Market Depth 75%
- Include: Why is this card 95% vs 30%? (explain data quality gap)

## SCENARIO EXPLAINER UI
6 scenarios need explanations:
- Bull (+30%): Market optimism. All prices increase 30%.
- Bear (-25%): Market downturn. All prices decrease 25%.
- POP Dilution: Risk that more PSA population exists. Grade trend down.
- Grade Upgrade: What if this card graded PSA 9? Upside estimate.
- JPY/THB +10%: Currency strength benefits yen-denominated cards.
- JPY/THB -10%: Currency weakness hurts yen-denominated portfolio.

Design: Info icon → click → modal with 2–3 sentence explanation + visual impact

## MOBILE CARD LAYOUT MOCKUP
Current Portfolio table: 12 columns (unreadable on mobile).
Proposed: Expandable card layout:
```
┌─────────────────────┐
│ FULL ART/PIKACHU    │
│ PSA 10 • +289.6%    │
│                     │
│ Cost: ฿2,558        │
│ Market: ฿9,966      │
│ P&L: ฿7,408         │
│                     │
│ [BUY] [LOW RISK]    │
│ [Expand ▼]          │
└─────────────────────┘
```

When expanded: show Signal reason, Confidence breakdown, Data source.

## ALERT CENTER UI MOCKUP
Design:
- In-app toast (top-right): "SLOWPOKE recovered 10% today"
- Notification preferences: Daily | Weekly | Per Signal Change
- Email digest template (screenshot or HTML mock)

## SHARING/EXPORT BUTTON DESIGN
- "Share Portfolio" button → generates unique read-only snapshot URL
- "Export to CSV" button → downloads all columns
- Social share buttons (Twitter, email)

## COLOR & TYPOGRAPHY SPEC
Current (inferred from screenshots): Blue header, green/red for gains/losses.
Propose: Dark mode variant? Accessibility (WCAG AA contrast)?

END OUTPUT
```

---

### Prompt 4: Conversion & Retention Agent

```
MISSION: Design habit loops, alerts, watchlist, and growth mechanics.

CONTEXT:
PSA × Collectr Tracer has no retention mechanics: no alerts, no watchlist, 
no daily reason to return. Need to:
- Create daily check-in habit
- Notify users of portfolio changes
- Drive portfolio sharing
- Build growth flywheel

DELIVERABLES (output in this exact format):

## WATCHLIST FEATURE SPEC
Design:
- Users add up to 5 cards to watch
- Set alert thresholds: "Notify me if price drops 10%"
- Dashboard widget shows 5 watched cards + change % since last check
- Clicking card → shows price history sparkline + live Collectr link

Format:
- Feature name: Watchlist
- MVP scope: 5 cards per user, price-change alerts only
- Premium scope: unlimited cards, add custom thresholds (e.g., volatility alerts)
- Data model: user_id | card_id | alert_threshold | alert_type

## ALERT CENTER SPEC
In-app notifications:
- Card gained 10%+: "FULL ART/PIKACHU is up 10% 📈"
- Card lost 10%+: "SLOWPOKE is down 10% 📉"
- Signal changed: "SLOWPOKE signal changed from HOLD to SELL"
- Confidence updated: "MEW EX confidence improved to 95%"

Email notifications (daily/weekly digest):
- Wins: "You made ฿5,000 in gains this week"
- Losers: "2 cards are underwater; consider reevaluating"
- Market: "Top market performer: DETECTIVE PIKACHU +33%"
- Action: "3 cards are BUY signals"

Email template:
- Subject line examples
- Design mock (text or HTML)
- Unsubscribe link

## PORTFOLIO SHARING FEATURE SPEC
Button: "Share Portfolio"
→ Generates URL: psa-tracer.app/portfolios/abc123 (read-only snapshot)
→ Shows:
  - Portfolio NAV
  - Top 3 gainers
  - Top 3 losers
  - Signal distribution
  - Avg confidence
  - Date snapshot taken

Social share buttons: Copy Link | Email | Twitter ("Check out my Pokemon card portfolio on PSA Tracer")

TTL: Permanent (URL doesn't expire) or 24h?

## GROWTH METRICS & RETENTION KPIs
Define:
- Daily Active Users (DAU): users who log in + check portfolio
- Portfolio Engagement: users who add/remove cards weekly
- Alert Engagement: % of users with alerts enabled + click notification
- Retention Curve: % of users returning on Day 1, 7, 30
- Sharing: % of portfolios shared, click-through rate from shared links
- Referral: If applicable, # of referred users who join

Success targets (estimate for 6 months):
- DAU target: X% of registered users
- Alert adoption: Y% of users enable
- Sharing adoption: Z% of users share
- Monthly retention: 50%+

## FREEMIUM GUARDRAILS PROPOSAL
Free tier limits:
- Alerts: 2 watched cards + 1 daily email digest?
- Exports: Cannot export to CSV?
- API: No API access?
- Historical: Cannot see trends beyond 30 days?

Justify: Why these limits encourage upgrade without blocking core value?

## REFERRAL MECHANIC (Optional)
If applicable:
- "Invite friends to PSA Tracer"
- Referrer bonus: +1 free watched card slot? Or early access to new features?
- Referred user bonus: Same as referrer?
- Tracking: How to avoid abuse? (1 referral per email?)

END OUTPUT
```

---

### Prompt 5: Market Intelligence Agent

```
MISSION: Document price sourcing, confidence scoring, and data freshness logic.

CONTEXT:
PSA × Collectr Tracer aggregates prices from Collectr, PSA, and eBay.
Confidence scores (95%, 50%, 30%) are shown but unexplained.
Need to document:
- Price sourcing rules (which source wins?)
- Confidence calculation (why 95% vs 30%?)
- Data freshness (when were prices last updated?)
- Edge cases (what if price missing for 24h?)

DELIVERABLES (output in this exact format):

## PRICE SOURCING DECISION TREE
Document rules:

If Collectr has price for this card:
  → Use Collectr price (source = "Collectr", confidence = 95%)
  → Also fetch PSA price estimate (for comparison)
  → Also fetch eBay sold average (for triangulation)
Else If PSA has estimate:
  → Use PSA estimate (source = "PSA", confidence = 50%)
  → Mark as "Estimated — no recent sales"
Else If eBay has sold average:
  → Use eBay average (source = "eBay", confidence = 50%)
  → Mark as "Market average — may not reflect exact grade"
Else:
  → Mark as REVIEW (confidence = 30%)
  → Show "No market data found"
  → Suggest "Verify on Collectr" action

## CONFIDENCE SCORE CALCULATION MODEL
Formula (example):
```
Confidence = (DataFreshness × 0.4) + (SourceReliability × 0.4) + (MarketDepth × 0.2)

Where:
- DataFreshness: How recent is the price? (100% if <1h, 90% if <24h, 50% if >7d)
- SourceReliability: Which source? (Collectr = 100%, PSA = 80%, eBay = 70%)
- MarketDepth: How many sales/listings? (100% if >10, 80% if 5–10, 50% if <5)

Result: 95%+ = HIGH | 50–94% = MEDIUM | <50% = LOW
```

Provide actual formula + examples:
- FULL ART/PIKACHU (Collectr recent, 20+ listings): 95%
- MEW EX (PSA estimate only, 2 sales): 50%
- PIKACHU S-P PROMO (no Collectr data, <48h old): 30%

## DATA FRESHNESS TRANSPARENCY SPEC
Per-card timestamp display:
- Portfolio table: Add "Last Update" column (e.g., "2:10 PM" or "2 hours ago")
- Tooltip on timestamp: "Collectr last checked at 2:10 PM. Prior sync: 1:15 PM."
- Dashboard KPI: "All prices as of 2:10 PM ⏱ LIVE"

Sync strategy:
- Collectr: Refresh every 1h (or on-demand Refresh Data button)
- PSA: Refresh every 24h (slower-moving data)
- eBay: Refresh every 4h (sold listings update frequently)

## SIGNAL GENERATION LOGIC DIAGRAM
Show decision tree for BUY/HOLD/SELL/REVIEW:

```
For each card:
1. Check confidence:
   - If confidence < 50%: signal = REVIEW (insufficient data)
   
2. Check price vs cost:
   - If (market - cost) / cost > 20%: points += 2 (upside)
   - If (market - cost) / cost < -10%: points -= 2 (downside)
   
3. Check trend:
   - If 7d price trend up: points += 1
   - If 7d price trend down: points -= 1
   
4. Check market depth:
   - If <5 recent sales: points -= 1 (illiquid)
   
5. Assign signal:
   - If points >= 2: BUY
   - If points = 1: HOLD
   - If points = 0: HOLD
   - If points <= -1: SELL
   - If confidence < 50%: REVIEW (overrides above)
```

Document with examples (FULL ART/PIKACHU should be BUY; SLOWPOKE should be SELL).

## POP INTEGRATION ARCHITECTURE
Current: POP Dilution is a scenario toggle.
Proposed:
- Add POP column to Portfolio table (current POP rank, e.g., "1,240 exist")
- Fetch from PSA PopReport API (if available) or hardcode current POP
- Historical POP trend: Store POP snapshots weekly; show sparkline in Portfolio
- Scenario: Grade Upgrade accounts for POP (higher grade = fewer exist = rarer)

Data model:
```
card_id | current_pop | pop_grade | pop_updated_at | pop_7d_ago | pop_30d_ago
```

## EDGE CASE HANDLING SPEC
What if price missing for 24h?
- Show last known price (stale) with "Data unavailable" flag
- Or: Omit card from Top 10 chart until price available?
- Or: Mark REVIEW signal until price available?

Recommend: Show stale price + orange warning "Price last updated 2 days ago"

What if Collectr API down?
- Fallback to PSA estimate
- Show badge "Estimated (Collectr unavailable)"
- Reduce confidence to 50%

What if price has wild swing (e.g., eBay sold one copy at 50% above market)?
- Flag as outlier; use median of last 10 sales, not last 1 sale
- Show in Exceptions: "PIKACHU has 1 outlier sale; using market median"

## RECONCILIATION & VALIDATION SPEC
How to ensure Portfolio P&L matches Dashboard totals?
- Dashboard: Sum(market_value - cost) = Unrealized P&L
- Verify in every refresh cycle
- If mismatch: log error, alert monitoring

How to validate scenario math?
- User enables Bull +30%
- For each card: scenario_market_value = market_value × 1.3
- Scenario P&L = scenario_market_value - cost
- Sum all scenario P&L → should equal scenario_unrealized_pnl shown in results

END OUTPUT
```

---

### Prompt 6: Monetization Agent

```
MISSION: Define premium features, pricing tiers, and revenue model.

CONTEXT:
PSA × Collectr Tracer is currently free. Need to:
- Identify premium-worthy features
- Design pricing tiers (Free, Pro, Enterprise)
- Estimate willingness-to-pay
- Define freemium guardrails
- Project revenue

DELIVERABLES (output in this exact format):

## PREMIUM FEATURE RECOMMENDATION
Rank top 7 features by monetization potential:

1. Feature Name | Free Limit | Pro Limit | Why Premium | Est. Monthly Willingness-to-Pay
2. Alerts & Notifications | 2 watched cards | Unlimited | Key retention driver; users pay for habit-building | $9.99
3. Portfolio Sharing & Snapshots | Limited TTL (7d) | Permanent + custom URLs | Pros want persistent links for advisors | $9.99
4. Historical Trends | Last 30 days | Last 365 days | Professionals analyze seasonality | $14.99
5. Advanced Scenarios | 2 toggles | All 6 + custom | Traders need more analysis | $14.99
6. API Access | None | Limited (100 calls/day) | Automation + integrations | $29.99 (Enterprise)
7. CSV Export | Limited | Unlimited + scheduled exports | Tax planning, recordkeeping | $9.99
8. POP Analysis & Tracking | None | Full | Graders/dealers need population data | $14.99

(Provide justification for each)

## PRICING TIER STRUCTURE

**FREE**
- Portfolio size: Up to 20 cards
- Alerts: 2 watched cards
- Email digest: Not available
- Scenarios: 2 (Bull, Bear) only
- Export: Cannot export CSV
- Historical: 30 days only
- API: None
- Price: $0/month

**PRO ($9.99/month or $99/year)**
- Portfolio size: Up to 100 cards
- Alerts: Unlimited watched cards + custom thresholds
- Email digest: Daily or weekly
- Scenarios: All 6 scenarios + custom macro assumptions
- Export: CSV + PDF snapshot export
- Historical: 365 days + trends
- API: Limited (100 API calls/day)
- Price: $9.99/month ($119.88/year) or $99/year (save 17%)

**ENTERPRISE (Custom)**
- Portfolio size: Unlimited
- Alerts: Unlimited + webhooks
- Email digest: Custom reports
- Scenarios: All + White-label forecasting
- Export: Unlimited + scheduled exports
- Historical: Unlimited
- API: Unlimited API calls + webhook integrations
- Data: Shared portfolio access for teams
- Support: Priority email + monthly strategy call
- Price: $299/month + ($2,999/year) minimum commitment

(Justify why each feature is premium)

## PRICING JUSTIFICATION FAQ
Write 5–7 FAQs:
- "Why is historical data premium?"
- "Why do I need alerts? Can't I just check the dashboard?"
- "Can I export my portfolio on free tier?"
- "What's the difference between Pro and Enterprise?"
- "Can I downgrade mid-month?"

## ANNUAL VS. MONTHLY PACKAGING
Recommend:
- Monthly: $9.99/month (churn-friendly, lower barrier)
- Annual: $99/year (17% discount) (reduces churn, improves LTV)
- Enterprise: Annual minimum ($2,999/year)

Justification: Annual customers have 3x lower churn.

## REVENUE MODEL PROJECTION (12-month estimate)
Assumptions:
- 1,000 registered users by Month 6
- 2,500 registered users by Month 12
- Free-to-paid conversion: 5% of free users
- Monthly churn: 10% (Pro), 5% (Enterprise)
- ARPU: ($9.99 × # Pro users) + (Enterprise contracts)

Rough forecast:
```
Month 1: $0 (launch, free only)
Month 2: $250 (25 Pro users × $9.99)
Month 3: $500 (50 Pro users)
...
Month 12: $5,000+ (150 Pro + 1 Enterprise @ $2,999/year ÷ 12)

12-month revenue estimate: $25,000–$50,000 (conservative)
Upside case (10% conversion, lower churn): $75,000+
```

## FREEMIUM GUARDRAILS STRATEGY
How to prevent free users from getting unlimited value without paying?

Propose:
- Portfolio size cap (20 cards) — forces upgrade when collection grows
- Alerts cap (2 watched) — drives habit but limits upside
- Historical data (30d) — sufficient to see trends but not long-term patterns
- No CSV export — free users can't auto-sync to tax software
- No API — free users can't build custom integrations

Rationale: All are features a **serious** Pokemon card investor (target user) would want → drives conversion without blocking casual users.

## GO-TO-MARKET MESSAGING (Pricing-focused)
Write positioning for each tier:
- **Free:** "Start tracking your Pokemon card portfolio. No credit card needed."
- **Pro:** "Smart alerts, historical trends, and portfolio sharing. For serious investors."
- **Enterprise:** "White-label solutions, API access, and custom reports. For dealers and institutions."

## IMPLEMENTATION ROADMAP
Phase 1 (Month 1): Launch free tier, monitor usage
Phase 2 (Month 2): Announce Pro tier, gate alerts + export
Phase 3 (Month 4): Enterprise sales (direct outreach to dealers)
Phase 4 (Month 6): Optional — Annual subscription discount

## RETENTION & PRICING RISKS
List 3 risks + mitigation:
1. **Risk:** Free users see value is low → don't upgrade
   Mitigation: In-app prompts ("Upgrade to get alerts") after key moments
   
2. **Risk:** Pro pricing too high ($9.99/month)
   Mitigation: A/B test $7.99 vs $9.99; survey users on willingness-to-pay
   
3. **Risk:** Enterprise churn (large customers leave)
   Mitigation: Dedicated account manager, quarterly business review

END OUTPUT
```

---

### Prompt 7: Frontend Engineer Agent

```
MISSION: Propose component architecture, state management, and performance.

CONTEXT:
PSA × Collectr Tracer is a React app with:
- Dashboard (KPI cards, charts, watch alert)
- Portfolio (12-column table)
- Add Card (search + intake)
- Insights (4 analytical cards)
- Exceptions (data quality alerts)
- P&L Performance (scenario simulations)

Need to:
- Audit component reusability
- Recommend state management
- Optimize data fetching
- Design empty/loading/error states
- Ensure mobile responsiveness

DELIVERABLES (output in this exact format):

## COMPONENT ARCHITECTURE AUDIT & REFACTORING

Current components (inferred):
- Dashboard.tsx
- Portfolio.tsx
- AddCard.tsx
- Insights.tsx
- Exceptions.tsx
- PAndLPerformance.tsx

Proposed reusable components:
- SignalBadge.tsx (BUY/HOLD/SELL/REVIEW badge with tooltip)
- ConfidenceIndicator.tsx (95%/50%/30% visual)
- RiskBadge.tsx (LOW/MEDIUM/HIGH)
- KPICard.tsx (metric + value + trend)
- DataTable.tsx (generic sortable/filterable table with pagination)
- ChartCard.tsx (recharts wrapper with title + loading state)
- PortfolioCard.tsx (mobile-friendly card layout)
- AlertCard.tsx (watch alert or exception banner)

Extract these from page-level components to encourage reuse.

## STATE MANAGEMENT RECOMMENDATION
Current (inferred): Likely React Context or basic useState.
Proposed: [Redux | Zustand | Jotai]?

Recommendation:
- Global state: portfolio (cards, totals), scenarios (Bull/Bear toggles), auth
- Local state: form inputs, table sort/filter, collapsed sections
- Data fetching: useQuery or RTK Query for server state

Example with Zustand:
```
const portfolioStore = create((set) => ({
  cards: [],
  pnl: 0,
  confidence: 0,
  setCards: (cards) => set({ cards }),
  addCard: (card) => set((state) => ({ cards: [...state.cards, card] })),
}))
```

Benefits: Less boilerplate than Redux; cleaner than Context for large apps.

## DATA-FETCH STRATEGY
Current: How are prices refreshed? On-demand "Refresh Data" button?
Proposed:

- **Background polling:** Every 1h, fetch Collectr prices (passive)
- **On-demand refresh:** "Refresh Data" button triggers immediate fetch
- **Real-time (optional):** WebSocket to Collectr for live price updates (premium feature)
- **Caching:** Store prices locally; only fetch if stale (>1h)
- **Error handling:** If API fails, show last cached price + warning

Fetch timing:
- Collectr: Every 1h (or on-demand)
- PSA: Every 24h (slower-moving)
- eBay: Every 4h

## EMPTY/LOADING/ERROR STATES (Per Page)

**Dashboard (empty state):**
```
❌ No cards added yet
[Button: Add my first card]
or
[Button: Try demo portfolio]
```

**Portfolio (loading state):**
```
⏳ Fetching latest prices...
[Shows skeleton table rows]
```

**Portfolio (error state):**
```
⚠️ Failed to load portfolio
Reason: "Connection timeout"
[Retry] [View cached data]
```

Create spec for all 7 pages. Ensure no crashes on empty state.

## PERFORMANCE OPTIMIZATION ROADMAP

1. **Lazy load charts:** Portfolio table is faster if charts load after
2. **Virtualize table:** If 100+ cards, only render visible rows (react-window)
3. **Code splitting:** Load Insights only when tab clicked
4. **Bundle optimization:** Tree-shake unused recharts plugins
5. **Image optimization:** Portfolio card images should be optimized/WebP
6. **Memoization:** Wrap scenario calculations in useMemo to avoid re-renders on every keystroke

Performance targets:
- Dashboard loads in <2s
- Portfolio table scrolls smoothly with 100 cards
- Scenario toggle applies visually within 500ms

## MOBILE BREAKPOINT SPEC

**375px (iPhone SE / small phone)**
- Single-column layout
- KPI cards stack vertically
- Table becomes card layout (expandable rows)
- Charts: reduce font size, hide legend
- Nav: Hamburger menu or bottom tab bar

**768px (iPad)**
- 2-column grid for KPI cards
- Table: 8 columns visible (hide Source, Risk initially)
- Charts: full width
- Nav: Side nav or top tabs

**1024px (desktop)**
- 3–4 column grid for KPI cards
- Table: all 12 columns visible
- Charts: side-by-side
- Nav: Full top navigation

## RESPONSIVE DESIGN IMPLEMENTATION GUIDE

- **CSS Framework:** Tailwind? Bootstrap? CSS Grid?
- **Media query approach:** Mobile-first (base styles for 375px, then add breakpoints)
- **Font sizing:** 14px base on mobile, 16px on desktop (rem units)
- **Spacing:** 8px grid system (consistent padding/margin)
- **Touch targets:** Buttons ≥44px × 44px on mobile
- **Flexbox strategy:** Prefer flexbox for rows, CSS Grid for complex layouts

## SCENARIO LOGIC TESTING STRATEGY

Unit tests for each scenario:
```
test('Bull +30% multiplies all card prices', () => {
  const card = { cost: 1000, marketValue: 1500 };
  const result = applyScenario(card, 'BULL');
  expect(result.marketValue).toBe(1500 * 1.3);
  expect(result.pnl).toBe(result.marketValue - card.cost);
});

test('POP Dilution reduces confidence', () => {
  const card = { confidence: 95 };
  const result = applyScenario(card, 'POP_DILUTION');
  expect(result.confidence).toBeLessThan(95);
});
```

(Provide test matrix for all 6 scenarios)

## ACCESSIBILITY (WCAG 2.1 AA)

- Color contrast: 4.5:1 for text
- Keyboard nav: All interactive elements tabbable
- ARIA labels: Signal badges, confidence indicators
- Screen reader: Table headers marked with <th>, links have descriptive text
- Mobile: Touch targets ≥44px

## TECH STACK RECOMMENDATION

- Frontend: React 18+
- State: Zustand
- Data fetching: TanStack Query (react-query)
- Charts: Recharts or Chart.js
- Styling: Tailwind CSS
- Form: React Hook Form
- Testing: Jest + React Testing Library
- Mobile: Responsive CSS (no separate native app needed initially)

END OUTPUT
```

---

### Prompt 8: QA / Edge Cases Agent

```
MISSION: Test all features, validate data, identify bugs and edge cases.

CONTEXT:
PSA × Collectr Tracer is ready for QA after Design + Frontend engineering.
Need to validate:
- All empty/loading/error states work
- Portfolio P&L matches Dashboard totals
- Scenarios apply correctly
- Confidence scores are auditable
- Mobile responsiveness
- Data reconciliation

DELIVERABLES (output in this exact format):

## EDGE CASE BUG LOG

Test each scenario and report bugs:

**Test: Empty Portfolio**
- Steps: 1. Open app as new user. 2. View Dashboard.
- Expected: Empty state shows "Add your first card" CTA, no crashes
- Actual: [What actually happened?]
- Severity: [CRITICAL | HIGH | MEDIUM | LOW]
- Reproduction: [How to reproduce]

**Test: Missing Price Data**
- Steps: 1. Load portfolio with card that has no Collectr price. 2. View Portfolio table.
- Expected: Card shows REVIEW signal, "No data" in Market Value column, no NaN errors
- Actual: [?]
- Severity: [?]

**Test: Scenario Math**
- Steps: 1. Enable Bull +30%. 2. Check P&L results table. 3. Manually verify one card: P&L should be (market × 1.3) - cost
- Expected: All 20 cards' P&L = (market × 1.3) - cost. Sum matches "Scenario P&L" total.
- Actual: [?]
- Severity: [?]

**Test: Confidence Score Accuracy**
- Steps: 1. View Portfolio. 2. Find card with 95% confidence. 3. Check why (should be Collectr source, recent price, >10 listings). 4. Find card with 30% confidence. 5. Check why (should be insufficient data or stale price).
- Expected: Confidence rationale matches documented logic
- Actual: [?]
- Severity: [?]

(Provide 15–20 edge case tests covering empty states, errors, data mismatches, mobile, scenarios, and reconciliation)

## DATA RECONCILIATION REPORT

**Verify Portfolio ↔ Dashboard Totals:**
- Sum all card P&L values from Portfolio table
- Compare to "Unrealized P&L" shown on Dashboard
- Must match exactly (to ฿)

**Verify Top 10 Chart ↔ Portfolio Rankings:**
- Top 10 chart shows "FULL ART/PIKACHU" at #1 with +225.9%
- Portfolio table shows FULL ART/PIKACHU at rank [?] with P&L % [?]
- Confirm: Rankings match, percentages match

**Verify Signal Distribution:**
- Portfolio shows 8 BUY, 4 HOLD, 2 SELL, 4 REVIEW
- Dashboard "Signal Mix" donut shows same counts
- Must match exactly

(Provide reconciliation checklist for all Dashboard ↔ Portfolio ↔ Insights pairs)

## SCENARIO VALIDATION MATRIX

Test all 6 scenarios individually and in combination:

| Scenario | Expected Behavior | Test Result | Notes |
|----------|---|---|---|
| Bull +30% | All market values × 1.3; P&L recalculated | ✓ or ✗ | [e.g., "Card 5 incorrect"] |
| Bear -25% | All market values × 0.75 | ✓ or ✗ | |
| POP Dilution | Confidence ↓ 10–20%; Signal may change | ✓ or ✗ | |
| Grade Upgrade | Market value estimates ↑ 10–20% | ✓ or ✗ | |
| JPY/THB +10% | Only Japanese cards affected; ฿ prices ↑ 10% | ✓ or ✗ | |
| JPY/THB -10% | Only Japanese cards affected; ฿ prices ↓ 10% | ✓ or ✗ | |
| Bull + Grade Upgrade | Both effects apply; DP changes compound | ✓ or ✗ | |

(Test all 15 combinations: 6 single + 9 pairs)

## MOBILE RESPONSIVENESS CHECKLIST

Test on 375px, 768px, 1024px viewports:

- [ ] Dashboard KPI cards stack vertically on 375px, 2-column on 768px
- [ ] Portfolio table becomes card layout on 375px (expandable rows)
- [ ] Portfolio cards are clickable/tappable (44px minimum height)
- [ ] Charts render correctly on mobile (no overlapping text, readable axis labels)
- [ ] Add Card search input is full-width and tappable
- [ ] Scenario toggles are touch-friendly (no small click targets)
- [ ] Navigation is accessible (hamburger menu or bottom tabs on <768px)
- [ ] No horizontal scroll needed to see critical info

(Provide detailed mobile test matrix)

## CONFIDENCE SCORE AUDIT

For each card, verify confidence calculation:

Card: FULL ART/PIKACHU
- Source: Collectr
- Data freshness: Updated 2:10 PM (within 1h) → 100%
- Source reliability: Collectr → 100%
- Market depth: 20+ listings → 100%
- **Calculated confidence:** (1.0 × 0.4) + (1.0 × 0.4) + (1.0 × 0.2) = 1.0 = 100%?
- **Displayed confidence:** 95%
- **Match?** ✓ or ✗

(Audit 5–10 cards covering 95%, 50%, 30% confidence levels)

## SIGNAL LOGIC VALIDATION

For each card, verify signal assignment:

Card: SLOWPOKE
- Confidence: 95% (use for signal)
- Price vs cost: (-47.8%) → points = -2 (downside)
- 7d trend: ? (down) → points -= 1
- Market depth: ? (few sales) → points -= 1
- **Total points:** -4
- **Expected signal:** SELL (points <= -1)
- **Displayed signal:** SELL
- **Match?** ✓

(Validate 10 cards: 3 BUY, 3 SELL, 3 HOLD, 1 REVIEW)

## ACCESSIBILITY TESTING (WCAG 2.1 AA)

- [ ] Color contrast (text): Measure with accessibility checker (target 4.5:1)
  - Green "BUY" badge: contrast OK? ✓
  - Red "SELL" badge: contrast OK? ✓
  - Blue "HOLD" badge: contrast OK? ✓

- [ ] Keyboard navigation: Can user navigate entire Dashboard using Tab + Enter only?
  - [Tab] Move to KPI cards
  - [Tab] Move to signal badges
  - [Tab] Move to chart controls
  - [Enter] Expand/collapse cards

- [ ] ARIA labels: Are all interactive elements labeled?
  - <button aria-label="Refresh portfolio">Refresh Data</button>
  - <span role="img" aria-label="Portfolio down 25%">📉</span>

- [ ] Screen reader: Test with NVDA/JAWS
  - Announce KPI card: "Cards: 20, PSA graded"
  - Announce signal badge: "BUY signal: 95% confidence"
  - Announce table: <th> headers announced for each column

## PERFORMANCE TESTING

- Dashboard page load: <2s (measure with Lighthouse)
- Portfolio table scroll: Smooth 60fps with 100 cards (measure frame drops)
- Scenario toggle: Visual update within 500ms
- Add Card search: Results appear within 300ms of typing

(Use DevTools Performance tab; provide metrics)

## SECURITY CHECKLIST

- [ ] No API keys in frontend code (check for hardcoded Collectr/PSA credentials)
- [ ] No XSS vulnerabilities (test: enter `<script>alert('xss')</script>` in search)
- [ ] No CSRF tokens missing (if form submission implemented)
- [ ] Sensitive data not in localStorage (check user auth tokens)
- [ ] API requests use HTTPS (no unencrypted requests)

## REGRESSION TEST SUITE (Recommend)

After each build, run:
1. Dashboard loads without errors
2. Portfolio P&L ↔ Dashboard total match
3. All 6 scenarios apply correctly
4. Top 10 chart ↔ Portfolio rankings match
5. Add Card search returns correct results
6. Mobile layout renders on 375px without horizontal scroll

## PRIORITY BUG FIX LIST

List all bugs found, sorted by severity:
1. [CRITICAL] Dashboard crashes on empty portfolio → FIX BEFORE LAUNCH
2. [HIGH] Scenario results table doesn't update → FIX BEFORE LAUNCH
3. [HIGH] Mobile: Portfolio table horizontally scrolls → FIX IN FIRST SPRINT
4. [MEDIUM] Confidence tooltip misspelled → FIX IN FIRST PATCH
5. [LOW] Chart legend is slightly misaligned on dark mode → FIX IN POLISH SPRINT

END OUTPUT
```

---

## Summary: How to Execute This Plan

1. **Wave 1 (Days 1–3):** Run Agent 1 (Product Strategist) + Agent 2 (UX Research) in parallel
2. **Wave 2 (Days 3–5):** Run Agent 5 (Market Intelligence) + Agent 6 (Monetization) in parallel
3. **Wave 3 (Days 5–15):** Run Agent 3 (UI Design) + Agent 7 (Frontend) + Agent 4 (Conversion) in parallel
4. **Wave 4 (Days 15–21):** Run Agent 8 (QA) after Wave 3 completes

**Total time: 21 days (3 weeks)**

**Deliverables collected at each milestone:**
- **Milestone 1 (Day 5):** Positioning, personas, IA, onboarding flow
- **Milestone 2 (Day 10):** Price logic, confidence model, monetization tiers
- **Milestone 3 (Day 15):** UI mockups, frontend architecture, growth mechanics
- **Milestone 4 (Day 21):** QA report, bug log, ready for sprint planning

---

## END OF PHASES 5–6
