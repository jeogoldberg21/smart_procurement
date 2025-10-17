@echo off
echo ========================================
echo Starting Streamlit Dashboard
echo ========================================
echo.
echo Please ensure Flask backend is running first!
echo.
timeout /t 3
streamlit run dashboard.py
pause
