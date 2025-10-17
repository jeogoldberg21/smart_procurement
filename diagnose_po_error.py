"""
Diagnose Purchase Order Loading Issues
"""
import os
import json

print("="*60)
print("  DIAGNOSING PO LOADING ISSUES")
print("="*60)
print()

# Step 1: Check directory
print("[1/4] Checking directory...")
po_dir = "data/purchase_orders"

if not os.path.exists(po_dir):
    print(f"      ❌ Directory not found: {po_dir}")
    exit(1)
else:
    print(f"      ✅ Directory exists: {po_dir}")

print()

# Step 2: List files
print("[2/4] Listing PO files...")
files = [f for f in os.listdir(po_dir) if f.endswith('.json') and f != 'po_counter.json']

if not files:
    print(f"      ❌ No PO files found")
    exit(1)
else:
    print(f"      ✅ Found {len(files)} PO file(s)")
    for f in files[:5]:
        print(f"         - {f}")
    if len(files) > 5:
        print(f"         ... and {len(files) - 5} more")

print()

# Step 3: Try loading files
print("[3/4] Testing file loading...")
errors = []
success = 0

for filename in files[:10]:  # Test first 10
    filepath = os.path.join(po_dir, filename)
    try:
        with open(filepath, 'r') as f:
            po = json.load(f)
            
        # Check required fields
        required = ['po_number', 'status', 'material', 'vendor', 'financial']
        missing = [field for field in required if field not in po]
        
        if missing:
            errors.append(f"{filename}: Missing fields: {missing}")
        else:
            success += 1
            
    except json.JSONDecodeError as e:
        errors.append(f"{filename}: JSON decode error - {e}")
    except Exception as e:
        errors.append(f"{filename}: Error - {e}")

print(f"      ✅ Successfully loaded: {success}/{len(files[:10])}")

if errors:
    print(f"      ❌ Errors found: {len(errors)}")
    print()
    print("      Error details:")
    for err in errors[:5]:
        print(f"         - {err}")
else:
    print(f"      ✅ All files valid")

print()

# Step 4: Test API
print("[4/4] Testing backend API...")
import requests

try:
    response = requests.get("http://localhost:5000/api/po/list?limit=5", timeout=5)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get('success'):
            pos = result.get('purchase_orders', [])
            print(f"      ✅ API working: {len(pos)} PO(s) returned")
            
            if pos:
                print()
                print("      Sample PO:")
                po = pos[0]
                print(f"         PO Number: {po.get('po_number')}")
                print(f"         Material: {po.get('material', {}).get('name')}")
                print(f"         Status: {po.get('status')}")
        else:
            print(f"      ❌ API returned error: {result.get('error')}")
    else:
        print(f"      ❌ API returned status {response.status_code}")
        print(f"      Response: {response.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print(f"      ❌ Backend not running")
    print(f"      Start with: python app.py")
except Exception as e:
    print(f"      ❌ Error: {e}")

print()
print("="*60)
print("  DIAGNOSIS COMPLETE")
print("="*60)
print()

if errors:
    print("⚠️  ISSUES FOUND:")
    print()
    print("Some PO files have errors:")
    for err in errors[:3]:
        print(f"  - {err}")
    print()
    print("Solution:")
    print("  1. Delete corrupted files")
    print("  2. Or regenerate POs")
    print()
else:
    print("✅ ALL FILES ARE VALID")
    print()
    print("If dashboard still shows error:")
    print("  1. Check backend console for errors")
    print("  2. Restart backend: python app.py")
    print("  3. Hard refresh browser: Ctrl+Shift+R")
    print()
