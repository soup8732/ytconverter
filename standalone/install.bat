@echo off
setlocal enabledelayedexpansion

:: ---------------- UI symbols and colors ----------------
set "CHECK=OK"
set "CROSS=ERR"
set "INFO=INFO"
set "STAR=*"

:: Detect ANSI support
>nul 2>&1 reg query "HKCU\Console" /v VirtualTerminalLevel && (
  set "GREEN=\033[0;32m"
  set "RED=\033[0;31m"
  set "YELLOW=\033[1;33m"
  set "CYAN=\033[0;36m"
  set "RESET=\033[0m"
) || (
  set "GREEN="
  set "RED="
  set "YELLOW="
  set "CYAN="
  set "RESET="
)

echo %STAR% %GREEN%Starting YTConverter installer (venv + PATH fixes)...%RESET%

:: ---------------- Helpers ----------------
:command_exists
where %1 >nul 2>&1
exit /b %errorlevel%

:die
echo %CROSS% %RED%%~1%RESET%
if "%~2"=="" (set "CODE=1") else (set "CODE=%~2")
endlocal & exit /b %CODE%

:: ---------------- Paths ----------------
set "REPO_DIR=%cd%"
set "VENV_DIR=%REPO_DIR%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_PIP=%VENV_DIR%\Scripts\pip.exe"
set "TOOLS_DIR=%REPO_DIR%\tools"
set "FFMPEG_DIR=%TOOLS_DIR%\ffmpeg\bin"
set "FFMPEG_EXE=%FFMPEG_DIR%\ffmpeg.exe"
set "FFMPEG_ZIP=%REPO_DIR%\ffmpeg.zip"
set "FFMPEG_TMP=%REPO_DIR%\ffmpeg_temp"

:: ---------------- System checks ----------------
echo %INFO% %CYAN%Checking system dependencies...%RESET%

call :command_exists powershell || call :die "PowerShell not found; required for download/extract." 1
echo %CHECK% %GREEN%PowerShell found.%RESET%

call :command_exists python || call :die "Python 3 not found. Install and add to PATH." 1
echo %CHECK% %GREEN%Python found.%RESET%

:: ---------------- Virtual environment ----------------
if not exist "%VENV_DIR%" (
  echo %INFO% %CYAN%Creating virtual environment in .venv...%RESET%
  python -m venv "%VENV_DIR%" || call :die "Failed to create virtual environment." 1
) else (
  echo %CHECK% %GREEN%Virtual environment already exists.%RESET%
)

if not exist "%VENV_PY%" call :die "Virtual environment is incomplete; missing Scripts\python.exe." 1

echo %INFO% %CYAN%Upgrading pip in venv...%RESET%
"%VENV_PY%" -m pip install --upgrade pip || call :die "Failed to upgrade pip in venv." 1
echo %CHECK% %GREEN%pip upgraded.%RESET%

echo %INFO% %CYAN%Installing Python packages in venv...%RESET%
"%VENV_PIP%" install --upgrade yt-dlp fontstyle colored requests || call :die "Failed to install Python packages in venv." 1
echo %CHECK% %GREEN%Python packages installed in venv.%RESET%

:: ---------------- FFmpeg setup ----------------
call :command_exists ffmpeg
if %errorlevel%==0 (
  echo %CHECK% %GREEN%FFmpeg already available on PATH.%RESET%
) else (
  if exist "%FFMPEG_EXE%" (
    echo %CHECK% %GREEN%FFmpeg already present at %FFMPEG_EXE%.%RESET%
  ) else (
    echo %INFO% %YELLOW%FFmpeg not found; downloading portable build...%RESET%
    if exist "%FFMPEG_ZIP%" del /f /q "%FFMPEG_ZIP%" >nul 2>&1
    if exist "%FFMPEG_TMP%" rmdir /s /q "%FFMPEG_TMP%" >nul 2>&1

    powershell -Command ^
      "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile '%FFMPEG_ZIP%'" ^
      || call :die "Failed to download FFmpeg ZIP." 1

    powershell -Command ^
      "Expand-Archive -Force -Path '%FFMPEG_ZIP%' -DestinationPath '%FFMPEG_TMP%'" ^
      || call :die "Failed to extract FFmpeg ZIP." 1

    for /f "delims=" %%F in ('dir /s /b /a-d "%FFMPEG_TMP%\ffmpeg-*\bin\ffmpeg.exe"') do (
      set "FOUND_FFMPEG=%%F"
    )

    if not defined FOUND_FFMPEG call :die "ffmpeg.exe not found after extraction." 1

    mkdir "%FFMPEG_DIR%" >nul 2>&1
    copy /y "%FOUND_FFMPEG%" "%FFMPEG_EXE%" >nul || call :die "Failed to copy ffmpeg.exe to tools directory." 1

    if exist "%FFMPEG_ZIP%" del /f /q "%FFMPEG_ZIP%" >nul 2>&1
    if exist "%FFMPEG_TMP%" rmdir /s /q "%FFMPEG_TMP%" >nul 2>&1

    echo %CHECK% %GREEN%FFmpeg placed at %FFMPEG_EXE%.%RESET%
  )
)

:: ---------------- PATH integration (optional) ----------------
echo.
echo %INFO% %CYAN%Adding optional PATH entries (user profile) so commands work globally...%RESET%

:: Add .venv\Scripts
for /f "usebackq tokens=2,*" %%A in (`reg query "HKCU\Environment" /v Path 2^>nul ^| findstr /i "Path"`) do set "USER_PATH=%%B"
set "ADD_VENV=1"
echo "!USER_PATH!" | find /i ".venv\Scripts" >nul && set "ADD_VENV=0"
if "!ADD_VENV!"=="1" (
  setx Path "!USER_PATH!;%VENV_DIR%\Scripts" >nul 2>&1 && (
    echo %CHECK% %GREEN%Added .venv\Scripts to user PATH (new terminals only).%RESET%
  ) || echo %INFO% %YELLOW%Could not modify user PATH; continue manually if needed.%RESET%
) else (
  echo %CHECK% %GREEN%.venv\Scripts already on user PATH.%RESET%
)

:: Add tools\ffmpeg\bin
set "ADD_FF=1"
echo "!USER_PATH!" | find /i "tools\ffmpeg\bin" >nul && set "ADD_FF=0"
if exist "%FFMPEG_EXE%" if "!ADD_FF!"=="1" (
  setx Path "!USER_PATH!;%FFMPEG_DIR%" >nul 2>&1 && (
    echo %CHECK% %GREEN%Added tools\ffmpeg\bin to user PATH (new terminals only).%RESET%
  ) || echo %INFO% %YELLOW%Could not modify user PATH; continue manually if needed.%RESET%
) else if exist "%FFMPEG_EXE%" (
  echo %CHECK% %GREEN%tools\ffmpeg\bin already on user PATH.%RESET%
)

:: ---------------- Final guidance ----------------
echo.
echo %CHECK% %GREEN%Setup complete.%RESET%
echo %INFO% %CYAN%Immediate use in this shell:%RESET%
echo    "%VENV_DIR%\Scripts\activate.bat"   & echo    yt-dlp --version   & echo    ffmpeg -version
echo %INFO% %CYAN%Or run app:%RESET%
echo    "%VENV_PY%" ytconverter.py
echo %INFO% %YELLOW%Note: PATH changes require a new terminal to take effect.%RESET%

endlocal
exit /b 0
