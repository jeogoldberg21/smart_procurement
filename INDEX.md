# 📚 Smart Procurement System - Complete File Index

## 🎯 Quick Navigation

**New to the project?** Start here:
1. **QUICKSTART.md** - Get running in 3 minutes
2. **README.md** - Complete documentation
3. **DEMO_GUIDE.md** - Hackathon presentation guide

**Want technical details?**
- **ARCHITECTURE.md** - System architecture
- **PROJECT_SUMMARY.md** - Feature overview
- **INSTALLATION.md** - Detailed setup guide

---

## 📁 Complete File Structure

```
smart_procurement/
│
├── 📄 Core Application Files
│   ├── app.py                      # Flask backend server (12.9 KB)
│   ├── dashboard.py                # Streamlit dashboard (24.2 KB)
│   ├── config.py                   # Configuration settings (1.3 KB)
│   └── requirements.txt            # Python dependencies
│
├── 🤖 Machine Learning
│   └── models/
│       ├── __init__.py
│       └── forecast_model.py       # Prophet forecasting model
│
├── 🛠️ Utilities
│   └── utils/
│       ├── __init__.py
│       ├── data_generator.py       # Mock data generation
│       └── notifications.py        # Alert system
│
├── 📊 Data Files (auto-generated)
│   └── data/
│       ├── material_prices.csv     # Historical prices
│       ├── inventory.json          # Stock levels
│       ├── vendors.json            # Vendor data
│       └── alerts.json             # Alert history
│
├── 📖 Documentation
│   ├── README.md                   # Main documentation (11.4 KB)
│   ├── QUICKSTART.md               # Quick start guide (3.9 KB)
│   ├── INSTALLATION.md             # Setup instructions (10.2 KB)
│   ├── DEMO_GUIDE.md               # Presentation guide (8.6 KB)
│   ├── ARCHITECTURE.md             # Technical architecture (19.7 KB)
│   ├── PROJECT_SUMMARY.md          # Feature overview (15.8 KB)
│   └── INDEX.md                    # This file
│
├── 🚀 Scripts
│   ├── start.py                    # Unified startup script
│   ├── test_system.py              # Test suite
│   ├── setup.bat                   # Windows setup
│   ├── run_backend.bat             # Start Flask
│   └── run_dashboard.bat           # Start Streamlit
│
└── ⚙️ Configuration
    ├── .env.example                # Environment template
    └── .gitignore                  # Git ignore rules
```

---

## 📄 File Descriptions

### Core Application Files

#### `app.py` (12.9 KB)
**Purpose:** Flask backend server with REST API

**Key Components:**
- 9 REST API endpoints
- Background scheduler (APScheduler)
- Price update simulation
- Forecast generation
- Alert checking
- Thread-safe data management

**Main Functions:**
- `load_data()` - Load CSV/JSON data
- `update_forecasts()` - Train ML models
- `check_alerts()` - Monitor for alerts
- `simulate_price_update()` - Update prices
- API endpoint handlers

**Usage:**
```bash
python app.py
# Starts on http://localhost:5000
```

#### `dashboard.py` (24.2 KB)
**Purpose:** Streamlit interactive dashboard

**Key Components:**
- 5 main pages (Overview, Price Analysis, Inventory, Alerts, Vendors)
- Plotly visualizations
- Real-time data fetching
- Custom CSS styling

**Main Functions:**
- `show_overview()` - Overview page
- `show_price_analysis()` - Price charts
- `show_inventory()` - Inventory management
- `show_alerts()` - Alert notifications
- `show_vendors()` - Vendor comparison
- `create_price_chart()` - Chart generation
- `create_inventory_gauge()` - Gauge charts

**Usage:**
```bash
streamlit run dashboard.py
# Opens http://localhost:8501
```

#### `config.py` (1.3 KB)
**Purpose:** Centralized configuration

