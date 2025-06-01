@echo off
setlocal enabledelayedexpansion

:: Define emoji symbols (default)
set "CHECK=✅"
set "CROSS=❌"
set "INFO=ℹ️"
set "STAR=✨"

:: ASCII fallback
set "CHECK_ASC=OK"
set "CROSS_ASC=ERR"
set "INFO_ASC=INFO"
set "STAR_ASC=*"

:: Assume emoji support
set "EMOJIS_SUPPORTED=1"

:: Choose symbols
if "%EMOJIS_SUPPORTED%"=="1" (
    set "SYM_CHECK=%CHECK%"
    set "SYM_CROSS=%CROSS%"
    set "SYM_INFO=%INFO%"
    set "SYM_STAR=%STAR%"
) else (
    set "SYM_CHECK=%CHECK_ASC%"
    set "SYM_CROSS=%CROSS_ASC%"
    set "SYM_INFO=%INFO_ASC%"
    set "SYM_STAR=%STAR_ASC%"
)

:: ANSI color codes for Windows 10+
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

echo %SYM_STAR% %GREEN%Starting YTConverter™ universal installer...%RESET%

:: Function to check if a command exists
:command_exists
    where %1 >nul 2>&1
    exit /b %errorlevel%

:: --- Check System Dependencies ---
echo %SYM_INFO% %CYAN%Checking system dependencies...%RESET%

:: Python
call :command_exists python
if %errorlevel% neq 0 (
    echo %SYM_CROSS% %RED%Python 3 not found. Install it from python.org and add to PATH.%RESET%
    echo %SYM_INFO% %YELLOW%https://www.python.org/downloads/windows/%RESET%
    pause
    goto :eof
) else (
    echo %SYM_CHECK% %GREEN%Python 3 found.%RESET%
)

:: Pip
call :command_exists pip
if %errorlevel% neq 0 (
    echo %SYM_CROSS% %RED%Pip not found. Ensure it's installed with Python.%RESET%
    pause
    goto :eof
) else (
    echo %SYM_CHECK% %GREEN%Pip found.%RESET%
)

:: FFmpeg
call :command_exists ffmpeg
if %errorlevel% neq 0 (
    echo %SYM_CROSS% %YELLOW%FFmpeg not found. Attempting to download...%RESET%

    :: Download FFmpeg ZIP
    powershell -Command ^
        "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'" || (
        echo %SYM_CROSS% %RED%Failed to download FFmpeg ZIP.%RESET%
        pause
        goto :eof
    )

    :: Extract ZIP
    powershell -Command ^
        "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath 'ffmpeg_temp'" || (
        echo %SYM_CROSS% %RED%Failed to extract FFmpeg ZIP.%RESET%
        pause
        goto :eof
    )

    :: Locate and copy ffmpeg.exe to current folder
    for /f "delims=" %%f in ('dir /s /b /a-d ffmpeg_temp\ffmpeg-*\bin\ffmpeg.exe') do (
        copy "%%f" . >nul
        echo %SYM_CHECK% %GREEN%FFmpeg downloaded and copied to local folder.%RESET%
        goto :ffmpeg_done
    )

    echo %SYM_CROSS% %RED%FFmpeg.exe not found after extraction.%RESET%
    pause
    goto :eof

:ffmpeg_done
) else (
    echo %SYM_CHECK% %GREEN%FFmpeg found.%RESET%
)

:: yt-dlp
call :command_exists yt-dlp
if %errorlevel% neq 0 (
    echo %SYM_INFO% %YELLOW%yt-dlp not found. Will be installed via pip.%RESET%
) else (
    echo %SYM_CHECK% %GREEN%yt-dlp found.%RESET%
)

:: --- Install Python Packages ---
echo.
echo %SYM_INFO% %CYAN%Installing/Upgrading Python packages...%RESET%

python -m pip install --upgrade pip || (
    echo %SYM_CROSS% %RED%Failed to upgrade pip.%RESET%
    goto :eof
)
echo %SYM_CHECK% %GREEN%Pip upgraded.%RESET%

python -m pip install --upgrade yt-dlp fontstyle colored requests || (
    echo %SYM_CROSS% %RED%Failed to install Python packages.%RESET%
    goto :eof
)
echo %SYM_CHECK% %GREEN%Python packages installed successfully.%RESET%

echo.
echo %SYM_CHECK% %GREEN%YTConverter™ is ready to roll!%RESET%
echo %SYM_INFO% %CYAN%To run: python ytconverter.py%RESET%

pause
endlocal
exit /b 0
