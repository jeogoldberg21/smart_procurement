"""
System test script to verify all components are working
"""
import os
import sys
import requests
import time

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_data_files():
    """Test if data files exist"""
    print_header("Testing Data Files")
    
    files = [
        'data/material_prices.csv',
        'data/inventory.json',
        'data/vendors.json'
    ]
    
    all_exist = True
    for file in files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some data files missing. Generating...")
        from utils.data_generator import initialize_data
        initialize_data()
        print("✓ Data files generated")
    
    return all_exist

def test_imports():
    """Test if all required modules can be imported"""
    print_header("Testing Python Imports")
    
    modules = [
        ('flask', 'Flask'),
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
        ('prophet', 'Prophet'),
        ('sklearn', 'Scikit-learn'),
        ('apscheduler', 'APScheduler'),
    ]
    
    all_imported = True
    for module, name in modules:
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_imported = False
    
    return all_imported

def test_models():
    """Test forecast model"""
    print_header("Testing Forecast Model")
    
    try:
        import pandas as pd
        from models.forecast_model import PriceForecastModel
        
        # Load data
        df = pd.read_csv('data/material_prices.csv')
        print(f"✓ Loaded {len(df)} price records")
        
        # Initialize model
        model = PriceForecastModel()
        print("✓ Model initialized")
        
        # Train for one material
        material = 'Copper'
        model.train_model(df, material)
        print(f"✓ Model trained for {material}")
        
        # Generate forecast
        forecast = model.forecast(material, periods=7)
        print(f"✓ Generated 7-day forecast")
        
        # Get recommendation
        recommendation = model.get_recommendation(df, material, forecast)
        print(f"✓ Recommendation: {recommendation['recommendation']}")
        print(f"  Reason: {recommendation['reason']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_flask_api():
    """Test Flask API endpoints"""
    print_header("Testing Flask API")
    
    base_url = "http://localhost:5000/api"
    
    print("⚠️  This test requires Flask backend to be running!")
    print("   Start it with: python app.py")
    print("\nWaiting 3 seconds...")
    time.sleep(3)
    
    endpoints = [
        '/health',
        '/materials',
        '/prices/current',
        '/recommendations',
        '/inventory',
        '/alerts'
    ]
    
    all_working = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {endpoint} - OK")
            else:
                print(f"✗ {endpoint} - Status {response.status_code}")
                all_working = False
        except requests.exceptions.ConnectionError:
            print(f"✗ {endpoint} - Connection failed (is Flask running?)")
            all_working = False
        except Exception as e:
            print(f"✗ {endpoint} - Error: {str(e)}")
            all_working = False
    
    return all_working

def test_configuration():
    """Test configuration"""
    print_header("Testing Configuration")
    
    try:
        import config
        
        print(f"✓ Flask Port: {config.FLASK_PORT}")
        print(f"✓ Streamlit Port: {config.STREAMLIT_PORT}")
        print(f"✓ Materials: {', '.join(config.MATERIALS)}")
        print(f"✓ Forecast Days: {config.FORECAST_DAYS}")
        print(f"✓ Price Update Interval: {config.PRICE_UPDATE_INTERVAL}s")
        print(f"✓ Forecast Update Interval: {config.FORECAST_UPDATE_INTERVAL}s")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Smart Procurement System - Test Suite                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Run tests
    results['Configuration'] = test_configuration()
    results['Data Files'] = test_data_files()
    results['Python Imports'] = test_imports()
    results['Forecast Model'] = test_models()
    results['Flask API'] = test_flask_api()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nTo start the system:")
        print("  1. Run: python app.py")
        print("  2. Run: streamlit run dashboard.py")
        print("  Or: python start.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        
        if not results['Python Imports']:
            print("\n💡 Install dependencies with: pip install -r requirements.txt")
        
        if not results['Flask API']:
            print("\n💡 Flask API test failed because backend is not running.")
            print("   This is normal if you haven't started it yet.")

if __name__ == "__main__":
    run_all_tests()
