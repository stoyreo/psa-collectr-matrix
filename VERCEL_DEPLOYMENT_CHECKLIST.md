# Vercel Deployment Checklist

## Pre-Deployment

### Code Preparation
- [ ] `api/matrix.py` exists and works
- [ ] `api/health.py` exists
- [ ] `public/index.html` created
- [ ] `scripts/quantitative_matrix.py` present
- [ ] `My Collection CSV - 19.csv` in project root
- [ ] `vercel.json` configured
- [ ] `requirements.txt` updated with all dependencies
- [ ] `.gitignore` created
- [ ] `.github/workflows/deploy-vercel.yml` created

### Local Testing (Optional)
```bash
# Test API function locally
pip install -r requirements.txt
python -c "from scripts.quantitative_matrix import parse_csv, analyze_cards; print('✓ Import works')"

# Test CSV parsing
python -c "from scripts.quantitative_matrix import parse_csv; cards = parse_csv('My Collection CSV - 19.csv'); print(f'✓ Loaded {len(cards)} cards')"
```

- [ ] Module imports work
- [ ] CSV parsing works
- [ ] 10-criteria scoring works
- [ ] Analysis produces JSON output

---

## Account Setup

### Vercel
- [ ] Created account at https://vercel.com
- [ ] Verified email
- [ ] Connected GitHub account

### GitHub
- [ ] Created GitHub account (if needed)
- [ ] Installed Git CLI
- [ ] Configured git with `git config --global user.name` and `user.email`

---

## Code Deployment

### Step 1: Initialize Git (if needed)
```bash
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer"
git init
```
- [ ] Git initialized

### Step 2: Add All Files
```bash
git add .
```
- [ ] All files staged

### Step 3: Create First Commit
```bash
git commit -m "Initial commit: quantitative matrix + Vercel config"
```
- [ ] Commit created

### Step 4: Create GitHub Repository
1. Go to https://github.com/new
2. Name: `psa-collectr-matrix` (or similar)
3. Description: "Pokémon Card Investment Matrix"
4. Public or Private (your choice)
5. Click "Create repository"
6. **Copy the HTTPS URL** shown

- [ ] Repository created on GitHub

### Step 5: Add Remote & Push
```bash
# Replace with your HTTPS URL from GitHub
git remote add origin https://github.com/YOUR_USERNAME/psa-collectr-matrix.git
git branch -M main
git push -u origin main
```

- [ ] Code pushed to GitHub
- [ ] Can see files at https://github.com/YOUR_USERNAME/psa-collectr-matrix

---

## Vercel Deployment

### Step 1: Import Project
1. Go to https://vercel.com/new
2. Click "Continue with GitHub"
3. Find your repository (`psa-collectr-matrix`)
4. Click "Import"

- [ ] Project selected

### Step 2: Configure Project
Vercel should auto-detect:
- **Framework Preset**: Other
- **Root Directory**: `.` (current)
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: (empty - serverless)

- [ ] Settings look correct

### Step 3: Deploy
Click "Deploy" button

- [ ] Deployment started
- [ ] Watch build logs in browser

Expected build time: 1-2 minutes

### Step 4: Get Live URL
Once deployed, you'll see:
```
Congratulations! Your project has been successfully deployed.
Production: https://psa-collectr-matrix-xxx.vercel.app
```

- [ ] Live URL received
- [ ] Copied and saved URL

---

## Post-Deployment Testing

### Test Dashboard
Open: `https://psa-collectr-matrix-xxx.vercel.app/`

Check:
- [ ] Page loads without errors
- [ ] Summary cards visible (Total, BUY, HOLD, SELL counts)
- [ ] Table shows cards
- [ ] No JavaScript errors (F12 console)

### Test API
Open: `https://psa-collectr-matrix-xxx.vercel.app/api/matrix`

Check:
- [ ] Returns JSON (not HTML error)
- [ ] Contains `timestamp`, `matrix`, `summary` keys
- [ ] Card data is present
- [ ] Confidence scores 50-95

### Test Health Check
Open: `https://psa-collectr-matrix-xxx.vercel.app/api/health`

