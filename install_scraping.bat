@echo off
echo ========================================
echo Installing Web Scraping Dependencies
echo ========================================
echo.

echo Installing BeautifulSoup4 and lxml...
pip install beautifulsoup4==4.12.2 lxml==4.9.3

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Web scraping is now enabled.
echo The system will fetch real-time commodity prices from:
echo - Yahoo Finance (Copper, Aluminum, Steel futures)
echo - Optional: Metal Price API (with API key)
echo - Optional: Commodities API (with API key)
echo.
echo To configure:
echo 1. Copy .env.example to .env
echo 2. Set ENABLE_REAL_TIME_SCRAPING=true
echo 3. (Optional) Add API keys for better data
echo.
echo See WEBSCRAPING_GUIDE.md for detailed documentation.
echo.
pause
