# 🏗️ Smart Procurement System - Architecture Documentation

## System Overview

The Smart Procurement System is a full-stack application designed to help factories optimize material purchasing decisions through real-time price monitoring, ML-based forecasting, and intelligent recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Streamlit Dashboard (Port 8501)                │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │  │
│  │  │Overview│ │ Price  │ │Inventory│ │ Alerts │ │Vendors │ │  │
│  │  │  Page  │ │Analysis│ │  Page   │ │  Page  │ │  Page  │ │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ │  │
│  │                                                            │  │
│  │  Plotly Charts | Metrics | Tables | Gauges                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND (Port 5000)                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    REST API Endpoints                     │  │
│  │  /api/prices  /api/forecast  /api/inventory  /api/alerts │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Background Scheduler (APScheduler)           │  │
│  │  ┌────────────────┐              ┌────────────────┐      │  │
│  │  │ Price Updates  │              │Forecast Updates│      │  │
│  │  │  (5 minutes)   │              │   (1 hour)     │      │  │
│  │  └────────────────┘              └────────────────┘      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Business Logic Layer                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │  │
│  │  │  Price   │  │Inventory │  │  Alert   │               │  │
│  │  │ Manager  │  │ Manager  │  │ Manager  │               │  │
│  │  └──────────┘  └──────────┘  └──────────┘               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ML/AI LAYER                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Prophet Forecasting Model                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │   Copper   │  │  Aluminum  │  │   Steel    │         │  │
│  │  │   Model    │  │   Model    │  │   Model    │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  │                                                            │  │
│  │  Features: Trend, Seasonality, Confidence Intervals       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Recommendation Engine                          │  │
│  │  Input: Current Price + Forecast                          │  │
│  │  Output: BUY NOW / WAIT / MONITOR                         │  │
│  │  Logic: Price change threshold analysis                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │material_     │  │inventory.json│  │vendors.json  │         │
│  │prices.csv    │  │              │  │              │         │
│  │              │  │              │  │              │         │
│  │30 days       │  │Stock levels  │  │Vendor prices │         │
│  │historical    │  │Consumption   │  │Ratings       │         │
│  │prices        │  │Thresholds    │  │Delivery      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │alerts.json   │  │forecast_     │                            │
│  │              │  │cache.json    │                            │
│  │Alert history │  │Cached        │                            │
│  │Notifications │  │predictions   │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (Streamlit)

**File:** `dashboard.py`

**Responsibilities:**
- User interface rendering
- Data visualization
- User interaction handling
- API consumption

**Key Features:**
- 5 main pages (Overview, Price Analysis, Inventory, Alerts, Vendors)
- Real-time data refresh
- Interactive Plotly charts
- Responsive design

**Technologies:**
- Streamlit 1.29.0
- Plotly 5.18.0
- Pandas for data manipulation

### 2. Backend Layer (Flask)

**File:** `app.py`

**Responsibilities:**
- REST API endpoints
- Business logic orchestration
- Background task scheduling
- Data management

**Key Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | System health check |
| `/api/prices/current` | GET | Current material prices |
| `/api/prices/historical/<material>` | GET | Historical price data |
| `/api/forecast/<material>` | GET | Price forecast |
| `/api/recommendations` | GET | Buy/wait recommendations |
| `/api/inventory` | GET | Inventory levels |
| `/api/vendors/<material>` | GET | Vendor comparison |
| `/api/alerts` | GET | Alert notifications |
| `/api/dashboard/summary` | GET | Complete dashboard data |

**Background Tasks:**
- Price updates: Every 5 minutes
- Forecast updates: Every 1 hour
- Alert checks: On every update

**Technologies:**
- Flask 3.0.0
- Flask-CORS 4.0.0
- APScheduler 3.10.4

### 3. ML/AI Layer

**File:** `models/forecast_model.py`

**Class:** `PriceForecastModel`

**Responsibilities:**
- Time-series forecasting
- Model training and prediction
- Recommendation generation

