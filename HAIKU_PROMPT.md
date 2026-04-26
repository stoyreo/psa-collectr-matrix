# Haiku Prompt — Ship PSA × Collectr Tracer Live on Vercel (Static, Zero-Ops)

**Paste everything below into a fresh Claude Haiku conversation. It is self-contained.**

---

## ROLE

You are a pragmatic shipping engineer. Your one job: get **PSA × Collectr Tracer** rendering at a working `https://*.vercel.app` URL with **zero backend, zero tunnel, zero CORS**. Static snapshot only. Do not improvise alternative architectures. Do not rebuild features. Ship the minimum.

**Working directory:** `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`

---

## 1 · WHY (read once, then forget)

The current "Failed to fetch" outage has 3 layered causes: local Flask not running, wrong CORS allowlist, and ngrok free-tier interstitial breaking CORS preflight. All three vanish if the frontend stops calling a backend at all and just reads a JSON file shipped with the build. That is the plan. Static snapshot only.

**Do not** implement: paid ngrok, Cloudflare Tunnel, Vercel API proxy route, single-process launcher. Those are explicitly rejected.

---

## 2 · DELIVERABLES

Exactly four artifacts. Nothing more.

1. **`scripts/build_snapshot.py`** — runs the existing portfolio engine in-process, writes one or more JSON files under `web/public/`. No Flask, no network server.
2. **`web/public/snapshot.json`** (and any sibling `*.json` the UI needs) — the actual data the page renders.
3. **Modified frontend** under `web/src/` — every API call replaced with `fetch('/snapshot.json')` (same-origin, static).
4. **`REFRESH_AND_PUSH.bat`** at workspace root — one double-click that runs `build_snapshot.py`, then `git add web/public/*.json`, `git commit -m "refresh snapshot"`, `git push`. That is the entire user-facing ops surface.

Optional but encouraged: move every dead file (`webapp.py`, `RUN_FLASK.bat`, `RUN_TUNNEL.bat`, `start_remote.py`, `start_tunnel.bat`, `start_webapp.bat`, `START_EVERYTHING.bat`) into `_archive/` so they cannot be accidentally launched. Do not delete — just archive.

---

## 3 · HARD CONSTRAINTS

- No Flask running anywhere in the deploy path.
- No tunnels (no ngrok, no cloudflared, no localhost.run).
- No `/api/*` routes in Next.js. No server-side functions. No middleware.
- No environment variables for API URLs. Remove every `NEXT_PUBLIC_API_URL` reference.
- No CORS code. Same-origin fetch only.
- One batch file for the user. Not five.
- Preserve the existing UI look and behavior except the live-refresh button — replace that button's handler with a tooltip that says "Run REFRESH_AND_PUSH.bat to update snapshot."

---

## 4 · STEP-BY-STEP PLAN

Follow this order. Do not skip steps.

**Step 1 — Inventory the contract.**
- Read `webapp.py`. List every route and the JSON shape it returns.
- Read `web/src/` (find the API client, likely `lib/api.ts` or similar). List every URL the frontend hits.
- Confirm the routes and the frontend calls match. If not, the snapshot must cover every URL the frontend actually uses.

**Step 2 — Write `scripts/build_snapshot.py`.**
- Import the same Python functions the Flask routes call. Do not duplicate logic.
- For each endpoint, dump the result to `web/public/<name>.json`. If there's only one endpoint, name it `snapshot.json`. If multiple, mirror the URL path: `/api/cards` → `web/public/cards.json`.
- Pretty-print is fine. UTF-8. No BOM.
- Print a one-line summary of what was written.

**Step 3 — Patch the frontend.**
- Replace every `fetch(API_BASE + '/api/cards')` with `fetch('/cards.json')`.
- Delete the `API_BASE` constant and any env-var lookups.
- If the frontend has a "Refresh" button that re-fetched live data, leave the button visible but make it just re-fetch the static JSON (so the page can be reloaded without a full reload), and add a small caption: "Snapshot — regenerate locally to update."

**Step 4 — Write `REFRESH_AND_PUSH.bat`.**

```bat
@echo off
cd /d "%~dp0"
echo [1/3] Building snapshot...
python scripts\build_snapshot.py || goto :error
echo [2/3] Committing...
git add web/public/*.json
git commit -m "refresh snapshot %DATE% %TIME%" || echo (nothing to commit)
echo [3/3] Pushing...
git push || goto :error
echo Done. Vercel will redeploy in ~60s.
pause
exit /b 0
:error
echo FAILED. See output above.
pause
exit /b 1
```

**Step 5 — Run it once.**
- Execute `python scripts/build_snapshot.py` and confirm `web/public/snapshot.json` exists and is non-empty.
- Run `npm --prefix web run build` (or `pnpm`/`yarn` — match what the repo uses). It must succeed with zero errors.
- `git add`, commit, push.

**Step 6 — Verify on Vercel.**
- Wait for the deploy to finish.
- Open the Vercel URL in a browser.
- Open DevTools → Network. Confirm: only same-origin requests, all 200, no `ngrok`, no `localhost`, no CORS errors in console.
- Confirm the page shows real data, not an empty state.

**Step 7 — Archive the dead files** (only after Step 6 is green).
- `mkdir _archive` and move the files listed in §2.

---

## 5 · VERIFICATION CHECKLIST

Before declaring done, every box must be checked:

- [ ] `web/public/snapshot.json` exists and is > 1 KB.
- [ ] `grep -rEi "ngrok|localhost:5000|NEXT_PUBLIC_API_URL"` over `web/src/` returns zero matches.
- [ ] `npm --prefix web run build` exits 0.
- [ ] Vercel deployment URL loads without "Failed to fetch".
- [ ] DevTools Network tab on the live URL shows only same-origin 200s.
- [ ] DevTools Console shows zero red errors.
- [ ] `REFRESH_AND_PUSH.bat` completes end-to-end on a clean shell.
- [ ] Re-running `REFRESH_AND_PUSH.bat` after editing the CSV produces a new commit and a new deploy with updated numbers.

---

## 6 · WHEN STUCK

- If `build_snapshot.py` blows up because a Flask route relied on Flask context (`request`, `current_app`, etc.), refactor the underlying function to take plain arguments. Do not import Flask in `build_snapshot.py`.
- If a route fetches *live* prices from Collectr/PSA/eBay, that's fine — call those scrapers directly from `build_snapshot.py`. The cost is paid at snapshot-build time, not on every page load.
- If the frontend calls an endpoint you can't easily snapshot (e.g. an image proxy), copy those images into `web/public/img/` at build time and rewrite the URLs.

---

## 7 · OUTPUT FORMAT

When done, reply with exactly:

1. The Vercel URL.
2. A one-line `git log -1 --oneline` of the deploy commit.
3. The verification checklist with every box checked.
4. List of files created, modified, and archived.

No essays. No alternative proposals. No "we could also…". Ship it.

---

*End of prompt. Begin.*
