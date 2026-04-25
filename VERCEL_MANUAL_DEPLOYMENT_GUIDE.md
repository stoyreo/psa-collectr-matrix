# Vercel Deployment — Manual Completion Guide

## Status Update
✓ GitHub repository created: https://github.com/stoyreo/psa-collectr-matrix

**Next Steps (Manual):** Push code to GitHub, then import to Vercel

---

## Option 1: Push Code Using GitHub Desktop (Recommended, Easiest)

### Step 1: Download and Install GitHub Desktop
- Go to: https://desktop.github.com/
- Download and install

### Step 2: Clone Your Repository
1. Open GitHub Desktop
2. Click "File" → "Clone Repository"
3. Enter: `stoyreo/psa-collectr-matrix`
4. Choose location (e.g., `C:\Users\USER\Desktop\psa-matrix-clone`)
5. Click "Clone"

### Step 3: Copy Project Files
1. In File Explorer, navigate to:
   ```
   C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer
   ```
2. Copy these folders and files:
   - `api/` folder (matrix.py, health.py)
   - `public/` folder (index.html)
   - `scripts/` folder (quantitative_matrix.py)
   - `My Collection CSV - 19.csv`
   - `vercel.json`
   - `requirements.txt`

3. Paste into your cloned repository folder:
   ```
   C:\Users\USER\Desktop\psa-matrix-clone
   ```

### Step 4: Commit and Push
1. In GitHub Desktop:
   - You'll see all changes listed
   - Add Summary: "Initial commit: Pokémon Card Investment Matrix"
   - Click "Commit to main"
   - Click "Push origin"

2. Done! Your code is now on GitHub

---

## Option 2: Upload Files Manually via GitHub Web

### Step 1: Go to Your Repository
- Navigate to: https://github.com/stoyreo/psa-collectr-matrix

### Step 2: Click "Add file" → "Upload files"

### Step 3: Drag and Drop
1. Create a local folder with:
   - `api/` folder
   - `public/` folder
   - `scripts/` folder
   - `My Collection CSV - 19.csv`
   - `vercel.json`
   - `requirements.txt`

2. Drag this folder onto GitHub's upload area
3. Add commit message: "Initial commit: Pokémon Card Investment Matrix"
4. Commit

---

## Option 3: Using Git Command Line

### Step 1: Open Command Prompt
```
cd "C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer"
```

### Step 2: Initialize and Push
```bash
git init
git config user.name "Chin"
git config user.email "patipat.arc@gmail.com"
git add .
git commit -m "Initial commit: Pokémon Card Investment Matrix"
git branch -M main
git remote add origin https://github.com/stoyreo/psa-collectr-matrix.git
git push -u origin main
```

**Note:** If git push fails, GitHub Desktop (Option 1) is your best alternative.

---

## Part 2: Deploy to Vercel (After Code is in GitHub)

### Step 1: Go to Vercel
- Navigate to: https://vercel.com/new

### Step 2: Import Repository
1. Click "Continue with GitHub"
2. Find and select: `psa-collectr-matrix`
3. Click "Import"

### Step 3: Configure Project
Vercel will auto-detect settings. Confirm:
- **Framework Preset:** Other
- **Build Command:** `pip install -r requirements.txt`
- **Output Directory:** (leave empty)

### Step 4: Deploy
1. Click "Deploy"
2. Wait 1-2 minutes for build to complete
3. Get your live URL: `https://psa-collectr-matrix-xxx.vercel.app`

### Step 5: Test
- Dashboard: `https://psa-collectr-matrix-xxx.vercel.app/`
- API: `https://psa-collectr-matrix-xxx.vercel.app/api/matrix`
- Health: `https://psa-collectr-matrix-xxx.vercel.app/api/health`

---

## Files You Need

All these files are ready in your project folder:

### Essential Files
1. **vercel.json** — Vercel configuration
2. **requirements.txt** — Python dependencies
3. **api/matrix.py** — Main quantitative analysis API
4. **api/health.py** — Health check endpoint
5. **public/index.html** — Dashboard frontend
6. **scripts/quantitative_matrix.py** — Analysis engine
7. **My Collection CSV - 19.csv** — Your portfolio data

---

## Quick Reference

| Step | Method | Time |
|------|--------|------|
| 1. Push to GitHub | GitHub Desktop | 5 min |
| 2. Import to Vercel | Vercel Web UI | 2 min |
| 3. Deploy | Auto | 2 min |
| **Total** | | **9 min** |

---

## Troubleshooting

**"Repository not found"**
- Verify: https://github.com/stoyreo/psa-collectr-matrix exists
- Contains code files (not empty)

**"Build failed in Vercel"**
- Check: `requirements.txt` is present
- Check: `api/matrix.py` and `api/health.py` exist
- Check: `public/index.html` exists
- Check: CSV file is in root directory

**"Import says no repositories"**
- Log out and log back in to Vercel
- Disconnect/reconnect GitHub account
- Try again

---

## Success Indicators

When complete, you'll have:
- ✓ Live dashboard at `https://psa-collectr-matrix-xxx.vercel.app`
- ✓ Portfolio data displayed with BUY/HOLD/SELL signals
- ✓ API endpoint returning JSON
- ✓ No errors in browser console
- ✓ Mobile responsive design working

---

## After Deployment

### Updates
Whenever you change your portfolio CSV:
```bash
git add "My Collection CSV - 19.csv"
git commit -m "Update portfolio"
git push origin main
```
Vercel automatically redeploys in 1-2 minutes.

### Custom Domain (Optional)
In Vercel Dashboard → Settings → Domains:
1. Add your domain (e.g., `matrix.yourdomain.com`)
2. Update DNS settings (Vercel provides instructions)
3. Get automatic SSL/TLS certificate

---

## Support

- **Vercel Docs:** https://vercel.com/docs
- **Python on Vercel:** https://vercel.com/docs/functions/runtimes/python
- **GitHub Help:** https://docs.github.com

---

**Start with Option 1 (GitHub Desktop) — it's the easiest!**
