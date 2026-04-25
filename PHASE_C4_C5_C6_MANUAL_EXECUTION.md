# Phase C.4-C.6: Manual Execution Guide
## Vercel Hybrid Migration - Full Deployment & Monitoring

**Start Date:** April 25, 2026  
**Project:** PSA × Collectr Tracer  
**Objective:** Complete Vercel deployment, Lighthouse audit, and 7-day grace period monitoring

---

## ✅ PRE-EXECUTION CHECKLIST

Before starting, confirm:
- [ ] Project directory: `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer`
- [ ] `/web` folder exists with Next.js 14 frontend
- [ ] `.env.local` in `/web` configured with ngrok URL
- [ ] Flask backend running (execute `start_webapp.bat` if needed)
- [ ] ngrok tunnel active to localhost:5000
- [ ] Git installed on Windows
- [ ] GitHub account ready
- [ ] Chrome browser available

---

## PHASE C.4: GIT SETUP & GITHUB

### Step 1: Initialize Git Repository (Local)

Open **Command Prompt** and navigate to project root:

```cmd
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer"
```

Clean any old git artifacts:
```cmd
rmdir /s /q .git
del .gitignore
```

Initialize git:
```cmd
git init
git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"
```

Create `.gitignore`:
```cmd
(
echo # Next.js
echo node_modules/
echo .next/
echo .vercel/
echo dist/
echo build/
echo *.tsbuildinfo
echo.
echo # Environment
echo .env.local
echo .env.*.local
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
) > .gitignore
```

Stage and commit everything:
```cmd
git add .
git commit -m "Phase C.3-C.4: Next.js portfolio frontend - ready for Vercel"
```

**Expected output:** ✓ Commit message shows files committed

---

### Step 2: Create GitHub Repository

1. Go to: **https://github.com/new**
2. Fill in:
   - Repository name: `PSA-x-Collectr-Tracer`
   - Description: `Next.js portfolio management for PSA-graded Pokemon cards`
   - Visibility: **Public** (or Private if preferred)
3. Click **"Create repository"**

**Important:** Copy the HTTPS URL from the new repository (looks like: `https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer.git`)

---

### Step 3: Push Code to GitHub

Back in Command Prompt, execute (replace GITHUB_URL with your copied URL):

```cmd
git remote add origin https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer.git
git branch -M main
git push -u origin main
```

**Expected output:** ✓ Creates `main` branch, pushes all files to GitHub

---

## PHASE C.5: VERCEL DEPLOYMENT

### Step 1: Set Up Vercel Project

1. Go to: **https://vercel.com/new**
2. Click **"Import Git Repository"**
3. Select your newly created repository: `PSA-x-Collectr-Tracer`

### Step 2: Configure Project Settings

Fill in the deployment form:
- **Project Name:** `psa-collectr-tracer`
- **Root Directory:** Select `./web` (critical!)
- **Build Command:** `npm run build` (default should work)
- **Output Directory:** `.next` (default)

### Step 3: Add Environment Variables

Add these two variables in Vercel's environment section:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_BASE` | `https://automated-crummiest-puritan.ngrok-free.dev` |
| `TRACER_API_KEY` | `dev-secret-key-change-in-prod` |

⚠️ **Important:** These values MUST match your `.env.local` in `/web`

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-3 minutes for deployment to complete
3. Once complete, copy your Vercel URL (looks like: `https://psa-collectr-tracer.vercel.app`)
4. Save this URL - you'll need it for testing and monitoring

**Expected output:** ✓ Green checkmark showing successful deployment

---

## PHASE C.5: LIGHTHOUSE AUDIT

Test all 4 pages using Chrome's Lighthouse tool. **Target scores:**
- Performance: ≥ 90
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 90

### Page 1: Dashboard
1. Open: `https://psa-collectr-tracer.vercel.app/` (replace domain with your Vercel URL)
2. Press **F12** to open DevTools
3. Click the **"Lighthouse"** tab
4. Click **"Analyze page load"**
5. Wait 1-2 minutes for results
6. Screenshot scores or document results

### Page 2: Portfolio
1. Navigate to: `https://psa-collectr-tracer.vercel.app/portfolio`
2. Repeat Lighthouse audit steps above

### Page 3: Add Card
1. Navigate to: `https://psa-collectr-tracer.vercel.app/add-card`
2. Repeat Lighthouse audit steps above

### Page 4: P&L Analysis
1. Navigate to: `https://psa-collectr-tracer.vercel.app/pnl`
2. Repeat Lighthouse audit steps above

### Document Results

Create a file `LIGHTHOUSE_RESULTS.md` with your findings:

