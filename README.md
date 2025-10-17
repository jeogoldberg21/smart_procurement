# 🏭 Smart Procurement for Factories: Real-Time Material Price Insights

A complete AI-powered procurement system that helps factories monitor real-time market prices of raw materials, track inventory levels, and receive intelligent recommendations on the optimal time to purchase materials.

## 🎯 Features

### Core Capabilities
- **Real-Time Price Tracking**: Monitor live prices for Copper, Aluminum, and Steel
- **AI-Powered Forecasting**: 7-day price predictions using Facebook Prophet
- **Smart Recommendations**: BUY/WAIT/MONITOR decisions based on price trends
- **Inventory Management**: Track stock levels with automated alerts
- **Vendor Comparison**: Compare prices across multiple suppliers
- **Alert System**: Notifications for price drops and low inventory
- **Interactive Dashboard**: Beautiful Streamlit UI with charts and metrics

### Technical Highlights
- **Backend**: Flask REST API with scheduled background tasks
- **ML Model**: Facebook Prophet for time-series forecasting
- **Frontend**: Streamlit dashboard with Plotly visualizations
- **Data Storage**: CSV and JSON for easy prototyping
- **Auto-Updates**: Periodic price and forecast refreshes

## 📁 Project Structure

```
smart_procurement/
├── app.py                      # Flask backend server
├── dashboard.py                # Streamlit dashboard
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── data/                      # Data storage
│   ├── material_prices.csv    # Historical price data
│   ├── inventory.json         # Current inventory levels
│   ├── vendors.json           # Vendor information
│   ├── alerts.json            # Alert history
│   └── procurement.db         # SQLite database (optional)
│
├── models/                    # ML models
│   ├── __init__.py
│   └── forecast_model.py      # Prophet forecasting model
│
└── utils/                     # Utility modules
    ├── __init__.py
    ├── data_generator.py      # Mock data generation
    └── notifications.py       # Alert system
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd d:/Hackathon/SRM/smart_procurement
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate initial data** (optional - will auto-generate on first run)
   ```bash
   python -m utils.data_generator
   ```

4. **Configure environment** (optional)
   ```bash
   copy .env.example .env
   # Edit .env with your preferences
   ```

### Running the Application

**Option 1: Run both services together (Recommended)**

Open two terminal windows:

**Terminal 1 - Start Flask Backend:**
```bash
python app.py
```
The backend will start on `http://localhost:5000`

**Terminal 2 - Start Streamlit Dashboard:**
```bash
streamlit run dashboard.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`

**Option 2: Use the startup script**
```bash
python start.py
```

### First Time Setup

When you first run the application:
1. The system will automatically generate 30 days of historical price data
2. Mock inventory levels will be created for all materials
3. Vendor data will be initialized
4. ML models will be trained on the historical data
5. Initial forecasts will be generated

This process takes about 30-60 seconds.

## 📊 Dashboard Features

### 1. Overview Page
- Current prices for all materials
- BUY/WAIT/MONITOR recommendations
- Price trend charts (last 7 days)
- Recent alerts and notifications
- Key metrics summary

### 2. Price Analysis
- Detailed price history (30 days)
- 7-day price forecasts with confidence intervals
- AI-powered buy/wait recommendations
- Historical statistics and volatility
- Price distribution analysis

### 3. Inventory Management
- Real-time stock levels with gauge charts
- Days remaining calculations
- 30-day consumption forecasts
- Low stock alerts
- Reorder recommendations

### 4. Alerts & Notifications
- Price drop alerts (>5% decrease)
- Low inventory warnings
- Alert filtering by type and severity
- Alert history and summary

### 5. Vendor Comparison
- Top vendor recommendations
- Price comparison across suppliers
- Vendor ratings and reliability scores
- Delivery time and payment terms
- Cost calculator for bulk orders

## 🤖 AI Forecasting Logic

The system uses Facebook Prophet to forecast material prices:

```python
# Decision Logic
if forecasted_price > current_price + 2%:
    recommendation = "BUY NOW"
    reason = "Price expected to rise"
    
elif forecasted_price < current_price - 2%:
    recommendation = "WAIT"
    reason = "Price expected to drop"
    
else:
    recommendation = "MONITOR"
    reason = "Price expected to remain stable"
```

### Forecast Features
- 7-day ahead predictions
- 95% confidence intervals
- Trend detection
- Seasonality analysis
- Best day to buy identification

## 🔔 Alert System

### Alert Types
1. **PRICE_DROP**: Triggered when price drops >5%
2. **PRICE_INCREASE**: Triggered when price rises >5%
3. **LOW_INVENTORY**: Triggered when stock < minimum threshold

### Alert Severities
- **CRITICAL**: Immediate action required (low inventory)
- **WARNING**: Important but not urgent (price changes)
- **INFO**: Informational updates

### Notification Channels
- In-app dashboard notifications
- Console alerts (email/WhatsApp simulation)
- Alert history logging

## 📡 API Endpoints

The Flask backend provides the following REST API endpoints:

### System
- `GET /api/health` - System health check
- `GET /api/materials` - List of tracked materials

### Prices
- `GET /api/prices/current` - Current prices for all materials
- `GET /api/prices/historical/<material>` - Historical price data
- `GET /api/forecast/<material>` - Price forecast for material

### Recommendations
- `GET /api/recommendations` - Buy/wait recommendations for all materials

