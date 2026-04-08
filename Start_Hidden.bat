@echo off
title Jss Wealthtech - Hidden Background Mode
cd /d "%~dp0"
echo Starting hidden background engine...
start "" /min pythonw run_headless.py
echo Started. Check Task Manager for pythonw.exe
timeout /t 2 >nul
