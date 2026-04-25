# Phase C.4-C.6: Vercel Deployment, Lighthouse, and Grace Period

**Status:** Ready to Execute  
**Date Created:** 2026-04-25  
**Estimated Duration:** 30-45 minutes (C.4 + C.5), 7 days (C.6)

---

## 📋 Overview

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| C.4.0 | Git initialization | 5 min | ✅ Ready |
| C.4.1 | GitHub repository creation | 5 min | ⏳ Manual |
| C.4.2 | Code push to GitHub | 5 min | ⏳ Manual |
| C.4.3 | Vercel import & deploy | 10 min | ⏳ Manual |
| C.5.0 | Lighthouse audits (4 pages) | 15 min | ⏳ Manual |
| C.6.0 | Grace period monitoring | 7 days | ⏳ Monitoring |

---

## 🚀 QUICK START

### Option A: Automated (Python)
```bash
python deploy_automation.py
```
Guides you through all steps with interactive prompts.

### Option B: Batch File (Windows)
```cmd
DEPLOY_TO_GITHUB.bat
```
Automates local git setup, then provides instructions for cloud deployment.

### Option C: PowerShell Script
```powershell
powershell -ExecutionPolicy Bypass -File PHASE_C4_DEPLOY.ps1
```

---

## ✅ PHASE C.4: Deploy to Vercel

### Step 1: Initialize Git (Automated)
```bash
git init
git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"
git add .
git commit -m "Phase C.3-C.4: Next.js portfolio frontend"
```

### Step 2: Create GitHub Repository (Manual)
1. Go to: https://github.com/new
2. **Repository name:** `PSA-x-Collectr-Tracer`
3. **Description:** Portfolio Intelligence Platform for PSA-Graded Pokemon Cards
4. **Visibility:** Public (recommended)
5. Click **Create repository**

### Step 3: Push Code to GitHub (Manual)
```bash
git remote add origin https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer.git
git branch -M main
git push -u origin main
```
*Note: Replace `YOUR_USERNAME` with your GitHub username*

### Step 4: Deploy to Vercel (Manual)
1. Go to: https://vercel.com/new
2. Click **Import Git Repository**
3. Select **PSA-x-Collectr-Tracer**
4. **Project Settings:**
   - Name: `psa-collectr-tracer`
   - Framework: Next.js
   - Root Directory: `./web`

5. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_BASE = https://automated-crummiest-puritan.ngrok-free.dev
   TRACER_API_KEY = dev-secret-key-change-in-prod
   ```

6. Click **Deploy**
7. Wait 2-3 minutes for build to complete

**Expected Outcome:**
- Vercel deployment live at: `https://psa-collectr-tracer.vercel.app` (or custom domain)
- Dashboard accessible from any network
- Portfolio data loading from Flask backend via ngrok tunnel

---

## ✅ PHASE C.5: Lighthouse Audit

### Audit All Pages
For each page below, run Lighthouse audit:

#### Dashboard: `/`
```bash
# Visit: https://psa-collectr-tracer.vercel.app/
```

#### Portfolio: `/portfolio`
```bash
# Visit: https://psa-collectr-tracer.vercel.app/portfolio
```

#### Add Card: `/add-card`
```bash
# Visit: https://psa-collectr-tracer.vercel.app/add-card
```

#### P&L: `/pnl`
```bash
# Visit: https://psa-collectr-tracer.vercel.app/pnl
```

### Running Lighthouse
1. **Open DevTools:** `F12` in Chrome
2. **Navigate to:** Lighthouse tab
3. **Select Profile:** Mobile (default)
4. **Click:** Analyze page load
5. **Wait:** 1-2 minutes for report

### Target Scores
```
✓ Performance: ≥ 90
✓ Accessibility: ≥ 95
✓ Best Practices: ≥ 95
✓ SEO: ≥ 90
```

### If Scores Below Target
Common optimization opportunities:
- [ ] Image optimization (WebP format, lazy loading)
- [ ] Code splitting (React.lazy for routes)
- [ ] Remove unused CSS
- [ ] Minify JavaScript/CSS
- [ ] Enable gzip compression
- [ ] Cache static assets
- [ ] Reduce Time to Interactive (TTI)

---

## ✅ PHASE C.6: 7-Day Grace Period

### Timeline
- **Start:** Today (2026-04-25)
- **End:** 2026-05-02 (Day 7)
- **Cutover:** 2026-05-03 (Day 8)