```markdown
# Lighthouse Audit Results
**Date:** April 25, 2026
**Vercel URL:** https://psa-collectr-tracer.vercel.app

## Dashboard
- Performance: 95/100 ✓
- Accessibility: 97/100 ✓
- Best Practices: 98/100 ✓
- SEO: 90/100 ✓

## Portfolio
[Results...]

## Add Card
[Results...]

## P&L
[Results...]

## Summary
All pages meet or exceed target scores. Ready for grace period.
```

---

## PHASE C.6: GRACE PERIOD MONITORING (Days 1-7)

**Grace Period:** April 25 - May 2, 2026  
**Cutover Date:** May 3, 2026 (Day 8)

During this period, both Vercel and Flask backends will run in parallel.

### Daily Monitoring Checklist

Create `GRACE_PERIOD_LOG.md` and check daily:

```markdown
# Grace Period Monitoring Log

**Start:** April 25, 2026  
**End:** May 3, 2026 (Cutover Day)  
**Vercel URL:** https://psa-collectr-tracer.vercel.app

## Day 1 (April 25)
- [ ] Vercel deployment accessible and responsive
- [ ] Dashboard loads without errors
- [ ] Portfolio data displays correctly
- [ ] Network requests show 200 OK status
- [ ] Console has no JavaScript errors
- [ ] Flask backend still running independently
- [ ] ngrok tunnel remains active
- **Notes:** All systems operational, grace period begins

## Day 2 (April 26)
- [ ] Vercel still accessible
- [ ] Check API connectivity (console Network tab)
- [ ] Verify no performance degradation
- [ ] Monitor error logs
- **Notes:**

## Day 3 (April 27)
- [ ] Spot check all 4 pages
- [ ] Verify data freshness
- **Notes:**

## Day 4 (April 28)
- [ ] Mid-grace period status check
- **Notes:**

## Day 5 (April 29)
- [ ] Verify no issues accumulated
- **Notes:**

## Day 6 (April 30)
- [ ] Final pre-cutover validation
- **Notes:**

## Day 7 (May 1)
- [ ] All systems stable before cutover
- **Notes:**

## Cutover Day (May 3)
- [ ] Verify Vercel is production-ready
- [ ] Flask backend can be shut down
- [ ] Begin Phase D (Tab Repairs)
```

### How to Check Daily

1. **Access Vercel:** Open `https://psa-collectr-tracer.vercel.app`
2. **Check Dashboard:** Verify portfolio data loads
3. **Open DevTools:** Press F12
4. **Check Console:** Look for red error messages
5. **Check Network:** Verify API calls return 200 status
6. **Update Log:** Record date, status, any issues

### Troubleshooting During Grace Period

| Issue | Solution |
|-------|----------|
| 404 Not Found | Check Vercel deployment status, verify URLs correct |
| API 500 Error | Verify Flask backend running, ngrok tunnel active |
| Slow loading | Check Vercel deployment logs, consider performance |
| Console errors | Take screenshot, note error details in log |

---

## COMPLETION & SIGN-OFF

Once all 7 days complete:

✅ **Phase C.4 Complete**
- Git repository initialized and pushed to GitHub
- Code ready for production

✅ **Phase C.5 Complete**
- Vercel deployment successful
- Lighthouse audit scores meet targets
- Vercel URL: `https://psa-collectr-tracer.vercel.app` (or your custom domain)

✅ **Phase C.6 Complete**
- 7-day grace period monitoring complete
- No critical issues identified
- All systems stable

**Ready for Phase D:** Tab Repairs (20 minutes)

---

## QUICK REFERENCE

### Key Commands

```bash
# Git setup
git init
git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"

# GitHub
git remote add origin [GITHUB_URL]
git push -u origin main

# Check status anytime
git status
git log --oneline
```

### Critical URLs

- **Project Root:** `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer`
- **Next.js Frontend:** `/web`
- **GitHub:** `https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer`
- **Vercel Console:** `https://vercel.com/`
- **Deployed Site:** `https://psa-collectr-tracer.vercel.app`

### Support Files

- `FULL_AUTO_DEPLOY.bat` - Batch script version of this guide
- `GRACE_PERIOD_LOG.md` - Daily monitoring template
- `LIGHTHOUSE_RESULTS.md` - Audit results documentation

---

## SUCCESS CRITERIA ✓

Phase C.4-C.6 is complete when:

1. ✓ Git repository initialized with all code committed
2. ✓ GitHub repository created and code pushed
3. ✓ Vercel deployment successful and accessible
4. ✓ Lighthouse audits run on all 4 pages with target scores met
5. ✓ 7-day grace period monitoring completed without critical issues
6. ✓ Both Vercel and Flask running in parallel successfully
7. ✓ Ready to proceed to Phase D (Tab Repairs)

---

**Next:** Phase D - Tab Repairs (60 minutes)
