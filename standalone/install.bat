@echo off
setlocal enabledelayedexpansion

echo * Starting YTConverter installer (venv + PATH fixes)...

:: ---------------- Helpers ----------------
:command_exists
where %1 >nul 2>&1
exit /b %errorlevel%

:die
echo ERROR: %~1
if "%~2"=="" (set "CODE=1") else (set "CODE=%~2")
exit /b %CODE%

:: ---------------- Paths ----------------
set "REPO_DIR=%cd%"
set "VENV_DIR=%REPO_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"

:: ---------------- System checks ----------------
echo Checking system dependencies...

call :command_exists python || echo WARNING: Python not found
echo Python check done.

:: ---------------- Virtual environment ----------------
if not exist "%VENV_DIR%" (
  echo Creating virtual environment in .venv...
  python -m venv "%VENV_DIR%" || echo WARNING: Failed to create venv
) else (
  echo Virtual environment already exists.
)

if not exist "%VENV_PY%" echo WARNING: Virtual environment incomplete

"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PIP%" install --upgrade yt-dlp requests colored fontstyle

echo Installer finished.
exit /b 0
