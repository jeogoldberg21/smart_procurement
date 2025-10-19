"""
Unique Selling Point (USP) Analyzer
Calculates the "Procurement Opportunity Score"
"""
import numpy as np

class USPAnalyzer:
    def __init__(self):
        # Weights for the score components
        self.weights = {
            'price_opportunity': 0.4,
            'inventory_need': 0.3,
            'vendor_quality': 0.2,
            'market_stability': 0.1
        }

    def calculate_opportunity_score(self, material, price_data, inventory_data, vendor_data, supply_chain_insights):
        """
        Calculates the Procurement Opportunity Score for a given material.
        """
        scores = {}

        # 1. Price Opportunity Score
        price_rec = price_data.get('recommendation', {})
        if price_rec.get('recommendation') == 'BUY NOW':
            scores['price_opportunity'] = 100
        elif price_rec.get('recommendation') == 'MONITOR':
            scores['price_opportunity'] = 50
        else: # WAIT
            scores['price_opportunity'] = 10

        # 2. Inventory Need Score
        inv_item = inventory_data.get(material, {})
        if inv_item:
            current_stock = inv_item.get('current_stock', 0)
            min_threshold = inv_item.get('min_threshold', 1)
            if current_stock < min_threshold:
                scores['inventory_need'] = 100
            elif current_stock < min_threshold * 1.2:
                scores['inventory_need'] = 70
            else:
                scores['inventory_need'] = 20
        else:
            scores['inventory_need'] = 50 # Neutral if no inventory data

        # 3. Vendor Quality Score
        if vendor_data:
            best_vendor = vendor_data[0] # Assuming sorted by quality/price
            rating = best_vendor.get('rating', 3.0)
            scores['vendor_quality'] = (rating / 5.0) * 100
        else:
            scores['vendor_quality'] = 50 # Neutral

        # 4. Market Stability Score
        health_score = supply_chain_insights.get('supply_chain_health_score', 50)
        scores['market_stability'] = health_score

        # Calculate final weighted score
        final_score = 0
        for component, weight in self.weights.items():
            final_score += scores.get(component, 50) * weight

        return {
            'opportunity_score': round(final_score, 2),
            'breakdown': scores,
            'recommendation': self._get_recommendation(final_score)
        }

    def _get_recommendation(self, score):
        if score >= 80:
            return "Excellent opportunity. Conditions are highly favorable for procurement."
        elif score >= 60:
            return "Good opportunity. Consider procuring now to take advantage of the current conditions."
        elif score >= 40:
            return "Fair opportunity. You may want to wait for more favorable conditions."
        else:
            return "Not recommended. It is advised to wait for a better opportunity."

_usp_analyzer = None

def get_usp_analyzer():
    global _usp_analyzer
    if _usp_analyzer is None:
        _usp_analyzer = USPAnalyzer()
    return _usp_analyzer
