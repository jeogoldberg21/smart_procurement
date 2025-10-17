"""
Complete System Check - Diagnose All Issues
"""
import os
import sys

print("="*70)
print("  SMART PROCUREMENT SYSTEM - COMPLETE DIAGNOSTIC")
print("="*70)
print()

errors = []
warnings = []

# 1. Check Data Files
print("[1/8] Checking Data Files...")
required_files = {
    'data/material_prices.csv': 'Price history',
    'data/inventory.json': 'Inventory data',
    'data/vendors.json': 'Vendor data'
}

for file, desc in required_files.items():
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"      ✅ {desc}: {file} ({size} bytes)")
    else:
        print(f"      ❌ Missing: {file}")
        errors.append(f"Missing {desc}: {file}")

print()

# 2. Check Dependencies
print("[2/8] Checking Python Packages...")
required_packages = [
    'pandas', 'numpy', 'flask', 'streamlit', 
    'plotly', 'prophet', 'requests'
]

for package in required_packages:
    try:
        __import__(package)
        print(f"      ✅ {package}")
    except ImportError:
        print(f"      ❌ {package} - NOT INSTALLED")
        errors.append(f"Missing package: {package}")

print()

# 3. Test Data Loading
print("[3/8] Testing Data Loading...")
try:
    import pandas as pd
    df = pd.read_csv('data/material_prices.csv')
    print(f"      ✅ Loaded {len(df)} price records")
    print(f"      ✅ Materials: {df['material'].unique().tolist()}")
except Exception as e:
    print(f"      ❌ Error loading prices: {e}")
    errors.append(f"Data loading error: {e}")

print()

# 4. Test Forecast Model
print("[4/8] Testing Forecast Model...")
try:
    from utils.forecast_model import ForecastModel
    model = ForecastModel()
    
    # Test forecast
    forecast = model.forecast_material('Copper', days=7)
    
    if forecast and 'forecast' in forecast:
        print(f"      ✅ Forecast generated: {len(forecast['forecast'])} days")
        print(f"      ✅ Recommendation: {forecast.get('recommendation', {}).get('recommendation')}")
    else:
        print(f"      ❌ Forecast failed or incomplete")
        errors.append("Forecast generation failed")
        
except Exception as e:
    print(f"      ❌ Forecast error: {e}")
    errors.append(f"Forecast error: {e}")

print()

# 5. Test Recommendations
print("[5/8] Testing Recommendations...")
try:
    from utils.forecast_model import ForecastModel
    model = ForecastModel()
    
    recommendations = model.get_all_recommendations()
    
    if recommendations:
        print(f"      ✅ Generated {len(recommendations)} recommendations")
        for rec in recommendations:
            print(f"         - {rec['material']}: {rec['recommendation']}")
    else:
        print(f"      ❌ No recommendations generated")
        errors.append("Recommendations failed")
        
except Exception as e:
    print(f"      ❌ Recommendation error: {e}")
    errors.append(f"Recommendation error: {e}")

print()

# 6. Test Backend API
print("[6/8] Testing Backend API...")
try:
    import requests
    
    response = requests.get("http://localhost:5000/api/health", timeout=2)
    
    if response.status_code == 200:
        print(f"      ✅ Backend is running")
        
        # Test key endpoints
        endpoints = [
            '/api/prices/current',
            '/api/recommendations',
            '/api/inventory'
        ]
        
        for endpoint in endpoints:
            try:
                r = requests.get(f"http://localhost:5000{endpoint}", timeout=5)
                if r.status_code == 200:
                    print(f"      ✅ {endpoint}")
                else:
                    print(f"      ❌ {endpoint} - Status {r.status_code}")
                    warnings.append(f"Endpoint {endpoint} returned {r.status_code}")
            except:
                print(f"      ❌ {endpoint} - Failed")
                warnings.append(f"Endpoint {endpoint} failed")
    else:
        print(f"      ❌ Backend returned status {response.status_code}")
        errors.append("Backend not responding properly")
        
except requests.exceptions.ConnectionError:
    print(f"      ❌ Backend is NOT running")
    errors.append("Backend not running - Start with: python app.py")
except Exception as e:
    print(f"      ❌ Backend error: {e}")
    errors.append(f"Backend error: {e}")

print()

# 7. Test Dashboard
print("[7/8] Testing Dashboard...")
try:
    import streamlit
    print(f"      ✅ Streamlit installed")
    
    if os.path.exists('dashboard.py'):
        print(f"      ✅ dashboard.py exists")
    else:
        print(f"      ❌ dashboard.py missing")
        errors.append("Dashboard file missing")
        
except ImportError:
    print(f"      ❌ Streamlit not installed")
    errors.append("Streamlit not installed")

print()

# 8. Test PO System
print("[8/8] Testing PO System...")
try:
    from utils.po_generator import PurchaseOrderGenerator
    po_gen = PurchaseOrderGenerator()
    
    pos = po_gen.list_pos(limit=5)
    print(f"      ✅ PO system working: {len(pos)} PO(s) found")
    
except Exception as e:
    print(f"      ⚠️  PO system: {e}")
    warnings.append(f"PO system: {e}")

print()
print("="*70)
print("  DIAGNOSTIC SUMMARY")
print("="*70)
print()

if not errors and not warnings:
    print("✅ ALL SYSTEMS OPERATIONAL!")
    print()
    print("Your system is working correctly.")
    print()
    print("If you're still having issues:")
    print("  1. Restart backend: python app.py")
    print("  2. Restart dashboard: streamlit run dashboard.py")
    print("  3. Refresh browser (F5)")
    
elif errors:
    print(f"❌ CRITICAL ISSUES FOUND: {len(errors)}")
    print()
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    print()
    print("FIXES NEEDED:")
    print()
    
    if any('Missing package' in e for e in errors):
        print("  Install missing packages:")
        print("    pip install pandas numpy flask streamlit plotly prophet requests")
        print()
    
    if any('Missing' in e and 'data' in e for e in errors):
        print("  Regenerate data files:")
        print("    python regenerate_data_usd.py")
        print()
    
    if any('Backend not running' in e for e in errors):
        print("  Start backend:")
        print("    python app.py")
        print()
        
elif warnings:
    print(f"⚠️  WARNINGS: {len(warnings)}")
    print()
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")
    print()
    print("System mostly working but some features may not function properly.")

print()
print("="*70)
print()
