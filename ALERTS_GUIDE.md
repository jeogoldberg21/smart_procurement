# Alert System Guide

## 🔔 Overview

The Smart Procurement System includes a comprehensive alert system that monitors prices, inventory, and forecasts to provide actionable notifications.

---

## 📊 Alert Types

### 1. **Price Alerts**

#### PRICE_DROP (⚠️ WARNING)
- **Trigger**: Price drops by ≥5% (configurable)
- **Message**: "Material price dropped X% to $Y/ton. Consider buying!"
- **Action**: Evaluate purchasing opportunity

#### PRICE_INCREASE (ℹ️ INFO)
- **Trigger**: Price increases by ≥5%
- **Message**: "Material price increased X% to $Y/ton."
- **Action**: Monitor trend, consider delaying purchases

### 2. **Inventory Alerts**

#### LOW_INVENTORY (🔴 CRITICAL)
- **Trigger**: Stock < 3 days remaining
- **Message**: "Material inventory CRITICAL: X tons remaining (~Y days). Immediate action required!"
- **Action**: Place emergency order immediately

#### LOW_INVENTORY (⚠️ WARNING)
- **Trigger**: Stock < 7 days remaining
- **Message**: "Material inventory low: X tons remaining (~Y days). Plan reorder soon."
- **Action**: Schedule reorder within 1-2 days

#### HIGH_INVENTORY (ℹ️ INFO)
- **Trigger**: Stock > 90% of capacity
- **Message**: "Material inventory high: X tons (Y% of capacity). Consider reducing orders."
- **Action**: Reduce future order quantities

### 3. **Forecast Alerts**

#### FORECAST_BUY (⚠️ WARNING)
- **Trigger**: AI recommends "BUY NOW"
- **Message**: "Material: [Reason]. Action: BUY NOW"
- **Action**: Purchase before predicted price increase

#### FORECAST_WAIT (ℹ️ INFO)
- **Trigger**: AI recommends "WAIT"
- **Message**: "Material: [Reason]. Action: WAIT"
- **Action**: Delay purchase, prices expected to drop

### 4. **Smart Reorder Alerts**

#### REORDER_NOW (⚠️ WARNING)
- **Trigger**: Low stock (7-14 days) + favorable price forecast
- **Message**: "Optimal reorder time! Stock: X days remaining + Favorable price forecast."
- **Action**: Place order now for best value

#### REORDER_WAIT (ℹ️ INFO)
- **Trigger**: Low stock but prices expected to drop
- **Message**: "Stock low (X days) but prices expected to drop. Monitor closely."
- **Action**: Wait if possible, monitor daily

---

## 🎯 Alert Severity Levels

| Severity | Color | Priority | Response Time |
|----------|-------|----------|---------------|
| **CRITICAL** | 🔴 Red | Highest | Immediate (< 1 hour) |
| **WARNING** | 🟡 Yellow | High | Same day |
| **INFO** | 🔵 Blue | Normal | Within 1-2 days |

---

## ⚙️ Configuration

### Alert Thresholds

Edit in `config.py` or `.env`:

```python
# Price change threshold (%)
PRICE_DROP_THRESHOLD = 5  # Alert if price drops ≥5%

# Inventory threshold (tons)
INVENTORY_THRESHOLD = 100  # Alert if stock < 100 tons
```

### Alert Frequency

Alerts are checked:
- **After every forecast update** (every 1 hour)
- **After every price update** (every 5 minutes)
- **Manually via API** (on-demand)

### Duplicate Prevention

The system prevents duplicate alerts:
- **Price alerts**: 1-hour cooldown
- **Inventory alerts**: 6-hour cooldown
- **Forecast alerts**: 24-hour cooldown
- **Reorder alerts**: 24-hour cooldown

---

## 🔧 How Alerts Work

### Alert Generation Flow

```
1. Trigger Event (price update, forecast, etc.)
   ↓
2. Check conditions for each material
   ↓
3. Check if similar alert exists (avoid duplicates)
   ↓
4. Create alert if conditions met
   ↓
5. Save to alerts.json
   ↓
6. Display in console
   ↓
7. Show in dashboard
   ↓
8. (Optional) Send email/SMS
```

### Alert Storage

Alerts are stored in `data/alerts.json`:

```json
{
  "id": 1,
  "timestamp": "2024-10-15T17:30:00",
  "type": "PRICE_DROP",
  "material": "Copper",
  "message": "Copper price dropped 7.2% to $8234.50/ton. Consider buying!",
  "severity": "WARNING",
  "read": false
}
```

---

## 📱 Accessing Alerts

### 1. **Dashboard UI**

Navigate to **🔔 Alerts** page:
- View all alerts
- Filter by type/severity
- Mark as read
- See alert summary

### 2. **API Endpoints**

#### Get Alerts
```bash
GET /api/alerts?limit=50&unread_only=false
```

Response:
```json
{
  "alerts": [...],
  "summary": {
    "total": 45,
    "unread": 12,
    "by_severity": {
      "CRITICAL": 2,
      "WARNING": 8,
      "INFO": 35
    },
    "by_type": {
      "PRICE_DROP": 5,
      "LOW_INVENTORY": 3,
      "FORECAST_BUY": 4
    }
  }
}
```

#### Mark Alert as Read
```bash
POST /api/alerts/123/read
```

#### Trigger Alert Check
```bash
POST /api/alerts/trigger
```

### 3. **Console Output**

Alerts are printed to console in real-time:

