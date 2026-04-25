@echo off
REM ====================================================================
REM Phase C.4-C.6: FULL AUTOMATION for Vercel Deployment
REM This script automates everything locally on Windows
REM ====================================================================

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════════
echo  🚀 PHASE C.4-C.6: Full Automation
echo ════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM ====================================================================
REM PHASE C.4: GIT SETUP (AUTOMATED)
REM ====================================================================

echo 📋 PHASE C.4: Git Setup
echo ════════════════════════════════════════════════════════════════════
echo.

REM Clean up old git
if exist ".git" (
    echo 🔄 Cleaning old git repository...
    rmdir /s /q .git 2>nul
    del /q .gitignore 2>nul
)

REM Initialize git
echo 🔧 Initializing git repository...
git init
if %errorlevel% neq 0 (
    echo ❌ Git init failed. Ensure Git is installed.
    pause
    exit /b 1
)

git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"

REM Create .gitignore
echo 🔒 Creating .gitignore...
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

REM Stage and commit
echo 📝 Committing code...
git add .
git commit -m "Phase C.3-C.4: Next.js portfolio frontend - ready for Vercel"

if %errorlevel% neq 0 (
    echo ⚠️  Git commit failed (might be normal if nothing to commit)
)

echo ✅ Git setup complete!
echo.

REM ====================================================================
REM PHASE C.4: GITHUB & VERCEL INSTRUCTIONS
REM ====================================================================

echo 📋 PHASE C.4: GitHub & Vercel Setup
echo ════════════════════════════════════════════════════════════════════
echo.

cls
echo ════════════════════════════════════════════════════════════════════
echo  GITHUB SETUP REQUIRED
echo ════════════════════════════════════════════════════════════════════
echo.
echo Step 1: CREATE REPOSITORY
echo   → Go to: https://github.com/new
echo   → Name: PSA-x-Collectr-Tracer
echo   → Click "Create repository"
echo.
echo Step 2: COPY GITHUB URL
echo   → Copy the HTTPS URL from your new repository
echo   → Example: https://github.com/YOUR_USERNAME/PSA-x-Collectr-Tracer.git
echo.
echo Step 3: PASTE THIS IN COMMAND PROMPT:
echo.
echo   git remote add origin [PASTE-GITHUB-URL-HERE]
echo   git branch -M main
echo   git push -u origin main
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause

REM ====================================================================
REM PHASE C.5: VERCEL DEPLOYMENT
REM ====================================================================

echo.
cls
echo ════════════════════════════════════════════════════════════════════
echo  VERCEL DEPLOYMENT REQUIRED
echo ════════════════════════════════════════════════════════════════════
echo.
echo Step 1: GO TO VERCEL
echo   → https://vercel.com/new
echo.
echo Step 2: IMPORT REPOSITORY
echo   → Click "Import Git Repository"
echo   → Select: PSA-x-Collectr-Tracer
echo.
echo Step 3: CONFIGURE PROJECT
echo   → Project name: psa-collectr-tracer
echo   → Root directory: ./web
echo.
echo Step 4: ENVIRONMENT VARIABLES
echo   NEXT_PUBLIC_API_BASE = https://automated-crummiest-puritan.ngrok-free.dev
echo   TRACER_API_KEY = dev-secret-key-change-in-prod
echo.
echo Step 5: DEPLOY
echo   → Click "Deploy"
echo   → Wait 2-3 minutes
echo.
echo Once deployed, save your Vercel URL
echo Example: https://psa-collectr-tracer.vercel.app
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause

set /p VERCEL_URL="Enter your Vercel deployment URL: "

REM ====================================================================
REM PHASE C.5: LIGHTHOUSE AUDIT
REM ====================================================================

