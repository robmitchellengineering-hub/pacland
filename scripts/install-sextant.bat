@echo off
REM SEXTANT + VVS SDK — double-click installer (Windows).
REM Double-click this file; it installs both tools.
setlocal

echo ==============================================
echo   SEXTANT + Valiant Verification SDK installer
echo ==============================================
echo.

where python >nul 2>nul || (echo [X] Python 3 not found. Install from https://www.python.org/downloads/ & pause & exit /b 1)
where node >nul 2>nul || (echo [X] Node.js not found. Install Node 18+ from https://nodejs.org & pause & exit /b 1)
where git >nul 2>nul || (echo [X] git not found. Install from https://git-scm.com & pause & exit /b 1)
echo [OK] prerequisites present

set SEXTANT_DIR=%USERPROFILE%\sextant
if exist "%SEXTANT_DIR%\.git" (
  echo [OK] SEXTANT already present - updating
  git -C "%SEXTANT_DIR%" pull --quiet
) else (
  echo [..] Downloading SEXTANT ...
  git clone --quiet --depth 1 https://github.com/robmitchellengineering-hub/pacland.git "%SEXTANT_DIR%"
)

echo [..] Installing the Valiant Verification SDK ...
where valiant >nul 2>nul || npm install -g "https://api.morpheus.nz/api/functions/getPackage?name=valiant-verification-sdk&version=0.2.0"

echo SEXTANT-node.bat launcher
(
  echo @echo off
  echo cd /d "%%~dp0"
  echo python -m pacland.sextant_node
) > "%SEXTANT_DIR%\SEXTANT-node.bat"

echo.
echo ==============================================
echo   Done.
echo   SEXTANT:  %SEXTANT_DIR%
echo   Open it:  double-click SEXTANT-node.bat
echo   VVS:      run 'valiant status' in a terminal
echo ==============================================
pause
