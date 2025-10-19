"""
Purchase Order Generator
Auto-generates PO based on recommendations with PDF export
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


class PurchaseOrderGenerator:
    """
    Generates purchase orders based on AI recommendations
    """
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.po_dir = os.path.join(data_dir, 'purchase_orders')
        os.makedirs(self.po_dir, exist_ok=True)
        
        # Load PO counter
        self.counter_file = os.path.join(self.po_dir, 'po_counter.json')
        self.po_counter = self._load_counter()
    
    def _load_counter(self) -> int:
        """Load PO counter from file"""
        if os.path.exists(self.counter_file):
            with open(self.counter_file, 'r') as f:
                data = json.load(f)
                return data.get('counter', 1000)
        return 1000
    
    def _save_counter(self):
        """Save PO counter to file"""
        with open(self.counter_file, 'w') as f:
            json.dump({'counter': self.po_counter}, f)
    
    def _convert_value(self, value):
        """Convert numpy types to native Python types"""
        if isinstance(value, (np.integer, np.int64, np.int32)):
            return int(value)
        elif isinstance(value, (np.floating, np.float64, np.float32)):
            return float(value)
        elif isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, dict):
            return {k: self._convert_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value
    
    def _get_next_po_number(self) -> str:
        """Generate next PO number"""
        self.po_counter += 1
        self._save_counter()
        return f"PO-{datetime.now().strftime('%Y%m')}-{self.po_counter:04d}"
    
    def generate_po(self, 
                   material: str,
                   recommendation: Dict,
                   vendor: Dict,
                   quantity: float,
                   inventory_data: Dict,
                   requester: str = "Procurement Manager") -> Dict:
        """
        Generate a purchase order
        
        Args:
            material: Material name
            recommendation: AI recommendation data
            vendor: Vendor information
            quantity: Order quantity in tons
            inventory_data: Current inventory data
            requester: Person requesting the order
        
        Returns:
            Purchase order dictionary
        """
        # Convert all inputs to native Python types
        vendor = self._convert_value(vendor)
        inventory_data = self._convert_value(inventory_data)
        recommendation = self._convert_value(recommendation)
        quantity = float(quantity)
        
        po_number = self._get_next_po_number()
        current_date = datetime.now()
        
        # Calculate delivery date
        delivery_days = int(vendor.get('delivery_days', 7))
        expected_delivery = current_date + timedelta(days=delivery_days)
        
        # Calculate costs
        unit_price = float(vendor['price'])
        subtotal = quantity * unit_price
        tax_rate = 0.18  # 18% GST
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        # Calculate savings
        current_price = recommendation.get('current_price', unit_price)
        potential_savings = (current_price - unit_price) * quantity
        
        # Create PO
        po = {
            'po_number': po_number,
            'status': 'DRAFT',
            'created_date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': requester,
            
            # Material Information
            'material': {
                'name': material,
                'quantity': quantity,
                'unit': 'tons',
                'unit_price': round(unit_price, 2),
                'current_market_price': round(current_price, 2)
            },
            
            # Vendor Information
            'vendor': {
                'name': vendor['name'],
                'rating': vendor.get('rating', 'N/A'),
                'payment_terms': vendor.get('payment_terms', 'Net 30'),
                'min_order': vendor.get('min_order', 0),
                'reliability': vendor.get('reliability', 'Medium')
            },
            
            # Delivery Information
            'delivery': {
                'expected_date': expected_delivery.strftime('%Y-%m-%d'),
                'delivery_days': delivery_days,
                'delivery_address': inventory_data.get('location', 'Warehouse A'),
                'contact_person': requester,
                'contact_phone': '+91-XXXXXXXXXX'
            },
            
            # Financial Information
            'financial': {
                'subtotal': round(subtotal, 2),
                'tax_rate': tax_rate,
                'tax_amount': round(tax_amount, 2),
                'total_amount': round(total_amount, 2),
                'currency': 'USD',
                'potential_savings': round(potential_savings, 2)
            },
            
            # AI Recommendation Context
            'ai_recommendation': {
                'recommendation': recommendation.get('recommendation', 'N/A'),
                'reason': recommendation.get('reason', 'N/A'),
                'confidence': recommendation.get('confidence', 'N/A'),
                'forecast_change': f"{recommendation.get('price_change_pct', 0):.2f}%",
                'best_day_to_buy': recommendation.get('best_day_to_buy', 'N/A')
            },
            
            # Inventory Context
            'inventory_context': {
                'current_stock': inventory_data.get('current_stock', 0),
                'min_threshold': inventory_data.get('min_threshold', 0),
                'daily_consumption': inventory_data.get('daily_consumption', 0),
                'days_remaining': round(inventory_data.get('current_stock', 0) / 
                                      max(inventory_data.get('daily_consumption', 1), 1), 1)
            },
            
            # Terms and Conditions
            'terms': [
                "Payment terms as per vendor agreement",
                "Quality inspection upon delivery",
                "Penalties for late delivery as per contract",
                "Material specifications as per industry standards",
                "Insurance coverage during transit"
            ],
            
            # Approval Workflow
            'approvals': {
                'requester': {'name': requester, 'status': 'APPROVED', 'date': current_date.strftime('%Y-%m-%d')},
                'manager': {'name': 'Pending', 'status': 'PENDING', 'date': None},
                'finance': {'name': 'Pending', 'status': 'PENDING', 'date': None}
            }
        }
        
        # Save PO to file
        self._save_po(po)
        
        return po
    
    def _save_po(self, po: Dict):
        """Save PO to JSON file"""
        filename = f"{po['po_number']}.json"
        filepath = os.path.join(self.po_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(po, f, indent=2, cls=NumpyEncoder)
    
    def get_po(self, po_number: str) -> Optional[Dict]:
        """Retrieve a PO by number"""
        filename = f"{po_number}.json"
        filepath = os.path.join(self.po_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def list_pos(self, status: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """List all POs, optionally filtered by status"""
        pos = []
        
        if not os.path.exists(self.po_dir):
            return pos
        
        for filename in sorted(os.listdir(self.po_dir), reverse=True):
            if filename.endswith('.json') and filename != 'po_counter.json':
                filepath = os.path.join(self.po_dir, filename)
                with open(filepath, 'r') as f:
                    po = json.load(f)
                    
                    if status is None or po.get('status') == status:
                        pos.append(po)
                        
                    if len(pos) >= limit:
                        break
        
        return pos
    
    def update_po_status(self, po_number: str, new_status: str, updated_by: str = "System") -> bool:
        """Update PO status"""
        po = self.get_po(po_number)
        
        if po:
            po['status'] = new_status
            po['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            po['last_updated_by'] = updated_by
            
            self._save_po(po)
            return True
        
        return False
    
    def generate_po_text(self, po: Dict) -> str:
        """Generate text representation of PO"""
        text = f"""
{'='*80}
                          PURCHASE ORDER
{'='*80}