```
🔔 ALERT [WARNING]: Copper price dropped 7.2% to $8234.50/ton. Consider buying!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Smart Procurement Alert
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: PRICE_DROP
Material: Copper
Severity: WARNING

Copper price dropped 7.2% to $8234.50/ton. Consider buying!

Time: 2024-10-15T17:30:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎨 Dashboard Display

### Alert Card Format

```
┌─────────────────────────────────────┐
│ 🔴 CRITICAL                         │
│ LOW_INVENTORY                       │
│                                     │
│ Aluminum inventory CRITICAL:        │
│ 45 tons remaining (~2.3 days).      │
│ Immediate action required!          │
│                                     │
│ 📅 2024-10-15 17:30:00             │
└─────────────────────────────────────┘
```

### Alert Filters

- **By Type**: PRICE_DROP, LOW_INVENTORY, FORECAST_BUY, etc.
- **By Severity**: CRITICAL, WARNING, INFO
- **By Status**: Read / Unread
- **By Material**: Copper, Aluminum, Steel

---

## 🚀 Advanced Features

### 1. **Smart Reorder Logic**

Combines inventory levels with price forecasts:

```python
if days_remaining < 14 and forecast == "BUY NOW":
    → Alert: "Optimal reorder time!"
    
if days_remaining < 14 and forecast == "WAIT":
    → Alert: "Stock low but prices dropping. Monitor closely."
```

### 2. **Automatic Cleanup**

Old alerts are automatically removed:
- Keeps last **30 days** of alerts
- Runs during each alert check
- Prevents database bloat

### 3. **Duplicate Prevention**

Prevents alert spam:
- Tracks recent alerts by material + type
- Enforces cooldown periods
- Only alerts on significant changes

---

## 📧 Email Notifications (Optional)

### Setup Email Alerts

1. **Configure SMTP** (future feature):
```python
EMAIL_ALERTS = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
ALERT_EMAIL = "procurement@company.com"
```

2. **Email Template**:
```
Subject: [CRITICAL] Smart Procurement Alert

Material: Aluminum
Type: LOW_INVENTORY
Severity: CRITICAL

Aluminum inventory CRITICAL: 45 tons remaining (~2.3 days).
Immediate action required!

Time: 2024-10-15 17:30:00

---
Smart Procurement System
```

---

## 🧪 Testing Alerts

### Manual Testing

```python
# In Python console
from utils.notifications import NotificationManager

manager = NotificationManager()

# Test price drop alert
manager.create_alert(
    'PRICE_DROP',
    'Copper',
    'Copper price dropped 7.5% to $8200/ton. Consider buying!',
    'WARNING'
)

# Test inventory alert
manager.create_alert(
    'LOW_INVENTORY',
    'Aluminum',
    'Aluminum inventory low: 85 tons remaining (~3 days)',
    'CRITICAL'
)
```

### API Testing

```bash
# Trigger alert check
curl -X POST http://localhost:5000/api/alerts/trigger

# Get alerts
curl http://localhost:5000/api/alerts?limit=10

# Mark as read
curl -X POST http://localhost:5000/api/alerts/1/read
```

---

## 📊 Alert Analytics

### View Alert Summary

```python
summary = notification_manager.get_alert_summary()

# Returns:
{
  'total': 45,
  'unread': 12,
  'by_severity': {
    'CRITICAL': 2,
    'WARNING': 8,
    'INFO': 35
  },
  'by_type': {
    'PRICE_DROP': 5,
    'LOW_INVENTORY': 3,
    'FORECAST_BUY': 4,
    'REORDER_NOW': 2
  }
}
```

---

## 🔍 Troubleshooting

### Issue: No Alerts Appearing

**Check:**
1. Alert thresholds in config
2. Data is updating (prices, inventory)
3. `data/alerts.json` exists and is writable
4. Console output for alert messages

**Solution:**
```bash
# Manually trigger alert check
curl -X POST http://localhost:5000/api/alerts/trigger

# Check alert file
cat data/alerts.json
```

### Issue: Too Many Alerts

**Solution:**
```python
# Increase thresholds
PRICE_DROP_THRESHOLD = 10  # Only alert on 10%+ drops

# Or increase cooldown periods in notifications.py
_has_recent_alert(material, 'PRICE_DROP', hours=6)  # 6-hour cooldown
```

### Issue: Duplicate Alerts

**Solution:**
The system already prevents duplicates. If you see duplicates:
1. Check cooldown periods
2. Verify `_has_recent_alert()` is working
3. Ensure alerts are being saved properly

---

## 📈 Best Practices

1. **Review alerts daily** - Check dashboard every morning
2. **Prioritize by severity** - Handle CRITICAL alerts first
3. **Mark as read** - Keep track of what you've reviewed
4. **Adjust thresholds** - Fine-tune based on your needs
5. **Monitor trends** - Look for patterns in alerts
6. **Act quickly** - Respond to time-sensitive alerts promptly

---

## 🎯 Alert Action Guide

| Alert Type | Immediate Action | Follow-up |
|------------|------------------|-----------|
| **PRICE_DROP** | Review forecast, consider buying | Place order if confirmed |
| **LOW_INVENTORY** | Check lead times, place order | Confirm delivery date |
| **FORECAST_BUY** | Evaluate budget, prepare PO | Execute purchase |
| **REORDER_NOW** | Combine orders for efficiency | Track shipment |
| **HIGH_INVENTORY** | Reduce next order quantity | Review consumption rate |

---

## 🔮 Future Enhancements

Planned improvements:
- [ ] SMS/WhatsApp notifications
- [ ] Email integration
- [ ] Slack/Teams webhooks
- [ ] Custom alert rules
- [ ] Alert escalation
- [ ] Alert acknowledgment workflow
- [ ] Alert history analytics
- [ ] Predictive alerting (ML-based)

---

**Version**: 1.0  
**Last Updated**: October 2024  
**Status**: ✅ Fully Functional
