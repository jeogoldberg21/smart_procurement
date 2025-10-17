"""
Fix Corrupted Purchase Order Files
Deletes corrupted PO files and provides instructions to regenerate
"""
import os
import json
import shutil

print("="*60)
print("  FIXING CORRUPTED PO FILES")
print("="*60)
print()

po_dir = "data/purchase_orders"
backup_dir = "data/purchase_orders_backup"

# Step 1: Create backup
print("[1/3] Creating backup...")
if os.path.exists(po_dir):
    if not os.path.exists(backup_dir):
        shutil.copytree(po_dir, backup_dir)
        print(f"      ✅ Backup created: {backup_dir}")
    else:
        print(f"      ⚠️  Backup already exists: {backup_dir}")
else:
    print(f"      ❌ PO directory not found")
    exit(1)

print()

# Step 2: Check and remove corrupted files
print("[2/3] Checking PO files...")
files = [f for f in os.listdir(po_dir) if f.endswith('.json') and f != 'po_counter.json']

corrupted = []
valid = []

for filename in files:
    filepath = os.path.join(po_dir, filename)
    try:
        with open(filepath, 'r') as f:
            po = json.load(f)
        valid.append(filename)
    except:
        corrupted.append(filename)

print(f"      ✅ Valid files: {len(valid)}")
print(f"      ❌ Corrupted files: {len(corrupted)}")

if corrupted:
    print()
    print("      Corrupted files:")
    for f in corrupted:
        print(f"         - {f}")

print()

# Step 3: Delete corrupted files
if corrupted:
    print("[3/3] Removing corrupted files...")
    
    for filename in corrupted:
        filepath = os.path.join(po_dir, filename)
        os.remove(filepath)
        print(f"      ✅ Deleted: {filename}")
    
    print()
    print(f"      ✅ Removed {len(corrupted)} corrupted file(s)")
else:
    print("[3/3] No corrupted files to remove")

print()
print("="*60)
print("  FIX COMPLETE")
print("="*60)
print()

if corrupted:
    print(f"✅ Removed {len(corrupted)} corrupted PO file(s)")
    print(f"✅ Backup saved to: {backup_dir}")
    print()
    print("Next steps:")
    print("  1. Restart backend: python app.py")
    print("  2. Refresh dashboard (F5)")
    print()
    if valid:
        print(f"  {len(valid)} valid PO(s) remain and will display")
    else:
        print("  No valid POs remain")
        print("  Generate new POs via dashboard or run:")
        print("  python create_sample_po.py")
else:
    print("✅ All PO files are valid")
    print()
    print("If dashboard still shows error:")
    print("  1. Restart backend: python app.py")
    print("  2. Hard refresh browser: Ctrl+Shift+R")

print()
