@echo off
cd /d "%~dp0"
echo Pushing dep fix (web/.npmrc legacy-peer-deps=true)...
git add web/.npmrc
git commit -m "Fix: legacy-peer-deps for lucide-react vs React 19"
git push
if errorlevel 1 (
    echo Push failed.
    pause
    exit /b 1
)
echo.
echo Done. Vercel will auto-redeploy in ~30s.
pause