**Forecasting Process:**

```python
1. Data Preparation
   ├── Load historical prices
   ├── Format for Prophet (ds, y columns)
   └── Sort by date

2. Model Training
   ├── Initialize Prophet model
   ├── Configure seasonality
   ├── Fit on historical data
   └── Store trained model

3. Prediction
   ├── Create future dataframe (7 days)
   ├── Generate predictions
   ├── Calculate confidence intervals
   └── Return forecast

4. Recommendation Logic
   ├── Compare current vs forecast price
   ├── Calculate % change
   ├── Apply decision rules:
   │   ├── If +2%: BUY NOW
   │   ├── If -2%: WAIT
   │   └── Else: MONITOR
   └── Return recommendation + reason
```

**Model Parameters:**
- `daily_seasonality`: False
- `weekly_seasonality`: True
- `yearly_seasonality`: False
- `changepoint_prior_scale`: 0.05
- `interval_width`: 0.95 (95% confidence)

**Technologies:**
- Prophet 1.1.5
- Scikit-learn 1.3.2
- NumPy 1.26.2

### 4. Notification Layer

**File:** `utils/notifications.py`

**Class:** `NotificationManager`

**Responsibilities:**
- Alert creation and management
- Notification dispatch
- Alert history tracking

**Alert Types:**
1. **PRICE_DROP**: Price decreased > threshold
2. **PRICE_INCREASE**: Price increased > threshold
3. **LOW_INVENTORY**: Stock below minimum

**Alert Severities:**
- **CRITICAL**: Requires immediate action
- **WARNING**: Important but not urgent
- **INFO**: Informational only

**Notification Channels:**
- Console output (current)
- Email (simulated, ready for SMTP)
- WhatsApp (simulated, ready for Twilio)

### 5. Data Layer

**Files:**
- `data/material_prices.csv`: Historical price data
- `data/inventory.json`: Current stock levels
- `data/vendors.json`: Vendor information
- `data/alerts.json`: Alert history

**Data Generation:**

**File:** `utils/data_generator.py`

**Functions:**
- `generate_historical_prices()`: Creates 30 days of mock price data
- `generate_inventory_data()`: Creates inventory levels
- `generate_vendor_data()`: Creates vendor comparison data
- `initialize_data()`: Orchestrates all data generation

**Data Characteristics:**
- Realistic price volatility
- Random walk with trend
- Seasonal patterns
- Vendor price variations

## Data Flow

### 1. Price Update Flow

```
Timer (5 min) → simulate_price_update()
                      ↓
              Update price_data
                      ↓
              check_alerts()
                      ↓
         notification_manager.check_price_alerts()
                      ↓
              Create alerts if threshold exceeded
                      ↓
              Save to alerts.json
```

### 2. Forecast Update Flow

```
Timer (1 hour) → update_forecasts()
                      ↓
         forecast_model.train_all_materials()
                      ↓
         For each material:
           ├── Train Prophet model
           ├── Generate 7-day forecast
           └── Calculate recommendation
                      ↓
         Store in forecast_results
                      ↓
         check_alerts()
```

### 3. Dashboard Request Flow

```
User opens dashboard → Streamlit loads
                      ↓
         fetch_data("dashboard/summary")
                      ↓
         HTTP GET to Flask API
                      ↓
         Flask: get_dashboard_summary()
                      ↓
         Aggregate data from:
           ├── price_data
           ├── inventory_data
           ├── forecast_results
           └── notification_manager
                      ↓
         Return JSON response
                      ↓
         Streamlit renders UI
```

## Configuration Management

**File:** `config.py`

**Configuration Categories:**

1. **Server Settings**
   - Flask port: 5000
   - Streamlit port: 8501
   - Debug mode

2. **Materials**
   - List of tracked materials
   - Can be extended easily

3. **Update Intervals**
   - Price updates: 300s (5 min)
   - Forecast updates: 3600s (1 hour)

