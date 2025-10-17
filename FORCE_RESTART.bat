@echo off
cls
echo ============================================
echo   FORCE RESTARTING BACKEND WITH FIX
echo ============================================
echo.

echo [1/3] Killing all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo      Done!
echo.

echo [2/3] Starting Flask Backend...
echo.
start "Smart Procurement Backend" cmd /k "cd /d d:\Hackathon\SRM\smart_procurement && python app.py"
timeout /t 3 /nobreak >nul
echo      Backend started in new window!
echo.

echo [3/3] Instructions:
echo      1. Wait for backend to show "Running on http://127.0.0.1:5000"
echo      2. Go to dashboard and refresh (F5)
echo      3. Try generating PO again
echo.

echo ============================================
echo   BACKEND RESTARTED WITH FIX!
echo ============================================
echo.
echo The fix is now active. Generate PO should work!
echo.
pause
