"""
Test PDF Export Functionality
"""
import os
import sys

print("="*60)
print("  Testing PDF Export")
print("="*60)
print()

# Test 1: Check if reportlab is installed
print("[1/4] Checking ReportLab installation...")
try:
    import reportlab
    print("      ✅ ReportLab is installed")
    reportlab_available = True
except ImportError:
    print("      ❌ ReportLab is NOT installed")
    print("      💡 Run: pip install reportlab==4.0.7")
    reportlab_available = False

print()

# Test 2: Check PDF directory
print("[2/4] Checking PDF directory...")
pdf_dir = "data/purchase_orders/pdf"
if os.path.exists(pdf_dir):
    print(f"      ✅ Directory exists: {pdf_dir}")
    files = os.listdir(pdf_dir)
    print(f"      📁 Files in directory: {len(files)}")
    if files:
        for f in files[:5]:  # Show first 5 files
            print(f"         - {f}")
else:
    print(f"      ❌ Directory does not exist: {pdf_dir}")
    print("      Creating directory...")
    os.makedirs(pdf_dir, exist_ok=True)
    print("      ✅ Directory created")

print()

# Test 3: Test simple exporter
print("[3/4] Testing Simple PDF Exporter...")
try:
    from utils.simple_pdf_exporter import get_simple_pdf_exporter
    
    sample_po = {
        'po_number': 'PO-202510-TEST',
        'status': 'DRAFT',
        'created_date': '2025-10-16 14:30:00',
        'created_by': 'Test User',
        'material': {
            'name': 'Copper',
            'quantity': 100,
            'unit': 'tons',
            'unit_price': 8450.00,
            'current_market_price': 8500.00
        },
        'vendor': {
            'name': 'Test Vendor Inc.',
            'rating': 4.5,
            'payment_terms': 'Net 30',
            'reliability': 'High'
        },
        'delivery': {
            'expected_date': '2025-10-23',
            'delivery_days': 7,
            'delivery_address': 'Warehouse A',
            'contact_person': 'Test Person'
        },
        'financial': {
            'subtotal': 845000.00,
            'tax_rate': 0.18,
            'tax_amount': 152100.00,
            'total_amount': 997100.00,
            'potential_savings': 5000.00
        },
        'ai_recommendation': {
            'recommendation': 'BUY NOW',
            'reason': 'Price expected to rise',
            'confidence': 'High',
            'forecast_change': '+2.5%'
        },
        'inventory_context': {
            'current_stock': 150,
            'min_threshold': 100,
            'daily_consumption': 15,
            'days_remaining': 10.0
        },
        'terms': [
            'Payment terms as per vendor agreement',
            'Quality inspection upon delivery',
            'Penalties for late delivery as per contract'
        ],
        'approvals': {
            'requester': {'name': 'Test User', 'status': 'APPROVED', 'date': '2025-10-16'},
            'manager': {'name': 'Pending', 'status': 'PENDING', 'date': None},
            'finance': {'name': 'Pending', 'status': 'PENDING', 'date': None}
        }
    }
    
    exporter = get_simple_pdf_exporter()
    filepath = exporter.export_po_to_pdf(sample_po)
    
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        print(f"      ✅ Export successful!")
        print(f"      📄 File: {filepath}")
        print(f"      📊 Size: {file_size:,} bytes")
    else:
        print(f"      ❌ File not created: {filepath}")
        
except Exception as e:
    print(f"      ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 4: Check via API
print("[4/4] Testing API endpoint...")
try:
    import requests
    
    # Check if backend is running
    response = requests.get("http://localhost:5000/api/health", timeout=2)
    
    if response.status_code == 200:
        print("      ✅ Backend is running")
        
        # Try to list POs
        po_response = requests.get("http://localhost:5000/api/po/list?limit=5", timeout=5)
        
        if po_response.status_code == 200:
            pos = po_response.json().get('purchase_orders', [])
            print(f"      📋 Found {len(pos)} purchase orders")
            
            if pos:
                # Try to export first PO
                po_number = pos[0]['po_number']
                print(f"      🔄 Testing PDF export for {po_number}...")
                
                pdf_response = requests.get(
                    f"http://localhost:5000/api/po/{po_number}/pdf",
                    timeout=10
                )
                
                if pdf_response.status_code == 200:
                    result = pdf_response.json()
                    print(f"      ✅ PDF export API works!")
                    print(f"      📄 Path: {result.get('pdf_path')}")
                else:
                    print(f"      ❌ PDF export failed: {pdf_response.text}")
            else:
                print("      ℹ️  No POs to test with")
        else:
            print(f"      ❌ Failed to list POs: {po_response.status_code}")
    else:
        print("      ❌ Backend not responding")
        
except requests.exceptions.ConnectionError:
    print("      ❌ Backend is not running")
    print("      💡 Start backend: python app.py")
except Exception as e:
    print(f"      ❌ Error: {e}")

print()
print("="*60)
print("  Test Complete")
print("="*60)
print()

# Summary
print("📊 SUMMARY:")
print()
if reportlab_available:
    print("✅ ReportLab: Installed")
    print("✅ PDF Export: Should work with full formatting")
else:
    print("❌ ReportLab: Not installed")
    print("⚠️  PDF Export: Will create text files (.txt) instead")
    print("💡 To fix: Run install_reportlab.bat or pip install reportlab")

print()
print("📁 Check your PDFs in:")
print(f"   {os.path.abspath('data/purchase_orders/pdf')}")
print()
