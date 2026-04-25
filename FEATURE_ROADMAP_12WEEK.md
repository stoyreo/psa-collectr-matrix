# PSA × Collectr Tracer: 12-Week Feature Roadmap & Implementation Plan

**Document Date:** April 21, 2026  
**Timeline:** Week 1–12 (3 months to feature-complete MVP with Tier 1 core features)  
**Target:** Soft launch Week 6 (free tier only), Pro tier Week 9, Enterprise tier Week 12+  
**Team Assumptions:** 1 full-stack eng + 1 backend + 1 QA/ops (3 person team)

---

## EXECUTIVE SUMMARY

| Phase | Week(s) | Focus | Launchers | Personas | Monetization |
|-------|---------|-------|-----------|----------|--------------|
| **Phase 0: Foundation** | 1–2 | Multi-source pricing, portfolio dashboard, signal engine | Free tier MVP | All | Freemium foundation |
| **Phase 1: MVP Launch** | 3–4 | Onboarding wizard, confidence scoring, first insights | Free tier soft launch (50 users) | Collector, Flipper | Validate ARPU |
| **Phase 2: Pro Tier** | 5–7 | Real-time alerts, scenario modeling, trend analysis | Pro tier beta (closed loop with flippers) | Flipper, active Collector | Launch paid tier |
| **Phase 3: Scale & Enterprise** | 8–10 | Multi-user, API, batch ops, inventory metrics, reporting | Enterprise pre-sales demos | Dealer | Establish enterprise GTM |
| **Phase 4: Hardening** | 11–12 | Performance optimization, mobile app prep, data migration | Stable production, mobile roadmap | All | Expand TAM |

---

## PHASE 0: FOUNDATION (Week 1–2)
**Goal:** Build technical backbone; Tier 0 features fully functional  
**Launcher:** Internal testing, "dogfooding" with 5 internal users  
**Success Criteria:**
- [ ] Multi-source price aggregation working reliably (Collectr, PSA, eBay)
- [ ] Portfolio dashboard displays NAV, P&L, top gainers/losers
- [ ] Buy/Hold/Sell signal engine produces signals (no confidence scoring yet)
- [ ] Postgres DB schema supports 10K+ cards
- [ ] CSV import functional (batch add cards)

### Architecture Decisions

```
Backend (Node.js/Express or Python/FastAPI):
├── API Layer
│   ├── /portfolio (GET, POST, PUT, DELETE)
│   ├── /prices (GET, caching layer)
│   ├── /signals (GET, signal engine)
│   └── /auth (JWT, local dev)
├── Data Layer
│   ├── Postgres (portfolios, cards, transactions)
│   ├── Redis (price cache, 24-hour TTL)
│   └── Collectr API client (webhook listener for real-time)
├── Signal Engine (deterministic)
│   ├── Calculate fair value from 3 sources
│   ├── Assign signal (BUY if <15% fair value, SELL if >20% above, else HOLD)
│   └── Store signal + timestamp for trends
└── Background Jobs
    ├── Daily price refresh (6 AM Bangkok time)
    ├── Real-time Collectr webhook listener
    └── Weekly data validation (audit trail)

Frontend (React + TypeScript):
├── Pages
│   ├── /dashboard (KPI cards, portfolio summary)
│   ├── /portfolio (card grid, list view)
│   ├── /add-card (search form, manual entry)
│   └── /auth (login, signup)
├── Components
│   ├── <PortfolioSummary /> (NAV, P&L, gains)
│   ├── <CardGrid /> (responsive, 1–4 columns)
│   ├── <SignalBadge /> (BUY/HOLD/SELL)
│   └── <PriceCell /> (market value, source)
└── Styles
    ├── Tailwind CSS + dark mode
    ├── Mobile-first (375px base)
    └── 3 breakpoints (375, 768, 1024)

Database Schema (MVP):
users:
  id (PK), email, password_hash, created_at, country, segment (collector/flipper/dealer)

portfolios:
  id (PK), user_id (FK), name, created_at, updated_at, is_demo (bool)

cards:
  id (PK), portfolio_id (FK), psa_id, name, grade, cost_basis_thb, 
  acquisition_date, created_at, updated_at

prices:
  id (PK), card_id (FK), source (collectr/psa/ebay), market_value_thb, 
  source_data (JSON), confidence_pct, timestamp, is_current (bool)

signals:
  id (PK), card_id (FK), signal (BUY/HOLD/SELL), confidence_pct, 
  fair_value_thb, timestamp, reasoning (JSON)

transactions:
  id (PK), portfolio_id (FK), type (buy/sell), card_id (FK), 
  amount_thb, timestamp, notes
```

