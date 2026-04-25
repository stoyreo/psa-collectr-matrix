# Vercel Deployment — Quick Start (5 Minutes)

## The Absolute Minimum Steps

### Step 1: Create GitHub Account
If you don't have one: https://github.com/signup

### Step 2: Create Vercel Account
Go to: https://vercel.com/signup → Sign in with GitHub

### Step 3: Push Code to GitHub

```bash
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer"

git init
git add .
git commit -m "Initial commit"
git branch -M main

# Create repo on GitHub at github.com/new
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/psa-matrix.git
git push -u origin main
```

### Step 4: Deploy to Vercel

1. Go to: https://vercel.com/new
2. Click "Continue with GitHub"
3. Find your `psa-matrix` repository
4. Click "Import"
5. Click "Deploy"
6. **Wait 1-2 minutes for build...**
7. Get your live URL: `https://psa-matrix-xxx.vercel.app`

### Done! ✓

Your dashboard is now live at: `https://psa-matrix-xxx.vercel.app`

---

## Share the URL

```
Send this to your team:
https://psa-matrix-xxx.vercel.app
```

Anyone can access it. No login needed. Works on mobile.

---

## Key Endpoints

```
Dashboard:  https://psa-matrix-xxx.vercel.app/
API:        https://psa-matrix-xxx.vercel.app/api/matrix
Health:     https://psa-matrix-xxx.vercel.app/api/health
```

---

## Make Updates

```bash
# Make changes to CSV or code
# Then:
git add .
git commit -m "Update portfolio"
git push origin main

# Vercel auto-redeploys in 1-2 minutes
# Your live URL updates automatically
```

---

## That's It!

No servers to maintain. No uptime to worry about. No cost.

Just push to GitHub → Vercel deploys automatically.

---

## Optional: Custom Domain

Want `matrix.yourdomain.com` instead of `psa-matrix-xxx.vercel.app`?

1. In Vercel dashboard, go to Settings → Domains
2. Add your domain
3. Update DNS (Vercel tells you how)
4. Wait 10 minutes

Done. SSL/TLS included.

---

## Rollback

If something breaks:

```bash
# See all deployments
vercel deployments

# Rollback to previous (in Vercel dashboard)
# Or just fix code and push again
git push origin main
```

---

## Local Testing (Optional)

Want to test before pushing?

```bash
# Install Vercel CLI
npm install -g vercel

# Run locally
vercel dev

# Visit http://localhost:3000
```

---

## Troubleshooting

**"Build failed"**
- Check build logs in Vercel dashboard
- Most common: CSV file not committed to git
- Solution: `git add "My Collection CSV - 19.csv"` and `git push`

**"CSV not found"**
- Same as above

**"Import error"**
- Check `scripts/quantitative_matrix.py` exists and is in git
- Redeploy: `git push origin main`

---

## Support

- Vercel docs: https://vercel.com/docs
- Status page: https://status.vercel.com
- Support: https://vercel.com/support

---

## Summary

```
5 min total:
  2 min - Create accounts
  2 min - Push code
  1 min - Deploy on Vercel

Result:
  ✓ Live, global app
  ✓ Free forever (basically)
  ✓ Auto-scaling
  ✓ 99.9% uptime
  ✓ Your own URL
```

---

**Ready? Start at Step 1 above!**

---

*Vercel Quick Start v1.0*
