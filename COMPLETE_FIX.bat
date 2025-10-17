@echo off
cls
echo ====================================================================
echo   COMPLETE SYSTEM FIX - Smart Procurement
echo ====================================================================
echo.

echo [Step 1/5] Fixing Corrupted PO Files...
echo.
python fix_corrupted_pos.py
echo.
pause

echo.
echo [Step 2/5] Regenerating Data Files...
echo.
python regenerate_data_usd.py
echo.
pause

echo.
echo [Step 3/5] Stopping All Python Processes...
echo.
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo Done!
echo.

echo [Step 4/5] Starting Backend...
echo.
start "Smart Procurement Backend" cmd /k "cd /d d:\Hackathon\SRM\smart_procurement && python app.py"
echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul
echo.

echo [Step 5/5] Starting Dashboard...
echo.
start "Smart Procurement Dashboard" cmd /k "cd /d d:\Hackathon\SRM\smart_procurement && streamlit run dashboard.py"
echo.

echo ====================================================================
echo   SYSTEM RESTART COMPLETE!
echo ====================================================================
echo.
echo Two windows should have opened:
echo   1. Backend (Flask) - http://localhost:5000
echo   2. Dashboard (Streamlit) - http://localhost:8501
echo.
echo Wait for both to fully start, then:
echo   1. Open browser to http://localhost:8501
echo   2. Check Overview page for recommendations
echo   3. Check Price Analysis for forecasts
echo   4. Try generating a PO
echo.
echo If issues persist, check the backend window for errors.
echo.
pause
