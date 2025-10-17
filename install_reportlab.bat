@echo off
echo ========================================
echo   Installing ReportLab for PDF Export
echo ========================================
echo.

echo Installing reportlab...
pip install reportlab==4.0.7

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Now restart the backend:
echo 1. Stop backend (Ctrl+C)
echo 2. Run: python app.py
echo 3. Try PDF export again
echo.
pause