**Settings:**
- Server ports (Flask: 5000, Streamlit: 8501)
- Materials list
- Update intervals
- Alert thresholds
- File paths
- Forecasting parameters

**Usage:**
```python
import config
materials = config.MATERIALS
```

#### `requirements.txt`
**Purpose:** Python dependencies

**Key Packages:**
- flask==3.0.0
- streamlit==1.29.0
- prophet==1.1.5
- plotly==5.18.0
- pandas==2.1.4
- numpy==1.26.2
- scikit-learn==1.3.2
- apscheduler==3.10.4

**Usage:**
```bash
pip install -r requirements.txt
```

---

### Machine Learning

#### `models/forecast_model.py`
**Purpose:** Price forecasting with Prophet

**Key Classes:**
- `PriceForecastModel` - Main forecasting class

**Key Methods:**
- `prepare_data()` - Format data for Prophet
- `train_model()` - Train Prophet model
- `forecast()` - Generate predictions
- `get_recommendation()` - BUY/WAIT/MONITOR logic
- `train_all_materials()` - Batch training

**Features:**
- 7-day ahead forecasting
- 95% confidence intervals
- Trend and seasonality detection
- Recommendation engine

**Usage:**
```python
from models.forecast_model import PriceForecastModel
model = PriceForecastModel()
model.train_model(df, 'Copper')
forecast = model.forecast('Copper', periods=7)
```

---

### Utilities

#### `utils/data_generator.py`
**Purpose:** Generate mock data for demo

**Key Functions:**
- `generate_historical_prices()` - 30 days of price data
- `generate_inventory_data()` - Stock levels
- `generate_vendor_data()` - Vendor information
- `initialize_data()` - Generate all data

**Features:**
- Realistic price volatility
- Random walk with trend
- Configurable materials
- Vendor price variations

**Usage:**
```bash
python -m utils.data_generator
```

#### `utils/notifications.py`
**Purpose:** Alert and notification system

**Key Classes:**
- `NotificationManager` - Alert management

**Key Methods:**
- `create_alert()` - Create new alert
- `check_price_alerts()` - Monitor price changes
- `check_inventory_alerts()` - Monitor stock levels
- `get_recent_alerts()` - Retrieve alerts
- `get_alert_summary()` - Alert statistics

**Features:**
- 3 alert types (PRICE_DROP, PRICE_INCREASE, LOW_INVENTORY)
- 3 severity levels (CRITICAL, WARNING, INFO)
- Alert history tracking
- Email/WhatsApp simulation

**Usage:**
```python
from utils.notifications import NotificationManager
manager = NotificationManager()
manager.create_alert('PRICE_DROP', 'Copper', 'Price dropped 7%', 'WARNING')
```

---

### Documentation Files

#### `README.md` (11.4 KB)
**Audience:** All users

**Contents:**
- Feature overview
- Installation instructions
- Usage guide
- API documentation
- Configuration options
- Troubleshooting
- Future enhancements

**When to read:** First time using the system

#### `QUICKSTART.md` (3.9 KB)
**Audience:** Users who want to get started fast

**Contents:**
- 3-minute setup guide
- Essential commands
- Common issues
- Demo tips

**When to read:** When you need to run the system quickly

#### `INSTALLATION.md` (10.2 KB)
**Audience:** Users having installation issues

**Contents:**
- System requirements
- Platform-specific instructions
- Troubleshooting guide
- Docker setup
- Verification steps

**When to read:** When installation fails or for production deployment

#### `DEMO_GUIDE.md` (8.6 KB)
**Audience:** Hackathon presenters

**Contents:**
- 5-minute demo script
- Talking points
- Q&A preparation
- Visual highlights
- Winning strategies

**When to read:** Before hackathon presentation

#### `ARCHITECTURE.md` (19.7 KB)
**Audience:** Developers and technical reviewers

**Contents:**
- System architecture diagrams
- Component details
- Data flow
- API specifications
- Scalability considerations
- Security recommendations

