"""
Quick test to verify PO generation fix
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

print("🧪 Testing PO Generation Fix...")
print("=" * 60)

try:
    # Test PO generation
    response = requests.post(
        f"{API_BASE}/po/generate",
        json={
            'material': 'Copper',
            'quantity': 100,
            'requester': 'Test User'
        },
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS! PO Generated:")
        print(f"   PO Number: {result['po']['po_number']}")
        print(f"   Material: {result['po']['material']['name']}")
        print(f"   Quantity: {result['po']['material']['quantity']} tons")
        print(f"   Total: ${result['po']['financial']['total_amount']:,.2f}")
        print(f"   Vendor: {result['po']['vendor']['name']}")
        print(f"\n   Message: {result['message']}")
        print("\n" + "=" * 60)
        print("✅ Fix successful! You can now generate POs in the dashboard.")
    else:
        print(f"\n❌ Error: {response.json()}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Make sure the backend is running:")
    print("   python app.py")
