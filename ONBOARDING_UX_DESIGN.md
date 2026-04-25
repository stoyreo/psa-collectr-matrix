# PSA × Collectr Tracer: Onboarding & UX Design Specification

**Date:** April 21, 2026  
**Project:** Pokemon Card Portfolio Tracker Redesign  
**Audience:** New collectors, flippers, dealers  
**Goal:** Reduce time-to-first-insight from signup to meaningful portfolio view (target: <5 min)

---

## 1. REVISED INFORMATION ARCHITECTURE

### Current State Analysis
```
Tab Structure (7 tabs):
├── Dashboard      [Overview - landing page, empty state]
├── Portfolio      [Card inventory view]
├── Add Card       [Input form - action, not browsing]
├── Collectr       [API sync status - backend concern]
├── Insights       [Analytics + trends]
├── Exceptions     [Alerts + review flags]
└── P&L Performance [Financial summary]
```

**Problem:** "Add Card" as a tab is unusual (it's an action, not a destination). "Collectr" is backend-focused (users don't need to see this). Empty Dashboard creates initial friction.

---

### Proposed Information Architecture

#### Desktop (1024px+)
```
┌─────────────────────────────────────────────────────────────┐
│  Logo  │ Dashboard │ Portfolio │ Insights │ P&L │ Settings  │
│        │           │           │          │     │ (⚙️)      │
└─────────────────────────────────────────────────────────────┘
         Primary Navigation (6 tabs)
         
Content Area:
├─ Dashboard: Overview + Quick Actions
├─ Portfolio: Card grid/list + Add Card inline (FAB button)
├─ Insights: Trends, winners/losers, confidence scores
├─ P&L: Financial performance + scenario builder
├─ Settings: Collectr sync, alerts, user preferences
```

**Key Changes:**
1. **Remove "Add Card" as tab** → Floating Action Button (FAB) or inline within Portfolio
2. **Consolidate "Exceptions" into "Insights"** → "Exceptions" becomes a filter/tab within Insights
3. **Move "Collectr"** → Settings > Data Sync
4. **Rename "Dashboard"** → Keep name, but redesign as onboarding landing + quick stats
5. **Add "Settings"** → Unified preferences, sync status, alert configuration

#### Tab Ordering (Priority)
```
Left-to-right priority:
1. Dashboard    [Entry point, overview]
2. Portfolio    [Core action - where users spend time]
3. Insights     [Value prop - why users return]
4. P&L          [Financial summary - secondary]
5. Settings     [Configuration - low frequency]
```

---

## 2. FIRST-RUN ONBOARDING FLOW

### 4-Step Wizard: "Welcome to Your Card Collection"

**Entry Trigger:** First app load with empty portfolio  
**Duration:** 2-3 minutes  
**Exit:** Redirect to Dashboard with demo portfolio OR empty portfolio (user choice)

---

### Step 1: User Segmentation
**Headline:** "What's your collecting style?"  
**Subheading:** "We'll customize insights for your strategy."

```
Segmentation Options:
┌──────────────────────────────────────────┐
│ 🎮 COLLECTOR                             │
│ Build long-term collection. Track rarity │
│ & condition. Minimize sales.             │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ 💰 FLIPPER                               │
│ Buy low, sell quickly. Track ROI &       │
│ timing. Active trading.                  │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ 🏪 DEALER                                │
│ Bulk inventory & operations. Track       │
│ margin, volume, inventory age.           │
└──────────────────────────────────────────┘
```

**Why:** Tailor dashboard KPIs, sorting defaults, and alert thresholds.  
**Copy for each:**
- **Collector:** "Signal priority: HOLD (appreciation), REVIEW (condition risk)"
- **Flipper:** "Signal priority: SELL (peak value), BUY (entry opportunity)"
- **Dealer:** "Signal priority: Move inventory, margin >25%, age <90 days"

**Next Action:** "Next: Add Your First Card"

---

### Step 2: Add First Card (Guided Search)

