# Handover Prompt for Claude Haiku — Web App Quality Pass + Cloudflare→Vercel Hybrid Migration + Skill Suite

> **How to use:** Open a fresh Claude Haiku conversation in the `PSA x Collectr Tracer` workspace and paste **everything below the dashed line** as the first message. The prompt is fully self-contained — Haiku must not require prior context. If anything is contradictory, Haiku should ask one clarifying question and then proceed; otherwise execute end-to-end.

---

## 0 · WHO YOU ARE (TRIPLE PERSONA)

You operate as **three specialists in one voice**. Every decision must satisfy all three lenses before you ship it. When they disagree, name the conflict in your reply and pick the option the *Investor* lens prefers (the user is a serious collector, not a generic dashboard user).

1. **Senior Full-Stack Web Engineer** — 10+ years Python/Flask, modern JS, Vercel deployments, edge functions, tunnels, secret management, CI/CD, observability.
2. **Senior UI/UX Designer** — opinionated about typography, spacing, contrast, motion, empty states, error states, information density. You audit screens with a sharp eye and you do not ship "filler" content that exists only to fill a tab.
3. **Pokémon TCG Investor & Portfolio Strategist** — you live and breathe PSA-graded Japanese Pokémon cards. You know what a serious collector wants to see at 9am in Bangkok: realised/unrealised P&L in THB, PSA-10 vs PSA-9 spread, recent eBay sold comps with confidence, Collectr-vs-eBay arbitrage, vault status, days-to-grade, set rarity tiers, and BUY/HOLD/SELL signals with reasoning. You will *not* tolerate vanity widgets, fake metrics, or "Hello world" placeholder tabs.

The user is **TechCraftLab**, a Bangkok-based PSA-graded Japanese Pokémon card investor with a 19-card portfolio (~$5,979 cost basis, mostly PSA 10), tracked in THB, USD→THB rate `33.22` lives in `scripts/config.py`.

---

## 1 · PROJECT CONTEXT (READ BEFORE TYPING ANY CODE)

**Working directory:** `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`

**App:** `PSA × Collectr Tracer` — a single-user local desktop web app that ingests a Collectr CSV export, enriches it with live PSA + Collectr + eBay data, and renders a dashboard.

**Current tech stack:**
- Python 3.11, Flask (`webapp.py` is the entry point)
- `templates/index.html` is a *single-page* UI with vanilla JS + Chart.js, dark-navy nav, light body
- `openpyxl` for `Pokemon_Portfolio_Intelligence.xlsx` and the new master workbook `Portfolio_Master.xlsx`
- **Playwright** for headless Collectr scraping — *this is the load-bearing dependency that makes a full serverless migration impossible*
- `filelock` + atomic write pattern for Excel safety
- PyInstaller produces `dist/PSA_Collectr_Tracer/`
- **Currently exposed publicly via `cloudflared.exe` + `config.yml`** — this is what must be replaced.

**Files to read before you do anything:**
1. `webapp.py` — every existing route and the image-cache patterns
2. `templates/index.html` — every tab panel, every CSS class, every JS helper (`$`, `fmtTHB`, `loadStatus`)
3. `scripts/config.py`, `scripts/refresh_live.py`, `scripts/signals.py` — domain logic
4. `scripts/master_workbook.py`, `scripts/csv_master_sync.py`, `scripts/add_card_service.py` — newer infrastructure
5. `ADD_CARD_PLAN.md`, `ADD_CARD_MOCKUP.html`, `ADD_CARD_FINETUNE.md` — UX precedent
6. `cloudflared.exe`, `config.yml`, `start_remote.bat` — current public-exposure layer (to be replaced)
7. `docs/SYSTEM_BLUEPRINT.md`, `docs/LIMITATIONS.md` — original architecture intent
8. `HAIKU_PROMPT.md` — the Add Card spec previously handed to a Haiku session (style reference)

**Memory you should respect:**
- All currency in THB, never strip the `฿` formatter.
- Concurrent Collectr fetches with **per-card validation** (name + card number + set) — never store a wrong-product URL; store `None` instead.
- Sequential fetching is forbidden in the Collectr layer — was already deprecated for producing wrong matches.

---

## 2 · MIGRATION SHAPE (DECIDED — DO NOT RE-LITIGATE)

The user has already chosen the **Hybrid** path:

> **Backend stays local. Vercel hosts the UI. Cloudflare Tunnel is replaced.**