### Week 1 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Database schema + migrations** | Backend | 1 | `schema.sql` + Postgres instance | None |
| **Collectr API integration** | Backend | 2 | Working client, webhook listener | Need Collectr dev account |
| **PSA + eBay scraper/API** | Backend | 1.5 | Price aggregation (no confidence yet) | eBay API docs |
| **Signal engine (deterministic)** | Backend | 1 | BUY/HOLD/SELL logic, stored in DB | Price aggregation done |
| **Portfolio dashboard UI** | Frontend | 2 | KPI cards, NAV, P&L, top gainers | Price API done |
| **Card grid + search** | Frontend | 1.5 | Display 50+ cards, basic filtering | Card API done |
| **Auth scaffolding** | Backend + Frontend | 1 | JWT + protected routes | None |

**Week 1 Deliverables (End of Day Friday):**
- [ ] Database live on Postgres
- [ ] Collectr API integration working (fetch prices for sample cards)
- [ ] Dashboard displaying sample 15-card demo portfolio with NAV
- [ ] Signal engine calculating signals (no confidence scoring yet)
- [ ] Auth flow scaffolded (login works, JWT tokens issued)

### Week 2 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Price aggregation + weighting** | Backend | 1 | Multi-source pricing logic (no confidence yet) | Signal engine done |
| **Portfolio P&L calculations** | Frontend | 1 | Show gain/loss per card, portfolio total | Prices working |
| **CSV import** | Backend + Frontend | 1 | Bulk add cards (15-card demo) | Card schema stable |
| **Responsive mobile (375px)** | Frontend | 1.5 | Bottom nav, card list scrolls properly | Dashboard layout stable |
| **Price caching layer** | Backend | 0.5 | Redis 24-hour TTL | Prices working |
| **Data validation + audit trail** | Backend | 0.5 | Log all DB changes (who, when, what) | Schema done |
| **QA + bug fixes** | QA/Ops | 1 | Regression testing, mobile testing | All features done |

**Week 2 Deliverables (End of Day Friday):**
- [ ] Multi-source pricing working (Collectr takes priority, eBay fallback)
- [ ] Demo portfolio imported and displaying with correct NAV, P&L
- [ ] Portfolio summary showing top 3 gainers, top 2 losers
- [ ] Mobile nav (bottom tab bar) fully responsive at 375px, 768px
- [ ] CSV import functional (can bulk-import DEMO_PORTFOLIO.csv)
- [ ] All Tier 0 features green ✓

---

