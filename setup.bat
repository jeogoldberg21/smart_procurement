@echo off
echo ========================================
echo Smart Procurement System - Setup
echo ========================================
echo.
echo Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.
echo ========================================
echo Generating initial data...
echo ========================================
echo.
python -m utils.data_generator
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the system:
echo 1. Run: python app.py (in one terminal)
echo 2. Run: streamlit run dashboard.py (in another terminal)
echo.
echo Or simply run: python start.py
echo.
pause