**When to read:** For technical deep-dive or extending the system

#### `PROJECT_SUMMARY.md` (15.8 KB)
**Audience:** Project managers and stakeholders

**Contents:**
- High-level overview
- Feature checklist
- Business value
- Metrics and statistics
- Success criteria

**When to read:** For project overview or status report

#### `INDEX.md` (This file)
**Audience:** All users

**Contents:**
- Complete file listing
- File descriptions
- Navigation guide

**When to read:** To understand project structure

---

### Scripts

#### `start.py`
**Purpose:** Unified startup script

**What it does:**
1. Checks for data files
2. Generates data if needed
3. Starts Flask backend (background thread)
4. Starts Streamlit dashboard (main thread)
5. Opens browser automatically

**Usage:**
```bash
python start.py
```

#### `test_system.py`
**Purpose:** System verification

**Tests:**
- Configuration loading
- Data file existence
- Python package imports
- ML model training
- API endpoint responses

**Usage:**
```bash
python test_system.py
```

**Output:**
```
✓ PASS - Configuration
✓ PASS - Data Files
✓ PASS - Python Imports
✓ PASS - Forecast Model
✓ PASS - Flask API
```

#### `setup.bat` (Windows)
**Purpose:** Automated setup

**What it does:**
1. Installs Python dependencies
2. Generates initial data
3. Displays next steps

**Usage:**
```bash
setup.bat
```

#### `run_backend.bat` (Windows)
**Purpose:** Start Flask backend

**Usage:**
```bash
run_backend.bat
```

#### `run_dashboard.bat` (Windows)
**Purpose:** Start Streamlit dashboard

**Usage:**
```bash
run_dashboard.bat
```

---

### Configuration Files

#### `.env.example`
**Purpose:** Environment variable template

**Variables:**
- FLASK_PORT
- STREAMLIT_PORT
- EMAIL_ALERTS
- WHATSAPP_ALERTS
- ALERT_EMAIL
- PRICE_DROP_THRESHOLD
- INVENTORY_THRESHOLD

**Usage:**
```bash
cp .env.example .env
# Edit .env with your values
```

#### `.gitignore`
**Purpose:** Git ignore rules

**Ignores:**
- Python cache files
- Virtual environments
- IDE files
- Log files
- OS files

---

## 🗺️ Navigation Guide

### I want to...

**...get started quickly**
→ Read `QUICKSTART.md`

**...understand all features**
→ Read `README.md`

**...fix installation issues**
→ Read `INSTALLATION.md`

**...prepare for demo**
→ Read `DEMO_GUIDE.md`

**...understand the architecture**
→ Read `ARCHITECTURE.md`

**...see project overview**
→ Read `PROJECT_SUMMARY.md`

**...find a specific file**
→ Read `INDEX.md` (this file)

**...run the system**
→ Run `python start.py`

**...test the system**
→ Run `python test_system.py`

**...modify the code**
→ Edit `app.py`, `dashboard.py`, or model files

**...add new materials**
→ Edit `config.py` and run `python -m utils.data_generator`

**...customize alerts**
→ Edit `utils/notifications.py`

**...change ML model**
→ Edit `models/forecast_model.py`

---

## 📊 File Statistics

### Code Files
- **Python files:** 10
- **Total lines of code:** ~2,500+
- **Total code size:** ~80 KB

### Documentation Files
- **Markdown files:** 7
- **Total documentation:** ~70 KB
- **Total pages:** ~50+

### Configuration Files
- **Config files:** 3
- **Batch scripts:** 3

### Data Files (Generated)
- **CSV files:** 1 (material_prices.csv)
- **JSON files:** 3 (inventory, vendors, alerts)

### Total Project
- **Files:** 22+
- **Directories:** 3
- **Size:** ~150 KB (excluding dependencies)

---

## 🔍 File Dependencies

