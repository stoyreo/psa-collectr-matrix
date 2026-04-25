# Phase A Startup Checklist for Haiku

## Current Tab Inventory (7 tabs)
When you run `start_webapp.bat` and open the app, you'll see these tabs in the nav. Screenshot each one:

1. **dashboard** — Portfolio overview (?)
2. **portfolio** — Card holdings table (?)
3. **add-card** — New card search + PSA/Collectr/eBay lookup (partially implemented)
4. **insights** — Signals + analysis (?)
5. **collectr** — Collectr market data (?)
6. **exceptions** — Edge cases / errors (?)
7. **pnl-performance** — P&L by time period (?)

**Your job in Phase A**: Screenshot each, assess all three personas (Engineer / Designer / Investor), and decide: **keep? merge? redesign? delete?**

## Success Criteria for Phase A
- [ ] `start_webapp.bat` launches without error
- [ ] App accessible at `http://localhost:5000`
- [ ] All 7 tabs load and render (even if partially broken)
- [ ] Screenshots captured for each tab
- [ ] `WEB_AUDIT_2026Q2.md` written with template:
  ```markdown
  ## <Tab Name>
  **Engineer verdict:** <broken/works-with-bugs/works> + 1-line reason
  **Designer verdict:** 1 line on layout/hierarchy/contrast/density
  **Investor verdict:** 1 line on investor utility in THB
  **Top 3 fixes:** ranked by priority
  **Worth keeping?** yes/merge-into-X/delete
  ```
- [ ] A "Cross-tab issues" section (nav bugs, colors, a11y, etc.)
- [ ] A prioritized fix backlog with effort estimates (S/M/L)

## Environment Notes
- **Working directory**: `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`
- **Python**: 3.11 (confirm with `python --version` in the workspace)
- **Dependencies**: All listed in `requirements.txt` (already exists)
- **Live data**: 19-card portfolio in `Portfolio_Master.xlsx`, live Collectr/PSA/eBay prices will fetch on startup
- **Tunnel**: Currently `cloudflared.exe` + `config.yml` (will replace in Phase C)

## Before You Start
1. Verify Python 3.11+ is available
2. Verify `start_webapp.bat` can run without requiring admin
3. Check if any tabs are missing (not all 7 may render if there's a backend error)
4. Note any error messages in the browser console

## What NOT to Do in Phase A
- Do not modify code
- Do not run `BUILD_EXE.bat`
- Do not touch `Portfolio_Master.xlsx` or `scripts/`
- Do not replace `cloudflared.exe` yet (Phase C)

---

**When you're done with Phase A**, post your audit to this document and wait for the user's one-line approval (`go` / `tweak: ...`) before proceeding to Phase B.
