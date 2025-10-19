"""
Data generator for mock material prices and inventory
"""
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

def generate_historical_prices(materials, days=30):
    """
    Generate mock historical price data for materials with varied trends
    """
    # Use time-based seed for variation
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    
    # Base prices (INR per ton) - Converted from USD at ~83 INR/USD
    base_prices = {
        'Copper': 705500,   # ~8500 USD * 83
        'Aluminum': 199200, # ~2400 USD * 83
        'Steel': 66400      # ~800 USD * 83
    }
    
    # Volatility factors (in INR)
    volatility = {
        'Copper': 12450,    # ~150 USD * 83
        'Aluminum': 6640,   # ~80 USD * 83
        'Steel': 2490       # ~30 USD * 83
    }
    
    # Different trend patterns for each material
    trends = {
        'Copper': 'rising',      # Upward trend - should get BUY NOW
        'Aluminum': 'falling',   # Downward trend - should get WAIT
        'Steel': 'rising'        # Rising trend - should get BUY NOW
    }
    
    data = []
    end_date = datetime.now()
    
    for material in materials:
        base = base_prices[material]
        vol = volatility[material]
        trend_type = trends.get(material, 'stable')
        
        # Generate price trend with specific patterns
        prices = [base]
        for i in range(days - 1):
            change = np.random.normal(0, vol * 0.5)  # Reduced randomness
            
            # Apply trend based on material
            if trend_type == 'rising':
                # Upward trend in recent days (last 40%)
                if i > days * 0.6:
                    trend = vol * 0.15  # Strong upward trend
                else:
                    trend = vol * 0.05  # Slight upward
            elif trend_type == 'falling':
                # Downward trend in recent days
                if i > days * 0.6:
                    trend = -vol * 0.15  # Strong downward trend
                else:
                    trend = -vol * 0.05  # Slight downward
            else:  # stable
                trend = np.random.uniform(-vol * 0.02, vol * 0.02)  # Very small changes
            
            new_price = prices[-1] + change + trend
            # Keep within reasonable bounds
            new_price = max(new_price, base * 0.85)
            new_price = min(new_price, base * 1.15)
            prices.append(new_price)
        
        # Create date range
        dates = [end_date - timedelta(days=days-1-i) for i in range(days)]
        
        for date, price in zip(dates, prices):
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'material': material,
                'price': round(price, 2),
                'volume': np.random.randint(1000, 5000),
                'source': 'Market Data'
            })
    
    return pd.DataFrame(data)

def generate_inventory_data(materials):
    """
    Generate current inventory levels
    """
    np.random.seed(42)
    
    inventory = {}
    for material in materials:
        inventory[material] = {
            'current_stock': round(np.random.uniform(50, 500), 2),
            'unit': 'tons',
            'min_threshold': 100,
            'max_capacity': 1000,
            'daily_consumption': round(np.random.uniform(10, 30), 2),
            'last_updated': datetime.now().isoformat(),
            'location': 'Warehouse A',
            'status': 'Normal'
        }
        
        # Set status based on stock level
        if inventory[material]['current_stock'] < inventory[material]['min_threshold']:
            inventory[material]['status'] = 'Low Stock'
        elif inventory[material]['current_stock'] > inventory[material]['max_capacity'] * 0.8:
            inventory[material]['status'] = 'High Stock'
    
    return inventory

def generate_vendor_data(materials):
    """
    Generate mock vendor comparison data
    """
    np.random.seed(42)
    
    vendor_names = [
        'Global Metals Inc.',
        'Prime Suppliers Ltd.',
        'MetalCorp Trading',
        'Industrial Materials Co.',
        'Elite Resources Group'
    ]
    
    vendors = {}
    for material in materials:
        vendors[material] = []
        
        # Get current market price as baseline
        base_price = {
            'Copper': 705500,
            'Aluminum': 199200,
            'Steel': 66400
        }[material]
        
        for vendor in vendor_names[:3]:  # Top 3 vendors per material
            vendors[material].append({
                'name': vendor,
                'price': round(base_price * np.random.uniform(0.95, 1.08), 2),
                'rating': round(np.random.uniform(3.5, 5.0), 1),
                'delivery_days': int(np.random.randint(3, 15)),
                'min_order': int(np.random.choice([10, 25, 50, 100])),
                'payment_terms': str(np.random.choice(['Net 30', 'Net 60', 'Advance', 'COD'])),
                'reliability': str(np.random.choice(['High', 'Medium', 'High']))
            })
        
        # Sort by price
        vendors[material] = sorted(vendors[material], key=lambda x: x['price'])
    
    return vendors

def initialize_data(data_dir='data'):
    """
    Initialize all mock data files
    """
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    materials = ['Copper', 'Aluminum', 'Steel']
    
    # Generate and save historical prices
    prices_df = generate_historical_prices(materials, days=30)
    prices_df.to_csv(os.path.join(data_dir, 'material_prices.csv'), index=False)
    print(f"[X] Generated material_prices.csv with {len(prices_df)} records")
    
    # Generate and save inventory data
    inventory = generate_inventory_data(materials)
    with open(os.path.join(data_dir, 'inventory.json'), 'w') as f:
        json.dump(inventory, f, indent=2)
    print(f"[X] Generated inventory.json with {len(inventory)} materials")
    
    # Generate and save vendor data
    vendors = generate_vendor_data(materials)
    with open(os.path.join(data_dir, 'vendors.json'), 'w') as f:
        json.dump(vendors, f, indent=2)
    print(f"[X] Generated vendors.json with vendor data")
    
    return prices_df, inventory, vendors

if __name__ == '__main__':
    initialize_data()
