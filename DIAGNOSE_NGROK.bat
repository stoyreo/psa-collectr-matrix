@echo off
REM ───────────────────────────────────────────────────────────────────────────
REM PSA × Collectr Tracer — ngrok Diagnostic Tool
REM Checks ngrok installation, auth token, and tunnel connectivity
REM ───────────────────────────────────────────────────────────────────────────

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  ngrok Diagnostic Tool                                               ║
echo ║  Checking installation, authentication, and connectivity             ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Check 1: ngrok binary availability
REM ───────────────────────────────────────────────────────────────────────────
echo [1/5] Checking ngrok binary...
where /q ngrok.exe
if errorlevel 1 (
    if exist "ngrok.exe" (
        echo ✓ ngrok.exe found in project root
        set NGROK_PATH=%cd%\ngrok.exe
    ) else (
        echo ✗ FAIL: ngrok.exe not found
        echo    Search locations:
        echo    • System PATH
        echo    • Project root: %cd%
        echo.
        echo    Solution: Download from https://ngrok.com/download
        call SETUP_NGROK.bat
        exit /b 1
    )
) else (
    echo ✓ ngrok.exe found in system PATH
    for /f "delims=" %%A in ('where ngrok.exe') do set NGROK_PATH=%%A
)
echo    Path: !NGROK_PATH!
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Check 2: ngrok version
REM ───────────────────────────────────────────────────────────────────────────
echo [2/5] Checking ngrok version...
!NGROK_PATH! --version >nul 2>&1
if errorlevel 1 (
    echo ✗ FAIL: ngrok binary is invalid or corrupted
    echo    Try reinstalling from https://ngrok.com/download
    pause
    exit /b 1
) else (
    !NGROK_PATH! --version
)
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Check 3: ngrok authentication token
REM ───────────────────────────────────────────────────────────────────────────
echo [3/5] Checking ngrok authentication...
if exist "%USERPROFILE%\.ngrok2\ngrok.yml" (
    echo ✓ ngrok config file found
    findstr /i "authtoken" "%USERPROFILE%\.ngrok2\ngrok.yml" >nul
    if errorlevel 1 (
        echo ✗ FAIL: No authtoken in config
        echo    Run: ngrok config add-authtoken YOUR_TOKEN
        echo    Get token: https://dashboard.ngrok.com/auth
        pause
        exit /b 1
    ) else (
        echo ✓ Auth token is configured
    )
) else (
    echo ! WARNING: No ngrok config file found
    echo    ngrok free tier will work but without reserved domains
    echo    For reserved domain, get auth token at: https://dashboard.ngrok.com/auth
    echo    Then run: ngrok config add-authtoken YOUR_TOKEN
)
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Check 4: Flask backend availability
REM ───────────────────────────────────────────────────────────────────────────
echo [4/5] Checking Flask backend...
curl -s -o nul -w "%%{http_code}" http://localhost:5000/api/status >nul 2>&1
if errorlevel 1 (
    echo ! Flask not running (this is OK for ngrok diagnostic)
    echo    Start Flask first: RUN_FLASK.bat
) else (
    echo ✓ Flask backend is running on localhost:5000
)
echo.

REM ───────────────────────────────────────────────────────────────────────────
REM Check 5: Test ngrok tunnel (free domain, no auth required)
REM ───────────────────────────────────────────────────────────────────────────
echo [5/5] Testing ngrok tunnel with free domain...
echo    (This will start a temporary tunnel for 10 seconds)
echo.

timeout /t 2 >nul

REM Start ngrok in background with random free domain
start "ngrok Test" /min cmd /c "!NGROK_PATH! http 5000 --log=stdout --log-level=info"

REM Wait for tunnel to establish
set TUNNEL_WAIT=0
:test_tunnel
if %TUNNEL_WAIT% geq 10 (
    echo ✗ FAIL: Tunnel failed to establish within 10 seconds
    echo    Check your internet connection
    echo    Verify ngrok service is online: https://status.ngrok.com
    taskkill /FI "WINDOWTITLE eq ngrok Test" /T /F >nul 2>&1
    pause
    exit /b 1
)

timeout /t 1 >nul
set /a TUNNEL_WAIT+=1
goto test_tunnel

REM Kill test tunnel
taskkill /FI "WINDOWTITLE eq ngrok Test" /T /F >nul 2>&1

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║  ✓ All ngrok diagnostics passed!                                     ║
echo ║                                                                       ║
echo ║  Next steps:                                                         ║
echo ║  1. Run RUN_FLASK.bat (start Flask backend)                         ║
echo ║  2. Run START_EVERYTHING.bat (full stack startup)                   ║
echo ║                                                                       ║
echo ║  For reserved domain 'automated-crummiest-puritan.ngrok-free.dev':  ║
echo ║  • Requires ngrok Pro account (not free tier)                       │
echo ║  • Visit: https://dashboard.ngrok.com/cloud/reserved-domains       │
echo ║  • Verify it's reserved to your account                            │
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

pause
