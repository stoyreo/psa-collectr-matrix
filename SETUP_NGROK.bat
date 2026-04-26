@echo off
REM ───────────────────────────────────────────────────────────────────────────
REM PSA × Collectr Tracer — ngrok Setup Helper
REM Downloads and installs ngrok if not already available
REM ───────────────────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  ngrok Installation Helper                                           ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM Check if ngrok is already available
where /q ngrok.exe
if not errorlevel 1 (
    echo ✓ ngrok.exe found in PATH
    echo Location:
    where ngrok.exe
    echo.
    pause
    exit /b 0
)

if exist "ngrok.exe" (
    echo ✓ ngrok.exe found in project root
    pause
    exit /b 0
)

echo WARNING: ngrok.exe not found in PATH or project root
echo.
echo ┌─────────────────────────────────────────────────────────────────────┐
echo │  Option 1: Download ngrok from official source (RECOMMENDED)       │
echo │  ───────────────────────────────────────────────────────────────── │
echo │  1. Visit: https://ngrok.com/download                             │
echo │  2. Sign up for free ngrok account                                │
echo │  3. Download ngrok for Windows (64-bit zip)                       │
echo │  4. Extract ngrok.exe to this folder:                             │
echo │     %cd%                                                   │
echo │  5. Get your auth token from: https://dashboard.ngrok.com/auth   │
echo │  6. Run: ngrok config add-authtoken YOUR_TOKEN_HERE              │
echo │  7. Verify reserved domain at: https://dashboard.ngrok.com/cloud │
echo │                                                                     │
echo │  Option 2: Install via Package Manager                            │
echo │  ───────────────────────────────────────────────────────────────── │
echo │  • Chocolatey: choco install ngrok                                │
echo │  • Scoop: scoop install ngrok                                     │
echo │  • Windows Package Manager: winget install ngrok                  │
echo └─────────────────────────────────────────────────────────────────────┘
echo.
echo IMPORTANT:
echo  • Reserved domain 'automated-crummiest-puritan.ngrok-free.dev' requires:
echo    - Valid ngrok Pro/Business account
echo    - OR free tier with domain forwarding enabled
echo  • After installing ngrok, run START_EVERYTHING.bat again
echo.

pause
exit /b 1