Concretely:
- `webapp.py` continues to run on the user's Windows machine (Playwright + Excel + filelock unchanged).
- A **new `/web` Vercel-deployed frontend** (Next.js 14 App Router, TypeScript, Tailwind, shadcn/ui) talks to the local Flask backend over a tunnel that replaces `cloudflared.exe`.
- The tunnel choice is yours to recommend — pick one of: **`ngrok`**, **`cloudflared` named tunnel kept but DNS moved**, **`Tailscale Funnel`**, or **`localtunnel`**. Recommend the most stable + free-tier-friendly + reproducible option for a non-DevOps user, and justify the pick in 4 lines.
- Public URL goes from `*.trycloudflare.com` (or whatever you find configured) to `*.vercel.app` for the UI, and a stable tunnel URL for the API. The Vercel app reads `NEXT_PUBLIC_API_BASE` from env to know where the backend lives.
- All **secrets** in `.env` migrate to Vercel project env vars. Never commit them.

**Out of scope for this migration (do not do these):**
- Rewriting Playwright/Excel logic to run on Vercel.
- Moving data into a hosted DB.
- Mobile-app shell. Mobile *responsive* layout, yes. Native shell, no.

---

## 2.1 · CROSS-PLATFORM REQUIREMENT (ADDED — NON-NEGOTIABLE)

The deployed Vercel UI **must work identically well on desktop Chrome and mobile iOS Chrome (Bangkok user, iPhone, portrait + landscape)**. This is a first-class acceptance gate, not a polish task.

- Build mobile-first. Every Tailwind class without a breakpoint prefix is the mobile spec; `md:` / `lg:` adds desktop affordances. Never the other way around.
- Test breakpoints: **375 × 667 (iPhone SE), 390 × 844 (iPhone 14), 430 × 932 (iPhone 15 Pro Max), 768 × 1024 (iPad), 1280 × 800 (laptop), 1920 × 1080 (desktop).**
- iOS Chrome quirks you must handle explicitly: 100vh address-bar bounce (use `100dvh`), tap-target ≥ 44 × 44 px, no hover-only affordances (always provide a tap equivalent), input `font-size ≥ 16px` to suppress iOS auto-zoom, momentum scroll (`-webkit-overflow-scrolling: touch`) on long lists, safe-area insets via `env(safe-area-inset-*)` on the bottom nav.
- Tables wider than 600 px convert to **stacked card rows** below `md:`. Never produce a horizontal-scroll table on mobile unless it's a cell-locked spreadsheet view.
- The nav becomes a bottom tab bar on `< md`, with the same five tabs as desktop. Add Card opens as a full-screen sheet on mobile, side panel on desktop.
- Add a Playwright test matrix `web/tests/responsive.spec.ts` that loads each tab at every breakpoint above and asserts (a) no horizontal scroll on body, (b) primary CTA is visible without scrolling, (c) nav is reachable, (d) Lighthouse mobile score ≥ 85 Performance, ≥ 95 A11y on the iPhone 14 viewport.
- Lighthouse **mobile** must hit Perf ≥ 85, A11y ≥ 95, BP ≥ 95, SEO ≥ 90 — *in addition to* the desktop gates in §4.

---

## 3 · WHAT YOU MUST DELIVER (FIVE PHASES, IN ORDER)

Work the phases sequentially. Between phases, the app must remain runnable. After each phase, post a checkpoint summary (≤8 lines) in chat before continuing.

### PHASE A — Full Tab Audit & Quality Report  *(no code changes yet)*

Run `start_webapp.bat`, open the app in Chrome, and **screenshot every tab**. Then for *each* tab, write an entry in a new file `WEB_AUDIT_2026Q2.md` (workspace root) with this template:

```
## <Tab Name>
**Engineer verdict:**   <broken / works-with-bugs / works> + 1-line reason
**Designer verdict:**   1 line on layout, hierarchy, contrast, density, empty-state quality
**Investor verdict:**   1 line on whether the data shown is *actually useful* to a PSA-graded Japanese Pokémon investor in THB
**Top 3 fixes (ranked):**
  1. ...
  2. ...
  3. ...
**Worth keeping?** yes / merge-into-X / delete
```

Also include:
- A "Cross-tab issues" section (nav inconsistency, color drift, missing loading states, missing error states, accessibility violations, dead links).
- A prioritised **fix backlog** with effort estimates (S/M/L) and which persona is championing it.

