# Remote Deployment Checklist — Quantitative Matrix

## Pre-Deployment Verification

### Code Changes ✓
- [x] `quantitative_matrix.py` moved to `scripts/` folder
- [x] `webapp.py` updated with new routes
- [x] Import statement updated: `from scripts.quantitative_matrix import ...`
- [x] `PSA_Collectr_Tracer.spec` includes `scripts.quantitative_matrix` in hidden imports
- [x] `templates/quantitative_matrix.html` created and verified
- [x] All imports tested locally and working

### File Locations
```
scripts/quantitative_matrix.py      ✓ Present
templates/quantitative_matrix.html  ✓ Present
My Collection CSV - 19.csv          ✓ Present
webapp.py                           ✓ Updated
PSA_Collectr_Tracer.spec            ✓ Updated
start_remote.py                     ✓ Ready
```

### Local Testing ✓
```bash
# Test imports
python -c "from scripts.quantitative_matrix import parse_csv; print('✓')"
# Result: ✓ Import successful

# Test web app locally
python webapp.py
# Then visit: http://localhost:5000/matrix
# Result: ✓ Dashboard loads with live data
```

---

## Build Steps

### 1. Install Dependencies
```bash
pip install pyinstaller
pip install cloudflared  # For remote tunnel
```

**Status**: Check with `pyinstaller --version`

### 2. Clean Previous Builds
```bash
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer"
rmdir /s /q dist build 2>nul
del PSA_Collectr_Tracer.spec 2>nul
```

**Status**: Verify `dist/` and `build/` folders are gone

### 3. Build Remote Executable
```bash
pyinstaller PSA_Collectr_Tracer.spec
```

**Status**: Watch for completion message:
```
Successfully building executable...
Built to: dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
```

### 4. Verify Build Contents
```bash
# Check executable exists
dir dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe

# Check templates bundled
dir dist\PSA_Collectr_Tracer\_internal\templates\quantitative_matrix.html

# Check CSV included
dir dist\PSA_Collectr_Tracer\My\ Collection\ CSV\ -\ 19.csv
```

**Status**: All three should exist

---

## Local Smoke Test

### 1. Run the Built Executable
```bash
dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
```

**Status**: Should see console output:
```
PSA x Collectr Tracer — Web App
http://localhost:5000
```

### 2. Test Dashboard Route
Open browser: **http://localhost:5000/matrix**

**Status**: 
- [ ] Page loads (not 404 error)
- [ ] Summary cards visible (total cards, BUY/HOLD/SELL counts)
- [ ] Tables load with card data
- [ ] No JavaScript errors (check F12 console)

### 3. Test API Endpoint
```bash
curl http://localhost:5000/api/quantitative-matrix
```

**Status**: Should return valid JSON with:
- `timestamp`
- `matrix` array with card data
- `summary` with counts
- `key_buy_drivers` list
- `risk_flags` list

### 4. Test Filtering
Visit: **http://localhost:5000/matrix**
- [ ] Click filter dropdown
- [ ] Select "BUY" — only BUY cards shown
- [ ] Select "HOLD" — only HOLD cards shown  
- [ ] Select "SELL" — only SELL cards shown
- [ ] Select "" (blank) — all cards shown

---

## Remote Deployment

### 1. Start Cloudflare Tunnel
```bash
python start_remote.py
```

**Status**: Should output:
```
[TUNNEL] Starting cloudflared tunnel...
[TUNNEL] Live URL: https://xxx-xxx-yyy.trycloudflare.com
[EMAIL] Notification sent to recipients
```

### 2. Verify Remote Access
From any device/browser:

**Visit**: `https://xxx-xxx-yyy.trycloudflare.com/matrix`

**Status**:
- [ ] Dashboard loads
- [ ] Live data visible
- [ ] No CORS/security errors
- [ ] Filtering works
- [ ] API endpoint accessible