### Dependency Graph

```
app.py
├── config.py
├── models/forecast_model.py
│   └── (Prophet, Pandas, NumPy)
├── utils/notifications.py
└── utils/data_generator.py

dashboard.py
├── config.py
└── (Streamlit, Plotly, Requests)

start.py
├── app.py
└── dashboard.py

test_system.py
├── app.py
├── models/forecast_model.py
└── utils/data_generator.py
```

---

## 📦 Data Flow

```
utils/data_generator.py
    ↓
data/material_prices.csv
data/inventory.json
data/vendors.json
    ↓
app.py (loads data)
    ↓
models/forecast_model.py (trains on data)
    ↓
app.py (serves via API)
    ↓
dashboard.py (fetches and displays)
    ↓
User Interface
```

---

## 🎯 Entry Points

### For Users
1. **Quick Start:** `QUICKSTART.md`
2. **Run System:** `python start.py`
3. **View Dashboard:** http://localhost:8501

### For Developers
1. **Architecture:** `ARCHITECTURE.md`
2. **Backend Code:** `app.py`
3. **Frontend Code:** `dashboard.py`
4. **ML Model:** `models/forecast_model.py`

### For Presenters
1. **Demo Guide:** `DEMO_GUIDE.md`
2. **Project Summary:** `PROJECT_SUMMARY.md`
3. **Run Demo:** `python start.py`

---

## 🔄 Update Frequency

### Auto-Generated Files
- `data/material_prices.csv` - Updated every 5 minutes (simulated)
- `data/alerts.json` - Updated on alert creation
- `data/forecast_cache.json` - Updated every 1 hour

### Static Files
- All code files - Manual updates only
- All documentation - Manual updates only
- Configuration files - Manual updates only

---

## 💾 Backup Recommendations

### Critical Files (Always Backup)
- `app.py`
- `dashboard.py`
- `models/forecast_model.py`
- `config.py`
- All documentation files

### Generated Files (Can Regenerate)
- `data/*.csv`
- `data/*.json`
- `__pycache__/`

### Configuration Files (Backup if Customized)
- `.env`
- `config.py`

---

## 🚀 Quick Commands Reference

```bash
# Setup
pip install -r requirements.txt
python -m utils.data_generator

# Run
python start.py
# OR
python app.py                    # Terminal 1
streamlit run dashboard.py       # Terminal 2

# Test
python test_system.py

# Generate Data
python -m utils.data_generator

# Test Model
python -m models.forecast_model

# Test Notifications
python -m utils.notifications
```

---

## 📞 Support

### Documentation Priority
1. **QUICKSTART.md** - First stop for new users
2. **README.md** - Comprehensive guide
3. **INSTALLATION.md** - Setup issues
4. **ARCHITECTURE.md** - Technical questions
5. **DEMO_GUIDE.md** - Presentation help

### Troubleshooting Order
1. Run `python test_system.py`
2. Check console logs
3. Review `INSTALLATION.md`
4. Check `README.md` troubleshooting section

---

## ✅ File Checklist

Use this to verify complete project:

- [ ] app.py
- [ ] dashboard.py
- [ ] config.py
- [ ] requirements.txt
- [ ] models/__init__.py
- [ ] models/forecast_model.py
- [ ] utils/__init__.py
- [ ] utils/data_generator.py
- [ ] utils/notifications.py
- [ ] start.py
- [ ] test_system.py
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] INSTALLATION.md
- [ ] DEMO_GUIDE.md
- [ ] ARCHITECTURE.md
- [ ] PROJECT_SUMMARY.md
- [ ] INDEX.md
- [ ] .env.example
- [ ] .gitignore
- [ ] setup.bat
- [ ] run_backend.bat
- [ ] run_dashboard.bat

**Total:** 22 essential files

---

**Last Updated:** October 2024  
**Version:** 1.0  
**Maintained By:** Smart Procurement Team
