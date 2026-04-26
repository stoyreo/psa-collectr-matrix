@echo off
REM REFRESH_AND_PUSH.bat — One-click snapshot refresh and deploy
REM Runs the portfolio engine → writes snapshot.json → commits → pushes to Vercel

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================
echo   PSA × Collectr Tracer — Snapshot Refresh & Push
echo ============================================================
echo.

echo [1/3] Building snapshot...
python scripts\build_snapshot.py
if errorlevel 1 (
    echo.
    echo ERROR: Snapshot build failed. Check output above.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Committing to git...
git add web\public\snapshot.json
git commit -m "refresh snapshot %date% %time%" || (
    echo No changes to commit.
)

echo.
echo [3/3] Pushing to Vercel...
git push
if errorlevel 1 (
    echo.
    echo ERROR: Git push failed. Check network and git status.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✓ Done! Vercel will redeploy in ~60 seconds.
echo ============================================================
echo.
pause
exit /b 0
