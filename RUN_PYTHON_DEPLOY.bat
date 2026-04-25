@echo off
REM Phase C.4-C.6: Deployment Automation (Python)

cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════════
echo  Phase C.4-C.6: Vercel Deployment Automation
echo ════════════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo.
    echo Please ensure Python is installed and added to PATH
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found. Starting automation...
echo.

REM Run the Python automation script
python deploy_automation.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Automation script encountered an error
    pause
    exit /b 1
)

echo.
echo ✅ Automation complete!
pause