**Headline:** "Find and add your first card"  
**Subheading:** "Search PSA TCGPlayer, enter cost basis."

```
Card Search Form:
┌─────────────────────────────────┐
│ Card Name/PSA #                 │
│ [Search input] 🔍               │
│ (e.g., "Charizard-Holo" or      │
│  "25102155" for PSA ID)         │
└─────────────────────────────────┘

Results Preview:
┌─────────────────────────────────┐
│ Charizard Holo Base Set PSA 9   │
│ Last Market: ฿45,000            │
│ [Select]                        │
└─────────────────────────────────┘

Cost Basis Input:
┌─────────────────────────────────┐
│ What did you pay? (฿)           │
│ [Input field: ฿28,500]          │
│                                 │
│ Optional: Acquisition date      │
│ [Date picker: March 2024]       │
└─────────────────────────────────┘
```

**Helper Text:**  
- "Can't find your card? Search PSA number or add manually."
- "Cost basis helps us calculate your gain/loss."

**Data Captured:**
- `card_name`, `psa_grade`, `psa_id`
- `cost_basis_thb`, `acquisition_date`
- `user_segment` (from Step 1)

**Next Action:** "View Your Insight"

---

### Step 3: First Insight (Value Proposition)

**Headline:** "Here's what we see in your collection"

**Display (conditional on user segment):**

**If COLLECTOR:** 
```
┌─────────────────────────────────────────┐
│ Your Strongest Position                 │
│ Charizard Holo Base Set PSA 9           │
│ Cost: ฿28,500 → Market: ฿45,000        │
│ Gain: +₿16,500 (+58%) 📈               │
│                                         │
│ Signal: HOLD (appreciation trajectory) │
│ Confidence: 94%                         │
│ Why: Consistent 8-month uptrend         │
└─────────────────────────────────────────┘

Action: "View Full Insights" [Button]
```

**If FLIPPER:**
```
┌─────────────────────────────────────────┐
│ Next Sell Opportunity                   │
│ Charizard Holo Base Set PSA 9           │
│ Entry: ฿28,500 → Current: ฿45,000      │
│ Quick Profit: +₿16,500 (+58%)           │
│ Holding time: 6 months                  │
│                                         │
│ Signal: SELL (peak detected)            │
│ Confidence: 89%                         │
│ Suggested price: ฿44,500               │
└─────────────────────────────────────────┘

Action: "See Other Opportunities" [Button]
```

**If DEALER:**
```
┌─────────────────────────────────────────┐
│ Inventory Summary                       │
│ 1 card | ฿16,500 net gain              │
│ Avg Hold: 6 months | Margin: 58%       │
│                                         │
│ Action: Add more cards to build         │
│ your portfolio view and unlock          │
│ predictive insights.                    │
└─────────────────────────────────────────┘

Action: "Add More Cards" [Button]
```

**Why:** Show immediate value—don't just say "collection tracked," show insight.

**Next Action:** "Set Up Alerts (Optional)"

---

### Step 4: Setup Alerts (Engagement)

**Headline:** "Stay ahead of the market"  
**Subheading:** "How often should we alert you?"

```
Alert Preferences:
┌──────────────────────────────────────┐
│ ☑ Price drops >15% below cost basis  │
│ ☑ Recommended SELL signal            │
│ ☐ Weekly portfolio summary           │
│ ☐ Market milestone (e.g., new ATH)  │
└──────────────────────────────────────┘

Frequency:
┌──────────────────────────────────────┐
│ Email: Daily Digest / Weekly / Never │
│ [Dropdown: Daily Digest selected]    │
└──────────────────────────────────────┘

Channel:
┌──────────────────────────────────────┐
│ techcraftlab.bkk@gmail.com           │
│ [Verified]                           │
└──────────────────────────────────────┘
```

**Copy:**  
"Stay informed without noise—alerts only when your cards matter."

**Skip Option:** "Skip for now" [Link]

