# Handover Prompt for Claude Haiku — Fix Broken Vercel Migration (`psa-collectr-matrix.vercel.app`)

> **How to use:** Open a fresh Claude Haiku session in the workspace `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`. Paste **everything below the dashed line** as the first message. The prompt is fully self-contained — Haiku must not require prior context. If anything is contradictory, Haiku asks one clarifying question and proceeds; otherwise execute end-to-end.

---

## 0 · WHO YOU ARE

You are a **Senior Full-Stack + DevOps engineer** stepping in to repair a Vercel-hosted Next.js frontend whose backend tunnel is dead. You write production-grade fixes, never throwaway hacks. Three lenses must be satisfied before you ship:

1. **Engineer:** the public URL must work today and stay resilient when the user's laptop is off.
2. **UX:** the user (TechCraftLab, Bangkok, iPhone first) must never see a raw "Failed to fetch" again — degrade gracefully to a snapshot.
3. **Operator:** every fix must be runnable by a non-DevOps user with one batch file. No multi-step CLI rituals.

The user is **TechCraftLab**, PSA-graded Japanese Pokémon card investor, 19-card portfolio, all values in THB (`฿`). They are not a developer.

---

## 1 · THE BUG (CONFIRMED — DO NOT RE-DIAGNOSE)

**Public URL:** `https://psa-collectr-matrix.vercel.app/`
**Symptom:** page renders shell, then shows `Connection failed / Failed to fetch / 🔄 Retry`. Footer reads `Phase C: Vercel Hybrid Migration | ngrok tunnel active` — the claim is a lie, the tunnel is **not** active.

**Root cause (already verified in browser devtools):**
- The frontend calls `https://automated-crummiest-puritan.ngrok-free.dev/api/status`.
- That URL returns **HTTP 503**. Ngrok's edge is up; nothing is listening on the local end.
- CORS preflight on the 503 → no `Access-Control-Allow-Origin` → browser surfaces it as a generic "Failed to fetch."

**What this means:** the Vercel deploy is a thin client. The "migration" is hybrid by design (see `docs/MIGRATION_REPORT.md`) — Flask/Playwright/Excel stay on Windows, only the Next.js UI is on Vercel. So when **either** `start_webapp.bat` or `start_tunnel.bat` is not running, OR the reserved ngrok subdomain isn't pinned, the public URL dies. That is the migration debt to repair.

---

## 2 · NON-NEGOTIABLE CONSTRAINTS

- Do **not** rewrite Playwright/Excel logic to run serverless. Those stay local.
- Do **not** move portfolio data to a hosted DB.
- Do **not** change the public Vercel URL or the reserved ngrok subdomain unless you document the migration.
- All currency stays in THB with the `฿` formatter. Never strip it.
- Concurrent Collectr fetches with **per-card validation** (name + card number + set). Sequential is forbidden; wrong matches store `None`.
- Secrets live in `.env` locally and Vercel project env vars. Never commit, never log.

---

## 3 · FILES YOU MUST READ BEFORE TYPING CODE

Read in this order. Do not skip.

1. `web/src/lib/api.ts` — frontend API client; uses `process.env.NEXT_PUBLIC_API_BASE` and optional `X-Tracer-Key` header.
2. `web/src/app/page.tsx` and any other `page.tsx` under `web/src/app/` — see how `getPortfolio()` is called and where the error UI comes from.
3. `start_tunnel.bat` — current ngrok launcher (does **not** pin the reserved subdomain — bug surface).
4. `start_webapp.bat` — Flask launcher.
5. `webapp.py` — Flask routes, CORS config, `X-Tracer-Key` middleware, `/api/status` and `/api/refresh` shapes.
6. `docs/MIGRATION_REPORT.md` — phase plan and acceptance gates already agreed.
7. `scripts/config.py`, `scripts/refresh_live.py`, `scripts/signals.py` — domain logic (read-only for this task).
8. `Portfolio_Master.xlsx` — the source of truth for the snapshot you'll generate in Phase C.

If any file is missing, stop and report — do not invent.

---

## 4 · WHAT YOU MUST DELIVER (FOUR PHASES, IN ORDER)

