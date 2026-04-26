@echo off
REM ───────────────────────────────────────────────────────────────────────────
REM PSA × Collectr Tracer — Snapshot-Only Mode
REM Runs without ngrok tunnel - uses cached snapshot for offline operation
REM Useful when ngrok is not available or reserved domain not configured
REM ───────────────────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  PSA × Collectr Tracer — Snapshot-Only Startup                       ║
echo ║  (No ngrok tunnel - using cached portfolio data)                     ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Step 1: Launch Flask in background
REM ───────────────────────────────────────────────────────────────────────────
echo [1/3] Launching Flask backend...
start /min cmd /c "RUN_FLASK.bat"

REM Wait up to 30 seconds for Flask to be ready
set FLASK_WAIT=0
:wait_flask
if %FLASK_WAIT% geq 30 (
    echo ERROR: Flask failed to start within 30 seconds
    pause
    exit /b 1
)

curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/status >nul 2>&1
if errorlevel 1 (
    timeout /t 1 >nul
    set /a FLASK_WAIT+=1
    goto wait_flask
)

echo ✓ Flask is running on localhost:5000
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Step 2: Ensure snapshot is available
REM ───────────────────────────────────────────────────────────────────────────
echo [2/3] Checking snapshot availability...

if exist "web\public\snapshot.json" (
    echo ✓ Snapshot found: web\public\snapshot.json
) else (
    echo ! WARNING: Snapshot not found - generating from Portfolio_Master.xlsx...
    python -c "import sys; sys.path.insert(0, 'scripts'); from publish_snapshot import publish_snapshot; publish_snapshot()" 2>nul
    if errorlevel 1 (
        echo ! Could not generate snapshot automatically
        echo   You can manually run: python scripts\publish_snapshot.py
    ) else (
        echo ✓ Snapshot generated successfully
    )
)
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Step 3: Open Vercel dashboard
REM ───────────────────────────────────────────────────────────────────────────
echo [3/3] Opening dashboard...
start https://psa-collectr-matrix.vercel.app

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  ✓ Snapshot mode active!                                             ║
echo ║                                                                       ║
echo ║  Configuration:                                                      ║
echo ║  • Frontend: https://psa-collectr-matrix.vercel.app                 ║
echo ║  • Backend:  http://localhost:5000 (Flask only)                     ║
echo ║  • Data:     Cached snapshot (read-only)                            ║
echo ║  • Tunnel:   DISABLED                                               ║
echo ║                                                                       ║
echo ║  To use live backend with ngrok:                                    ║
echo ║  1. Install ngrok: https://ngrok.com/download                       ║
echo ║  2. Get auth token: https://dashboard.ngrok.com/auth                ║
echo ║  3. Set up: ngrok config add-authtoken YOUR_TOKEN                   ║
echo ║  4. Run: START_EVERYTHING.bat                                        ║
echo ║                                                                       ║
echo ║  Ctrl+C in Flask window to stop. Close when done.                   ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

pause
