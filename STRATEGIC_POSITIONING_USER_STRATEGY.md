# PSA × Collectr Tracer: Strategic Positioning & User Strategy

**Document Date:** April 21, 2026  
**Product Status:** Pre-launch, feature-complete prototype  
**Target Market:** Thailand/Southeast Asia (home market advantage) with global expansion potential

---

## POSITIONING STATEMENT

PSA × Collectr Tracer is the only multi-source portfolio intelligence platform built for Pokemon collectible cards, purpose-built for Thailand's emerging PSA-graded market. It aggregates real-time pricing from Collectr (the regional benchmark for Japanese imports), PSA market data, and eBay listings to give collectors, traders, and dealers complete portfolio visibility—with buy/sell/hold signals powered by confidence-scored pricing and risk-based scenario modeling.

Unlike spreadsheet-first tracking or general collectible apps, Tracer combines institutional-grade analytics (POP dilution modeling, currency exposure analysis, portfolio concentration metrics) with casual collector workflows, making it the bridge between hobbyists managing personal collections and professionals managing inventory.

For a market historically fragmented across WhatsApp groups, Discord channels, and Excel files, Tracer provides the single source of truth for card valuations and portfolio strategy.

---

## USER PERSONAS

### 1. COLLECTOR: The Passionate Hobbyist

**Profile:** Sai is a 28-year-old Bangkok-based Pokemon TCG collector who started with Japanese import cards in 2019. He owns 12–50 PSA-graded cards (Thai Baht 100K–500K total value) and buys 2–4 cards per month at local markets or via Collectr. He tracks his collection in a personal spreadsheet and follows prices on Collectr, occasionally checking eBay for comparable sales. Sai loves the hobby for nostalgia and the hunt for rare cards; profit is a secondary benefit. He attends local meetups and has a small Discord group of 8–10 collector friends.

**Goals:**
- Know the current market value of his collection in real-time
- Identify undervalued cards worth adding to the collection
- Spot which cards in his portfolio are appreciating fastest (bragging rights in the collector community)
- Understand trends (e.g., why Full Art Pikachu jumped 289% while Slowpoke tanked)
- Feel confident he's not overpaying for new acquisitions
- Share interesting P&L stories with his collector group

**Pain Points:**
- Manually updating spreadsheet with prices from Collectr (takes 30+ minutes weekly)
- Collectr website has no built-in portfolio tracking; requires manual comparison
- Can't easily see which of his cards are "winners" vs. "losers" without calculations
- No confidence scoring for pricing data (sometimes Collectr has no match, forcing eBay estimates)
- Currency confusion between Thai Baht, USD, and JPY when comparing prices across marketplaces
- Anxiety about individual card decisions ("Should I sell this Slowpoke before it drops more?")

