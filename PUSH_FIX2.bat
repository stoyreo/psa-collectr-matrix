@echo off
cd /d "%~dp0"
echo Removing root vercel.json (Flask leftover) and pushing...
git rm vercel.json 2>nul
git commit -m "Remove root vercel.json - hybrid deploy uses /web only"
git push
if errorlevel 1 (
    echo Push failed.
    pause
    exit /b 1
)
echo.
echo Done. Vercel will auto-redeploy with Next.js defaults in ~30s.
pause
