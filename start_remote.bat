@echo off
title PSA x Collectr Tracer — Remote Access
cd /d "%~dp0"

echo ============================================================
echo   PSA x Collectr Tracer — Remote Access (Cloudflare Tunnel)
echo   Free - no account - no auth token required
echo ============================================================
echo.

:: Install Flask if missing
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Flask...
    python -m pip install flask --quiet
)

:: Install playwright if missing (needed for live data)
python -c "import playwright" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Playwright...
    python -m pip install playwright --quiet
    python -m playwright install chromium
)

:: Install Anthropic SDK if missing (for Claude AI summary)
python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Anthropic SDK...
    python -m pip install anthropic --quiet
)

echo [INFO] Starting server + Cloudflare tunnel...
echo [INFO] Your public URL will appear below in a few seconds.
echo [INFO] Press Ctrl+C to stop everything.
echo.

python start_remote.py

pause
