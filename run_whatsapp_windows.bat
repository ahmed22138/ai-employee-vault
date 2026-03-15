@echo off
REM WhatsApp Test - Windows Version
REM Double-click this file to run

echo ========================================
echo WhatsApp Watcher - Windows Mode
echo ========================================
echo.

cd /d "E:\all-d-files\Ai_Employee_Vault"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed!
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
echo.
echo Starting WhatsApp Watcher...
echo Browser will open with QR code!
echo.

set WHATSAPP_HEADLESS=false
python watchers\whatsapp_watcher.py

pause