### Inventory
- `GET /api/inventory` - All inventory data
- `GET /api/inventory/<material>` - Specific material inventory

### Vendors
- `GET /api/vendors/<material>` - Vendor comparison for material

### Alerts
- `GET /api/alerts?limit=10&unread_only=false` - Recent alerts

### Dashboard
- `GET /api/dashboard/summary` - Complete dashboard summary

## ⚙️ Configuration

Edit `config.py` or create a `.env` file to customize:

```python
# Update intervals
PRICE_UPDATE_INTERVAL = 300      # 5 minutes
FORECAST_UPDATE_INTERVAL = 3600  # 1 hour

# Alert thresholds
PRICE_DROP_THRESHOLD = 5         # Percentage
INVENTORY_THRESHOLD = 100        # Tons

# Forecasting
FORECAST_DAYS = 7                # Days ahead
HISTORICAL_DAYS = 30             # Days of history

# Materials
MATERIALS = ['Copper', 'Aluminum', 'Steel']
```

## 🎨 Customization

### Adding New Materials

1. Edit `config.py`:
   ```python
   MATERIALS = ['Copper', 'Aluminum', 'Steel', 'Zinc']
   ```

2. Update `utils/data_generator.py` with base prices:
   ```python
   base_prices = {
       'Copper': 8500,
       'Aluminum': 2400,
       'Steel': 800,
       'Zinc': 3000  # Add new material
   }
   ```

3. Regenerate data:
   ```bash
   python -m utils.data_generator
   ```

### Connecting Real Data Sources

Replace mock data in `app.py` with real API calls:

```python
import yfinance as yf

def fetch_real_copper_price():
    ticker = yf.Ticker("HG=F")  # Copper futures
    data = ticker.history(period="1d")
    return data['Close'].iloc[-1]
```

### Email Integration

Update `utils/notifications.py`:

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(alert):
    msg = MIMEText(alert['message'])
    msg['Subject'] = f"Alert: {alert['type']}"
    msg['From'] = 'system@factory.com'
    msg['To'] = config.ALERT_EMAIL
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email', 'your-password')
        server.send_message(msg)
```

## 🧪 Testing

### Test the Forecast Model
```bash
cd models
python forecast_model.py
```

### Test Data Generation
```bash
python -m utils.data_generator
```

### Test Notifications
```bash
python -m utils.notifications
```

### Test API Endpoints
```bash
# Start the Flask server first
python app.py

# In another terminal
curl http://localhost:5000/api/health
curl http://localhost:5000/api/prices/current
curl http://localhost:5000/api/recommendations
```

## 📈 Demo Data

The system includes 30 days of mock historical data:

- **Copper**: Base price ~$8,500/ton, volatility ±$150
- **Aluminum**: Base price ~$2,400/ton, volatility ±$80
- **Steel**: Base price ~$800/ton, volatility ±$30

Inventory levels are randomly generated between 50-500 tons with realistic consumption rates.

## 🎯 Hackathon Presentation Tips

### Key Highlights
1. **Real-time monitoring** with auto-refresh
2. **AI-powered forecasting** using Prophet
3. **Smart recommendations** save money
4. **Beautiful visualizations** with Plotly
5. **Complete system** - backend + frontend + ML

### Demo Flow
1. Show Overview page with current prices
2. Navigate to Price Analysis - show forecast
3. Explain BUY/WAIT recommendation logic
4. Show Inventory page with gauges
5. Display Alerts page
6. Compare vendors for best price

### Value Proposition
- **Cost Savings**: Buy at optimal times based on forecasts
- **Risk Reduction**: Avoid stockouts with inventory alerts
- **Time Savings**: Automated monitoring vs manual checking
- **Data-Driven**: ML-based decisions vs gut feeling

## 🔧 Troubleshooting

### Issue: Prophet installation fails
**Solution**: Install Prophet dependencies first
```bash
pip install pystan
pip install prophet
```

### Issue: Dashboard shows "System Offline"
**Solution**: Ensure Flask backend is running
```bash
python app.py
```

### Issue: No data displayed
**Solution**: Generate initial data
```bash
python -m utils.data_generator
```

### Issue: Port already in use
**Solution**: Change ports in config.py
```python
FLASK_PORT = 5001
STREAMLIT_PORT = 8502
```

## 📝 Future Enhancements

- [ ] Integration with real commodity price APIs (Yahoo Finance, MetalMiner)
- [ ] IoT sensor integration for real-time inventory tracking
- [ ] Multi-user authentication and role-based access
- [ ] Purchase order generation and tracking
- [ ] Historical purchase analysis and ROI calculation
- [ ] Mobile app for on-the-go monitoring
- [ ] WhatsApp/SMS alerts integration
- [ ] Advanced ML models (LSTM, ARIMA)
- [ ] Multi-currency support
- [ ] Export reports to PDF/Excel

## 👥 Team & Credits

Built for the Smart Procurement Hackathon

**Technologies Used:**
- Python 3.x
- Flask (Backend)
- Streamlit (Frontend)
- Facebook Prophet (ML)
- Plotly (Visualizations)
- Pandas & NumPy (Data Processing)
- APScheduler (Background Tasks)

## 📄 License

This project is created for hackathon purposes. Feel free to use and modify as needed.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test individual components
4. Check console logs for errors

---

**Built with ❤️ for smarter procurement decisions**
