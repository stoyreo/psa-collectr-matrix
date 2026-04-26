@echo off
title ngrok Tunnel - PSA x Collectr Tracer
cd /d "%~dp0"

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  ngrok Tunnel — PSA × Collectr Tracer                         ║
echo ║  Attempting to establish secure tunnel to localhost:5000     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if ngrok is available in PATH or project root
where /q ngrok.exe
if errorlevel 1 (
    if exist "ngrok.exe" (
        set NGROK=ngrok.exe
    ) else (
        echo ✗ ERROR: ngrok.exe not found!
        echo.
        echo Solution:
        echo  1. Download from: https://ngrok.com/download
        echo  2. Extract ngrok.exe to: %cd%
        echo  3. Or add ngrok to your system PATH
        echo.
        echo For reserved domain support:
        echo  1. Create account at https://ngrok.com
        echo  2. Get auth token from https://dashboard.ngrok.com/auth
        echo  3. Run: ngrok config add-authtoken YOUR_TOKEN
        echo  4. Reserve domain at https://dashboard.ngrok.com/cloud/reserved-domains
        echo.
        pause
        exit /b 1
    )
) else (
    set NGROK=ngrok.exe
)

echo [+] Found ngrok: !NGROK!
echo.

REM Check if config file exists and has auth token
if exist "%USERPROFILE%\.ngrok2\ngrok.yml" (
    echo [+] ngrok config found
    findstr /i "authtoken" "%USERPROFILE%\.ngrok2\ngrok.yml" >nul
    if errorlevel 1 (
        echo [!] WARNING: No auth token configured
        echo     Free tier will use random URLs instead of reserved domain
    ) else (
        echo [+] Auth token configured - using reserved domain
    )
) else (
    echo [!] WARNING: No ngrok auth token - using free tier with random URL
    echo    Get auth token: https://dashboard.ngrok.com/auth
    echo    Set up with: ngrok config add-authtoken YOUR_TOKEN
)

echo.
echo Attempting to start tunnel...
echo.

REM Try to start with reserved domain (will fall back to random if not available)
!NGROK! http 5000 --domain=automated-crummiest-puritan.ngrok-free.dev --log=stdout --log-level=info 2>&1

REM If that fails, fallback to random domain
if errorlevel 1 (
    echo.
    echo [!] Reserved domain failed. Trying random free domain...
    echo.
    !NGROK! http 5000 --log=stdout --log-level=info
)

pause
