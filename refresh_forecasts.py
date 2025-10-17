"""
Quick script to refresh forecasts and test recommendations
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

print("🔄 Refreshing forecasts...")
print("=" * 60)

# Get current recommendations
try:
    response = requests.get(f"{API_BASE}/recommendations", timeout=10)
    if response.status_code == 200:
        data = response.json()
        recommendations = data.get('recommendations', [])
        
        print(f"\n✅ Found {len(recommendations)} recommendations:\n")
        
        for rec in recommendations:
            material = rec.get('material', 'Unknown')
            recommendation = rec.get('recommendation', 'N/A')
            reason = rec.get('reason', 'N/A')
            current_price = rec.get('current_price', 0)
            avg_forecast = rec.get('avg_forecast_price', 0)
            change_pct = rec.get('price_change_pct', 0)
            savings = rec.get('potential_savings', 0)
            
            # Color coding
            if recommendation == 'BUY NOW':
                icon = '🟢'
            elif recommendation == 'WAIT':
                icon = '🟡'
            else:
                icon = '🔵'
            
            print(f"{icon} {material}:")
            print(f"   Recommendation: {recommendation}")
            print(f"   Current Price: ${current_price:.2f}/ton")
            print(f"   Forecast Price: ${avg_forecast:.2f}/ton")
            print(f"   Expected Change: {change_pct:+.2f}%")
            print(f"   Potential Savings: ${savings:.2f}/ton")
            print(f"   Reason: {reason}")
            print()
        
        # Summary
        buy_count = sum(1 for r in recommendations if r.get('recommendation') == 'BUY NOW')
        wait_count = sum(1 for r in recommendations if r.get('recommendation') == 'WAIT')
        monitor_count = sum(1 for r in recommendations if r.get('recommendation') == 'MONITOR')
        
        print("=" * 60)
        print(f"📊 Summary:")
        print(f"   BUY NOW: {buy_count}")
        print(f"   WAIT: {wait_count}")
        print(f"   MONITOR: {monitor_count}")
        print("=" * 60)
        
    else:
        print(f"❌ Error: API returned status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error connecting to backend: {e}")
    print("\n💡 Make sure the backend is running:")
    print("   python app.py")