4. **Alert Thresholds**
   - Price drop threshold: 5%
   - Inventory threshold: 100 tons

5. **Forecasting Parameters**
   - Forecast days: 7
   - Historical days: 30

6. **File Paths**
   - Data directory
   - CSV/JSON file locations

## Security Considerations

### Current Implementation (Prototype)
- No authentication
- No encryption
- Local file storage
- CORS enabled for all origins

### Production Recommendations
1. **Authentication**
   - JWT tokens
   - Role-based access control
   - Session management

2. **Data Security**
   - HTTPS/TLS
   - Database encryption
   - API key management

3. **Input Validation**
   - Request sanitization
   - SQL injection prevention
   - XSS protection

4. **Rate Limiting**
   - API request throttling
   - DDoS protection

## Scalability Considerations

### Current Limitations
- Single-threaded Flask (dev server)
- In-memory data storage
- No caching layer
- No load balancing

### Scaling Strategies

1. **Horizontal Scaling**
   - Deploy multiple Flask instances
   - Use Gunicorn/uWSGI
   - Add load balancer (Nginx)

2. **Database**
   - Migrate to PostgreSQL/MongoDB
   - Add connection pooling
   - Implement caching (Redis)

3. **Asynchronous Processing**
   - Use Celery for background tasks
   - Message queue (RabbitMQ/Redis)
   - Separate forecast service

4. **CDN & Caching**
   - Cache static assets
   - API response caching
   - Browser caching headers

## Performance Optimization

### Current Performance
- API response time: <100ms
- Forecast generation: ~30s (initial)
- Dashboard load time: ~2s

### Optimization Opportunities

1. **Caching**
   - Cache forecast results
   - Cache historical data queries
   - Implement ETags

2. **Database Indexing**
   - Index on material + date
   - Optimize queries

3. **Lazy Loading**
   - Load charts on demand
   - Paginate historical data

4. **Code Optimization**
   - Vectorize operations
   - Reduce API calls
   - Optimize Prophet parameters

## Monitoring & Logging

### Current Implementation
- Console logging
- Basic error handling

### Production Requirements

1. **Application Monitoring**
   - Request/response logging
   - Error tracking (Sentry)
   - Performance metrics

2. **System Monitoring**
   - CPU/Memory usage
   - Disk space
   - Network traffic

3. **Business Metrics**
   - Forecast accuracy
   - Recommendation success rate
   - User engagement

## Testing Strategy

### Unit Tests
- Test forecast model accuracy
- Test recommendation logic
- Test data generation

### Integration Tests
- Test API endpoints
- Test background tasks
- Test alert system

### End-to-End Tests
- Test complete user workflows
- Test dashboard interactions

### Performance Tests
- Load testing API
- Stress testing forecast generation

## Deployment

### Local Development
```bash
python app.py
streamlit run dashboard.py
```

### Production Deployment

**Option 1: Traditional Server**
```bash
# Backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
streamlit run dashboard.py --server.port 8501
```

**Option 2: Docker**
```dockerfile
# Backend container
FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app"]

# Frontend container
FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "dashboard.py"]
```

**Option 3: Cloud (AWS/Azure/GCP)**
- Backend: Elastic Beanstalk / App Service / Cloud Run
- Frontend: S3 + CloudFront / Blob Storage / Cloud Storage
- Database: RDS / Azure SQL / Cloud SQL

## Maintenance

### Regular Tasks
- Update dependencies
- Retrain models with new data
- Review alert thresholds
- Clean old data

### Backup Strategy
- Daily database backups
- Version control for code
- Configuration backups

## Future Architecture Enhancements

1. **Microservices**
   - Separate forecast service
   - Separate notification service
   - API gateway

2. **Real-time Data**
   - WebSocket connections
   - Server-sent events
   - Real-time price feeds

3. **Advanced ML**
   - Ensemble models
   - Deep learning (LSTM)
   - Anomaly detection

4. **Mobile App**
   - React Native app
   - Push notifications
   - Offline support

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Smart Procurement Team