## PHASE 1: MVP SOFT LAUNCH (Week 3–4)
**Goal:** Launch free tier to 50 external users; validate product-market fit with Collector persona  
**Launcher:** Closed-beta invite (50 collector friends, TechCraftLab's network)  
**Success Criteria:**
- [ ] Onboarding wizard completes for >90% of new users
- [ ] Time-to-first-value <5 minutes
- [ ] <10% of users stuck on card search (help flow working)
- [ ] NPS >30 in feedback survey (question: "How likely to recommend?")
- [ ] >70% of users add a real card (not just demo)

### Features to Build

| Feature | Owner | Effort | Why Now | Acceptance Criteria |
|---------|-------|--------|---------|-------------------|
| **4-Step Onboarding Wizard** | Frontend | 2d | Must have before external users; reduces friction | User completes all 4 steps in <3 min |
| **Confidence Scoring (basic)** | Backend | 1.5d | Shows value prop (why Tracer > spreadsheet); builds trust | Display "95% / 50% / 30%" tiers on each price |
| **Price Trend Sparklines** | Frontend | 1d | Collector wants "why did Pikachu jump 289%?" | 30/90/365-day sparklines show trend direction |
| **Empty State + 3 CTAs** | Frontend | 0.5d | Critical for first impression (empty dashboard) | "Add my cards" / "Try demo" / "Learn more" paths clear |
| **Card Search + Manual Entry** | Frontend | 1d | User can't find card in DB → manual fallback | Search works, manual add form handles missing cards |
| **Help Center Scaffolding** | Content | 0.5d | Reduce support burden (FAQ, video guides) | 5–10 FAQ pages, link to YT guides |

### Week 3 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Onboarding wizard UX** | Frontend | 1.5 | Step 1 (segmentation) through Step 4 (alerts setup), all flows working | Dashboard layout stable |
| **Confidence scoring display** | Frontend | 0.5 | Show 95% / 50% / 30% badges on price cells | Prices have confidence_pct in DB |
| **Empty state + 3 CTAs** | Frontend | 0.5 | Landing page when portfolio empty; test all 3 paths | Auth working |
| **Card search improvement** | Frontend | 0.5 | Auto-complete from PSA DB; fallback to manual | PSA DB indexed |
| **Analytics scaffolding** | Backend + Frontend | 0.5 | Track: page views, feature clicks, time-to-first-value | None |
| **Email setup** | Backend | 1 | Send welcome email, alert emails (no scheduling yet) | SMTP configured |
| **Mobile testing** | QA | 1 | Verify wizard works on iPhone 12 (375px) | Wizard done |

**Week 3 Deliverables (End of Day Friday):**
- [ ] 4-step wizard fully functional and tested on mobile + desktop
- [ ] Confidence scoring visible on all prices (95%/50%/30% badges)
- [ ] Empty state dashboard with 3 CTAs ("Add my cards" / "Try demo" / "Learn more")
- [ ] Card search works, manual fallback functional
- [ ] Analytics tracking implemented (Mixpanel / Amplitude)
- [ ] Beta invite email drafted and ready to send

### Week 4 Task Breakdown (Soft Launch Week)

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Soft launch preparation** | Ops | 2 | Invite 50 users, monitor uptime, prepare support responses | All features stable from Week 3 |
| **First insights personalization** | Frontend | 1 | Show different insights for Collector vs Flipper (Step 3 of wizard) | Confidence scoring done |
| **Basic alerts scaffolding** | Backend | 1 | Users can configure email alerts (not triggered yet) | Email sending working |
| **Feedback collection** | Ops | 1 | Deploy survey link (Typeform), weekly sync calls with 5–10 beta users | None |
| **Bug fixes + stabilization** | QA | 2 | Address critical issues from beta users, performance optimization | Beta users active |

**Week 4 Deliverables (End of Day Friday):**
- [ ] 50 beta users invited and onboarding
- [ ] <2 min response time for dashboard load (p99)
- [ ] Zero critical bugs after 48 hours (or hotfixed within 4 hours)
- [ ] NPS >30 collected from 20 beta users
- [ ] Feature adoption tracked: % completing wizard, % adding real card, % enabling alerts

**Phase 1 Success Metrics:**
- **Activation rate:** >90% complete wizard
- **Time-to-value:** 4.2 min average (target <5)
- **Real card add rate:** 75% of users add ≥1 real card (not just demo)
- **Churn week 1:** <10% (expect some "just browsing" dropoff)
- **NPS:** 35 (target >30)
- **Support load:** <5 emails/week (onboarding + one bug)

---

## PHASE 2: PRO TIER LAUNCH (Week 5–7)
**Goal:** Launch Pro tier ($12/month) targeting Flipper persona; unlock monetization  
**Launcher:** Close beta loop with 10–20 active flippers; early access for Pro  
**Success Criteria:**
- [ ] Pro tier signup flow working (Stripe integration)
- [ ] Real-time alerts configured and firing (push + email)
- [ ] Scenario modeling dashboard functional (Bull/Bear toggles)
- [ ] Free→Pro conversion rate 8–10% within 2 weeks of launch
- [ ] Pro churn <3% MoM (expect seasonal variation)

### Features to Build

| Feature | Owner | Effort | Why Now | Acceptance Criteria |
|---------|-------|--------|---------|-------------------|
| **Real-time Price Alerts** | Backend + Frontend | 3d | Flipper's #1 need; retention lever; requires infrastructure (webhooks) | Alert fires within 2 min of price crossing threshold |
| **Scenario Modeling (Bull/Bear/Currency)** | Frontend + Backend | 3d | Differentiator; complex UX but high value for Flipper | Bull +30%, Bear −25%, JPY ±10% scenarios calculate correctly |
| **Trend Analysis (30/90/365d)** | Frontend | 1.5d | Supports narrative ("why did Pikachu spike?"); builds confidence | Charts render, trends visualize correctly |
| **Stripe Integration + Billing** | Backend | 1.5d | Enable paid tier; recurring charges; subscription management | Stripe webhooks working, subscription renews automatically |
| **Pro Tier UI (feature gates)** | Frontend | 1d | Hide Pro features from Free users; show "upgrade" prompts | Accurate feature gating, clear CTAs to upgrade |
| **Portfolio Concentration Metrics** | Backend + Frontend | 1.5d | Flipper needs to see "40% Pikachu = concentration risk" | Dashboard shows % allocation per card, concentration warnings |
| **Advanced Filtering** | Frontend | 1d | Filter by grade, signal, risk, P&L %; search functionality | Filters work in combination, results update instantly |

### Week 5 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Real-time alert infrastructure** | Backend | 2 | Webhooks + email/push service (Twilio or similar); alert logic | Collectr webhook listener done |
| **Alert configuration UI** | Frontend | 1 | Users set thresholds (price, signal change) per card | Alert backend done |
| **Scenario modeling engine** | Backend | 1.5 | Bull/Bear/Currency logic; store scenarios in DB | Signal engine stable |
| **Scenario modeling UI** | Frontend | 1.5 | Interactive toggles, real-time recalculation of portfolio value | Engine done |
| **Trend chart (30/90/365d)** | Frontend | 1 | Line chart showing price history; zoom/pan | Prices stored with timestamps |
| **Stripe + Billing setup** | Backend | 1.5 | Checkout flow, subscription management, webhook handling | Stripe account ready |
| **QA + performance testing** | QA | 1 | Load test: 100 users adding alerts simultaneously | All features done |

**Week 5 Deliverables (End of Day Friday):**
- [ ] Real-time alert system working (tested with manual price updates)
- [ ] Scenario modeling fully interactive (Bull/Bear/Currency ±10%)
- [ ] Trend charts rendering correctly (30/90/365d views)
- [ ] Stripe integration complete (test transactions working)
- [ ] Pro tier hidden from Free users; clear "upgrade" CTAs visible

### Week 6 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Portfolio concentration dashboard** | Frontend | 1 | Show % allocation per card, concentration warnings (e.g., "40% Pikachu") | Card data structure stable |
| **Advanced filtering UI** | Frontend | 1 | Filter combinations (grade + signal + risk), search, sorting | Card attributes indexed in DB |
| **Trigger-based alerts** | Backend | 1 | Alert fires when: price crosses ±15%, signal changes BUY→HOLD, etc. | Alert infrastructure done |
| **Pro onboarding flow** | Frontend | 0.5 | Guided intro to Pro features (signals, scenarios, alerts); 3-min walkthrough | Pro features done |
| **Email templates** | Backend + Ops | 1 | Welcome email (free → Pro), alert emails, weekly digest | Email service working |
| **Mobile Pro tier** | Frontend | 0.5 | Ensure Pro features visible and usable on 375px | Responsive design stable |
| **Competitor research + positioning** | Ops | 1 | Document GTM messaging for Flipper persona; finalize landing page copy | Strategy doc stable |

**Week 6 Deliverables (End of Day Friday):**
- [ ] Portfolio concentration metrics visible (% per card, risk warnings)
- [ ] Advanced filtering working (combinations of grade, signal, risk, P&L %)
- [ ] Alert triggers tested and firing correctly
- [ ] Pro onboarding flow streamlined (<3 min)
- [ ] Mobile experience for Pro features verified
- [ ] GTM messaging ready for launch

### Week 7 Task Breakdown (Pro Launch Week)

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Pro tier soft launch** | Ops | 2 | Announce to 50 beta users, invite 10–20 Flippers to early access, monitor churn | All Pro features stable |
| **Sales page setup** | Ops + Biz | 1 | Landing page, pricing page, FAQs; Flipper-targeted messaging | Copy ready |
| **Support + billing issues** | Ops | 2 | Address Stripe issues, failed payments, upgrade questions | None |
| **Metrics collection** | Analytics | 1 | Track free→Pro conversions, churn, feature adoption | Analytics instrumented |
| **Feedback collection (Flipper)** | Ops | 1 | Weekly sync calls with 5–10 active Flippers; capture feature requests | Pro users active |
| **Bug fixes + optimization** | QA | 1 | Address Pro-tier-specific issues (e.g., scenario recalculation slow) | Flippers testing |

**Week 7 Deliverables (End of Day Friday):**
- [ ] Pro tier live and accepting payments
- [ ] 10–20 Flippers in early access, providing feedback
- [ ] Free→Pro conversion funnel instrumented
- [ ] Pro churn tracking in place (<3% target)
- [ ] Sales page + pricing live on marketing site

**Phase 2 Success Metrics:**
- **Free→Pro conversion:** 8–10% within 2 weeks
- **Pro MRR:** $120–240 (10–20 users at $12/month)
- **Alert accuracy:** >95% trigger correctly
- **Scenario modeling adoption:** >70% of Pro users try ≥1 scenario
- **Churn rate:** <3% MoM (very few cancellations)
- **Support load:** <10 emails/week (mostly billing + feature requests)

---

## PHASE 3: SCALE & ENTERPRISE (Week 8–10)
**Goal:** Launch Enterprise tier; begin dealer pre-sales; prepare for Series A  
**Launcher:** Direct outreach to 10 dealers in Chatuchak Market; demo video + sales deck  
**Success Criteria:**
- [ ] Enterprise tier spec finalized (custom pricing)
- [ ] Multi-user + role-based access working
- [ ] API + webhooks functional (for integrations)
- [ ] 2–3 dealer pilots signed (beta accounts)
- [ ] Enterprise CAC payback <18 months

### Features to Build

| Feature | Owner | Effort | Why Now | Acceptance Criteria |
|---------|-------|--------|---------|-------------------|
| **Multi-user Accounts + Roles** | Backend + Frontend | 3d | Enterprise must-have; enables multi-person operations | 3 roles (Admin, Manager, Analyst) with correct permissions |
| **API + Webhooks** | Backend | 2d | Enable integrations; support dealer inventory systems | REST API works; webhooks fire on price/signal changes |
| **Batch Import/Export (CSV)** | Backend + Frontend | 1.5d | Dealers have 500+ cards; need bulk operations | Import 1K cards in <10 sec; export as CSV |
| **Inventory Metrics Dashboard** | Frontend | 2d | Dealers need: turnover velocity, age distribution, dead stock | Dashboard shows card age, turnover rate, concentration |
| **POP Dilution Alerts** | Backend | 1.5d | When Pikachu gets reprinted, alert dealers to margin compression | Alert fires within 1 hour of reprint detection |
| **Advanced Reporting (PDF/XLSX)** | Backend + Frontend | 2d | Quarterly audit reports, supplier performance dashboards | Generate multi-page PDF/XLSX reports on demand |
| **Audit Trails + Compliance** | Backend | 1d | Log all changes (who, when, what); regulatory requirement | All DB changes logged with user + timestamp |

### Week 8 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Multi-user architecture** | Backend | 1.5 | Add user_role, org_id to DB; permission checking middleware | User schema refactor |
| **Role-based access control (RBAC)** | Backend | 1 | Admin/Manager/Analyst permissions; test permission edge cases | RBAC middleware done |
| **Multi-user UI** | Frontend | 1.5 | Invite users, manage roles, view user activity log | Backend RBAC done |
| **API scaffolding** | Backend | 1 | REST endpoints for cards, portfolios, alerts, transactions | DB schema stable |
| **Webhook delivery** | Backend | 1 | On price cross threshold / signal change; retry logic | API done |
| **Batch import UI** | Frontend | 1 | CSV upload form, progress bar, error handling | Import endpoint done |
| **QA + security review** | QA + Sec | 1 | Test permission bypasses, data isolation between orgs | Multi-user features done |

**Week 8 Deliverables (End of Day Friday):**
- [ ] Multi-user accounts fully functional (create user, assign role, permissions enforced)
- [ ] API scaffold complete (test endpoints working)
- [ ] Webhooks delivering price/signal updates reliably
- [ ] Batch import/export working (tested with 100+ card CSV)
- [ ] Security review passed (no permission bypasses)

### Week 9 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Inventory metrics engine** | Backend | 1.5 | Calculate: turnover velocity, age distribution, dead stock (>90d) | Transaction history indexed |
| **Inventory dashboard UI** | Frontend | 1.5 | Charts showing: cards by age, velocity distribution, concentration | Engine done |
| **POP dilution detection** | Backend | 1 | Daily check for new prints (integrate with Pokemon TCG API or manual curated list) | Card DB structure stable |
| **POP dilution alerts** | Frontend + Backend | 0.5 | Notify dealers when reprint detected; show margin impact | Detection engine done |
| **Reporting engine** | Backend | 1.5 | Generate PDF (quarterly audit) and XLSX (supplier perf); template system | Data aggregation done |
| **Audit trail storage + UI** | Backend + Frontend | 1 | Store all changes; queryable audit log per org | All features trigger audit logs |
| **Enterprise sales deck** | Ops + Biz | 1 | Slides: ROI for dealers, pricing tiers, case studies, integration examples | Strategy doc ready |
| **Dealer outreach script** | Ops | 1 | 10 target dealers identified; email + phone script; demo video recorded | Marketing assets ready |

**Week 9 Deliverables (End of Day Friday):**
- [ ] Inventory metrics dashboard complete (turnover, age, concentration visible)
- [ ] POP dilution detection working (tested with known reprints)
- [ ] Reporting engine functional (PDF/XLSX generation)
- [ ] Audit trails logged and queryable
- [ ] Enterprise sales deck finalized
- [ ] 10 dealers identified + outreach script ready

### Week 10 Task Breakdown (Enterprise Launch Week)

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Enterprise onboarding flow** | Frontend + Ops | 1.5 | Custom setup call, CSV import, user invitations, first insights | Features stable |
| **Sales outreach** | Biz | 3 | Phone + in-person demos in Chatuchak Market; collect feedback; schedule POCs | Script + deck ready |
| **Beta dealer accounts setup** | Ops | 1 | 2–3 dealers onboarded; monitor usage; collect feedback | Onboarding flow done |
| **Performance optimization** | Backend | 1 | Optimize queries for 1K+ card portfolios; caching strategy | Inventory metrics slow |
| **API documentation** | Backend + Ops | 1 | OpenAPI/Swagger spec; sample requests; auth examples | API endpoints stable |
| **Support infrastructure** | Ops | 0.5 | Slack channel for Enterprise customers; SLA monitoring | None |

**Week 10 Deliverables (End of Day Friday):**
- [ ] Enterprise tier live (custom pricing)
- [ ] 2–3 dealer pilots onboarded and using platform
- [ ] Sales pipeline established (5–10 "warm" deals)
- [ ] API documented + tested
- [ ] Performance validated for 1K+ card portfolios

**Phase 3 Success Metrics:**
- **Enterprise MRR:** $300–600 (2–3 customers at $150–200/month average)
- **Multi-user adoption:** >70% of Enterprise accounts have >1 user
- **API usage:** >100 requests/day across beta accounts
- **Dealer feedback NPS:** >45
- **Sales pipeline:** 5–10 "warm" opportunities identified
- **Support load:** <20 emails/week (mostly integration questions)

---

## PHASE 4: HARDENING & MOBILE (Week 11–12)
**Goal:** Stabilize production; prepare mobile app roadmap; plan Series A  
**Launcher:** Public launch (free tier) + Enterprise presales  
**Success Criteria:**
- [ ] 99.5% uptime SLA met
- [ ] Zero P1 bugs in 2-week period
- [ ] Mobile app roadmap finalized
- [ ] 500+ free users by end of week 12
- [ ] $1K+ MRR (free + Pro + Enterprise combined)

### Features to Build (Minor)

| Feature | Owner | Effort | Why Now | Acceptance Criteria |
|---------|-------|--------|---------|-------------------|
| **Dark Mode Toggle** | Frontend | 0.5d | Polish; engagement lever; requested by users | Dark theme applies system-wide; persists in local storage |
| **Performance Monitoring** | Backend + Ops | 1d | Monitor API response times, DB query times; alerting | Dashboard shows p50/p95/p99 latencies |
| **Data Migration / Backup** | Backend + Ops | 1d | Automated daily backups; recovery tested | Backups automated; recovery procedure documented |
| **Mobile App Kickoff** | Design + Frontend | 1d | Identify iOS/Android tech stack (React Native? Flutter?); architecture doc | Tech stack chosen; architecture doc ready |

### Week 11 Task Breakdown

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Dark mode implementation** | Frontend | 0.5 | All pages support dark mode; toggle in settings | Design system updated |
| **Performance monitoring setup** | Backend + Ops | 1 | Datadog/New Relic alerts on p99 latency, error rates | Infrastructure access granted |
| **Load testing** | QA + Backend | 1 | Simulate 1K concurrent users; identify bottlenecks; optimize | Monitoring done |
| **Automated backups** | Backend + Ops | 0.5 | Daily snapshots; tested recovery | DB access + script ready |
| **Mobile app architecture** | Design + Frontend | 1 | Finalize tech stack decision (React Native vs Flutter); architecture doc | Team alignment on choice |
| **Browser compatibility testing** | QA | 1 | Test on: Chrome, Safari, Firefox (latest 2 versions); fix issues | None |
| **Accessibility audit** | QA | 0.5 | WCAG 2.1 AA compliance check; fix critical issues | None |
| **Security hardening** | Backend + Sec | 1 | SQL injection tests, XSS tests, CSRF protection, rate limiting | None |

**Week 11 Deliverables (End of Day Friday):**
- [ ] Dark mode fully implemented + tested
- [ ] Performance monitoring alerting on SLA violations
- [ ] Load test passed (1K concurrent users, <2s p99 latency)
- [ ] Automated backup + recovery procedure documented
- [ ] Mobile app architecture doc finalized
- [ ] Security audit passed

### Week 12 Task Breakdown (Public Launch + Planning)

| Task | Owner | Days | Deliverable | Blocker |
|------|-------|------|-------------|---------|
| **Public launch prep** | Ops + Biz | 1.5 | Marketing email campaign, social media blitz, press release | Sales deck + copy ready |
| **Public launch day** | All | 1 | Monitor uptime, support responses, celebrate 🎉 | All systems healthy |
| **Series A planning** | Biz + Founder | 2 | Pitch deck, financial model, investor list; start outreach | Metrics + traction ready |
| **Mobile roadmap doc** | Design + Frontend | 1 | iOS/Android phased rollout plan (Week 13–20); wireframes | Architecture done |
| **Post-launch bug triage** | QA + Eng | 1 | Address public launch issues; maintain <4h response time | Launch day + 1 week |
| **User onboarding analysis** | Ops + Analytics | 1 | Deep dive into Week 1 cohort; retention curve; LTV estimate | Analytics complete |

**Week 12 Deliverables (End of Day Friday):**
- [ ] Public launch completed; 500+ free signups by EOD
- [ ] 99.5% uptime maintained throughout launch day
- [ ] Series A pitch deck + financial model finalized
- [ ] Mobile roadmap (Week 13–20) documented
- [ ] First-cohort retention metrics analyzed ($X MRR from Week 1 users)

**Phase 4 Success Metrics:**
- **Free tier signups:** 500+ by EOD week 12
- **Cumulative MRR:** $1,000+ (free tier + Pro + Enterprise)
- **Uptime:** 99.5% (targets SLA)
- **First-cohort churn:** <15% (expect some "just browsing" dropoff)
- **Feature adoption:** >60% of free users add ≥5 cards
- **Support quality:** <2h avg response time

---

## ROADMAP GANTT CHART

```
Phase 0 (Foundation)        Week 1-2:   ████████
Phase 1 (MVP Soft Launch)   Week 3-4:           ████████
Phase 2 (Pro Tier)          Week 5-7:                   ████████████
Phase 3 (Enterprise)        Week 8-10:                              ████████████
Phase 4 (Hardening)         Week 11-12:                                        ████████
```

---

## TEAM ALLOCATION & ROLES

**Assumptions:** 3-person engineering team, 1-2 ops/biz support

### Full-Stack Engineer (1 FTE)
- Weeks 1–4: Portfolio dashboard, card CRUD, auth
- Weeks 5–7: Scenario modeling UI, alerts configuration
- Weeks 8–12: Batch operations, reporting UI, mobile kickoff

### Backend Engineer (1 FTE)
- Weeks 1–2: DB schema, API scaffolding, price aggregation
- Weeks 3–4: Confidence scoring, analytics
- Weeks 5–7: Alert triggers, real-time webhooks, Stripe integration
- Weeks 8–10: Multi-user architecture, API, inventory metrics
- Weeks 11–12: Performance optimization, security hardening

### QA / Operations (0.5 FTE)
- Weeks 1–2: Regression testing, mobile testing
- Weeks 3–4: Beta user onboarding, feedback collection
- Weeks 5–7: Pro tier testing, conversion tracking
- Weeks 8–12: Load testing, security audit, launch coordination

### Business / Founder (0.5–1 FTE)
- Weeks 1–4: Product strategy, feedback synthesis
- Weeks 5–7: Sales page, GTM messaging for Flipper
- Weeks 8–10: Enterprise sales outreach, dealer demos
- Weeks 11–12: Series A prep, public launch GTM

---

## KEY DEPENDENCIES & RISKS

### Critical Path (Must Complete On Time)
1. **Week 1:** Database + Collectr API (blocks everything else)
2. **Week 2:** Price aggregation + signal engine (blocks Tier 1 features)
3. **Week 4:** Onboarding wizard (blocks soft launch)
4. **Week 7:** Stripe integration (blocks Pro revenue)
5. **Week 10:** Multi-user (blocks Enterprise pilot)

### Potential Blockers

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Collectr API rate limits or changes** | Can't refresh prices in real-time | Pre-negotiate API limits; build eBay fallback; cache aggressively |
| **Stripe approval delay** | Can't launch Pro tier | Apply for Stripe account immediately (Week 1) |
| **Data volume growth (>10K cards)** | Query performance degrades | Implement caching + DB indexing by Week 8 |
| **Pokemon TCG Print announces (POP dilution)** | Manual detection burden | Build automated detection by Week 9; fallback to community posts |
| **Mobile app tech stack indecision** | Timeline slips | Make React Native vs Flutter decision by Week 9 |

### Contingency Plans

- **If Collectr API unavailable:** Use eBay + PSA APIs only (signal accuracy drops, but still functional)
- **If Stripe delays:** Use PayPal integration (slightly different UX) + manual invoicing for Enterprise
- **If team capacity drops:** Defer Phase 4 (mobile, hardening) to Week 13+; launch with Tier 0 + Tier 1 only
- **If soft launch user feedback negative:** Extend Phase 1 by 1 week; gather feedback, iterate

---

## SUCCESS METRICS & KPIs BY PHASE

### Phase 0 (Foundation)
- ✓ Zero critical bugs in demo portfolio
- ✓ Dashboard loads in <2 seconds
- ✓ Price data freshness: >95% updated within 24 hours

### Phase 1 (MVP Soft Launch)
- ✓ Onboarding completion: >90%
- ✓ Time-to-first-value: <5 minutes
- ✓ Free users: 50 (target)
- ✓ NPS: >30
- ✓ Real card add rate: >70%

### Phase 2 (Pro Tier)
- ✓ Free→Pro conversion: 8–10%
- ✓ Pro MRR: $120–240
- ✓ Alert accuracy: >95%
- ✓ Scenario adoption: >70% of Pro users
- ✓ Churn: <3% MoM

### Phase 3 (Enterprise)
- ✓ Enterprise MRR: $300–600
- ✓ Multi-user adoption: >70%
- ✓ Sales pipeline: 5–10 warm leads
- ✓ Dealer feedback NPS: >45
- ✓ API usage: >100 req/day

### Phase 4 (Hardening)
- ✓ Uptime: 99.5%
- ✓ Cumulative MRR: $1,000+
- ✓ Free signups: 500+ by EOD week 12
- ✓ First-cohort churn: <15%
- ✓ Feature adoption: >60%

---

## RESOURCE REQUIREMENTS & BUDGET ESTIMATE

| Resource | Cost | Quantity | Subtotal | Timeline |
|----------|------|----------|----------|----------|
| **Infrastructure (AWS/GCP)** | $500–1K/month | 3 months | $1.5–3K | Ongoing |
| **Third-party APIs** | Collectr, PSA, eBay | $0–500 | Ongoing | Ongoing |
| **Stripe (payment processing)** | 2.9% + $0.30 per txn | Per transaction | Variable | Week 7+ |
| **Email service (SendGrid)** | $0–20/month | 1 | $0–60 | Ongoing |
| **Analytics (Mixpanel)** | $0–995/month | 1 | $0–3K | Ongoing |
| **Monitoring (DataDog/New Relic)** | $15–200/month | 1 | $50–600 | Week 8+ |
| **Personnel (3 eng + 0.5 ops)** | ~$15K/month | 3.5 FTE | ~$45K | 12 weeks |
| **Marketing / Launch** | $2–5K (content, ads, email) | 1 | $2–5K | Week 3–12 |
| **Legal / Compliance** | $1–2K (terms, privacy, licensing) | 1 | $1–2K | Week 1 |
| **Total 12-week cost** | | | **~$49–58K** | |

---

## GO / NO-GO DECISION GATES

| Gate | Decision Point | Criteria |
|------|----------------|----------|
| **After Phase 0** | Proceed to Phase 1? | Zero critical bugs in MVP; all Tier 0 features working. **GO if:** Yes. **NO-GO if:** Multiple bugs remain or critical path is <1 week away. |
| **After Phase 1** | Soft launch with beta users? | Onboarding completion >85%; NPS >25. **GO if:** Yes. **NO-GO if:** Users stuck on card search; NPS <25. |
| **After Phase 2** | Launch Pro tier publicly? | Free→Pro conversion >5%; churn <5%; no critical bugs. **GO if:** Yes. **NO-GO if:** Conversion flat (<3%) or churn >5%. |
| **After Phase 3** | Enterprise pre-sales? | Multi-user working; 2+ dealer pilots signed. **GO if:** Yes. **NO-GO if:** Technical issues or zero dealer interest. |
| **After Phase 4** | Public launch? | >250 free users; 99% uptime; <3 P1 bugs. **GO if:** Yes. **NO-GO if:** <250 users or uptime <99%. |

---

## APPENDIX: FEATURE DEPENDENCY MAP

```
Tier 0 (Foundation)
├── Portfolio Dashboard ✓
├── Multi-source Price Aggregation ✓
└── Buy/Hold/Sell Signal Engine ✓

Tier 1 (Core Engagement) — Depends on Tier 0
├── Confidence Scoring ✓
├── Real-time Alerts (depends on webhook infra)
├── Scenario Modeling (depends on signal stability)
├── Insights Dashboard
└── Trend Analysis

Tier 2 (Premium) — Depends on Tier 0 + Tier 1
├── Multi-user Accounts (depends on auth refactor)
├── API + Webhooks (depends on backend stability)
├── Batch Operations
├── Advanced Reporting
├── Portfolio Concentration Metrics
├── Currency Exposure Dashboard
└── POP Dilution Alerts

Tier 3 (Differentiators)
├── Inventory Turnover Metrics
├── Peer Benchmarking
├── Grade Upgrade Forecasting
└── Mobile App (not on critical path)

Tier 4 (Growth)
├── Social Features
├── Marketplace Integration
├── Advanced Education
└── Automated Buy Leads
```

---

## NEXT STEPS

1. **Week 0 (Pre-Work):**
   - [ ] Collectr, PSA, eBay API accounts + documentation
   - [ ] Stripe account application + approval
   - [ ] AWS/GCP project setup + billing configured
   - [ ] Team kickoff: assign owners, clarify blockers
   - [ ] Finalize database schema with team

2. **Week 1 Start:**
   - [ ] All three engineers start on their Phase 0 tasks simultaneously
   - [ ] Daily standup (10 min, 9 AM Bangkok time)
   - [ ] Weekly all-hands (Friday 5 PM)
   - [ ] Tracking in Jira / Linear with sprint structure

3. **Communication & Support:**
   - Slack channel: #psa-tracer-eng (engineers only)
   - Slack channel: #psa-tracer-biz (founder, ops, biz)
   - Weekly metrics review (Mondays)
   - Bi-weekly all-hands (full team)

---

**Roadmap Version:** 1.0  
**Prepared by:** TechCraftLab  
**Date:** April 21, 2026  
**Next Review:** EOD Week 2 (Phase 0 assessment)
