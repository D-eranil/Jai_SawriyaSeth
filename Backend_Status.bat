@echo off
setlocal EnableDelayedExpansion
title Jss Wealthtech - Backend Status
cd /d "%~dp0"
set PID_FILE=data\logs\headless.pid
set LOG_FILE=data\logs\headless.log

if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    echo Backend PID file found: !PID!
    tasklist /FI "PID eq !PID!" | findstr /I "pythonw.exe python.exe" >nul
    if %errorlevel%==0 (
        echo Status: RUNNING
    ) else (
        echo Status: PID file exists but process not found
    )
) else (
    echo Status: NOT RUNNING (pid file missing)
)

if exist "%LOG_FILE%" (
    echo.
    echo Last 20 log lines:
    powershell -NoProfile -Command "Get-Content -Path '%LOG_FILE%' -Tail 20"
) else (
    echo Log file not found yet.
)
pause
endlocal
