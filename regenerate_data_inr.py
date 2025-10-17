"""
Regenerate all data files with INR prices
Run this script to update all data to Indian Rupees
"""
import os
import sys

print("="*60)
print("  REGENERATING DATA WITH INR PRICES")
print("="*60)
print()

# Step 1: Delete old data files
print("[1/3] Deleting old data files...")
data_files = [
    'data/material_prices.csv',
    'data/inventory.json',
    'data/vendors.json',
    'data/forecast_cache.json'
]

for file in data_files:
    if os.path.exists(file):
        os.remove(file)
        print(f"      [X] Deleted {file}")
    else:
        print(f"      - {file} not found (OK)")

print()

# Step 2: Regenerate data
print("[2/3] Regenerating data with INR prices...")
from utils.data_generator import initialize_data

initialize_data()
print()

# Step 3: Verify
print("[3/3] Verifying new data...")
import pandas as pd
import json

# Check prices
if os.path.exists('data/material_prices.csv'):
    df = pd.read_csv('data/material_prices.csv')
    print(f"      [X] Prices CSV: {len(df)} records")
    
    # Show sample prices
    latest = df[df['date'] == df['date'].max()]
    print()
    print("      Latest Prices (INR):")
    for _, row in latest.iterrows():
        print(f"        {row['material']}: INR {row['price']:,.2f}/ton")
    print()

# Check inventory
if os.path.exists('data/inventory.json'):
    with open('data/inventory.json', 'r') as f:
        inv = json.load(f)
    print(f"      [X] Inventory: {len(inv)} materials")

# Check vendors
if os.path.exists('data/vendors.json'):
    with open('data/vendors.json', 'r') as f:
        vendors = json.load(f)
    print(f"      [X] Vendors: {sum(len(v) for v in vendors.values())} total")
    
    # Show sample vendor prices
    print()
    print("      Sample Vendor Prices (INR):")
    for material, vendor_list in vendors.items():
        if vendor_list:
            v = vendor_list[0]
            print(f"        {material} - {v['name']}: INR {v['price']:,.2f}/ton")

print()
print("="*60)
print("  DATA REGENERATION COMPLETE!")
print("="*60)
print()
print("[X] All data files now use INR (Indian Rupees)")
print()
print("Next steps:")
print("1. Restart backend: python app.py")
print("2. Restart dashboard: streamlit run dashboard.py")
print("3. Refresh browser (F5)")
print()
print("Expected prices:")
print("  Copper:    INR 7,00,000 - INR 7,10,000/ton")
print("  Aluminum:  INR 1,95,000 - INR 2,05,000/ton")
print("  Steel:     INR 65,000 - INR 68,000/ton")
print()
