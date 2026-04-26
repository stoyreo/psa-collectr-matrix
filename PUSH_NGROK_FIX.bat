@echo off
title Push ngrok bypass fix to Vercel
cd /d "%~dp0"

echo ============================================================
echo   Pushing ngrok-skip-browser-warning header fix
echo   File: web/src/lib/api.ts
echo ============================================================
echo.

REM Reset the Linux-side stale lock if present (doesn't matter on Windows)
if exist ".git\index.lock" del /q ".git\index.lock"

git add web/src/lib/api.ts
if errorlevel 1 (
    echo [ERROR] git add failed
    pause
    exit /b 1
)

git commit -m "fix(api): send ngrok-skip-browser-warning to bypass interstitial"
if errorlevel 1 (
    echo [ERROR] git commit failed
    pause
    exit /b 1
)

git push
if errorlevel 1 (
    echo [ERROR] git push failed
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Push complete. Vercel will auto-redeploy in ~30-60s.
echo   Then refresh https://psa-collectr-matrix.vercel.app/
echo ============================================================
echo.
pause
