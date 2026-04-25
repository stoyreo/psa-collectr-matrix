@echo off
REM Phase C.3 — Automated Next.js Setup & Test
REM This script installs dependencies and starts dev server

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════════
echo  Phase C.3 — Next.js Setup & Test
echo ════════════════════════════════════════════════════════════════════
echo.

REM Check if node_modules exists
if exist "node_modules\" (
    echo ✅ Dependencies already installed
    goto :RUN_DEV
)

echo 📦 Installing dependencies (this may take 2-3 minutes)...
echo.
call npm install --legacy-peer-deps
if %errorlevel% neq 0 (
    echo.
    echo ❌ npm install failed. Check error messages above.
    pause
    exit /b 1
)

:RUN_DEV
echo.
echo ════════════════════════════════════════════════════════════════════
echo ✅ Setup complete!
echo ════════════════════════════════════════════════════════════════════
echo.
echo 🚀 Starting Next.js dev server...
echo.
echo    → Visit: http://localhost:3000
echo    → Verify Dashboard loads
echo    → Check browser console for any errors
echo.
echo 📝 Check Flask is running:
echo    → Flask terminal should show: "Running on http://127.0.0.1:5000"
echo.
echo 🔗 Verify ngrok tunnel is active:
echo    → Run: start_tunnel.bat (if not already running)
echo    → Copy ngrok URL to .env.local if it changed
echo.
echo Press Ctrl+C to stop dev server
echo ════════════════════════════════════════════════════════════════════
echo.

call npm run dev