**Completion:**
```
✅ Setup Complete!
   You're ready to start tracking.
   
[Dashboard] [Add More Cards]
```

---

## 3. DEMO PORTFOLIO SPECIFICATION

### Purpose
- **Show value immediately** without requiring user to input 15+ cards
- **Demonstrate all signal types** (BUY, HOLD, SELL, REVIEW)
- **Show realistic scenarios** (winners, losers, weak confidence)
- **Enable Bull scenario** (+30% market impact for demo)

### 15-Card Demo Portfolio

#### CSV Format:
```csv
Card Name,PSA Grade,Cost (฿),Market Value (฿),Signal,Confidence (%),Risk Flag,Category,Notes
Charizard Base Set Holo,9,28500,45000,HOLD,94,None,Winner,+58% gain over 8mo
Mewtwo Shadowless 1st Edition,8,22000,35500,HOLD,91,None,Winner,+61% appreciation
Blastoise Base Set Holo,7,15000,22500,HOLD,87,None,Winner,+50% steady growth
Pikachu Illustrator Promo,10,8500,5200,SELL,78,None,Loser,-39% below entry (oversold)
Dragonite Holo Base Set,6,12000,9000,SELL,82,None,Loser,-25% market decline
Venusaur Base Set Holo,8,18000,17200,HOLD,45,REVIEW,"Weak Confidence","45% confidence—condition concerns"
Machamp 1st Edition Holo,7,11000,10700,HOLD,50,REVIEW,"Weak Confidence","Authentication flag on market"
Alakazam Base Set Holo,9,16500,24000,HOLD,92,None,Winner,+45% recent momentum
Nidoking Shadowless,8,9500,14200,BUY,88,None,Opportunity,"Undervalued, momentum building"
Vileplume Holo Fossil,6,5000,7200,BUY,85,None,Opportunity,"+44% upside in Bull scenario"
Raichu Base Set Holo,7,8500,10200,HOLD,79,None,Neutral,"+20% stable, low volatility"
Gengar Base Set Holo,8,13500,19800,HOLD,89,None,Winner,"+47% appreciation consistent"
Articuno Holo Base Set,6,7000,8900,HOLD,72,None,Neutral,"+27% modest growth"
Zapdos Holo Base Set,6,7200,9100,HOLD,71,None,Neutral,"+26% baseline tracking"
Moltres Holo Base Set,6,7100,8700,HOLD,68,None,Neutral,"+22% underperforming trio"
```

### Breakdown by Category

| Category | Count | Cards | Rationale |
|----------|-------|-------|-----------|
| **Winners** | 3 | Charizard, Mewtwo, Blastoise, Alakazam, Gengar | Show gains of +45% to +61% |
| **Losers** | 2 | Pikachu Illustrator, Dragonite | Show losses of -25% to -39% |
| **Weak Confidence** | 2 | Venusaur, Machamp | REVIEW flags; condition/auth risk |
| **Opportunities (BUY)** | 2 | Nidoking, Vileplume | Undervalued; show upside in scenarios |
| **Neutral (HOLD)** | 6 | Raichu, Articuno, Zapdos, Moltres, + 2 others | Stable, low volatility |

### Signal Distribution
- **HOLD:** 9 cards (60%) — most portfolios are mostly hold
- **SELL:** 2 cards (13%) — overvalued or declining
- **BUY:** 2 cards (13%) — opportunities
- **REVIEW:** 2 cards (13%) — flagged for attention

### Scenario: Bull Market (+30% Impact)
When user toggles "Bull Market" scenario, market values adjust:
```
Scenario Toggle: [Normal] [Bull Market +30%]

Example (Vileplume):
Normal:   ฿7,200 (44% gain)
Bull:     ฿9,360 (87% gain) ← Shows upside potential
```

Apply +30% to all market values in Bull scenario.

### Data Structure (JSON Alternative)
```json
{
  "demo_portfolio_id": "DEMO_001_COLLECTOR",
  "user_segment": "COLLECTOR",
  "cards": [
    {
      "card_id": "charizard_base_9",
      "name": "Charizard Base Set Holo",
      "psa_grade": 9,
      "psa_id": "25102155",
      "cost_basis_thb": 28500,
      "market_value_thb": 45000,
      "market_value_bull_thb": 58500,
      "acquisition_date": "2023-08-15",
      "signal": "HOLD",
      "confidence": 94,
      "risk_flags": [],
      "category": "Winner"
    }
    // ... additional 14 cards
  ],
  "portfolio_total": {
    "cost_basis": 158700,
    "market_value": 234700,
    "gain_thb": 76000,
    "gain_pct": 47.9,
    "confidence_avg": 80.5
  }
}
```

---

## 4. EMPTY-STATE FLOW DIAGRAM

### First-Time User Journey

```
┌─────────────────────┐
│  App Loads          │
│  (First Time)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────┐
│  EMPTY DASHBOARD LANDING        │
│  "Start Tracking Your Cards"    │
│                                 │
│  [👤] "I'm a Collector"         │
│  [💰] "Flipper" / [🏪] "Dealer" │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┬──────────┐
     │           │          │
     ▼           ▼          ▼
  [Path 1]   [Path 2]   [Path 3]
     │           │          │
     
PATH 1: "Add My Cards Now"
     │
     ▼
┌──────────────────────┐
│ 4-Step Onboarding    │
│ Wizard Starts        │
│ (See Section 2)      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Dashboard Populated  │
│ with First Card +    │
│ Insight             │
└──────────────────────┘

PATH 2: "Try Demo Portfolio"
     │
     ▼
┌──────────────────────┐
│ Load Demo Portfolio  │
│ (15 sample cards)    │
│ See all signals,     │
│ trends, P&L          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ [Import Demo]        │
│ or                   │
│ [Start Fresh]        │
└──────────────────────┘

PATH 3: "Learn More (FAQ/Help)"
     │
     ▼
┌──────────────────────┐
│ Help Center          │
│ - How signals work   │
│ - Confidence scoring │
│ - Adding cards       │
│ - Integrations       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Return to Empty      │
│ Dashboard or Start   │
│ Onboarding          │
└──────────────────────┘
```

### Landing Page Copy
```
Headline:
"Track Every Card, Every Gain"

Subheading:
"Real-time market data for your collection. 
Know exactly what you own and when to buy, hold, or sell."

Three Call-to-Actions:
1. ➕ "Add My Cards" → 4-step onboarding
2. 🎮 "Try Demo" → Load 15-card sample portfolio
3. ❓ "How It Works" → FAQ / guided tour
```

---

## 5. MOBILE INFORMATION ARCHITECTURE

### Breakpoint Strategy

#### **375px (Mobile / iPhone SE, 12, 13)**

**Navigation Pattern:** Bottom Tab Bar (iOS-native, thumb-friendly)

```
┌──────────────────────┐
│ [Title] [Settings⚙] │  ← Header
├──────────────────────┤
│                      │
│   Main Content       │
│   (Scrollable)       │
│                      │
├──────────────────────┤
│ 🏠 📊 ➕ 💹 ⚙      │  ← Bottom Nav (5 icons)
│ DA   IN    P&L SET    │
└──────────────────────┘

Tabs (Left-to-Right):
1. 🏠 Dashboard     [Primary]
2. 📊 Portfolio     [Core action]
3. ➕ Add Card      [FAB as tab for mobile]
4. 💹 Insights      [Analytics]
5. ⚙ Settings      [Consolidated]

Hidden/Collapsed:
- P&L moved to Insights > P&L tab
- Reduces 7 tabs → 5 mobile tabs
- Swipe navigation available
```

**Header:**
- Title of current section
- Settings icon (⚙) as secondary action

