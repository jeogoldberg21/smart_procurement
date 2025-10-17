"""
Create a sample Purchase Order for testing
"""
import os
import sys

print("="*60)
print("  CREATING SAMPLE PURCHASE ORDER")
print("="*60)
print()

# Check if backend is running
print("[1/3] Checking backend...")
import requests

try:
    response = requests.get("http://localhost:5000/api/health", timeout=2)
    if response.status_code == 200:
        print("      ✅ Backend is running")
    else:
        print("      ❌ Backend not responding properly")
        print("      Please start backend: python app.py")
        sys.exit(1)
except:
    print("      ❌ Backend is not running")
    print("      Please start backend: python app.py")
    sys.exit(1)

print()

# Generate a sample PO
print("[2/3] Generating sample PO...")

try:
    response = requests.post(
        "http://localhost:5000/api/po/generate",
        json={
            'material': 'Copper',
            'quantity': 100,
            'requester': 'Test User'
        },
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        po = result.get('po', {})
        print(f"      ✅ PO Generated: {po.get('po_number')}")
        print(f"      Material: {po.get('material', {}).get('name')}")
        print(f"      Quantity: {po.get('material', {}).get('quantity')} tons")
        print(f"      Total: ${po.get('financial', {}).get('total_amount', 0):,.2f}")
    else:
        print(f"      ❌ Failed: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"      ❌ Error: {e}")
    sys.exit(1)

print()

# Verify PO exists
print("[3/3] Verifying PO...")

try:
    response = requests.get(
        "http://localhost:5000/api/po/list?limit=10",
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        pos = result.get('purchase_orders', [])
        print(f"      ✅ Found {len(pos)} purchase order(s)")
        
        if pos:
            print()
            print("      Purchase Orders:")
            for po in pos:
                print(f"        - {po['po_number']}: {po['material']['name']} ({po['status']})")
    else:
        print(f"      ❌ Failed to list POs: {response.text}")
        
except Exception as e:
    print(f"      ❌ Error: {e}")

print()
print("="*60)
print("  SAMPLE PO CREATED!")
print("="*60)
print()
print("✅ Now refresh your dashboard (F5)")
print("✅ Go to Purchase Orders → View POs tab")
print("✅ You should see the sample PO")
print()