### Systems Running in Parallel
During grace period, BOTH must be active:
```
┌─────────────────────────────────────┐
│ Vercel (Production Frontend)         │
│ URL: https://psa-collectr-tracer... │
└──────────────────┬──────────────────┘
                   │
                   ├─ API calls to
                   │
                   ▼
┌─────────────────────────────────────┐
│ ngrok Tunnel                        │
│ https://automated-crummiest-... │
└──────────────────┬──────────────────┘
                   │
                   ├─ Forwards to
                   │
                   ▼
┌─────────────────────────────────────┐
│ Flask Backend (localhost:5000)      │
│ Running on your local machine       │
└─────────────────────────────────────┘
```

### Daily Monitoring Checklist
```
Day 1-7 (2026-04-25 to 2026-05-02):

Daily at 9 AM:
  ☐ Vercel deployment accessible
  ☐ Dashboard loads with portfolio data
  ☐ Browser console: No errors
  ☐ Network tab: All API calls return 200 status
  ☐ Flask backend running (`localhost:5000`)
  ☐ ngrok tunnel active (check dashboard)
  ☐ Log any issues in GRACE_PERIOD_LOG.md

If Issues Found:
  → Check Flask is running: `start_webapp.bat`
  → Check ngrok is running: `start_tunnel.bat`
  → Check .env variables match ngrok URL
  → Review browser console for specific errors
```

### Monitoring Log
Track daily status in: **GRACE_PERIOD_LOG.md**

Example entry:
```markdown
### Day 1 (2026-04-25)
- [x] Vercel accessible (4ms response time)
- [x] Portfolio data loads (5 cards displayed)
- [x] No console errors
- [x] API healthy (200 OK)
- Notes: All systems operational, no issues
```

### Cutover Checklist (Day 8: 2026-05-03)
```
Before decommissioning any tunnels:

☐ All 7 days completed successfully
☐ No production issues reported
☐ All 4 pages tested on mobile + desktop
☐ Lighthouse scores documented
☐ User confirmed system is stable

Decommission (if applicable):
  ☐ Turn off Cloudflare tunnel (if using)
  ☐ Keep ngrok tunnel as permanent HTTPS bridge
  ☐ Archive old Cloudflare tunnel logs
  ☐ Update documentation with final architecture
```

---

## 🎯 Success Criteria

### C.4: Vercel Deployment
✅ Vercel deployment URL is live  
✅ All 4 tabs load without errors  
✅ Portfolio data displays correctly  
✅ Navigation between pages works  

### C.5: Lighthouse Audit
✅ Desktop Performance ≥ 90 (or optimized to target)  
✅ Mobile Accessibility ≥ 95 (or optimized to target)  
✅ Best Practices ≥ 95 (or optimized to target)  
✅ SEO ≥ 90 (or optimized to target)  

### C.6: Grace Period
✅ 7 consecutive days of successful operation  
✅ No production-blocking issues  
✅ Both Flask + Vercel accessed successfully  
✅ ngrok tunnel remained stable  
✅ Final cutover completed safely  

---

## 📝 Next: Phase D & E

After C.6 completion:
- **Phase D:** Tab Repairs (20 min)
  - Add sticky headers to Portfolio
  - Implement grade premium column
  - Split P&L (realized vs unrealized)

- **Phase E:** 12 Skill Suite (60 min)
  1. web-design-audit
  2. pokemon-investor-review
  3. vercel-deploy
  4. tunnel-cutover
  5. ux-tab-repair
  6. accessibility-axe
  7. performance-budget
  8. image-validation
  9. mobile-ios-parity
  10. card-crud
  11. card-search
  12. image-fallback-chain

---

## 🆘 Troubleshooting

### "Failed to fetch" Error
**Cause:** Flask not running or ngrok URL changed  
**Fix:**
1. Check Flask: `start_webapp.bat`
2. Check ngrok: `start_tunnel.bat`
3. Update `.env.local` with new ngrok URL

### Lighthouse Scores Low
**Cause:** Missing image optimization, large bundles  
**Fix:**
1. Enable Next.js Image Optimization
2. Implement code splitting
3. Minify assets
4. Enable compression

### ngrok URL Changed (Free Tier)
**Cause:** Free tier resets daily  
**Fix:**
1. Get new URL from ngrok dashboard
2. Update: `.env.local`, Vercel dashboard, Flask reference
3. Restart dev server: `npm run dev`

---

**Created:** 2026-04-25  
**Phase Status:** Ready for execution  
**Automation Scripts:** Available in project root
