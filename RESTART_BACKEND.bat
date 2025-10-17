@echo off
echo ========================================
echo   Restarting Flask Backend
echo ========================================
echo.

echo Step 1: Stopping old backend process...
taskkill /F /PID 28464 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Starting new backend...
echo.
echo Backend will start in a new window...
echo.
start "Flask Backend" cmd /k "python app.py"

echo.
echo ========================================
echo   Backend Restarted!
echo ========================================
echo.
echo The backend is now running with the fix.
echo You can now generate POs in the dashboard.
echo.
pause
