@echo off
REM Phase C.4: Deploy Next.js frontend to GitHub and Vercel
REM Prerequisites: Git installed, GitHub CLI (gh) optional

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════════
echo  Phase C.4: Deploy to GitHub and Vercel
echo ════════════════════════════════════════════════════════════════════
echo.

REM Step 1: Clean up old git artifacts
if exist ".git" (
    echo 🔄 Cleaning up existing git repository...
    rmdir /s /q .git 2>nul
)

REM Step 2: Initialize git
echo 📦 Initializing git repository...
git init
git config user.name "TechCraftLab"
git config user.email "techcraftlab.bkk@gmail.com"

REM Step 3: Create .gitignore
echo 🔒 Creating .gitignore...
(
    echo # Next.js
    echo node_modules/
    echo .next/
    echo .vercel/
    echo dist/
    echo build/
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
    echo.
    echo # Build artifacts
    echo *.tsbuildinfo
) > .gitignore

REM Step 4: Stage and commit
echo 📝 Committing code...
git add .
git commit -m "Phase C.3-C.4: Next.js portfolio frontend - ready for Vercel"

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Git commit failed. Check git configuration and try again.
    pause
    exit /b 1
)

REM Step 5: Display instructions
echo.
echo ════════════════════════════════════════════════════════════════════
echo ✅ Git initialization complete!
echo ════════════════════════════════════════════════════════════════════
echo.
echo 📋 NEXT STEPS:
echo.
echo 1️⃣  CREATE GITHUB REPOSITORY:
echo    → Go to: https://github.com/new
echo    → Name: PSA-x-Collectr-Tracer
echo    → Click "Create repository"
echo.
echo 2️⃣  ADD REMOTE AND PUSH:
echo    → Copy the HTTPS or SSH URL from GitHub
echo    → Run these commands:
echo       git remote add origin [paste-github-url-here]
echo       git branch -M main
echo       git push -u origin main
echo.
echo 3️⃣  DEPLOY TO VERCEL:
echo    → Go to: https://vercel.com/new
echo    → Import from GitHub
echo    → Set Environment Variables:
echo       NEXT_PUBLIC_API_BASE: https://automated-crummiest-puritan.ngrok-free.dev
echo       TRACER_API_KEY: dev-secret-key-change-in-prod
echo    → Click "Deploy"
echo.
echo 4️⃣  RUN LIGHTHOUSE AUDIT:
echo    → Open Chrome DevTools (F12)
echo    → Lighthouse tab
echo    → Target: Perf ≥90, A11y ≥95, BP ≥95, SEO ≥90
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause
