"""
Configuration file for Smart Procurement System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = True

# Streamlit Configuration
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))

# Currency Configuration
CURRENCY = 'INR'  # Indian Rupees
CURRENCY_SYMBOL = '₹'
USD_TO_INR_RATE = 83.0  # Approximate conversion rate

# Alert Configuration
EMAIL_ALERTS = os.getenv('EMAIL_ALERTS', 'false').lower() == 'true'
WHATSAPP_ALERTS = os.getenv('WHATSAPP_ALERTS', 'false').lower() == 'true'
ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'procurement@factory.com')
PRICE_DROP_THRESHOLD = float(os.getenv('PRICE_DROP_THRESHOLD', 5))  # Percentage
INVENTORY_THRESHOLD = float(os.getenv('INVENTORY_THRESHOLD', 100))  # Tons

# Materials Configuration
MATERIALS = ['Copper', 'Aluminum', 'Steel']

# Preferred Supplier Configuration
PREFERRED_SUPPLIERS = {
    'Copper': 'Global Metals Inc.',  # Example preferred supplier for Copper
    'Aluminum': 'MetalCorp Trading',  # Example preferred supplier for Aluminum
    'Steel': 'Global Metals Inc.'  # Example preferred supplier for Steel
}

# Data Paths
DATA_DIR = 'data'
MATERIAL_PRICES_CSV = os.path.join(DATA_DIR, 'material_prices.csv')
INVENTORY_JSON = os.path.join(DATA_DIR, 'inventory.json')
VENDORS_JSON = os.path.join(DATA_DIR, 'vendors.json')
FORECAST_CACHE = os.path.join(DATA_DIR, 'forecast_cache.json')

# Database
DATABASE_PATH = os.path.join(DATA_DIR, 'procurement.db')

# Forecasting Configuration
FORECAST_DAYS = 7
HISTORICAL_DAYS = 30

# Update Intervals (in seconds)
PRICE_UPDATE_INTERVAL = 300  # 5 minutes
FORECAST_UPDATE_INTERVAL = 3600  # 1 hour

# Web Scraping Configuration
ENABLE_REAL_TIME_SCRAPING = os.getenv('ENABLE_REAL_TIME_SCRAPING', 'true').lower() == 'true'
SCRAPING_INTERVAL = int(os.getenv('SCRAPING_INTERVAL', 300))  # 5 minutes
USE_FALLBACK_ON_SCRAPE_FAIL = True

# API Keys (optional - for premium data sources)
METAL_PRICE_API_KEY = os.getenv('METAL_PRICE_API_KEY', '')
COMMODITIES_API_KEY = os.getenv('COMMODITIES_API_KEY', '')
