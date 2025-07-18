@echo off
title Setup Auto Scraper for Startup
echo ================================================
echo    Setting up Auto Scraper for Windows Startup
echo ================================================
echo.
echo This script will set up the HackerRank Auto Scraper to run:
echo - At Windows startup
echo - After sleep/hibernate resume
echo - With administrative privileges
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "BATCH_FILE=%SCRIPT_DIR%auto_scraper.bat"

echo.
echo Creating Windows Task Scheduler entries...
echo.

REM Create startup task
echo Creating startup task...
schtasks /create /tn "HackerRank Auto Scraper - Startup" /tr "\"%BATCH_FILE%\"" /sc onstart /ru "SYSTEM" /rl highest /f
if %errorlevel% neq 0 (
    echo Warning: Failed to create startup task with SYSTEM account, trying with current user...
    schtasks /create /tn "HackerRank Auto Scraper - Startup" /tr "\"%BATCH_FILE%\"" /sc onstart /f
)

REM Create resume from sleep/hibernate task
echo Creating resume task...
schtasks /create /tn "HackerRank Auto Scraper - Resume" /tr "\"%BATCH_FILE%\"" /sc onevent /ec System /mo "*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and EventID=1]]" /f
if %errorlevel% neq 0 (
    echo Warning: Event-based task creation failed, creating logon task as fallback...
    schtasks /create /tn "HackerRank Auto Scraper - Logon" /tr "\"%BATCH_FILE%\"" /sc onlogon /f
)

echo.
echo ================================================
echo Setup completed!
echo ================================================
echo.
echo The following tasks have been created:
echo 1. HackerRank Auto Scraper - Startup (runs at Windows startup)
echo 2. HackerRank Auto Scraper - Resume (runs after sleep/hibernate)
echo.
echo You can view/manage these tasks in Windows Task Scheduler:
echo - Press Win+R, type "taskschd.msc", and press Enter
echo - Look for tasks named "HackerRank Auto Scraper"
echo.
echo To test: Restart your computer or put it to sleep and wake it up.
echo.
echo Press any key to exit...
pause >nul
