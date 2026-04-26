@echo off
title Push Vercel proxy fix
cd /d "%~dp0"

echo ============================================================
echo   Pushing Vercel server-side proxy for ngrok backend
echo   - web/src/app/api/[...path]/route.ts  (new proxy)
echo   - web/src/lib/api.ts                  (use same-origin)
echo ============================================================
echo.

if exist ".git\index.lock" del /q ".git\index.lock"

git add "web/src/app/api/[...path]/route.ts" "web/src/lib/api.ts"
if errorlevel 1 (echo [ERROR] git add failed & pause & exit /b 1)

git commit -m "fix(api): add Vercel same-origin proxy for ngrok backend"
if errorlevel 1 (echo [ERROR] git commit failed & pause & exit /b 1)

git push
if errorlevel 1 (echo [ERROR] git push failed & pause & exit /b 1)

echo.
echo ============================================================
echo   Push complete. Vercel will redeploy in ~30-60s.
echo ============================================================
echo.
pause