PO Number: {po['po_number']}
Date: {po['created_date']}
Status: {po['status']}

{'='*80}
VENDOR INFORMATION
{'='*80}
Vendor Name:        {po['vendor']['name']}
Rating:             {po['vendor']['rating']}/5.0
Payment Terms:      {po['vendor']['payment_terms']}
Reliability:        {po['vendor']['reliability']}

{'='*80}
MATERIAL DETAILS
{'='*80}
Material:           {po['material']['name']}
Quantity:           {po['material']['quantity']} {po['material']['unit']}
Unit Price:         ${po['material']['unit_price']:.2f}/{po['material']['unit']}
Market Price:       ${po['material']['current_market_price']:.2f}/{po['material']['unit']}

{'='*80}
DELIVERY INFORMATION
{'='*80}
Expected Delivery:  {po['delivery']['expected_date']}
Delivery Time:      {po['delivery']['delivery_days']} days
Delivery Address:   {po['delivery']['delivery_address']}
Contact Person:     {po['delivery']['contact_person']}

{'='*80}
FINANCIAL SUMMARY
{'='*80}
Subtotal:           ${po['financial']['subtotal']:,.2f}
Tax ({po['financial']['tax_rate']*100:.0f}%):            ${po['financial']['tax_amount']:,.2f}
Total Amount:       ${po['financial']['total_amount']:,.2f}
Potential Savings:  ${po['financial']['potential_savings']:,.2f}

{'='*80}
AI RECOMMENDATION CONTEXT
{'='*80}
Recommendation:     {po['ai_recommendation']['recommendation']}
Reason:             {po['ai_recommendation']['reason']}
Confidence:         {po['ai_recommendation']['confidence']}
Forecast Change:    {po['ai_recommendation']['forecast_change']}

{'='*80}
INVENTORY CONTEXT
{'='*80}
Current Stock:      {po['inventory_context']['current_stock']} tons
Min Threshold:      {po['inventory_context']['min_threshold']} tons
Daily Consumption:  {po['inventory_context']['daily_consumption']} tons
Days Remaining:     {po['inventory_context']['days_remaining']} days

{'='*80}
TERMS AND CONDITIONS
{'='*80}
"""
        for i, term in enumerate(po['terms'], 1):
            text += f"{i}. {term}\n"
        
        text += f"""
{'='*80}
APPROVAL STATUS
{'='*80}
Requester:  {po['approvals']['requester']['name']} - {po['approvals']['requester']['status']}
Manager:    {po['approvals']['manager']['name']} - {po['approvals']['manager']['status']}
Finance:    {po['approvals']['finance']['name']} - {po['approvals']['finance']['status']}

{'='*80}
"""
        return text


# Global instance
_po_generator = None

def get_po_generator():
    """Get or create global PO generator instance"""
    global _po_generator
    if _po_generator is None:
        _po_generator = PurchaseOrderGenerator()
    return _po_generator


if __name__ == '__main__':
    # Test the PO generator
    generator = PurchaseOrderGenerator()
    
    # Sample data
    material = "Copper"
    recommendation = {
        'recommendation': 'BUY NOW',
        'reason': 'Price expected to rise by 2.5%',
        'confidence': 'High',
        'current_price': 8500,
        'price_change_pct': 2.5,
        'best_day_to_buy': 1
    }
    vendor = {
        'name': 'Global Metals Inc.',
        'price': 8450,
        'rating': 4.5,
        'delivery_days': 7,
        'payment_terms': 'Net 30',
        'reliability': 'High'
    }
    inventory = {
        'current_stock': 150,
        'min_threshold': 100,
        'daily_consumption': 15,
        'location': 'Warehouse A'
    }
    
    # Generate PO
    po = generator.generate_po(material, recommendation, vendor, 100, inventory)
    
    print("✓ Purchase Order Generated!")
    print(f"PO Number: {po['po_number']}")
    print(f"Total Amount: ${po['financial']['total_amount']:,.2f}")
    print(f"\nPO saved to: data/purchase_orders/{po['po_number']}.json")
    
    # Print PO
    print("\n" + generator.generate_po_text(po))