**Decision-Making Style:**
- Emotion-driven (collection pride, FOMO on rare cards)
- Community-influenced (asks friends for second opinions before big buys)
- Data-naive (trusts but doesn't deeply analyze; wants simple visuals)
- Risk-averse (prefers low-risk "blue chip" cards like PSA 10 Pikachu)
- Long-term holder (rarely sells; buy-and-hold mentality)

**Willingness-to-Pay:**
- Free tier: Essential use case (viewing collection value, basic alerts)
- $3–5 USD/month (~100–150 THB): Willing if it saves >5 hours/month and adds confidence
- $10+/month: Unlikely unless offered institutional-grade features (which he doesn't need)
- Optimistic LTV: $3/month × 36 months (3 years) = $108 per customer

**Feature Priorities:**
1. Portfolio summary dashboard
2. Buy signal alerts (new opportunities)
3. Price trend sparklines
4. Confidence scoring on prices
5. Peer benchmarking (how does my collection compare to others?)

---

### 2. FLIPPER: The Active Trader

**Profile:** Niran is a 35-year-old semi-professional trader in Bangkok who manages a rotating portfolio of 30–150 PSA-graded cards worth 500K–2M THB. He buys 5–15 cards per week on Collectr and local markets, holds them for 2–8 weeks, then sells for 15–30% margins. He has deep market knowledge and tracks multiple spreadsheets: one for acquisition costs, one for current market value, one for target sell prices. Niran spends 2–3 hours daily on research and has a Telegram group of 20+ traders sharing leads. He's motivated by consistent returns, not the hobby itself.

**Goals:**
- Identify entry points: cards trading below their "true" market value
- Get early warnings when a card's signal changes from BUY to HOLD or SELL
- Optimize hold duration: know when to sell (maximum price window, market saturation)
- Minimize holding cost: understand concentration risk and capital efficiency
- Monitor inventory turnover ratio (velocity of sales)
- Hedge currency risk: model JPY/THB swings and their impact on margins
- Batch sell signals: identify which 10 cards to liquidate this week for cash flow

**Pain Points:**
- No buy/sell timing signals; relies entirely on manual analysis
- Price aggregation is slow: must check Collectr, PSA, eBay separately (30+ minutes per analysis session)
- Can't easily model "what if prices rise 20%" or "what if the Yen strengthens"; requires manual recalculation
- Confidence in pricing varies wildly by card (some have 1 Collectr match, others have none)
- Misses short windows: by the time he updates his spreadsheet, the buy opportunity is gone
- Currency exposure is invisible: doesn't know his true risk to JPY/THB fluctuations
- No batch operations: can't generate sell orders for 10 cards at once

**Decision-Making Style:**
- Data-driven (wants confidence scores, risk metrics, signal clarity)
- Speed-focused (needs near real-time alerts, not daily refreshes)
- Quantitative (understands P&L %, confidence intervals, scenario analysis)
- Margin-obsessed (will sell a card at 12% margin if capital efficiency improves)
- Risk-aware (models downside scenarios before acquiring)

**Willingness-to-Pay:**
- Free tier: Insufficient (no signals, no scenario modeling)
- $8–15 USD/month (~250–500 THB): Willing for real-time signals, confidence scoring, batch operations
- $25–50 USD/month: Willing for API access, bulk upload, advanced scenario modeling
- Optimistic LTV: $12/month × 60 months (5 years of active trading) = $720 per customer

**Feature Priorities:**
1. Real-time buy/sell signals with confidence scoring
2. Scenario modeling (Bull/Bear/Currency shifts)
3. Portfolio concentration metrics
4. Batch operations (add 10 cards, generate 10 sell orders)
5. Price trend alerts (notify when a card crosses a threshold)
6. Currency exposure dashboard
7. Turnover ratio tracking
8. API for spreadsheet integration

---

### 3. DEALER/INSTITUTION: The Professional Manager

**Profile:** Somchai runs a 15-year-old Pokemon card retail business in Chatuchak Market (Bangkok's famous collectibles district) with a showroom, online presence, and 2 part-time staff. His inventory fluctuates between 500–1,500 PSA-graded cards worth 5–15M THB. He buys in bulk from collectors, wholesalers, and Japanese importers, then sells to local retailers, international dealers, and tourists. Somchai operates on 20–30% margins and carries risk across hundreds of SKUs. He needs to optimize inventory turnover, manage cash flow, and comply with increasing regulations around collectibles as a high-value asset class in Thailand.

**Goals:**
- Real-time portfolio valuation for cash flow and loan collateral purposes
- Identify slow-moving inventory (deadstock risk)
- Spot arbitrage opportunities: buy at price X in Bangkok market, sell at price 1.2X to international dealer
- Model inventory risk: which 20% of SKUs drive 80% of portfolio value (concentration)
- Forecast demand: use historical sales velocity to predict which cards to stock more of
- Regulatory compliance: generate quarterly reports on inventory value for potential licensing/taxation
- Supplier optimization: understand which wholesale suppliers give best margins
- Staff accountability: track which team members' sales contribute most to margin

**Pain Points:**
- Inventory management is fragmented: Excel spreadsheets, written notes, photos in phone
- No real-time portfolio NAV; auditing requires manual counts
- Can't quickly answer "what's my current exposure to Pikachu cards?" across all grades
- Pricing is manual: checks Collectr daily but no automated sync to his system
- POP (Print on Demand) risk is invisible: doesn't know when new prints dilute his inventory value
- Currency exposure is blind spot: 40% of suppliers are Japanese, 30% are international
- Cash flow forecasting is reactive: reacts to shortfall, not proactive
- No scenario planning: can't model "what if international dealer demand drops 20%"

**Decision-Making Style:**
- Operationally focused (cares about throughput, inventory turns, cash flow)
- Risk-conservative (wants to minimize downside, understand what he owns)
- Compliance-aware (needs audit trails, reporting)
- Relationship-driven (focuses on supplier and customer relationships, less on data)
- Mid-to-long-term (holds inventory 2–8 months on average)

**Willingness-to-Pay:**
- Free tier: Unsuitable (lacks batch operations, reporting, integrations)
- Pro tier: Possibly useful (portfolio valuation, insights)
- Enterprise Custom: $100–500 USD/month (~3,500–17,500 THB) for custom integrations, API access, reporting, multi-user accounts
- Optimistic LTV: $150/month × 60 months = $9,000 per customer

**Feature Priorities:**
1. Multi-user accounts and role-based access (owner, manager, staff)
2. Real-time portfolio NAV and risk dashboards
3. Inventory turnover metrics (velocity, age of inventory)
4. POP dilution modeling and alerts
5. Batch import/export (CSV upload for 500 cards at once)
6. Custom reporting (quarterly inventory audits)
7. API access for inventory system integration
8. Scenario modeling for forecast planning
9. Supplier performance dashboards
10. Currency exposure management across multiple currencies

---

## FEATURE PRIORITY MATRIX

**Methodology:** Ranked by Impact Score = (User Impact × 1.5 + Retention Impact × 1.5 + Monetization Impact × 1.0), prioritizing high-impact items deliverable in 2–4 week sprints.

| Feature | Effort | User Impact | Retention | Monetization | Priority Score | Target Persona | Timeline |
|---------|--------|------------|-----------|--------------|----------------|-----------------|----------|
| **Tier 0: MVP Foundation** |
| Portfolio Dashboard (KPIs) | S | 5 | 5 | 2 | 17 | All | Week 1–2 |
| Multi-source Price Aggregation | S | 5 | 5 | 3 | 18 | All | Week 1–2 |
| Buy/Hold/Sell Signal Engine | M | 5 | 5 | 4 | 21 | Flipper | Week 2–4 |
| **Tier 1: Core Engagement** |
| Insights Dashboard (Top Gainers, Weak Positions) | M | 4 | 4 | 2 | 15 | All | Week 3–5 |
| Confidence Scoring on Prices | S | 4 | 3 | 3 | 14 | Collector, Flipper | Week 2–3 |
| Scenario Modeling (Bull/Bear/Currency) | M | 5 | 4 | 4 | 20 | Flipper, Dealer | Week 4–6 |
| Real-time Price Alerts | M | 4 | 4 | 3 | 16 | Flipper | Week 3–4 |
| **Tier 2: Premium Features** |
| Portfolio Concentration Risk Metrics | M | 4 | 3 | 3 | 15 | Flipper, Dealer | Week 5–6 |
| API Access for Data Export | L | 3 | 3 | 5 | 16 | Dealer | Week 7–10 |
| Multi-user Accounts & Role-Based Access | L | 4 | 4 | 5 | 18 | Dealer | Week 7–10 |
| Batch Operations (Add/Update/Delete 50+ Cards) | M | 4 | 3 | 4 | 17 | Flipper, Dealer | Week 5–7 |
| Custom Reporting & Audit Trails | L | 3 | 2 | 5 | 14 | Dealer | Week 8–12 |
| **Tier 3: Differentiators** |
| POP Dilution Alerts & Modeling | M | 4 | 3 | 4 | 16 | Flipper, Dealer | Week 6–8 |
| Currency Exposure Dashboard (JPY, USD, THB) | M | 4 | 3 | 4 | 16 | Flipper, Dealer | Week 6–8 |
| Inventory Turnover Metrics & Velocity Tracking | M | 3 | 3 | 4 | 14 | Dealer | Week 7–9 |
| Peer Benchmarking (Anonymous Collection Comparison) | M | 3 | 4 | 2 | 13 | Collector | Week 8–10 |
| Mobile App (iOS/Android) | L | 4 | 5 | 3 | 17 | All | Week 12–20 |
| **Tier 4: Growth & Retention** |
| Social Features (Share Wins, Compare Collections) | M | 3 | 4 | 1 | 11 | Collector | Week 10–12 |
| Advanced Grade Upgrade Forecasting | M | 3 | 2 | 3 | 11 | Collector | Week 9–11 |
| Educational Content (Market Trends, Grading 101) | S | 2 | 3 | 0 | 7 | Collector | Week 11–13 |
| Marketplace Integration (Automated Buy Leads) | L | 3 | 4 | 4 | 15 | Flipper, Dealer | Week 13–18 |

**Legend:**
- **Effort:** S (Small: 1–3 days), M (Medium: 1–2 weeks), L (Large: 3–6 weeks)
- **User Impact:** How much value the feature delivers (1=nice-to-have, 5=must-have)
- **Retention:** How much the feature improves retention (1=negligible, 5=highly sticky)
- **Monetization:** How much the feature enables premium pricing (1=free, 5=enterprise)
- **Priority Score:** Weighted formula above

---

## PRICING TIER PROPOSAL

### Strategic Rationale

Freemium Model is optimal because:

1. **Low barrier to adoption** in pre-launch phase: collectors won't pay to learn your tool
2. **Multi-segment monetization:** Collectors on free tier, flippers on Pro, dealers on Enterprise
3. **Network effects:** Free users create data (portfolios) that improve the platform for paid users
4. **Competitive positioning:** Only free tool with institutional analytics; upgrade as users scale

---

### FREE TIER: "Tracer Explorer"

**Positioning:** "Know your collection. Zero commitment."

**Price:** $0/month

**Limits:**
- Up to 20 cards per portfolio
- 1 portfolio only
- Daily price refresh (vs. real-time for Pro)
- Basic dashboard (NAV, P&L, top gainers/losers)
- No scenario modeling
- No API access
- No multi-user
- Community-supported (Discord, forum only; no email support)

**Included Features:**
- Portfolio management (add, edit, delete cards)
- Multi-source price aggregation (Collectr, PSA, eBay)
- Basic signals (BUY/HOLD/SELL) without confidence scoring
- Insights (top gainers, weak positions, high-risk cards)
- P&L summary
- Basic filtering & sorting
- Export to CSV (portfolio only)
- Mobile responsive (not native app)

**Monetization Strategy:**
- Converts 5–8% of free users to Pro within 6 months (typical SaaS freemium)
- Upsell trigger: when user tries to add card #21 or refreshes price data mid-day
- No ads (preserves trust with serious collectors)

---

### PRO TIER: "Tracer Trader"

**Positioning:** "Trade smarter. Real-time signals, confidence scoring, scenario modeling."

**Price:** $12 USD/month (~400 THB) | Annual: $120 (save 17%)

**Limits:**
- Up to 100 cards per portfolio
- Up to 3 portfolios (personal, watch list, past sales)
- Real-time price refresh (within 15 minutes of Collectr updates)
- Unlimited scenario modeling
- Email support (24–48 hour response)
- No API, no multi-user

**Included Features:**
- All Free tier features, plus:
- Confidence scoring on all prices (95%/50%/30% tiers)
- Buy/Hold/Sell signals with confidence percentage
- Risk scoring (LOW/MEDIUM/HIGH) by card
- Advanced insights (concentration metrics, signal mix, undervalued cards)
- Scenario modeling: Bull (+30%), Bear (−25%), POP Dilution, Grade Upgrade, JPY/THB ±10%
- Real-time price alerts (configurable thresholds)
- Currency exposure dashboard (JPY/USD/THB)
- Trend sparklines (30/90/365-day)
- Custom date ranges for P&L analysis
- Export to PDF (formatted reports)
- Advanced filtering (by grade, risk, signal, P&L %)
- Browser dark mode + mobile app priority (native iOS/Android roadmap)

**Target Users:**
- Active flippers (trading 5+ cards/month)
- Serious collectors (100+ card collection, $20K+ value)
- Niche dealers (100–300 card inventory)

**Monetization Strategy:**
- Higher margin than Enterprise (less customization cost)
- Expected conversion rate: 8–15% of free users
- Expected churn: 3–5% MoM (seasonal dips in trading = churn risk)
- Upsell path: show "Upgrade to Pro" dialog when user hits 21-card limit or tries real-time refresh
- Retention lever: scenario modeling and alerts are addictive once users experience them

---

### ENTERPRISE TIER: "Tracer Pro+"

**Positioning:** "Manage your portfolio like an institution. Custom pricing, multi-user, API, reporting."

**Price:** Custom ($100–500 USD/month depending on features) | Minimum annual: $1,200 USD (100 USD/month)

**Limits:**
- Unlimited cards, portfolios, users
- Real-time pricing (within 5 minutes)
- 99.5% uptime SLA
- Dedicated Slack/email support (4-hour response)
- API access with 10K requests/month
- Quarterly business review
- Custom feature roadmap input

**Included Features:**
- All Pro features, plus:
- Multi-user accounts with role-based access (Admin, Manager, Analyst, View-Only)
- Batch import/export (CSV, 1,000+ cards)
- Advanced reporting: quarterly inventory audits, P&L trends, supplier performance
- Inventory turnover metrics (velocity, age distribution, dead stock alerts)
- POP dilution alerts (notified when print production increases)
- Supplier integration: track cost per supplier, margin by supplier, repeat purchase patterns
- Advanced scenario modeling: custom scenarios (e.g., "what if 50% of inventory sells next month?")
- Cash flow forecasting: project liquidity based on historical turnover
- White-label option: custom branding, custom domain (e.g., inventory.somchai-cards.com)
- API: create cards, read portfolio data, list transactions, trigger alerts
- Webhooks: receive real-time updates when prices cross thresholds
- OAuth integration: single sign-on with customer systems
- Audit trails: track who changed what, when (for compliance)
- Custom reports: generate PDF/XLSX on-demand
- Data retention: 10 years (vs. 2 years for Pro)

**Target Users:**
- Professional dealers with 500+ SKU inventory
- Small wholesalers/distributors
- Multi-person operations (staff) needing shared access
- Collectors managing legal/tax implications of large portfolios (audit trails)

**Monetization Strategy:**
- High LTV: $150/month × 60 months = $9,000 average LTV per customer
- Pricing flexibility: quote custom based on:
  - Portfolio size (>500 cards = +$50/month)
  - User count (5+ users = +$30/month per additional user)
  - API volume (10K–50K requests = +$30/month)
  - White-label branding = +$100/month
- Sales-led GTM: direct outreach to known dealers, wholesalers
- Typical deal size: $150–300 USD/month
- Expected close rate: 10–15% of inbound dealer inquiries

---

### Pricing Justification by Feature

| Feature | Why Premium? | Free | Pro | Enterprise |
|---------|--------------|------|-----|------------|
| Portfolio dashboard | Basic tier | ✓ | ✓ | ✓ |
| Price aggregation | Core value | ✓ | ✓ | ✓ |
| Buy/Hold/Sell signals | Data requirement | × | ✓ | ✓ |
| Confidence scoring | Increases trust | × | ✓ | ✓ |
| Real-time alerts | Push infrastructure cost | × | ✓ | ✓ |
| Scenario modeling | Computation cost | × | ✓ | ✓ |
| Multi-user accounts | Infrastructure, compliance | × | × | ✓ |
| API access | Infrastructure, support load | × | × | ✓ |
| Advanced reporting | Support burden (custom reports) | × | × | ✓ |
| Batch operations | Infrastructure (database optimization) | × | × | ✓ |
| White-label | Product customization, support | × | × | ✓ |
| SLA/Uptime guarantee | Infrastructure, monitoring | × | × | ✓ |

---

## GO-TO-MARKET MESSAGING

### For Collectors: "Know Your Collection, Build Your Legacy"

**Headline:** "Turn your Pokemon TCG collection from a spreadsheet into a portfolio. See every card's story—past, present, and future."

**Subheading:** Collectr prices. PSA data. Real P&L. One dashboard. Collectors in Thailand finally have the visibility international investors have.

**Problem-Solution-Proof Framework:**

**Problem (their pain):**
- Scattered prices across Collectr, eBay, Discord channels
- Manual spreadsheets take 30+ minutes/week to maintain
- No confidence in your valuations (Collectr match? eBay estimate? Guess?)
- Missing the story behind your best cards (why did this Pikachu rocket 289%?)

**Solution (your value):**
- One source of truth: Portfolio dashboard syncs with Collectr automatically
- Confidence scoring: Know if your card's price is solid (95% confident) or a best guess (30%)
- Insights that matter: Top gainers, weak positions, cards worth watching
- Peace of mind: Real P&L tracking—no more "I think it's worth..."

**Proof (social proof):**
- "20-card portfolio tracked. ฿35K unrealized gains in 6 months."
- "85% average price confidence. Collectr data, PSA estimates, eBay comparables—all in one place."
- "Used by 100+ collectors in Bangkok. Join the community."

**CTA:** "Track your first collection free. Up to 20 cards. Sync with Collectr in 2 minutes."

**Acquisition Channels:**
- Community outreach: Collector Discord servers, Facebook groups, LINE groups
- Local partnerships: Card shops in Chatuchak Market, Bangkok collectibles scene
- Content marketing: Blog posts ("Why Your Pikachu Rose 289%"), YouTube unboxings with Tracer integrations
- Influencer seeding: Send free Pro accounts to top Thai Pokemon collectors (10–50K followers on TikTok/Instagram)
- Referral loop: "Share your collection—earn 3 months free when a friend joins"

---

### For Flippers: "Trade Smarter. Real-Time Signals. Confidence Scoring."

**Headline:** "Stop guessing when to buy and sell. Tracer's real-time signals and confidence scoring tell you exactly when to move."

**Subheading:** Flippers, dealers, and active traders in Southeast Asia now have the same tools institutional investors use: multi-source pricing, scenario modeling, portfolio concentration metrics—without the $500/month Bloomberg terminal.

**Problem-Solution-Proof Framework:**

**Problem (their pain):**
- Timing entry/exit windows is reactive (updates spreadsheet after the move)
- Price data is fragmented: check Collectr (15 min), eBay (another 15 min), PSA (another 10 min)
- No confidence in signals: how many Collectr matches does this card have? Is it a real price?
- Currency swings silently destroy margins (JPY rises 5% overnight, your margins compress 10%)
- Can't easily see concentration risk ("40% of my portfolio is Pikachu—that's a red flag")

**Solution (your value):**
- Real-time buy/sell signals: Notified within minutes when a card hits your threshold
- Confidence-scored pricing: Know when a signal is based on 5 Collectr matches (95% confident) vs. an estimate (30%)
- Scenario modeling: "If prices rise 30% (bull case), my portfolio is worth ฿350K. If they fall 25% (bear case), ฿200K. Currency risk: +/−5% upside/downside."
- Portfolio metrics: See concentration (Is Pikachu 40% of your value?), signal mix (8 BUYs, 2 SELLs), risk distribution

**Proof (technical credibility):**
- "23 cards analyzed. 8 BUY signals, 2 SELL signals, 85% average confidence."
- "Scenario modeling: Bull case +350K THB. Bear case −180K THB. Currency risk: JPY strength adds ฿15K upside."
- "Alert: Slowpoke hit SELL threshold. Price down 47.8%. Liquidate? Use scenario modeling to decide."

**CTA:** "Try Pro free for 2 weeks. Real-time signals, confidence scoring, scenario modeling. No credit card."

**Acquisition Channels:**
- Community outreach: Trader Telegram groups, Discord trading servers, Reddit r/PokemonTCG
- Performance marketing: Google Ads targeting "Pokemon card flip," "Pokemon TCG trader," "PSA 10 Pikachu price"
- Content marketing: "Flipping Profit Playbook" (case study), "How to Model Currency Risk in Pokemon Cards"
- Influencer seeding: Partner with top Thai/SE Asian flippers (Telegram, YouTube) for testimonials
- Freemium flow: Free tier → hit 21-card limit → "Upgrade to Pro to track 100 cards + real-time signals"

---

### For Dealers/Institutions: "Manage Your Inventory Like a Hedge Fund"

**Headline:** "From chaos to clarity. Real-time portfolio NAV, inventory turnover metrics, POP dilution alerts, multi-user access—everything professional dealers need."

**Subheading:** Somchai doesn't run a spreadsheet business. Neither should you. Tracer is the operating system for dealers managing 500–5,000 SKU inventory across wholesale, retail, and international channels.

**Problem-Solution-Proof Framework:**

**Problem (their pain):**
- Portfolio NAV is mystery (real-time inventory value unknown for cash flow, collateral)
- Slow-moving inventory invisible (which 20% of my 1,000 cards are dead stock?)
- Pricing is manual: daily Collectr checks, no sync
- POP dilution risk is blind (didn't know Pikachu got reprinted until margins compressed)
- Cash flow forecasting is reactive (reacts to shortfall, not proactive)
- Multi-person operations can't share access without shared spreadsheet chaos
- No audit trail (who changed this price? When? Why?)

**Solution (your value):**
- Real-time portfolio NAV: Dashboard shows current inventory value in THB. Cash flow planning becomes predictive.
- Inventory turnover metrics: See which cards sit 6+ months (deadstock), which sell in 2 weeks (hot items). Rebalance accordingly.
- POP dilution alerts: Notified when production increases, depreciation risk rises.
- Multi-user access: Owner sees full P&L. Manager sees inventory status. Staff can only add/update. Compliance trails log all changes.
- Scenario modeling: "If export demand drops 20%, my NAV declines ฿2M. If JPY weakens 10%, my Japanese supplier costs jump ฿500K."
- Advanced reporting: Quarterly audit reports. Supplier performance dashboards. Cash flow forecasts.

**Proof (institutional features):**
- "1,200 cards tracked. Real-time NAV: ฿12M. Portfolio concentration: 40% Pikachu (risk alert). Inventory velocity: 45-day average age."
- "POP Alert: Charizard EX reprint detected. Estimated margin compression: 15%. Recommend liquidation of 20-card position within 30 days."
- "Cash flow forecast: Based on 45-day turnover and 100 active SKUs, expect ฿500K liquidation next month. Plan accordingly."

**CTA:** "Book a 30-min demo. See your portfolio NAV in real-time. Custom pricing available."

**Acquisition Channels:**
- Direct outreach: Sales team identifies dealers via Chatuchak Market networks, Instagram retail accounts, wholesaler databases
- Partnership channels: Team up with Pokemon TCG distributors (Japanese importers) to co-market
- Local events: Sponsor card market events in Bangkok, Chiang Mai, Phuet. Demo at vendor booths.
- Content marketing: "The Dealer's Handbook: Managing 1,000 Cards Like a Hedge Fund" (white paper)
- Case studies: Feature successful dealers using Tracer in quarterly reports
- Annual user conference: Bring dealers together, share strategies, showcase platform

---

## MARKET & COMPETITIVE POSITION

### Why This Positioning Wins

1. **Thailand first-mover advantage:** No other platform targets SE Asian collectors with home market data (Collectr integration)
2. **Multi-segment monetization:** Free → Pro → Enterprise captures different willingness-to-pay across personas
3. **Institutional credibility:** Scenario modeling, POP alerts, confidence scoring differentiate from spreadsheet-only competitors
4. **Community flywheel:** Free users create data that improves pricing; paid users get better signals; network grows
5. **Natural upgrade path:** Collector → Flipper → Dealer mirrors real career progression in the hobby

### Competitive Landscape

| Competitor | Strength | Weakness | Your Advantage |
|------------|----------|----------|-----------------|
| Google Sheets + Collectr | Free, simple | Manual, error-prone | Automated, confidence-scored |
| PSA Price Guide API | Authoritative data | Slow, US-centric | Real-time multi-source, SE Asia focus |
| eBay (sold listings search) | Comprehensive comp data | Fragmented, noisy | Cleaned, aggregated, weighted |
| Generic portfolio trackers (Caulkhead, TCG Player) | Exist | US-focused, no confidence scoring | Thailand-first, confidence metrics, dealer tools |

---

## METRICS TO WATCH (Post-Launch)

### Tier 0: Acquisition & Activation
- **Free tier signup rate** (target: 50/week in first month, 200/week by month 3)
- **Free-to-Pro conversion rate** (target: 8% within 6 months)
- **Time-to-first-value** (target: <5 min to add first card)

### Tier 1: Engagement & Retention
- **Monthly active users (MAU)** by persona
- **Average portfolio size** (cards per user)
- **Churn rate by tier** (target: <3% for Pro, <5% seasonal variations)
- **Feature adoption** (% of Pro users using signals, scenarios)

### Tier 2: Monetization
- **ARPU** (average revenue per user) by segment
- **CAC payback period** (target: <18 months for Pro, <36 months for Enterprise)
- **LTV:CAC ratio** (target: >3:1)
- **Enterprise deal velocity** (# of closed deals per month)

### Tier 3: Product Health
- **Average price confidence score** (target: >80% across portfolio)
- **Signal accuracy** (test: do BUY signals outperform HOLDs? Validate quarterly)
- **Data freshness** (% of prices updated within 24 hours)
- **Customer support NPS** (target: >40 for Pro, >50 for Enterprise)

---

## NEXT STEPS

1. **Soft launch with free tier** to 50 collector friends (1 week feedback cycle)
2. **Refine pricing** based on willingness-to-pay feedback from flippers and dealers
3. **Build acquisition channels** (Discord, Telegram, local events) with founder-led outreach
4. **Develop Pro tier** (real-time signals, confidence scoring, scenario modeling) in 3–4 weeks
5. **Create enterprise sales deck** and schedule 10 dealer demos in Chatuchak Market
6. **Establish legal/compliance** for collectibles in Thailand (tax, licensing, AML considerations)

---

**Document prepared:** April 21, 2026  
**Next review:** After first 50 free users, 2-week feedback cycle
