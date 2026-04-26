@echo off
REM ───────────────────────────────────────────────────────────────────────────
REM PSA × Collectr Tracer — One-Click Launcher
REM Starts Flask backend + ngrok tunnel in parallel, opens Vercel dashboard
REM ───────────────────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  PSA × Collectr Tracer — Full Stack Startup                          ║
echo ║  Starting Flask + ngrok tunnel...                                    ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Step 1: Launch Flask in background
REM ───────────────────────────────────────────────────────────────────────────
echo [1/4] Launching Flask backend...
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

REM ───────────────────────────────────────────────────────────────────────────
REM Step 2: Launch ngrok tunnel in background
REM ───────────────────────────────────────────────────────────────────────────

REM First check if ngrok is installed
where /q ngrok.exe
if errorlevel 1 (
    if not exist "ngrok.exe" (
        echo.
        echo ✗ ERROR: ngrok.exe not found!
        echo.
        echo ngrok is required for this to work. Please install it:
        echo.
        echo  Option 1 - Download directly:
        echo    1. Visit https://ngrok.com/download
        echo    2. Download Windows 64-bit version
        echo    3. Extract ngrok.exe to: %cd%
        echo.
        echo  Option 2 - Package manager:
        echo    • Chocolatey: choco install ngrok
        echo    • Scoop: scoop install ngrok
        echo    • Windows Package Manager: winget install ngrok
        echo.
        echo  Option 3 - Skip ngrok (use snapshot fallback):
        echo    Run START_EVERYTHING_SNAPSHOT_ONLY.bat instead
        echo.
        pause
        exit /b 1
    )
)

echo [2/4] Starting ngrok tunnel to automated-crummiest-puritan.ngrok-free.dev...
start /min cmd /c "RUN_TUNNEL.bat"

REM Wait up to 60 seconds for ngrok to connect (extended for slower networks)
set NGROK_WAIT=0
:wait_ngrok
if %NGROK_WAIT% geq 60 (
    echo.
    echo ✗ ERROR: ngrok failed to connect within 60 seconds
    echo.
    echo Possible causes:
    echo  • Reserved domain requires ngrok Pro account
    echo  • No auth token configured
    echo  • Network connectivity issues
    echo  • ngrok service is down
    echo.
    echo Solutions:
    echo  1. Check ngrok logs: !USERPROFILE!\.ngrok2\ngrok.log
    echo  2. Run DIAGNOSE_NGROK.bat for detailed diagnostics
    echo  3. See https://status.ngrok.com for service status
    echo.
    pause
    exit /b 1
)

curl -s -H "ngrok-skip-browser-warning: 1" https://automated-crummiest-puritan.ngrok-free.dev/api/status >nul 2>&1
if errorlevel 1 (
    timeout /t 1 >nul
    set /a NGROK_WAIT+=1
    goto wait_ngrok
)

echo ✓ ngrok tunnel is active at https://automated-crummiest-puritan.ngrok-free.dev

REM ───────────────────────────────────────────────────────────────────────────
REM Step 3: (Optional) Publish snapshot
REM ───────────────────────────────────────────────────────────────────────────
echo [3/4] Updating snapshot for offline fallback...
python -c "import sys; sys.path.insert(0, 'scripts'); from publish_snapshot import publish_snapshot; publish_snapshot()" 2>nul

REM ───────────────────────────────────────────────────────────────────────────
REM Step 4: Open Vercel dashboard in default browser
REM ───────────────────────────────────────────────────────────────────────────
echo [4/4] Opening dashboard...
start https://psa-collectr-matrix.vercel.app

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  ✓ All systems online!                                               ║
echo ║  Frontend: https://psa-collectr-matrix.vercel.app                   ║
echo ║  Tunnel:   https://automated-crummiest-puritan.ngrok-free.dev       ║
echo ║  Backend:  http://localhost:5000                                    ║
echo ║                                                                       ║
echo ║  Ctrl+C in Flask/ngrok windows to stop. Close when done.            ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

pause