**Card List (Mobile):**
```
┌─────────────────────┐
│ Charizard Base 9    │  ← Card name
│ ฿45,000 | +58%  📈 │  ← Value + trend
│ HOLD | 94% ✓        │  ← Signal + confidence
└─────────────────────┘
[Swipe for options] or [Long-press menu]
```

**Dashboard (Mobile):**
```
┌──────────────────────┐
│ Portfolio Summary    │
│ 15 Cards Tracked    │
│ ฿234.7K value      │
│ +47.9% all-time    │
│                      │
│ [Quick Stats Bars]   │
│ HOLD: 9  SELL: 2   │
│ BUY: 2   REVIEW: 2 │
│                      │
│ [↓ Scroll for list]  │
└──────────────────────┘
```

**Advantages:**
- Bottom nav ≈ 8mm thumb reach (iOS standard)
- Vertical scrolling optimized for small screens
- Floating Action Button (FAB) unnecessary—Add Card is a tab
- Minimal header chrome

---

#### **768px (Tablet / iPad Mini, iPad)**

**Navigation Pattern:** Side Drawer + Hamburger (hybrid)

```
┌────────────────────────────────────┐
│☰ PSA Tracer │ Dashboard          │
├──────────────┬────────────────────┤
│ 📊 Portfolio │                    │
│ 📈 Insights  │   Main Content     │
│ 💹 P&L       │   (2-column layout │
│ ⚙ Settings   │    available)      │
│              │                    │
└──────────────┴────────────────────┘
```

**Layout Optimization:**
- Drawer toggles with hamburger (☰) menu
- Main nav: Portfolio, Insights, P&L, Settings (4 tabs)
- "Add Card" accessible via floating FAB (bottom-right) or Portfolio inline
- Content area wide enough for side-by-side card view + detail panel

**Drawer Menu:**
```
[≡ Menu]
├─ Dashboard
├─ Portfolio (1,234 cards)
├─ Insights
│  ├─ Trends
│  ├─ Exceptions
│  └─ Scenarios
├─ P&L Performance
└─ Settings
   ├─ Data Sync
   ├─ Alerts
   └─ Profile
```

**Portfolio View (Tablet):**
```
┌──────────────────┬──────────────────┐
│ Card List        │ Card Detail      │
│ (Scrollable)     │ (Expanded view)  │
│                  │                  │
│ ☑ Charizard 9   │ Charizard        │
│ ☑ Mewtwo 8      │ Base Set Holo    │
│ ☑ Blastoise 7   │ PSA 9            │
│    (13 more)     │                  │
│                  │ Cost: ฿28.5K    │
│ [Apply Filters]  │ Market: ฿45K    │
│                  │ Gain: +58%       │
│                  │                  │
│                  │ [Edit] [More]    │
└──────────────────┴──────────────────┘
```

---

#### **1024px+ (Desktop)**

**Navigation Pattern:** Horizontal Top Nav (current architecture)

```
┌──────────────────────────────────────────────────────┐
│ Logo │ Dashboard │ Portfolio │ Insights │ P&L │ ⚙  │
├──────────────────────────────────────────────────────┤
│                                                      │
│              Main Content Area (Full Width)         │
│              [Cards Grid / Table / Charts]          │
│                                                      │
│              [Floating Add Card Button] ➕          │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Full-Width Optimizations:**
- 6-tab horizontal navigation (Dashboard, Portfolio, Insights, P&L, Settings)
- Floating Action Button (FAB) for Add Card at bottom-right
- Dashboard: 3-column layout (Quick Stats | Recent Activity | Market Alerts)
- Portfolio: Grid view (8–12 cards per row) with inline editing
- Insights: Multi-chart dashboard (trends, heatmap, correlation)
- P&L: Advanced scenario builder with Bull/Bear toggles

**Dashboard (Desktop):**
```
┌─────────────┬──────────────┬──────────────┐
│ Quick Stats │ Recent Cards │ Market Pulse │
├─────────────┼──────────────┼──────────────┤
│ 15 Cards    │ Charizard 9  │ +3.2% today  │
│ ฿234.7K     │ +58% (HOLD)  │ 🔴 Dragonite│
│ +47.9% Gain │              │ -4.1%       │
│             │ Mewtwo 8     │             │
│ Confidence: │ +61% (HOLD)  │ Top Movers: │
│ 80.5% Avg   │              │ [See chart] │
│             │ [More Cards] │             │
└─────────────┴──────────────┴──────────────┘