Check:
- [ ] Returns: `{"status": "healthy", ...}`
- [ ] Timestamp is current

### Test Mobile
- [ ] Open dashboard on phone
- [ ] Responsive layout works
- [ ] Tables scroll properly

---

## Environment Variables (Optional)

If using Claude AI summaries or email notifications:

1. In Vercel dashboard → Project → Settings → Environment Variables
2. Add:
   - `ANTHROPIC_API_KEY` = your key
   - `GMAIL_APP_PASSWORD` = your password

- [ ] Variables set (or skipped if not needed)
- [ ] Redeployed after setting variables

---

## Domain Setup (Optional)

For custom domain like `matrix.yourdomain.com`:

1. In Vercel dashboard → Project → Settings → Domains
2. Add custom domain
3. Update DNS records (follow Vercel instructions)
4. Wait 10-15 minutes for propagation

- [ ] Custom domain added (or skipped)
- [ ] DNS updated (if using custom domain)
- [ ] Custom domain resolves (if applicable)

---

## Sharing & Promotion

### Share with Team
- [ ] Email team the dashboard URL
- [ ] Post in Slack/Teams/etc.
- [ ] Add to shared documents

### Bookmark Dashboard
- [ ] Saved in browser bookmarks
- [ ] Added to password manager

### Enable Auto-Updates
Every git push now deploys automatically:
- [ ] Understand auto-deployment behavior
- [ ] Ready to push updates

---

## Monitoring

### Set Up Alerts (Optional)
1. Vercel dashboard → Project → Monitoring
2. Configure alerts for:
   - [ ] Errors
   - [ ] High latency
   - [ ] Failed deployments

### Check Logs Periodically
```bash
vercel logs api/matrix --tail
```
- [ ] Understand how to view logs

---

## Rollback Plan

If deployment fails:

1. Check Vercel build logs for errors
2. Common issues:
   - [ ] CSV file not in git: Fix with `git add "My Collection CSV - 19.csv"`
   - [ ] Import error: Check `sys.path` in `api/matrix.py`
   - [ ] Missing requirements: Update `requirements.txt`
3. Fix locally and repush:
   ```bash
   git add .
   git commit -m "Fix deployment"
   git push origin main
   ```
   - [ ] Redeployed successfully

---

## Success Criteria

✓ **You're done when:**

- [ ] Dashboard loads at https://your-project.vercel.app
- [ ] Shows correct portfolio data
- [ ] API endpoint returns JSON
- [ ] No errors in browser console
- [ ] Team can access the URL
- [ ] You understand how to push updates
- [ ] You know where to find build logs

---

## Next Steps

After successful deployment:

1. **Share the URL** with team members
2. **Monitor the dashboard** daily
3. **Push updates** when portfolio changes
4. **Check logs** if issues arise
5. **Scale when needed** (Vercel handles auto-scaling)

---

## Maintenance

### Weekly
- [ ] Check dashboard loads correctly
- [ ] Verify API endpoint responds

### Monthly
- [ ] Review Vercel analytics
- [ ] Check usage (should be well within free tier)

### When Updating CSV
```bash
git add "My Collection CSV - 19.csv"
git commit -m "Update portfolio data"
git push origin main
# Vercel auto-deploys in 1-2 minutes
```

---

## Support Resources

| Issue | Resource |
|-------|----------|
| Vercel docs | https://vercel.com/docs |
| Python runtime | https://vercel.com/docs/functions/runtimes/python |
| Deployment failed | Check build logs in dashboard |
| Function timeout | Increase in `vercel.json` maxDuration |
| CORS errors | Check `vercel.json` headers |

---

## Emergency: Go Back to Local

If Vercel doesn't work out, you can revert:

```bash
# Go back to PyInstaller
pyinstaller PSA_Collectr_Tracer.spec
dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
```

Both approaches work independently.

---

**Estimated Time:**
- Setup: 5 minutes
- Deployment: 2 minutes
- Testing: 5 minutes
- **Total: 12 minutes**

---

*Vercel Deployment Checklist v1.0*
*Complete this checklist for successful cloud deployment*
