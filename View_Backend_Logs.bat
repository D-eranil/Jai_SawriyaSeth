@echo off
title Jss Wealthtech - Backend Logs
cd /d "%~dp0"
set LOG_FILE=data\logs\headless.log

if not exist "%LOG_FILE%" (
    echo Log file not found: %LOG_FILE%
    echo Start backend first using Start_Hidden.bat
    pause
    exit /b 1
)

echo Showing live logs from %LOG_FILE%
powershell -NoProfile -Command "Get-Content -Path '%LOG_FILE%' -Wait -Tail 80"
