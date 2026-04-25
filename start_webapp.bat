@echo off
title PSA x Collectr Tracer — Web App
cd /d "%~dp0"

echo ============================================================
echo   PSA x Collectr Tracer — Web App
echo ============================================================
echo.

:: Install Flask if missing
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Flask...
    python -m pip install flask --quiet
)

:: Install Anthropic SDK if missing (for Claude AI summary)
python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo [INFO] Installing Anthropic SDK...
    python -m pip install anthropic --quiet
)

:: Sync CSV into master workbook
echo [INFO] Syncing CSV into master workbook...
python -c "import sys; sys.path.insert(0,'scripts'); import csv_master_sync; result = csv_master_sync.run(); print(result)"

echo [INFO] Starting server at http://localhost:5000
echo [INFO] Press Ctrl+C to stop.
echo.

:: Open browser after 2-second delay (background)
start /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"

:: Start the Flask app
python webapp.py

pause
