@echo off
title HackerRank Leaderboard Auto Scraper
echo ================================================
echo    HackerRank Leaderboard Auto Scraper
echo ================================================
echo Starting automatic scraping process...
echo Script will run every 30 minutes
echo Google Sheets upload will attempt every 2 hours
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"

:loop
echo [%date% %time%] Starting scraper...
py cli_scraper_no_dotenv.py
if %errorlevel% neq 0 (
    echo [%date% %time%] Error running scraper: %errorlevel%
) else (
    echo [%date% %time%] Scraper completed successfully
)

echo [%date% %time%] Attempting Google Sheets upload...
py google_sheets_uploader.py
if %errorlevel% neq 0 (
    echo [%date% %time%] Error with Google Sheets upload: %errorlevel%
) else (
    echo [%date% %time%] Google Sheets upload process completed
)

echo [%date% %time%] Waiting 30 minutes before next run...
echo.
timeout /t 1800 /nobreak >nul
goto loop
