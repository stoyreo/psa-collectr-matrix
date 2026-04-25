@echo off
REM ───────────────────────────────────────────────────────────────────────────
REM PSA × Collectr Tracer — ngrok Tunnel Launcher
REM
REM This script exposes your local Flask backend (port 5000) to the internet
REM via ngrok, allowing the Vercel frontend to connect over HTTPS.
REM
REM Prerequisites:
REM  1. ngrok.exe downloaded from https://ngrok.com/download
REM  2. Flask app running on port 5000 (start_webapp.bat)
REM  3. .env file created with TRACER_API_KEY
REM
REM ───────────────────────────────────────────────────────────────────────────

echo.
echo [PSA Tracer] Starting ngrok tunnel...
echo.

REM Check if ngrok is available in PATH or project root
where /q ngrok.exe
if errorlevel 1 (
    if exist "ngrok.exe" (
        set NGROK=ngrok.exe
    ) else (
        echo ERROR: ngrok.exe not found in PATH or project root
        echo Please download from https://ngrok.com/download
        pause
        exit /b 1
    )
) else (
    set NGROK=ngrok.exe
)

REM Start ngrok tunnel
REM - Exposed on port 5000 (Flask backend)
REM - Log to stdout so you can see the generated URL
REM - Info log level to show connection details

%NGROK% http 5000 --log=stdout --log-level=info

REM After ngrok starts, you'll see output like:
REM   Session started successfully at https://abc-123-def.ngrok-free.app
REM
REM Next steps:
REM 1. Copy that URL (e.g., https://abc-123-def.ngrok-free.app)
REM 2. Update web\.env.local:
REM    NEXT_PUBLIC_API_BASE=https://abc-123-def.ngrok-free.app
REM 3. Update Vercel environment variables in dashboard
REM 4. Both should use the same URL + token from .env (TRACER_API_KEY)

pause
