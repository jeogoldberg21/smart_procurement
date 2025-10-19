"""
Notification system for price alerts and inventory warnings
"""
from datetime import datetime
import json
import os

class NotificationManager:
    """
    Manages alerts and notifications
    """
    
    def __init__(self, alert_log_path='data/alerts.json'):
        self.alert_log_path = alert_log_path
        self.alerts = []
        self.load_alerts()
    
    def load_alerts(self):
        """Load existing alerts from file"""
        if os.path.exists(self.alert_log_path):
            try:
                with open(self.alert_log_path, 'r') as f:
                    self.alerts = json.load(f)
            except:
                self.alerts = []
        else:
            self.alerts = []
    
    def save_alerts(self):
        """Save alerts to file"""
        os.makedirs(os.path.dirname(self.alert_log_path), exist_ok=True)
        with open(self.alert_log_path, 'w') as f:
            json.dump(self.alerts[-100:], f, indent=2)  # Keep last 100 alerts
    
    def create_alert(self, alert_type, material, message, severity='INFO'):
        """
        Create a new alert
        
        Args:
            alert_type: Type of alert (PRICE_DROP, LOW_INVENTORY, etc.)
            material: Material name
            message: Alert message
            severity: INFO, WARNING, CRITICAL
        """
        alert = {
            'id': len(self.alerts) + 1,
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'material': material,
            'message': message,
            'severity': severity,
            'read': False
        }
        
        self.alerts.append(alert)
        self.save_alerts()
        
        # Simulate sending notification
        self._send_notification(alert)
        
        return alert
    
    def _send_notification(self, alert):
        """
        Simulate sending notification (email/WhatsApp)
        """
        # In production, this would integrate with email/SMS services
        print(f"\n🔔 ALERT [{alert['severity']}]: {alert['message']}")
        
        # Simulate email
        if alert['severity'] in ['WARNING', 'CRITICAL']:
            self._simulate_email(alert)
    
    def _simulate_email(self, alert):
        """Simulate email notification"""
        email_content = f"""
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Smart Procurement Alert
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        Type: {alert['type']}
        Material: {alert['material']}
        Severity: {alert['severity']}
        
        {alert['message']}
        
        Time: {alert['timestamp']}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        # In production: send via SMTP
        print(email_content)
    
    def check_price_alerts(self, current_prices, previous_prices, threshold=5):
        """
        Check for significant price drops
        
        Args:
            current_prices: Dict of current material prices
            previous_prices: Dict of previous material prices
            threshold: Percentage drop to trigger alert
        """
        for material, current_price in current_prices.items():
            if material in previous_prices:
                prev_price = previous_prices[material]
                price_change_pct = ((current_price - prev_price) / prev_price) * 100
                
                # Check if similar alert was already created recently (avoid duplicates)
                if not self._has_recent_alert(material, 'PRICE_DROP', hours=1) and price_change_pct <= -threshold:
                    message = f"{material} price dropped {abs(price_change_pct):.1f}% to ${current_price:.2f}/ton. Consider buying!"
                    self.create_alert('PRICE_DROP', material, message, 'WARNING')
                
                elif not self._has_recent_alert(material, 'PRICE_INCREASE', hours=1) and price_change_pct >= threshold:
                    message = f"{material} price increased {price_change_pct:.1f}% to ${current_price:.2f}/ton."
                    self.create_alert('PRICE_INCREASE', material, message, 'INFO')
    
    def check_inventory_alerts(self, inventory, threshold=100):
        """
        Check for low inventory levels
        
        Args:
            inventory: Dict of inventory data
            threshold: Minimum stock level
        """
        for material, data in inventory.items():
            current_stock = data.get('current_stock', 0)
            min_threshold = data.get('min_threshold', threshold)
            daily_consumption = data.get('daily_consumption', 1)
            
            if current_stock < min_threshold:
                days_remaining = current_stock / daily_consumption
                
                # Only alert if not already alerted recently
                if not self._has_recent_alert(material, 'LOW_INVENTORY', hours=6):
                    if days_remaining < 3:
                        message = f"{material} inventory CRITICAL: {current_stock:.1f} tons remaining (~{days_remaining:.1f} days). Immediate action required!"
                        self.create_alert('LOW_INVENTORY', material, message, 'CRITICAL')
                    elif days_remaining < 7:
                        message = f"{material} inventory low: {current_stock:.1f} tons remaining (~{days_remaining:.1f} days). Plan reorder soon."
                        self.create_alert('LOW_INVENTORY', material, message, 'WARNING')
            
            # Check for overstocking
            max_capacity = data.get('max_capacity', 1000)
            if current_stock > max_capacity * 0.9:
                if not self._has_recent_alert(material, 'HIGH_INVENTORY', hours=24):
                    message = f"{material} inventory high: {current_stock:.1f} tons ({(current_stock/max_capacity)*100:.1f}% of capacity). Consider reducing orders."
                    self.create_alert('HIGH_INVENTORY', material, message, 'INFO')
    
    def get_recent_alerts(self, limit=10, unread_only=False):
        """Get recent alerts"""
        alerts = self.alerts
        
        if unread_only:
            alerts = [a for a in alerts if not a.get('read', False)]
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def mark_as_read(self, alert_id):
        """Mark alert as read"""
        found = False
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['read'] = True
                found = True
                break
        
        if found:
            self.save_alerts()
            print(f"✓ Alert {alert_id} marked as read")
            return True
        else:
            print(f"✗ Alert {alert_id} not found")
            return False
    
    def mark_all_as_read(self):
        """Mark all alerts as read"""
        count = 0
        for alert in self.alerts:
            if not alert.get('read', False):
                alert['read'] = True
                count += 1
        
        if count > 0:
            self.save_alerts()
            print(f"✓ Marked {count} alerts as read")
        
        return count
    
    def _has_recent_alert(self, material, alert_type, hours=1):
        """
        Check if a similar alert was created recently to avoid duplicates
        
        Args:
            material: Material name
            alert_type: Type of alert
            hours: Time window in hours
        """
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for alert in reversed(self.alerts):  # Check recent alerts first
            alert_time = datetime.fromisoformat(alert['timestamp'])
            if alert_time < cutoff_time:
                break
            
            if alert['material'] == material and alert['type'] == alert_type:
                return True
        
        return False
    
    def check_forecast_alerts(self, forecast_results):
        """
        Check forecast data and create alerts for predicted price changes
        
        Args:
            forecast_results: Dict of forecast results by material
        """
        for material, result in forecast_results.items():
            if not result:
                continue
            
            recommendation = result.get('recommendation', {})
            action = recommendation.get('action', '')
            
            # Alert for BUY NOW recommendations
            if action == 'BUY NOW' and not self._has_recent_alert(material, 'FORECAST_BUY', hours=24):
                reason = recommendation.get('reason', '')
                message = f"{material}: {reason} Action: BUY NOW"
                self.create_alert('FORECAST_BUY', material, message, 'WARNING')
            
            # Alert for significant predicted price increases
            elif action == 'WAIT' and not self._has_recent_alert(material, 'FORECAST_WAIT', hours=24):
                reason = recommendation.get('reason', '')
                message = f"{material}: {reason} Action: WAIT"
                self.create_alert('FORECAST_WAIT', material, message, 'INFO')
    
    def check_reorder_alerts(self, inventory, forecast_results):
        """
        Smart reorder alerts based on inventory and price forecasts
        
        Args:
            inventory: Dict of inventory data
            forecast_results: Dict of forecast results
        """
        for material, data in inventory.items():
            current_stock = data.get('current_stock', 0)
            daily_consumption = data.get('daily_consumption', 1)
            min_threshold = data.get('min_threshold', 100)
            
            days_remaining = current_stock / daily_consumption
            
            # Check if we should reorder based on inventory and price forecast
            if days_remaining < 14 and days_remaining > 7:  # Reorder window
                if material in forecast_results and forecast_results[material]:
                    recommendation = forecast_results[material].get('recommendation', {})
                    action = recommendation.get('action', '')
                    
                    if action == 'BUY NOW' and not self._has_recent_alert(material, 'REORDER_NOW', hours=24):
                        message = f"{material}: Optimal reorder time! Stock: {days_remaining:.1f} days remaining + Favorable price forecast."
                        self.create_alert('REORDER_NOW', material, message, 'WARNING')
                    elif action == 'WAIT' and not self._has_recent_alert(material, 'REORDER_WAIT', hours=24):
                        message = f"{material}: Stock low ({days_remaining:.1f} days) but prices expected to drop. Monitor closely."
                        self.create_alert('REORDER_WAIT', material, message, 'INFO')
    
    def get_alert_summary(self):
        """Get summary of alerts"""
        total = len(self.alerts)
        unread = len([a for a in self.alerts if not a.get('read', False)])
        
        by_severity = {}
        by_type = {}
        for alert in self.alerts:
            severity = alert['severity']
            alert_type = alert['type']
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
        
        return {
            'total': total,
            'unread': unread,
            'by_severity': by_severity,
            'by_type': by_type
        }
    
    def clear_old_alerts(self, days=30):
        """
        Clear alerts older than specified days
        
        Args:
            days: Number of days to keep
        """
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(days=days)
        
        self.alerts = [
            alert for alert in self.alerts
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ]
        self.save_alerts()
        
        return len(self.alerts)

if __name__ == '__main__':
    # Test notifications
    manager = NotificationManager()
    
    # Test price alert
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
    
    print(f"\nAlert Summary: {manager.get_alert_summary()}")
