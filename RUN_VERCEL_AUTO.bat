@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ============================================================
echo  Phase C.4-C.5 Auto Deploy - PSA x Collectr Tracer
echo  Repo: github.com/stoyreo/psa-collectr-matrix
echo ============================================================
echo.

REM Verify git is available
where git >nul 2>&1
if errorlevel 1 (
    echo [FAIL] git not found in PATH. Install Git for Windows first.
    pause
    exit /b 1
)

echo [0/6] Clearing any stale git index lock...
if exist ".git\index.lock" del /f /q ".git\index.lock"

echo [1/6] Removing .env from git tracking ^(security - has Gmail app password^)...
git rm --cached .env 2>nul

echo [2/6] Removing FUSE temp files from git tracking...
for /f "delims=" %%F in ('git ls-files ".fuse_hidden*" 2^>nul') do (
    git rm --cached "%%F" >nul 2>nul
)

echo [3/6] Removing local log files from tracking...
git rm --cached "output/portfolio_refresh.log" 2>nul

echo [4/6] Amending commit with cleaned tree + new .gitignore...
git add .gitignore
git commit --amend --no-edit
if errorlevel 1 (
    echo [FAIL] Commit amend failed. See output above.
    pause
    exit /b 1
)

echo [5/6] Configuring remote origin -^> github.com/stoyreo/psa-collectr-matrix...
git remote remove origin >nul 2>nul
git remote add origin https://github.com/stoyreo/psa-collectr-matrix.git
git branch -M main

echo.
echo [6/6] Pushing to GitHub...
echo        ^>^>^> A browser window may pop up for GitHub OAuth.
echo        ^>^>^> Click "Authorize" and return here.
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo ============================================================
    echo [FAIL] Push failed. Common causes:
    echo   - The repo at github.com/stoyreo/psa-collectr-matrix
    echo     does not exist yet, or is not empty.
    echo   - You cancelled the OAuth authorization popup.
    echo   - Network issue.
    echo ============================================================
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  SUCCESS - Code pushed to GitHub.
echo  https://github.com/stoyreo/psa-collectr-matrix
echo ============================================================
echo.
echo  Next step: Claude will now drive Vercel in Chrome
echo  to import this repo and deploy. Leave this window open
echo  or close it - your choice.
echo.
pause