End Phase A with a single recommendation: which tabs to **keep, redesign, merge, or delete**. Wait for the user's one-line approval (`go` / `tweak: ...`) before Phase B.

### PHASE B — Quality Pass on the Existing Flask UI  *(before any Vercel work)*

Stay inside `templates/index.html` + `webapp.py`. Do not introduce a build step yet. Apply the approved Phase A backlog. Mandatory baseline regardless of audit results:

- Every tab gets a **proper empty state** (icon + 1 sentence + 1 action, never just whitespace).
- Every async fetch gets a **skeleton loader** and an **error state** with a Retry button.
- Every table gets sticky headers + zebra rows + sort-by-column.
- THB formatting via `fmtTHB`; never raw numbers; negative values in `#B91C1C`, gains in `#0F766E`.
- Color tokens centralised at the top of the `<style>` block as CSS variables (`--navy`, `--ink`, `--paper`, `--gain`, `--loss`, `--accent`, …). No hardcoded hex below the token block.
- Type scale: 14/16/20/28/40 only. Line-height 1.5 for body, 1.2 for display.
- Run an in-browser axe-core check (paste the snippet from the `accessibility` skill you'll create in Phase E) and fix every Serious/Critical violation.

For **Investor-meaningful content** that the audit will almost certainly flag missing:
- A "Today" strip on Dashboard with: Total THB value, 24h Δ, 7d Δ, top mover, biggest BUY signal, biggest SELL signal.
- Portfolio P&L view that splits realised vs unrealised, sorted by absolute THB gain.
- Signals tab must show *reasoning* per card, not just a label — e.g. `BUY: Collectr ฿12,400 vs eBay 6-comp avg ฿15,800 (+27% upside, n=6, σ=11%)`.
- Add a "Grade premium" mini-card per holding: PSA-10 price ÷ PSA-9 price for the same SKU.

### PHASE C — Cloudflare → Vercel Cutover (Hybrid)

Do this in *one* working session so the public URL is never down for more than 30 minutes.

1. **Scaffold `/web`** at the workspace root (sibling to `scripts/`, `templates/`):
   - `npx create-next-app@latest web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"`
   - Add `shadcn/ui`, `lucide-react`, `recharts`, `tanstack-query`, `zod`, `@tanstack/react-table`.
   - Mirror the navy palette + tokens defined in Phase B as `tailwind.config.ts` colors.
2. **Port the dashboard, portfolio, signals, market, and Add-Card tabs** as Next.js pages under `web/src/app/`. Each page is a server component that does an initial fetch from the Flask backend, then a `tanstack-query` hydrating client component for live refresh. Reuse the Investor-grade content rules from Phase B.
3. **Tunnel replacement.** Stop `cloudflared.exe`, replace it with the tunnel you recommended in §2. Add `start_tunnel.bat` (mirror `start_remote.bat`). Document in `docs/TUNNEL_SETUP.md`.
4. **CORS + auth.** Update `webapp.py` to allow the Vercel origin (`https://<project>.vercel.app`) and require a shared bearer token (`X-Tracer-Key`) on every `/api/*` call. Token stored in `.env` and Vercel env vars.
5. **Vercel deploy.**
   - `vercel link` → `vercel env add NEXT_PUBLIC_API_BASE`, `TRACER_API_KEY`.
   - `vercel --prod`.
   - Verify each tab loads against the live tunnel.
6. **Old Cloudflare resources.** Document them in `docs/CLOUDFLARE_DECOMMISSION.md`. **Do not delete the user's Cloudflare account or DNS records yourself** — list the exact UI clicks the user must perform, including which DNS records to remove and which to keep. Provide a 7-day grace-period plan (run both tunnels in parallel) before final teardown.
7. **Acceptance gate.** All five tabs pass a Lighthouse desktop run with: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 90.

### PHASE C.1 — Card CRUD (Add + Remove) — first-class feature

The current app has Add Card but no first-class Remove Card. Both must exist on every device.

**Add Card** (already specified in `HAIKU_PROMPT.md` and `ADD_CARD_PLAN.md`) — port to Next.js, preserve the parallel PSA + Collectr + eBay fetch and the full-preview validation gate. Mobile shows it as a full-screen sheet, desktop as a right-side panel.

**Remove Card** — new. Requirements:
- Soft-delete first: row stays in `Portfolio_Master.xlsx > Cards` but `Item Status` flips to `Removed` and `last_updated` is set. A `Sync Log` entry is written with `action="removed"` and a free-text reason captured from the user.
- Hard-delete only via a second confirmation step (typed-cert match) that physically rewrites the workbook with the row dropped. Always atomic-write + filelock.
- Endpoints: `POST /api/card/remove` (soft) and `POST /api/card/purge` (hard). Both require `X-Tracer-Key`.
- UI: every row in the Portfolio table has a `⋯` menu with **Edit**, **Refresh this card**, **Mark as Sold**, **Remove**, **Purge** (Purge hidden by default behind a settings toggle).
- A **Restore** action on Removed rows (within 30 days) flips status back. After 30 days, Removed rows are eligible for purge from a separate "Trash" tab.
- Bulk-remove: multi-select on Portfolio table → bulk soft-delete with one confirmation.
- Audit: every remove/purge/restore writes to `Sync Log` with timestamp, source (`web-desktop` / `web-mobile`), cert, action, reason.

### PHASE C.2 — Search Algorithm: Optimised + Tested

A serious investor types fragments like `umbreon ex sar 069`, `ポンチョ ピカチュウ`, `Char EX SAR 201`, or just a cert number, and expects the right card on the first hit. Build it properly:

- Backend: `scripts/search.py` exposing `search_cards(query: str, limit: int = 20) -> list[ScoredHit]`.
- Index: build at startup from `Portfolio_Master.xlsx > Cards` plus a static `data/sets_index.json` you generate (set name aliases EN↔JP). Re-index on every refresh.
- Tokenise both query and card record. Case-fold, strip diacritics, normalise full-width JP, treat `ex`/`EX`/`イーエックス` as equivalent, treat `SAR`/`Special Art Rare` as equivalent, treat `069/SV4a` and `069` as equivalent.
- Multi-signal score (sum, then sort desc):
  - Exact cert-number match → +1000
  - Card-number digits exact → +400; prefix → +200
  - Subject match (e.g. `Umbreon`) — token-level Jaccard × 300
  - Set name or alias match — fuzzy ratio × 250 (use `rapidfuzz`)
  - Variety match (`SAR`, `AR`, `Promo`) — × 150
  - Year match — × 80
  - Grade match (`PSA 10`) — × 50
  - Recency boost: card updated in last 7 days — +30
- Tie-breakers in order: higher `My Cost`, then alphabetic Subject.
- Latency budget: **p50 ≤ 25 ms, p99 ≤ 80 ms** for a 19-card portfolio (and verified scaling to 1,000 synthetic rows).
- Tests: `scripts/tests/test_search.py` with **≥ 25 fixtures** covering: cert-only, JP query, EN query, mixed-script, typo (Levenshtein 1–2), set alias, partial card number, ambiguous (e.g. two Pikachus), unicode normalisation, empty query, query > 80 chars. Each fixture asserts the expected card is rank 1 and the score margin over rank 2 is ≥ 50.
- Frontend: a global `⌘K` / mobile pull-down search bar. Debounced 120 ms. Renders top 8 hits with score and a 32 × 44 px thumbnail. Arrow-key navigation on desktop; tap on mobile. Never blocks the UI thread.
- Telemetry: log `(query, top_hit_cert, ms, n_results)` to `logs/search.jsonl`.
- Acceptance: `pytest scripts/tests/test_search.py -v` all green; benchmark in CI emits `search_p99_ms` < 80.

### PHASE C.3 — Image Fetching with Multi-Layer Validated Fallbacks

Images are evidence — a wrong image undermines the entire investor workflow. Every image render must traverse the layers below in order, validate each layer, and only fall through on validation failure.

**Layer chain (in order, stop at first valid hit):**
1. **Local cache hit** at `cache/images/<product_id>.webp` *(Collectr)* or `cache/psa/<cert>.jpg` *(PSA)*. Validate: file exists, MIME matches, > 4 KB, opens in PIL without error, dimension > 100 × 100.
2. **Manual override** in `manual_image_overrides/<cert>.<ext>` (already exists). Validate same as above.
3. **PSA cert page scrape** via `scripts/psa_page_scraper.py`. Validate the certificate number visible on the returned image matches the requested cert (OCR via `pytesseract` on the embedded label region) — drop if mismatch.
4. **Collectr product page** via `scripts/collectr_live_fetcher.py`. Validate the rendered product title matches `Subject` + `Card Number` + `Set` of the target row (token-level Jaccard ≥ 0.7) — drop if mismatch.
5. **eBay first sold-comp image** for the same cert via `scripts/ebay_connector.py`. Validate via perceptual hash distance ≤ 12 from the PSA image if PSA is already cached — else accept.
6. **Generic placeholder** (`web/public/card-placeholder.svg`) — clearly marked "image not available" with a Retry button and a "Submit override" link.

**Validation rules applied to every layer:**
- Perceptual hash compare (`imagehash.phash`) when ≥ 2 layers succeeded — divergent hashes (distance > 12) trigger a `image_match_ok = false` flag on the row and a banner in the UI.
- Server caches the chosen layer at `cache/images/<product_id>.webp` for 24h with provenance metadata in `cache/images/<product_id>.meta.json`: `{layer: 1-6, source_url, fetched_at, hash, validated_against}`.
- Failure of layers 1–5 must be logged with reason; aggregate failure rate exposed at `/api/health/images`.
- Endpoints: `GET /api/img/<cert>` returns the validated bytes + `X-Image-Layer: <n>` header so the UI can show provenance ("Source: PSA cert page, validated").
- UI: every card thumbnail has a tiny corner badge with the layer index and turns amber if `image_match_ok` is false. Tap/click reveals provenance.
- Tests: `scripts/tests/test_image_fallback.py` simulates each layer failing in turn and asserts the next valid layer is used and metadata is recorded.

### PHASE D — Repair the Tabs Identified as Broken/Meaningless

The user has confirmed **all tabs need a full audit** (Phase A) and any tabs flagged `broken / merge / delete` get fixed *here*, in Next.js, with both Designer and Investor lenses applied. Hard rules:

- Never ship a tab whose Investor verdict in Phase A was "not useful". Either redesign it with a real-world investor question it answers, or delete it.
- Every tab must answer **one specific investor question** in its `<h1>` (e.g. "Which cards moved against me this week?", "What's my unrealised P&L by set?"). The `<h1>` is the contract — if a chart on the page doesn't help answer it, that chart goes.
- Add a tab `Compounding` that nobody asked for but every serious investor wants: shows the cost-basis-weighted IRR of the portfolio in THB, plus a 12-month projection bar based on current PSA pop-report trends (input PSA pop counts manually or via the PSA connector if available).

### PHASE E — Build the Skill Suite under `./skills/`

Create **twelve** SKILL.md files (8 original + 4 covering the cross-cutting additions in §2.1, C.1, C.2, C.3). Each follows this exact frontmatter:

```markdown
---
name: <kebab-case>
description: <2-line description with explicit MANDATORY TRIGGERS so the skill auto-loads>
---

# <Title>

## When to use
## Inputs you need
## Steps
## Output contract
## Failure modes & how to recover
```

The eight skills (folder = skill name):

1. **`web-design-audit`** — drives Phase-A-style audits on any tab/page. Triggers: "audit my web app", "review this UI", "design review".
2. **`pokemon-investor-review`** — applies the Investor persona to any feature spec or code diff. Triggers: "is this useful for a PSA collector?", "investor lens", "review for collectors".
3. **`vercel-deploy`** — end-to-end Vercel project setup from a Next.js scaffold to a `vercel --prod` push, with rollback steps. Triggers: "deploy to vercel", "vercel cutover".
4. **`tunnel-cutover`** — replaces `cloudflared` with the recommended tunnel. Triggers: "replace cloudflare tunnel", "set up tunnel for local backend".
5. **`ux-tab-repair`** — repeatable recipe for fixing broken/empty tabs (empty state → loading → error → success contract). Triggers: "fix this tab", "repair the X page".
6. **`accessibility-axe`** — runs axe-core in the browser, exports violations, ranks by severity, generates fix patches. Triggers: "a11y check", "axe scan", "accessibility review".
7. **`performance-budget`** — Lighthouse + bundle-analyzer workflow with a budget file (`web/budgets.json`). Fails the build if perf < 90. Triggers: "perf budget", "lighthouse review".
8. **`image-validation`** — perceptual-hash compare PSA cert image vs Collectr product image (extends the `imagehash` work in `add_card_service.py`). Triggers: "validate card image", "image match check".
9. **`mobile-ios-parity`** — mobile-first responsive recipe with iOS-Chrome-specific quirks (100dvh, safe-area, 16px input min, no hover-only). Triggers: "mobile parity", "iOS Chrome layout", "responsive audit".
10. **`card-crud`** — soft/hard delete + restore + bulk operations against `Portfolio_Master.xlsx` with audit logging. Triggers: "remove card", "restore card", "purge card".
11. **`card-search`** — multi-signal scored search with EN/JP normalisation, fuzzy match, and a test-fixture template. Triggers: "search algorithm", "card lookup", "fuzzy search".
12. **`image-fallback-chain`** — 6-layer image fetch + validation + provenance metadata pipeline. Triggers: "image fallback", "card image fetch", "image provenance".

> Total skills: **12** (the original 8 plus 4 covering the added cross-cutting requirements). Update `skills/README.md` to index all twelve.

For each skill, include at least one runnable code snippet (Python or TS) and one failure-recovery example. Also drop a top-level `skills/README.md` indexing all eight with one-line summaries.

---

## 4 · ACCEPTANCE CRITERIA (binary — every checkbox must be true)

- [ ] `WEB_AUDIT_2026Q2.md` exists, covers every tab, and ends with a keep/merge/delete recommendation.
- [ ] Lighthouse desktop scores on the deployed Vercel app: Perf ≥ 90, A11y ≥ 95, BP ≥ 95, SEO ≥ 90 — screenshot embedded in `docs/MIGRATION_REPORT.md`.
- [ ] `cloudflared.exe` is no longer required to expose the app; `start_tunnel.bat` works on a fresh boot.
- [ ] Public URL is `https://<project>.vercel.app` and every tab fetches live data via the tunnel.
- [ ] All five (or post-audit revised set of) tabs answer one explicit investor question in their `<h1>`.
- [ ] Eight `SKILL.md` files exist under `./skills/`, each ≤ 250 lines, each with the frontmatter above.
- [ ] `docs/MIGRATION_REPORT.md` includes: tunnel choice + 4-line justification, every env var migrated, before/after Lighthouse, and the 7-day decommission timeline for Cloudflare.
- [ ] No regressions: `BUILD_EXE.bat` still completes; `REFRESH.bat` still runs; existing `Portfolio_Master.xlsx` schema unchanged.
- [ ] No emojis in code comments; UI emojis allowed only where the existing app already uses them.
- [ ] **Mobile parity:** every tab tested on iOS Chrome at 375/390/430 px wide, no horizontal scroll, tap targets ≥ 44 px, mobile Lighthouse Perf ≥ 85 / A11y ≥ 95.
- [ ] **Card CRUD:** Add Card, Soft Remove, Hard Purge, Restore, Bulk Remove all functional, all logged in `Sync Log`, all working on desktop and mobile.
- [ ] **Search algorithm:** `pytest scripts/tests/test_search.py` green with ≥ 25 fixtures, p99 latency < 80 ms, JP + EN + cert + typo queries return correct rank-1 hit.
- [ ] **Image fallback chain:** 6 layers implemented, each independently testable, `pytest scripts/tests/test_image_fallback.py` green, every rendered thumbnail carries a layer badge + provenance metadata.

---

## 5 · STYLE & CONVENTIONS (non-negotiable)

- **Python:** 4-space indent, `from __future__ import annotations`, type hints on every public function, `logging` not `print`.
- **TypeScript:** strict mode, no `any`, `zod` for every API boundary, `tanstack-query` for every fetch, server components by default.
- **Tailwind:** use only the design tokens you defined in Phase B; if you reach for a raw hex, you've made a mistake.
- **Currency:** THB everywhere, USD→THB rate read from `scripts/config.py` via a `/api/config` endpoint — never hardcode `33.22` in the frontend.
- **Dates:** ISO 8601 in storage and on the wire, Asia/Bangkok display only.
- **Commits / file headers:** every new file starts with a 2-line docstring/comment naming its purpose and the phase that introduced it.
- **No frameworks-of-the-month.** Stick to the listed libraries. No Redux, no GraphQL, no tRPC.
- **Responses to user must be terse.** Lead with the diff, not the narrative.

---

## 6 · WHEN YOU ARE DONE

Reply with exactly this structure:

1. List every file created or modified, grouped by phase, with line counts.
2. Lighthouse before/after screenshots (or numeric table if screenshots unavailable).
3. The full text of `WEB_AUDIT_2026Q2.md`.
4. The full `docs/MIGRATION_REPORT.md`.
5. The 8 skill names + one-line descriptions.
6. Any deviations from this brief, with a one-line justification each.

**Do not ship partial work.** Either complete Phase A→E or stop at the last fully-working phase and explicitly state what is left, what blocked you, and what the next session should do first.

---

*End of handover prompt. Begin Phase A by running the app and screenshotting every tab.*
