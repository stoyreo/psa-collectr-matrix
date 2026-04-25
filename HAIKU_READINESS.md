# Haiku Readiness Check — 2026-04-25

## Workspace Status
✅ **READY FOR PHASE A** (Web Audit)

### Key Files Verified
| File | Lines | Status |
|------|-------|--------|
| `webapp.py` | 1222 | ✅ Entry point, all routes |
| `templates/index.html` | 2803 | ✅ SPA UI with 5 tabs |
| `scripts/config.py` | 294 | ✅ Config + USD→THB rate |
| `scripts/refresh_live.py` | — | ✅ Live fetch logic |
| `scripts/signals.py` | — | ✅ BUY/HOLD/SELL scoring |
| `Portfolio_Master.xlsx` | — | ✅ Source of truth |
| `start_webapp.bat` | — | ✅ Launch script |
| `BUILD_EXE.bat` | — | ✅ PyInstaller build |
| `docs/SYSTEM_BLUEPRINT.md` | — | ✅ Architecture reference |

### Prerequisites Already in Place
- Python 3.11 installed (verify with `python --version`)
- Flask, openpyxl, Playwright, filelock in requirements
- `cloudflared.exe` + `config.yml` active (will replace in Phase C)
- PSA/Collectr/eBay connectors already built
- Add Card feature partially implemented (see `ADD_CARD_PLAN.md`)
- 19-card portfolio in `Portfolio_Master.xlsx`

### Critical Path for Haiku
1. **Phase A**: Run `start_webapp.bat`, screenshot all 5 tabs, audit against the three personas (Engineer / Designer / Investor)
2. **Phase B**: Quality pass on `templates/index.html` + `webapp.py` — no build step yet, vanilla JS only
3. **Phase C**: Scaffold `/web` Next.js app, tunnel replacement, Vercel cutover (assumes Haiku has npm/Node.js available)

### Data to Preserve (Non-Negotiable)
- `Portfolio_Master.xlsx` schema — never break column names or validation
- `Sync Log` sheet — audit trail for all changes
- USD→THB rate: `33.22` (in `scripts/config.py`)
- All existing Playwright/Excel logic (Playwright cannot move to Vercel serverless)

### Environment Variables (.env)
Already exists at workspace root. Haiku will need to:
- Extract all secrets to a `.env.local` file (keep out of git)
- Migrate them to Vercel env vars in Phase C
- Create a `/api/config` endpoint to serve USD→THB rate to the frontend

### Known Quirks
- `cloudflared.exe` runs via `start_remote.bat` — will be replaced with a chosen tunnel in Phase C
- Portfolio refresh is sequential in `REFRESH.bat`, but Collectr fetches must be **concurrent** (see `feedback_collectr_refresh.md` in memory)
- Images have a 6-layer fallback chain (local cache → manual override → PSA → Collectr → eBay → placeholder)

### What Haiku Should NOT Do Yet
- Touch `scripts/` or `Portfolio_Master.xlsx` — Phase B only touches HTML/CSS/JS
- Run PyInstaller — no exe rebuild until Phase D
- Delete or rename `cloudflared.exe` — Phase C does the tunnel swap, documented in `docs/CLOUDFLARE_DECOMMISSION.md`

### Acceptance Gate for Haiku Handoff
✅ WEB_AUDIT_2026Q2.md created with every tab screenshotted and assessed by all three personas
✅ Phase A ends with a `go` / `tweak: ...` approval from the user before Phase B starts

---

**Next Step for User**: Paste the full handover prompt (the one provided) into a **fresh Haiku conversation** in this workspace. Haiku will begin Phase A immediately.