Below: [Grid of all 15 cards with inline actions]
```

---

### Responsive Breakpoint Summary Table

| Breakpoint | Device | Nav Pattern | Tab Count | Key Actions |
|------------|--------|-------------|-----------|-------------|
| **375px** | iPhone SE/12/13 | Bottom Bar | 5 tabs | Swipe nav, scroll-heavy |
| **768px** | iPad Mini / iPad | Side Drawer + Top | 4 main tabs | Drawer toggle, FAB, split view |
| **1024px+** | Desktop | Horizontal Top | 6 tabs | Full width, floating FAB |

---

### Mobile-First CSS Breakpoints (Pseudo-code)

```css
/* Mobile First (375px default) */
.nav { display: flex; flex-direction: column; position: fixed; bottom: 0; }
.content { padding-bottom: 60px; /* room for bottom nav */ }
.card-grid { display: grid; grid-template-columns: 1fr; }

/* Tablet (768px and up) */
@media (min-width: 768px) {
  .nav { flex-direction: row; position: fixed; left: 0; width: 200px; }
  .content { margin-left: 200px; padding-bottom: 0; }
  .card-grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop (1024px and up) */
@media (min-width: 1024px) {
  .nav { position: relative; width: auto; flex-direction: row; }
  .content { margin-left: 0; }
  .card-grid { grid-template-columns: repeat(4, 1fr); }
}
```

---

## 6. IMPLEMENTATION PRIORITIES

### Phase 1 (MVP - Weeks 1-2)
- [ ] Onboarding 4-step wizard (Steps 1-2)
- [ ] Empty-state landing page + 3 CTAs
- [ ] Demo portfolio CSV data
- [ ] Mobile bottom-nav (375px)

### Phase 2 (Week 3)
- [ ] Steps 3-4 of wizard (insights + alerts)
- [ ] Tablet drawer navigation (768px)
- [ ] Tab consolidation (remove Add Card tab, move to FAB)

### Phase 3 (Week 4+)
- [ ] P&L scenario builder with Bull/Bear toggles
- [ ] Advanced filtering in Portfolio
- [ ] Push notifications for alerts

---

## 7. SUCCESS METRICS

### Onboarding
- **Time-to-first-insight:** <5 minutes from signup
- **Wizard completion rate:** >80%
- **Demo portfolio conversion:** % who import demo → add real card within 7 days

### Engagement
- **Dashboard return rate:** 60%+ return within 7 days
- **Alert opt-in:** >70% enable alerts
- **Mobile adoption:** 40%+ of DAU on mobile

### Portfolio Growth
- **Avg cards per user (new):** 5+ by day 3, 15+ by day 30
- **Portfolio value diversity:** Avoid 80/20 concentration (top 2 cards = 40%+)

---

## 8. APPENDIX: Copy Guidelines

### Tone
- **Confident but not salesy:** "Know exactly what you own..."
- **Action-oriented:** Use imperatives—"Add your first card," "Try demo"
- **Respect expertise:** Collectors/flippers understand jargon (PSA, ROI, signal)

### Terminology
- **Signal:** BUY, HOLD, SELL, REVIEW (don't use "strong buy" or "weak hold")
- **Confidence:** Percentage (80%, 94%) not stars or emoji ratings
- **Market Value:** Always current, sourced from PSA/TCGPlayer
- **Gain:** Use ฿ (Thai Baht) and % for clarity—"₿16.5K (+58%)"

---

**Document Version:** 1.0  
**Last Updated:** April 21, 2026  
**Status:** Ready for Design Review