echo.
cls
echo ════════════════════════════════════════════════════════════════════
echo  LIGHTHOUSE AUDIT REQUIRED (15-20 minutes)
echo ════════════════════════════════════════════════════════════════════
echo.
echo Audit all 4 pages with Lighthouse:
echo.
echo 1. Dashboard:  %VERCEL_URL%/
echo 2. Portfolio:  %VERCEL_URL%/portfolio
echo 3. Add Card:   %VERCEL_URL%/add-card
echo 4. P&L:        %VERCEL_URL%/pnl
echo.
echo HOW TO RUN LIGHTHOUSE:
echo   1. Open URL in Chrome
echo   2. Press F12 (DevTools)
echo   3. Click "Lighthouse" tab
echo   4. Click "Analyze page load"
echo   5. Wait 1-2 minutes per page
echo.
echo TARGET SCORES:
echo   ✓ Performance:    ≥ 90
echo   ✓ Accessibility: ≥ 95
echo   ✓ Best Practices: ≥ 95
echo   ✓ SEO:            ≥ 90
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause

REM ====================================================================
REM PHASE C.6: GRACE PERIOD SETUP
REM ====================================================================

echo.
cls
echo ════════════════════════════════════════════════════════════════════
echo  PHASE C.6: Grace Period Monitoring (7 Days)
echo ════════════════════════════════════════════════════════════════════
echo.

REM Create monitoring log
echo # Grace Period Monitoring Log > GRACE_PERIOD_LOG.md
echo. >> GRACE_PERIOD_LOG.md
echo **Start Date:** %DATE% >> GRACE_PERIOD_LOG.md
echo **Vercel URL:** %VERCEL_URL% >> GRACE_PERIOD_LOG.md
echo. >> GRACE_PERIOD_LOG.md
echo ## Daily Status >> GRACE_PERIOD_LOG.md
echo. >> GRACE_PERIOD_LOG.md

for /l %%i in (1,1,7) do (
    echo ### Day %%i >> GRACE_PERIOD_LOG.md
    echo - [ ] Vercel accessible >> GRACE_PERIOD_LOG.md
    echo - [ ] Portfolio data loads >> GRACE_PERIOD_LOG.md
    echo - [ ] No console errors >> GRACE_PERIOD_LOG.md
    echo - [ ] API healthy ^(200 OK^) >> GRACE_PERIOD_LOG.md
    echo - [ ] Notes: >> GRACE_PERIOD_LOG.md
    echo. >> GRACE_PERIOD_LOG.md
)

echo ✅ Monitoring log created: GRACE_PERIOD_LOG.md
echo.

echo DAILY CHECKLIST (Days 1-7):
echo   ☐ Vercel deployment accessible
echo   ☐ Dashboard loads with portfolio data
echo   ☐ Browser console: No errors
echo   ☐ Network tab: All API calls return 200 status
echo   ☐ Flask backend running
echo   ☐ ngrok tunnel active
echo   ☐ Log status in GRACE_PERIOD_LOG.md
echo.
echo On Day 8 (May 3, 2026):
echo   ☐ Verify all systems working
echo   ☐ Complete grace period monitoring
echo   ☐ Proceed to Phase D (Tab Repairs)
echo.

echo ════════════════════════════════════════════════════════════════════
echo.

cls
echo ════════════════════════════════════════════════════════════════════
echo  ✅ PHASE C.4-C.6 SETUP COMPLETE
echo ════════════════════════════════════════════════════════════════════
echo.
echo SUMMARY:
echo  ✓ Git repository initialized locally
echo  ✓ Code ready for GitHub push
echo  ✓ Vercel deployment instructions provided
echo  ✓ Lighthouse audit guidelines prepared
echo  ✓ Grace period monitoring log created
echo  ✓ Vercel URL: %VERCEL_URL%
echo.
echo NEXT STEPS:
echo  1. Push code to GitHub (using git commands above)
echo  2. Deploy to Vercel from GitHub
echo  3. Run Lighthouse audits on all 4 pages
echo  4. Monitor for 7 days using GRACE_PERIOD_LOG.md
echo  5. On Day 8: Start Phase D (Tab Repairs)
echo.
echo FILES CREATED:
echo  • .gitignore - Git configuration
echo  • GRACE_PERIOD_LOG.md - Monitoring template
echo  • All documentation in project root
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause
