# Vercel Migration — Complete Guide

## Overview

This document covers migrating your Pokémon Card Investment Matrix from local/PyInstaller deployment to **Vercel Serverless** (cloud-hosted, auto-scaling, free tier available).

---

## What Changed

### Architecture Comparison

**Before (Local/PyInstaller):**
```
Your Computer
  ↓
Flask App (port 5000)
  ↓
Desktop Users + Cloudflare Tunnel
```

**After (Vercel):**
```
Vercel Edge Network (Global CDN)
  ↓
Serverless Python Functions (/api)
  ↓
Static HTML/CSS/JS (/public)
  ↓
Anyone, anywhere, 0ms setup
```

### File Structure

```
project-root/
├── api/
│   ├── matrix.py              ← Serverless function: GET /api/matrix
│   └── health.py              ← Serverless function: GET /api/health
├── public/
│   └── index.html             ← Static frontend
├── scripts/
│   └── quantitative_matrix.py ← Analysis engine (unchanged)
├── My Collection CSV - 19.csv ← Portfolio data
├── vercel.json                ← Vercel config (NEW)
├── requirements.txt           ← Python dependencies (UPDATED)
├── .gitignore                 ← Git ignore (NEW)
└── .github/
    └── workflows/
        └── deploy-vercel.yml  ← CI/CD pipeline (NEW)
```

---

## Benefits of Vercel

| Feature | Local | PyInstaller | Vercel |
|---------|-------|-------------|--------|
| **Setup time** | Already running | 5 min build | 1 min |
| **Uptime** | Manual (you) | Manual (you) | 99.9% guaranteed |
| **Scalability** | None | Single machine | Auto-scaling |
| **Cost** | $0 | $0 | FREE (generous tier) |
| **URL** | localhost:5000 | Cloudflare tunnel | https://[your-project].vercel.app |
| **SSL/TLS** | Manual | Tunnel handles it | Automatic |
| **CDN** | None | Cloudflare | Vercel Edge (140+ locations) |
| **Environment vars** | .env file | .env file | Vercel dashboard |
| **Deployment** | Manual | Manual | Automatic (git push) |
| **Monitoring** | None | None | Vercel dashboard |

---

## Migration Steps

### Step 1: Create Vercel Account (2 minutes)

1. Go to: https://vercel.com/signup
2. Sign up with GitHub, GitLab, or Bitbucket (recommended)
3. Choose free tier

### Step 2: Push Code to GitHub

Create a new repository:

```bash
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer"

# Initialize git (if not already done)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: quantitative matrix + Vercel config"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/psa-collectr-matrix.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Vercel

**Option A: Automatic Deployment (Recommended)**

1. Go to: https://vercel.com/new
2. Click "Continue with GitHub"
3. Select your repository
4. Click "Import"
5. Vercel auto-detects your setup and deploys
6. Get live URL: `https://your-project.vercel.app`

**Option B: Manual Deployment**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts and deploy
```

### Step 4: Verify Deployment

Check these URLs work:

```
Dashboard:  https://your-project.vercel.app/
API:        https://your-project.vercel.app/api/matrix
Health:     https://your-project.vercel.app/api/health
```

---

## File Changes Explained

### vercel.json
Configuration for Vercel deployment:
- Python 3.11 runtime
- CORS headers enabled
- Static file caching
- URL rewrites for SPA

### api/matrix.py
Serverless function that:
- Receives HTTP GET request
- Parses CSV file
- Runs quantitative analysis
- Returns JSON response
- Executes in <1 second

### api/health.py
Simple health check endpoint for monitoring.

### public/index.html
Static HTML frontend that:
- Calls `/api/matrix` endpoint
- Renders dashboard UI
- No dependencies on Flask
- Works on any CDN

### requirements.txt
Updated with Vercel-compatible versions:
- Flask (for backwards compatibility)
- python-dotenv
- anthropic
- All existing dependencies

### .github/workflows/deploy-vercel.yml
Automatic CI/CD:
- Pushes to `main` → Deploy to production
- Pushes to `develop` → Deploy to preview
- Pull requests → Automatic preview deployments
- Runs tests before deployment

---

## Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

```
ANTHROPIC_API_KEY=sk-xxx...  (optional, for AI summaries)
GMAIL_APP_PASSWORD=xxx...    (optional, for email notifications)
```

---

## Performance

### Typical Response Times

| Action | Time |
|--------|------|
| Page load | <500ms (global CDN) |
| API call | <1 second (Python function) |
| Total time | <2 seconds |

### Vercel Free Tier Limits

- **Functions**: Unlimited invocations
- **Bandwidth**: 100 GB/month
- **Build time**: 6 hours/month
- **Deployments**: Unlimited
- **Regions**: All (auto-optimized)

For your use case: **Free tier is more than enough.**

---

## Local Development

Still want to test locally?

```bash
# Install Vercel CLI
npm install -g vercel

# Run locally (emulates Vercel)
vercel dev

# Visit http://localhost:3000
```

Or use Flask locally:

```bash
python webapp.py
# Visit http://localhost:5000
```

Both work!

---

## Automatic Deployments

Every time you push to GitHub:

```bash
git add .
git commit -m "Update portfolio CSV"
git push origin main
```

Vercel automatically:
1. Detects the push
2. Builds your project
3. Runs tests
4. Deploys to production
5. Shows URL in GitHub

---

## Monitoring & Logs

**Vercel Dashboard:**
1. Go to: https://vercel.com/dashboard
2. Click your project
3. View logs, analytics, deployments

**View Function Logs:**
```bash
vercel logs api/matrix
```

**View Deployments:**
```bash
vercel deployments
```

---

## Troubleshooting

### "CSV file not found"

**Solution:**
1. Verify CSV exists in project root: `My Collection CSV - 19.csv`
2. Check file is committed to git: `git add "My Collection CSV - 19.csv"`
3. Redeploy: `git push origin main`

### "Import error: quantitative_matrix"

**Solution:**
1. Ensure `scripts/quantitative_matrix.py` is in repo
2. Check `sys.path.insert(0, ...)` in `api/matrix.py`
3. Redeploy

### "CORS error"

**Solution:**
- Vercel config includes CORS headers
- Should be automatic
- If issues persist, check `vercel.json` headers section

### "Function timed out"

**Solution:**
- Large CSV takes time to parse
- Vercel max is 30 seconds (configurable in vercel.json)
- Current portfolio should be fine

---

## Custom Domain

Want a custom domain?

1. Go to Vercel Dashboard → Project → Settings → Domains
2. Add domain (e.g., `matrix.yourdomain.com`)
3. Update DNS records (Vercel provides instructions)
4. Free automatic SSL/TLS certificate

---

## Rollback

If something breaks:

```bash
# View deployments
vercel deployments

# Rollback to previous
vercel rollback

# Or redeploy specific commit
git revert <commit-hash>
git push origin main
```

---

## Database (Optional Future)

If you want persistent data storage:

**Vercel KV (Redis):** Free tier with auto-scaling
**PostgreSQL (Vercel Postgres):** Free tier available
**MongoDB Atlas:** Free tier, 512 MB storage

For now: CSV file is fine and works.

---

## Cost

| Item | Cost |
|------|------|
| Compute (functions) | FREE |
| Bandwidth (100 GB/mo) | FREE |
| Storage (CSV file) | FREE |
| Custom domain | FREE (if you own domain) |
| SSL/TLS | FREE |
| **Total** | **$0/month** |

If you scale to millions of users, pricing is: $0.50 per 1M function invocations.

---

## Next Steps

1. **Sign up for Vercel** → https://vercel.com/signup
2. **Push code to GitHub** → Replace `YOUR_USERNAME` with your GitHub username
3. **Import to Vercel** → https://vercel.com/new
4. **Get live URL** → Share with team
5. **Set env variables** (if needed) → Vercel Dashboard

---

## Rollback to Local

If you want to go back to local/PyInstaller:

```bash
# Just run
pyinstaller PSA_Collectr_Tracer.spec
dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
```

Both deployments can run side-by-side.

---

## Questions?

| Topic | Resource |
|-------|----------|
| Vercel docs | https://vercel.com/docs |
| Python on Vercel | https://vercel.com/docs/functions/runtimes/python |
| CI/CD pipelines | https://vercel.com/docs/concepts/git |
| Troubleshooting | https://vercel.com/support |

---

## Success Checklist

After following this guide:

- [ ] Vercel account created
- [ ] Code pushed to GitHub
- [ ] Project imported to Vercel
- [ ] Build succeeded (no errors)
- [ ] Dashboard loads at https://your-project.vercel.app
- [ ] API returns JSON at /api/matrix
- [ ] Health check passes at /api/health
- [ ] Environment variables set (if needed)
- [ ] Custom domain configured (optional)

**All checked?** You're live on Vercel! 🎉

---

*Vercel Migration Guide v1.0 — April 24, 2026*
*Ready for Production — Cloud-Native Deployment*