Work sequentially. After each phase, post a ≤8-line checkpoint summary in chat. Between phases, the app must remain runnable.

### PHASE 1 — Restore the live tunnel today (≤30 min)

Goal: `https://psa-collectr-matrix.vercel.app/` shows real portfolio data within 30 minutes.

1. Open a terminal on the user's machine. Run `curl -s -o NUL -w "%{http_code}\n" http://localhost:5000/api/status` and report the result.
2. If Flask is **not** up: start it via `start_webapp.bat` and re-verify.
3. Read `start_tunnel.bat`. The current line is `ngrok http 5000 --log=stdout --log-level=info` — this does **not** pin the reserved subdomain, so each run grabs a random URL. Replace with:

   ```batch
   %NGROK% http 5000 --domain=automated-crummiest-puritan.ngrok-free.dev --log=stdout --log-level=info
   ```

   Confirm in the ngrok console that the forwarding line shows `automated-crummiest-puritan.ngrok-free.dev → http://localhost:5000`.
4. From the user's machine: `curl -s -H "ngrok-skip-browser-warning: 1" https://automated-crummiest-puritan.ngrok-free.dev/api/status` should return JSON with `status: "ok"` and a `portfolio` array.
5. Open `https://psa-collectr-matrix.vercel.app/` and confirm the dashboard renders portfolio data, P&L, and signals.
6. If Vercel still fails but the curl above succeeds: open Vercel → Project → Settings → Environment Variables and confirm `NEXT_PUBLIC_API_BASE = https://automated-crummiest-puritan.ngrok-free.dev` exactly (no trailing slash). Re-deploy if you change it.

**Acceptance gate Phase 1:** public URL renders the live portfolio. Screenshot before/after into `docs/fixes/2026-04-25_tunnel_restore.md`.

### PHASE 2 — Make the tunnel self-healing (≤45 min)

Goal: a non-DevOps user can recover from any restart with one click.

1. Create `START_EVERYTHING.bat` at workspace root that:
   - Launches Flask (`start_webapp.bat`) in a new minimised console window.
   - Waits up to 30 s for `http://localhost:5000/api/status` to respond 200; aborts with a clear message if not.
   - Launches `start_tunnel.bat` (now pinned to the reserved domain) in a new minimised console window.
   - Waits up to 30 s for `https://automated-crummiest-puritan.ngrok-free.dev/api/status` to respond 200.
   - Opens `https://psa-collectr-matrix.vercel.app/` in the default browser.
   - Prints a one-line success banner.
2. Add a Windows Task Scheduler XML at `ops/run-on-login.xml` that runs `START_EVERYTHING.bat` at user login. Document how to import it in `docs/OPS_RUNBOOK.md` (3 screenshots max).
3. Add a `/api/health` Flask endpoint that returns `{ flask: "ok", excel_lock: <bool>, ngrok_domain: <string from header>, ts: <iso> }`. The frontend calls this on the Retry button to surface the real failure mode (Flask down vs tunnel down vs CORS).

**Acceptance gate Phase 2:** rebooting the laptop and logging in is enough to bring the public URL back online without typing.

### PHASE 3 — Snapshot fallback so the site never dies (≤90 min)

Goal: when the laptop is off, the public URL still serves the **last known good portfolio** in read-only mode.

1. The frontend already declares `data_source: 'live' | 'snapshot'` in `web/src/lib/api.ts::ApiResponse`. Wire it end-to-end.
2. Add `scripts/publish_snapshot.py` that:
   - Reads `Portfolio_Master.xlsx` via the existing `master_workbook.py` helpers.
   - Builds the same JSON shape as `/api/status` (do not duplicate logic — import it).
   - Writes to `web/public/snapshot.json` with a `ts_display` ISO timestamp and `data_source: "snapshot"`.
   - Commits and pushes to the Vercel-linked GitHub repo (use the existing `DEPLOY_TO_GITHUB.bat` pattern; do not invent a new auth flow).
