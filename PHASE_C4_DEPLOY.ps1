# Phase C.4-C.6: Deploy to Vercel + Lighthouse + Grace Period
# Usage: powershell -ExecutionPolicy Bypass -File PHASE_C4_DEPLOY.ps1

Write-Host "═════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Phase C.4-C.6: Vercel Deployment + Lighthouse + Grace Period" -ForegroundColor Cyan
Write-Host "═════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Phase C.4: Deploy to Vercel
Write-Host "📋 PHASE C.4: Deploy to Vercel" -ForegroundColor Yellow
Write-Host ""
Write-Host "Prerequisites:" -ForegroundColor White
Write-Host "  ✓ Git installed"
Write-Host "  ✓ GitHub account with 'PSA x Collectr Tracer' repository"
Write-Host "  ✓ Vercel account (vercel.com)"
Write-Host ""

Write-Host "Step 1: Initialize Git repository" -ForegroundColor Green
Set-Location "PSA x Collectr Tracer"
git init
git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"
git add web/
git commit -m "Phase C.3: Next.js scaffolding complete"
Write-Host "✅ Git repository initialized and committed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Create GitHub repository and push code" -ForegroundColor Green
Write-Host "MANUAL ACTION REQUIRED:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/new"
Write-Host "  2. Repository name: PSA-x-Collectr-Tracer"
Write-Host "  3. Description: Portfolio Intelligence Platform for PSA-Graded Pokemon Cards"
Write-Host "  4. Select 'Public' or 'Private'"
Write-Host "  5. Click 'Create repository'"
Write-Host ""
Write-Host "Then run:" -ForegroundColor Yellow
Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer.git"
Write-Host "  git branch -M main"
Write-Host "  git push -u origin main"
Write-Host ""
Read-Host "Press Enter once you've pushed to GitHub"

Write-Host ""
Write-Host "Step 3: Deploy to Vercel" -ForegroundColor Green
Write-Host "MANUAL ACTION REQUIRED:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://vercel.com/new"
Write-Host "  2. Import 'PSA-x-Collectr-Tracer' repository from GitHub"
Write-Host "  3. Set Project name: psa-collectr-tracer"
Write-Host "  4. Environment Variables:"
Write-Host "     - NEXT_PUBLIC_API_BASE: https://automated-crummiest-puritan.ngrok-free.dev"
Write-Host "     - TRACER_API_KEY: dev-secret-key-change-in-prod"
Write-Host "  5. Click 'Deploy'"
Write-Host "  6. Wait for deployment to complete (2-3 minutes)"
Write-Host ""
Read-Host "Press Enter once deployment is complete and you have the Vercel URL"

Write-Host "✅ Phase C.4 Complete - Vercel deployment live" -ForegroundColor Green
Write-Host ""

# Phase C.5: Lighthouse Audit
Write-Host "📋 PHASE C.5: Lighthouse Audit" -ForegroundColor Yellow
Write-Host ""
Write-Host "Run Lighthouse on your Vercel deployment:" -ForegroundColor Green
Write-Host "  1. Open Chrome DevTools (F12)"
Write-Host "  2. Go to 'Lighthouse' tab"
Write-Host "  3. Click 'Analyze page load'"
Write-Host "  4. Target Scores:"
Write-Host "     - Performance: ≥ 90"
Write-Host "     - Accessibility: ≥ 95"
Write-Host "     - Best Practices: ≥ 95"
Write-Host "     - SEO: ≥ 90"
Write-Host ""
Write-Host "Run on all 4 pages:"
Write-Host "  - Dashboard (/"
Write-Host "  - Portfolio (/portfolio)"
Write-Host "  - Add Card (/add-card)"
Write-Host "  - P&L (/pnl)"
Write-Host ""
Read-Host "Press Enter once Lighthouse audit is complete"

Write-Host "✅ Phase C.5 Complete - Lighthouse audit documented" -ForegroundColor Green
Write-Host ""

# Phase C.6: Grace Period
Write-Host "📋 PHASE C.6: 7-Day Grace Period" -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting 7-day monitoring period..." -ForegroundColor Green
Write-Host ""
Write-Host "Daily checklist (Days 1-7):" -ForegroundColor White
Write-Host "  ☐ Vercel deployment is accessible"
Write-Host "  ☐ Flask backend on localhost:5000 is running"
Write-Host "  ☐ ngrok tunnel is active (https://automated-crummiest-puritan.ngrok-free.dev)"
Write-Host "  ☐ Dashboard loads with portfolio data"
Write-Host "  ☐ No errors in browser console"
Write-Host "  ☐ API calls return 200 status"
Write-Host ""
Write-Host "On Day 8 (2026-05-03):" -ForegroundColor Yellow
Write-Host "  ☐ Verify all systems working correctly"
Write-Host "  ☐ Turn off Cloudflare tunnel (if using)"
Write-Host "  ☐ Keep ngrok tunnel running as permanent HTTPS bridge"
Write-Host ""
Write-Host "✅ Phase C.6: Grace period active" -ForegroundColor Green
Write-Host ""

Write-Host "═════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Phase C.4-C.6 COMPLETE" -ForegroundColor Cyan
Write-Host "Next: Phase D (Tab Repairs) and Phase E (12 Skill Suite)" -ForegroundColor Cyan
Write-Host "═════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
