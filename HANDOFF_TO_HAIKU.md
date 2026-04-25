# Handoff to Claude Haiku — Phase A Execution

**Date**: 2026-04-25  
**Working Directory**: `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`  
**Scope**: Web App Quality Pass + Cloudflare→Vercel Hybrid Migration + Skill Suite (Phases A–E)  
**Mode**: Haiku should operate as triple persona (Engineer / Designer / Investor)

---

## Files Haiku Should Read First (In Order)
1. `docs/SYSTEM_BLUEPRINT.md` — 6-page architecture overview
2. `webapp.py` — Every route, image-cache patterns (1222 lines)
3. `templates/index.html` — UI structure, all 7 tabs, JS helpers (2803 lines)
4. `scripts/config.py` — Domain config, USD→THB rate `33.22` (294 lines)
5. `ADD_CARD_PLAN.md` — UX precedent for Phase C.1
6. `HAIKU_PROMPT.md` — Previous Add Card handoff (style reference)
7. `docs/LIMITATIONS.md` — Known constraints (Playwright, serverless, etc.)

## Current App State
- **Tech Stack**: Flask + vanilla JS + openpyxl + Playwright (Cloudflare-exposed)
- **Data Source**: 19-card PSA-graded Japanese Pokémon portfolio in `Portfolio_Master.xlsx`
- **Currency**: THB (฿) always — USD→THB rate `33.22` in `scripts/config.py`
- **Tabs**: 7 (dashboard, portfolio, add-card, insights, collectr, exceptions, pnl-performance)
- **Public URL**: `*.trycloudflare.com` (via `cloudflared.exe` + `config.yml`)

## Phase A: Web Audit (START HERE)
Haiku's **only** task in Phase A is to:
1. Run `start_webapp.bat`
2. Open app in Chrome at `http://localhost:5000`
3. Screenshot every tab
4. Assess each tab via THREE lenses simultaneously:
   - **Engineer**: Broken? Works with bugs? Works?
   - **Designer**: Layout, hierarchy, contrast, density, empty states
   - **Investor**: Is this *actually useful* to a PSA-graded JP card investor in THB?
5. Create `WEB_AUDIT_2026Q2.md` with template (see `HAIKU_PHASE_A_CHECKPOINT.md`)
6. End Phase A with a recommendation: **keep / merge / redesign / delete** for each tab
7. **WAIT** for user's one-line approval before moving to Phase B

**Acceptance**: User says `go` or `tweak: <change>`. Then Phase B begins.

---

## Personas Defined
### 1. Senior Full-Stack Engineer (10+ yrs Python/Flask)
- "Does this actually run? Are there memory leaks, slow queries, missing error states?"
- Focus: Performance, reliability, observability, testability
- Question per tab: "What would break in production? How would I debug this?"

### 2. Senior UI/UX Designer (opinionated)
- "Is the spacing right? Is the hierarchy clear? Is contrast sufficient? Does empty state communicate or just disappear?"
- Focus: Typography (14/16/20/28/40 only), spacing, color tokens, motion, information density
- Question per tab: "Would I ship this, or is it filler?"

### 3. Pokémon TCG Investor (Bangkok-based, THB, PSA-graded only)
- "Does this help me make a better buy/hold/sell decision at 9am in Bangkok?"
- Focus: P&L in THB, arbitrage signals, market comps, grade premiums, days-to-grade
- Question per tab: "Does this answer one specific investor question, or is it vanity?"

**Conflict resolution rule**: If the three personas disagree, pick the option the Investor lens prefers (user is a serious collector, not a generic dashboard user).

---

## Key Constraints (Non-Negotiable)
1. **Currency**: All amounts in THB with ฿ formatter. No raw numbers.
2. **Concurrent Collectr fetches**: Never sequential (causes wrong matches). Must be per-card validation (name + number + set).
3. **Excel schema**: `Portfolio_Master.xlsx` columns/validation never break. Sync Log is audit trail.
4. **No serverless Playwright**: Playwright cannot run on Vercel. Backend stays local.
5. **No emoji spam**: Code comments forbidden. UI emojis only where current app already uses them.
6. **Cross-platform**: Mobile-first Tailwind. iOS Chrome quirks (100dvh, safe-area, 16px input, no hover-only). Test on 375/390/430 px widths.
7. **Lighthouse gates**: Desktop (Perf ≥90, A11y ≥95, BP ≥95, SEO ≥90). Mobile (Perf ≥85, A11y ≥95).

---

## Memory Context (Haiku Should Respect)
Haiku has access to user memory at:  
`C:\Users\USER\AppData\Roaming\Claude\local-agent-mode-sessions\00668878-413c-4d6b-a8cf-1317dbd2e00a\0aaf7a19-baed-4005-ac61-f609403ac5d3\spaces\a75d2cc5-0cc9-4e04-b7c2-045ec6ce012e\memory\`

Key facts:
- User is **TechCraftLab**: Bangkok collector, PSA-graded Japanese Pokémon cards, Excel-first workflow
- **Portfolio**: 19 cards, ~฿198,551 cost basis (mostly PSA 10)
- **Concurrent validation rule**: Per-card agents validate URL match before storing (Collectr layer)
- **Previous work**: Complete portfolio intelligence system (10-sheet Excel, Python engine, REFRESH.bat launcher)

---

## Phases B–E (Haiku Will Execute If Approved)
After Phase A approval, Haiku continues:
- **Phase B**: Quality pass on `templates/index.html` + `webapp.py` (no build step yet)
- **Phase C**: Scaffold `/web` Next.js, tunnel replacement (ngrok/named Cloudflare/Tailscale/localtunnel), Vercel cutover
- **Phase C.1**: Card CRUD (Add/Remove/Restore/Bulk-remove) with soft/hard delete + audit logging
- **Phase C.2**: Search algorithm (EN/JP/fuzzy, ≥25 test fixtures, p99 < 80ms)
- **Phase C.3**: Image fallback chain (6 layers, perceptual-hash validation, layer badges)
- **Phase D**: Repair broken tabs identified in Phase A audit
- **Phase E**: Build 12 skills under `./skills/` (8 original + 4 cross-cutting)

Each phase produces checkpoint summaries. No regressions: `BUILD_EXE.bat` and `REFRESH.bat` must still work.

---

## Final Checkpoint: Haiku Ready?
- [x] Workspace verified (all files readable)
- [x] Python 3.11 + dependencies confirmed
- [x] `start_webapp.bat` runnable (Phase A prerequisite)
- [x] 7 tabs identified + inventory created
- [x] Personas defined
- [x] Non-negotiable constraints listed
- [x] Memory context available
- [x] Handoff document created

**Haiku is ready to start Phase A.**

---

## What to Do Now (User)

1. **Open a fresh conversation** with Claude Haiku (new session, same workspace)
2. **Paste the full handover prompt** (the original one provided to you) as the first message
3. Haiku will immediately begin Phase A:
   - Read the key files listed above
   - Run `start_webapp.bat`
   - Screenshot all 7 tabs
   - Create `WEB_AUDIT_2026Q2.md`
   - Post checkpoint summary
   - Await your approval before Phase B

4. **Approve Phase A** with one line:
   - `go` — if audit recommendations look good
   - `tweak: <specific feedback>` — if Haiku needs to refine the audit

Then Haiku proceeds to Phase B, C, C.1, C.2, C.3, D, E sequentially.

---

**End Handoff Document**
