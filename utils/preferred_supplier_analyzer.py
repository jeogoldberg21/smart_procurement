"""
Module for preferred supplier analytics and comparison
"""
import pandas as pd
from typing import Dict, List, Tuple
import config


class PreferredSupplierAnalyzer:
    """
    Analyzes preferred suppliers vs market averages and provides negotiation insights
    """
    
    def __init__(self, price_data: pd.DataFrame, vendor_data: Dict):
        self.price_data = price_data
        self.vendor_data = vendor_data
        
    def calculate_market_average(self, material: str) -> float:
        """
        Calculate the market average price for a specific material based on all vendors
        """
        if material not in self.vendor_data:
            return 0.0
            
        vendor_prices = [vendor['price'] for vendor in self.vendor_data[material]]
        if not vendor_prices:
            return 0.0
            
        return sum(vendor_prices) / len(vendor_prices)
    
    def get_preferred_supplier_price(self, material: str, preferred_supplier_name: str) -> float:
        """
        Get the price of the preferred supplier for a specific material
        """
        if material not in self.vendor_data:
            return 0.0
            
        for vendor in self.vendor_data[material]:
            if vendor['name'] == preferred_supplier_name:
                return vendor['price']
                
        return 0.0
    
    def compare_prices(self, material: str) -> Dict:
        """
        Compare preferred supplier price with market average
        """
        preferred_supplier_name = config.PREFERRED_SUPPLIERS.get(material)
        if not preferred_supplier_name:
            return {
                'material': material,
                'error': f'No preferred supplier configured for {material}',
                'market_average': 0.0,
                'preferred_price': 0.0,
                'price_difference': 0.0,
                'price_difference_percent': 0.0,
                'negotiation_suggestion': False,
                'suggestion_message': 'No preferred supplier configured'
            }
        
        market_average = self.calculate_market_average(material)
        preferred_price = self.get_preferred_supplier_price(material, preferred_supplier_name)
        
        if market_average == 0.0 or preferred_price == 0.0:
            return {
                'material': material,
                'error': 'Could not fetch vendor prices',
                'market_average': market_average,
                'preferred_price': preferred_price,
                'price_difference': 0.0,
                'price_difference_percent': 0.0,
                'negotiation_suggestion': False,
                'suggestion_message': 'Could not fetch vendor prices'
            }
        
        price_difference = preferred_price - market_average
        price_difference_percent = (price_difference / market_average) * 100
        
        # Determine if we should suggest negotiation
        negotiation_threshold = 5.0  # Negotiate if price is 5% or more above market average
        should_negotiate = price_difference_percent >= negotiation_threshold
        
        if should_negotiate:
            suggested_price = market_average * 0.95  # Suggest 5% below market average
            suggestion_message = f"Negotiate with {preferred_supplier_name} to reduce price from ₹{preferred_price:,.2f} to around ₹{suggested_price:,.2f} (5% below market average)"
        else:
            suggestion_message = f"Current price is competitive. No immediate negotiation needed with {preferred_supplier_name}"
        
        return {
            'material': material,
            'preferred_supplier': preferred_supplier_name,
            'market_average': market_average,
            'preferred_price': preferred_price,
            'price_difference': price_difference,
            'price_difference_percent': price_difference_percent,
            'negotiation_suggestion': should_negotiate,
            'suggestion_message': suggestion_message
        }
    
    def get_all_materials_comparison(self) -> List[Dict]:
        """
        Get comparison for all materials
        """
        results = []
        for material in config.MATERIALS:
            comparison = self.compare_prices(material)
            results.append(comparison)
        return results
    
    def get_negotiation_recommendations(self) -> List[Dict]:
        """
        Get only the materials where negotiation is recommended
        """
        all_comparisons = self.get_all_materials_comparison()
        return [comp for comp in all_comparisons if comp.get('negotiation_suggestion', False)]