### 3. Email Notification
Check inbox for:
- **From**: techcraftlab.bkk@gmail.com
- **To**: toy.theeranan@icloud.com, patipat.arc@gmail.com
- **Subject**: PSA × Collectr Tracer — Dashboard Ready
- **Contains**: Live URL + dashboard link

**Status**: [ ] Email received

### 4. Share Remote Link
The live URL format:
```
https://xxx-xxx-yyy.trycloudflare.com/matrix
```

Share with:
- [ ] Team members
- [ ] Advisors
- [ ] Collectors

---

## Monitoring

### Daily
- [ ] Check dashboard loads without errors
- [ ] Verify BUY/HOLD/SELL counts are reasonable
- [ ] Confirm CSV data reflects latest portfolio

### Weekly
- [ ] Review BUY signals (update if any new opportunities)
- [ ] Check performance (should be <2 seconds total)
- [ ] Validate against actual market prices

### Before Major Updates
- [ ] Run local smoke test
- [ ] Rebuild PyInstaller executable
- [ ] Test remote deployment
- [ ] Verify all routes work

---

## Rollback Plan

If something breaks on remote:

### Step 1: Stop Remote Tunnel
```bash
# Kill the cloudflared tunnel process
Ctrl+C in start_remote.py window
```

### Step 2: Check Local Version
```bash
# Verify local still works
python webapp.py
# Visit http://localhost:5000/matrix
```

### Step 3: Debug
```bash
# Check logs in start_remote.py console
# Look for error messages about quantitative matrix
```

### Step 4: Re-deploy
```bash
# Once fixed, rebuild and redeploy
pyinstaller PSA_Collectr_Tracer.spec
python start_remote.py
```

---

## Known Issues & Fixes

### Issue: Dashboard shows 0 cards
**Cause**: CSV file not found in remote deployment
**Fix**: Rebuild with `pyinstaller PSA_Collectr_Tracer.spec`

### Issue: BUY signals never appear
**Cause**: Portfolio is overvalued (not a bug)
**Fix**: Check if actual undervaluation > 20% in any cards

### Issue: Slow API response
**Cause**: CSV parsing takes time for large portfolios
**Fix**: Normal behavior; <2 seconds is expected

### Issue: Template not found error
**Cause**: PyInstaller didn't bundle templates
**Fix**: Run: `pyinstaller --clean PSA_Collectr_Tracer.spec`

---

## Final Verification

Before declaring deployment complete:

```
✓ Code changes applied
✓ PyInstaller build successful  
✓ Local smoke test passed
✓ Remote tunnel active
✓ Dashboard accessible via public URL
✓ API endpoint returns valid JSON
✓ Filtering works
✓ Email notification sent
✓ No console errors
✓ Performance acceptable (<2s response)
```

---

## Success Criteria

Remote deployment is **COMPLETE** when:

1. **Dashboard is live**: `https://xxx.trycloudflare.com/matrix` loads
2. **Data is visible**: All 23 cards show with scores and signals
3. **API works**: `https://xxx.trycloudflare.com/api/quantitative-matrix` returns JSON
4. **No errors**: Console shows no JavaScript or network errors
5. **Email sent**: Recipients received notification with live link

---

## Support

### If Dashboard Doesn't Load
1. Check browser console (F12) for JavaScript errors
2. Check `start_remote.py` console for Flask errors
3. Verify CSV file exists in deployment folder
4. Rebuild PyInstaller executable

### If CSV Data Missing
1. Verify `My Collection CSV - 19.csv` is in project root
2. Check it's readable (Windows file permissions)
3. Rebuild PyInstaller with: `pyinstaller PSA_Collectr_Tracer.spec`

### If Scores Are Wrong
1. Check CSV data is latest version
2. Verify quantitative_matrix.py logic (see QUICKSTART_MATRIX.md)
3. Compare with local testing to isolate issue

---

**Status**: Ready for Remote Build & Deployment

**Next Action**: Run `pyinstaller PSA_Collectr_Tracer.spec`

---

*Deployment Checklist v1.0 — 2026-04-24*
