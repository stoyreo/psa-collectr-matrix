@echo off
title PSA x Collectr Tracer — Build EXE
cd /d "%~dp0"

echo ============================================================
echo   PSA x Collectr Tracer — EXE Builder
echo   Output: dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
echo ============================================================
echo.

:: ── Install build dependencies ──────────────────────────────────────────────
echo [1/4] Installing dependencies...
python -m pip install pyinstaller flask openpyxl playwright --quiet
if errorlevel 1 (
    echo [ERROR] pip install failed. Make sure Python is in PATH.
    pause & exit /b 1
)

:: ── Install Playwright Chromium (runtime browser) ────────────────────────────
echo [2/4] Installing Playwright browser...
python -m playwright install chromium
if errorlevel 1 (
    echo [WARN]  Playwright browser install failed - live fetch will use cache fallback.
)

:: ── Clean previous build ────────────────────────────────────────────────────
echo [3/4] Cleaning previous build...
if exist "dist\PSA_Collectr_Tracer" rmdir /s /q "dist\PSA_Collectr_Tracer"
if exist "build"                     rmdir /s /q "build"

:: ── Run PyInstaller ─────────────────────────────────────────────────────────
echo [4/4] Building EXE (this takes 2-5 minutes)...
python -m PyInstaller PSA_Collectr_Tracer.spec --noconfirm
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed. Check output above for details.
    pause & exit /b 1
)

:: ── Copy runtime data files into dist folder ────────────────────────────────
echo.
echo [POST] Copying runtime data to dist folder...
if not exist "dist\PSA_Collectr_Tracer\cache"  mkdir "dist\PSA_Collectr_Tracer\cache"
if not exist "dist\PSA_Collectr_Tracer\output" mkdir "dist\PSA_Collectr_Tracer\output"
copy "My Collection CSV - 19.csv" "dist\PSA_Collectr_Tracer\" >nul

echo.
echo ============================================================
echo   BUILD COMPLETE!
echo.
echo   Your app is at:
echo   dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
echo.
echo   Double-click PSA_Collectr_Tracer.exe to launch.
echo   (You can move the entire PSA_Collectr_Tracer folder anywhere.)
echo ============================================================
echo.
pause
