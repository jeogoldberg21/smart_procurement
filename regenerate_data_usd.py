"""
Regenerate all data files with USD prices
Run this script to reset data to US Dollars
"""
import os

print("="*60)
print("  REGENERATING DATA WITH USD PRICES")
print("="*60)
print()

# Step 1: Delete old data files
print("[1/2] Deleting old data files...")
data_files = [
    'data/material_prices.csv',
    'data/inventory.json',
    'data/vendors.json',
    'data/forecast_cache.json'
]

for file in data_files:
    if os.path.exists(file):
        os.remove(file)
        print(f"      ✓ Deleted {file}")

print()

# Step 2: Regenerate data
print("[2/2] Regenerating data with USD prices...")
from utils.data_generator import initialize_data

initialize_data()
print()

print("="*60)
print("  DATA REGENERATION COMPLETE!")
print("="*60)
print()
print("✅ All data files now use USD (US Dollars)")
print()
print("Next steps:")
print("1. Restart backend: python app.py")
print("2. Restart dashboard: streamlit run dashboard.py")
print("3. Refresh browser (F5)")
print()
