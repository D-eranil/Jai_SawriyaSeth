@echo off
title Jss Wealthtech - Setup Diagnostics
cd /d "%~dp0"
python diagnostics.py
if errorlevel 1 (
    echo.
    echo Diagnostics failed. Please fix above issues.
    pause
    exit /b 1
)
echo.
echo Diagnostics passed. You can run Start.bat or Start_Hidden.bat
pause
