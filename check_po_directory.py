"""
Check and fix Purchase Order directory structure
"""
import os
import json

print("="*60)
print("  CHECKING PO DIRECTORY STRUCTURE")
print("="*60)
print()

# Check directories
print("[1/2] Checking directories...")

po_dir = "data/purchase_orders"
pdf_dir = "data/purchase_orders/pdf"

if not os.path.exists(po_dir):
    print(f"      ❌ Missing: {po_dir}")
    print(f"      Creating directory...")
    os.makedirs(po_dir, exist_ok=True)
    print(f"      ✅ Created: {po_dir}")
else:
    print(f"      ✅ Exists: {po_dir}")

if not os.path.exists(pdf_dir):
    print(f"      ❌ Missing: {pdf_dir}")
    print(f"      Creating directory...")
    os.makedirs(pdf_dir, exist_ok=True)
    print(f"      ✅ Created: {pdf_dir}")
else:
    print(f"      ✅ Exists: {pdf_dir}")

print()

# Check for PO files
print("[2/2] Checking for PO files...")

po_files = [f for f in os.listdir(po_dir) if f.endswith('.json') and f.startswith('PO-')]

if po_files:
    print(f"      ✅ Found {len(po_files)} PO file(s):")
    for f in po_files[:5]:  # Show first 5
        print(f"         - {f}")
    if len(po_files) > 5:
        print(f"         ... and {len(po_files) - 5} more")
else:
    print(f"      ⚠️  No PO files found")
    print(f"      This is why the dashboard shows 'Failed to fetch'")
    print()
    print(f"      To fix: Run 'python create_sample_po.py'")

print()
print("="*60)
print("  DIRECTORY CHECK COMPLETE")
print("="*60)
print()

if not po_files:
    print("⚠️  No purchase orders exist yet")
    print()
    print("To create a sample PO:")
    print("  1. Make sure backend is running (python app.py)")
    print("  2. Run: python create_sample_po.py")
    print("  3. Refresh dashboard (F5)")
    print()
else:
    print("✅ PO files exist")
    print("✅ If dashboard still shows error, restart backend")
    print()