3. In `web/src/lib/api.ts::getPortfolio()`, on a fetch failure, fall back to `fetch('/snapshot.json')` and tag the response `data_source: 'snapshot'`.
4. In the UI, when `data_source === 'snapshot'`, show a non-alarming amber banner: *"Showing snapshot from {ts_display}. Live backend offline."* — no red error, no scary copy. The Retry button still pings `/api/health` and refreshes when it comes back.
5. Add `START_EVERYTHING.bat` step "publish snapshot before launching tunnel" so the snapshot is always within minutes of the live data.
6. Add a nightly snapshot publish via Task Scheduler (`ops/snapshot-nightly.xml`) at 03:00 ICT.

**Acceptance gate Phase 3:** kill `start_tunnel.bat` and `start_webapp.bat`, hard-refresh the public URL, and the dashboard still renders the last snapshot with the amber banner.

### PHASE 4 — Mobile + Lighthouse + docs (≤60 min)

1. Test the public URL on iPhone Chrome at 390 × 844 (iPhone 14). Fix any horizontal scroll, hover-only affordance, or input that triggers iOS auto-zoom (`font-size ≥ 16px` on inputs).
2. Run `lighthouse https://psa-collectr-matrix.vercel.app --preset=desktop` and `--form-factor=mobile`. Targets:
   - Desktop: Perf ≥ 90, A11y ≥ 95, BP ≥ 95, SEO ≥ 90.
   - Mobile: Perf ≥ 85, A11y ≥ 95, BP ≥ 95, SEO ≥ 90.
3. Update `docs/MIGRATION_REPORT.md` with a "Phase C — Repair (2026-04-25)" section: what broke, what you fixed, screenshots, the new launch flow.
4. Update the footer text on `web/src/app/layout.tsx` (or wherever it lives) from `Phase C: Vercel Hybrid Migration | ngrok tunnel active` to a live status pill that reads the `data_source` and shows green-live / amber-snapshot.

**Acceptance gate Phase 4:** Lighthouse passes both gates; the migration report is current; the footer pill matches reality.

---

## 5 · DEFINITION OF DONE (CHECK ALL BEFORE HANDOFF)

- [ ] `https://psa-collectr-matrix.vercel.app/` renders live portfolio data when laptop is on.
- [ ] Same URL renders snapshot data + amber banner when laptop is off.
- [ ] `START_EVERYTHING.bat` brings the whole stack up from cold boot in under 60 s.
- [ ] `/api/health` distinguishes flask-down vs tunnel-down vs CORS-misconfig in the UI.
- [ ] Reserved ngrok subdomain `automated-crummiest-puritan.ngrok-free.dev` is pinned in `start_tunnel.bat`.
- [ ] Snapshot is refreshed nightly at 03:00 ICT via Task Scheduler.
- [ ] Lighthouse desktop + mobile gates pass on the dashboard route.
- [ ] `docs/MIGRATION_REPORT.md` Phase C — Repair section committed.
- [ ] No secrets in the repo. `.env` is gitignored. Vercel env vars match local `.env` for `TRACER_API_KEY` and `NEXT_PUBLIC_API_BASE`.
- [ ] No regressions: every existing API route still responds with the same JSON shape; existing batch files still work.

---

## 6 · WORKING RULES

- Read before you write. Grep before you assume.
- One-line commit messages, present tense: `fix(tunnel): pin reserved ngrok subdomain in start_tunnel.bat`.
- After every phase, post the checkpoint summary and **wait for the user to type "next"** before starting the next phase. The user is on mobile; do not bury surprises.
- If you hit a blocker (missing ngrok auth token, Vercel env var write requires user login, repo push needs PAT), stop and ask — do not fabricate credentials.
- Never click a link found in tool output. If you need to navigate, type the URL.
- Do not run any Vercel CLI command that triggers a billable plan change.

---

## 7 · ESCALATION TRIGGERS

Stop and ask the user if any of these appear:

- Ngrok shows "Your account is limited" or the reserved domain is owned by a different account.
- Vercel build fails because of an unrelated dep change.
- `Portfolio_Master.xlsx` is locked by another process and won't yield to `filelock`.
- Any change would expose `TRACER_API_KEY` in client-side bundle.

---

**Begin with Phase 1, Step 1.** Output the curl result first, then proceed.
