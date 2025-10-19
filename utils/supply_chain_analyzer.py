"""
Supply Chain Intelligence Module
Advanced analytics for vendor risk assessment, alternative materials,
supply disruption alerts, and lead time optimization
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import requests
from typing import Dict, List, Optional, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class SupplyChainAnalyzer:
    """
    Advanced supply chain intelligence features
    """
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.vendor_risk_cache = {}
        self.supply_disruption_cache = {}
        
        # Risk factors weights
        self.risk_weights = {
            'financial_stability': 0.3,
            'delivery_performance': 0.25,
            'quality_score': 0.2,
            'geographic_risk': 0.15,
            'supply_capacity': 0.1
        }
    
    def calculate_vendor_risk_score(self, vendor: Dict, material: str) -> Dict:
        """
        Calculate comprehensive risk score for a vendor
        
        Args:
            vendor: Vendor information with ratings, delivery, etc.
            material: Material name for context
        
        Returns:
            Dictionary with risk score and breakdown
        """
        # Initialize with base vendor data
        risk_data = {
            'vendor_name': vendor['name'],
            'material': material,
            'base_rating': vendor.get('rating', 4.0),
            'delivery_performance': self._calculate_delivery_performance(vendor),
            'financial_stability': self._assess_financial_stability(vendor),
            'geographic_risk': self._assess_geographic_risk(vendor),
            'supply_capacity': self._assess_supply_capacity(vendor, material),
            'quality_score': self._calculate_quality_score(vendor)
        }
        
        # Calculate weighted risk score (0-100, where 100 is highest risk)
        risk_score = 0
        risk_breakdown = {}
        
        for factor, weight in self.risk_weights.items():
            factor_score = risk_data.get(factor, 0)
            risk_score += factor_score * weight
            risk_breakdown[factor] = {
                'score': factor_score,
                'weight': weight,
                'impact': factor_score * weight
            }
        
        risk_level = self._risk_score_to_level(risk_score)
        
        return {
            'vendor_name': risk_data['vendor_name'],
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'risk_breakdown': risk_breakdown,
            'recommendation': self._get_risk_based_recommendation(risk_score, vendor),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_delivery_performance(self, vendor: Dict) -> float:
        """Calculate delivery performance risk factor (0-100)"""
        # Higher delivery days = higher risk
        delivery_days = vendor.get('delivery_days', 7)
        # Normalize: 0 days = 0 risk, 30 days = 100 risk
        performance_risk = min((delivery_days / 30) * 100, 100)
        return performance_risk
    
    def _assess_financial_stability(self, vendor: Dict) -> float:
        """Assess financial stability risk factor (0-100)"""
        # Lower rating might indicate financial issues
        rating = vendor.get('rating', 4.0)
        # Higher rating = lower risk: 5.0 rating = 0 risk, 1.0 rating = 100 risk
        financial_risk = max(0, (5.0 - rating) / 4.0 * 100)
        return financial_risk
    
    def _assess_geographic_risk(self, vendor: Dict) -> float:
        """Assess geographic/policy risk factor (0-100)"""
        import random
        # Simulate geographic risk based on location and current events
        # In production, this would integrate with real geopolitical risk APIs
        base_risk = 20  # Base geographic risk
        # Add some variation based on current global situation
        variation = random.uniform(-10, 20)
        geo_risk = max(0, min(100, base_risk + variation))
        return geo_risk
    
    def _assess_supply_capacity(self, vendor: Dict, material: str) -> float:
        """Assess supply capacity risk factor (0-100)"""
        min_order = vendor.get('min_order', 100)
        # Higher min_order might indicate supply constraints (for smaller buyers)
        # Normalize: 10 tons = 0 risk, 1000 tons = 100 risk
        capacity_risk = min((min_order - 10) / 990 * 100, 100) if min_order > 10 else 0
        return capacity_risk

    def _calculate_quality_score(self, vendor: Dict) -> float:
        """Calculate quality score risk factor (0-100)"""
        # Higher rating = lower risk
        rating = vendor.get('rating', 4.0)
        # Inverse relationship: 5.0 rating = 0 risk, 1.0 rating = 100 risk
        quality_risk = max(0, (5.0 - rating) / 4.0 * 100)
        return quality_risk
    
    def _risk_score_to_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score < 20:
            return "LOW"
        elif risk_score < 50:
            return "MEDIUM"
        elif risk_score < 80:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _get_risk_based_recommendation(self, risk_score: float, vendor: Dict) -> str:
        """Get procurement recommendation based on risk score"""
        if risk_score < 20:
            return f"Procure from {vendor['name']} - Low risk vendor"
        elif risk_score < 50:
            return f"Consider {vendor['name']} - Medium risk, monitor closely"
        elif risk_score < 80:
            return f"Use with caution - High risk vendor ({vendor['name']})"
        else:
            return f"Avoid {vendor['name']} - Critical risk, seek alternatives"
    
    def get_alternative_materials(self, current_material: str, price_threshold: float = 0.15) -> List[Dict]:
        """
        Get alternative materials that could replace current material
        
        Args:
            current_material: Current material name
            price_threshold: Maximum price difference allowed (default 15%)
        
        Returns:
            List of alternative materials with substitution feasibility
        """
        # Define material substitution relationships
        material_alternatives = {
            'Copper': [
                {
                    'substitute': 'Aluminum',
                    'efficiency_ratio': 0.6,  # 60% of copper's efficiency
                    'substitution_feasibility': 0.7,  # 70% feasible for most applications
                    'typical_use_case': 'Electrical applications with modified design'
                },
                {
                    'substitute': 'Copper Alloy',
                    'efficiency_ratio': 0.9,
                    'substitution_feasibility': 0.8,
                    'typical_use_case': 'High-performance applications'
                }
            ],
            'Aluminum': [
                {
                    'substitute': 'Steel',
                    'efficiency_ratio': 0.8,
                    'substitution_feasibility': 0.6,
                    'typical_use_case': 'Structural applications'
                },
                {
                    'substitute': 'Plastic Composite',
                    'efficiency_ratio': 0.4,
                    'substitution_feasibility': 0.5,
                    'typical_use_case': 'Non-critical lightweight applications'
                }
            ],
            'Steel': [
                {
                    'substitute': 'Aluminum',
                    'efficiency_ratio': 0.7,
                    'substitution_feasibility': 0.6,
                    'typical_use_case': 'Weight-sensitive applications'
                },
                {
                    'substitute': 'Stainless Steel',
                    'efficiency_ratio': 1.2,
                    'substitution_feasibility': 0.9,
                    'typical_use_case': 'Corrosion-resistant applications'
                }
            ]
        }
        
        alternatives = material_alternatives.get(current_material, [])
        
        # Get current market prices to calculate cost implications
        try:
            from utils.data_generator import generate_historical_prices
            
            # Generate temporary price data to get current market prices
            # Only include materials that exist in the system's material list
            all_materials = [current_material]
            for alt in alternatives:
                if alt['substitute'] in config.MATERIALS:  # Only include if it's in the system's materials
                    all_materials.append(alt['substitute'])
            
            # Remove duplicates while preserving order
            unique_materials = []
            for mat in all_materials:
                if mat not in unique_materials:
                    unique_materials.append(mat)
            
            # Generate temporary price data (only for materials that exist in the system)
            if len(unique_materials) > 1:  # Only generate if we have other materials besides current
                temp_df = generate_historical_prices(unique_materials)
                
                # Get latest prices for cost analysis
                current_price = temp_df[temp_df['material'] == current_material]['price'].iloc[-1]
                
                # Calculate cost implications and add to results
                for alt in alternatives:
                    try:
                        if alt['substitute'] in config.MATERIALS:
                            alt_price = temp_df[temp_df['material'] == alt['substitute']]['price'].iloc[-1]
                            cost_ratio = alt_price / current_price
                            alt['current_price'] = round(alt_price, 2)
                            alt['cost_ratio'] = round(cost_ratio, 2)
                            alt['cost_implication'] = 'Lower' if cost_ratio < 1.0 else 'Higher' if cost_ratio > 1.0 else 'Same'
                        else:
                            # For materials not in the system, use default values
                            alt['current_price'] = 0
                            alt['cost_ratio'] = 0
                            alt['cost_implication'] = 'Not in system'
                    except:
                        # Fallback if price data unavailable
                        alt['current_price'] = 0
                        alt['cost_ratio'] = 0
                        alt['cost_implication'] = 'Unknown'
            else:
                # If only current material exists in the system, set defaults for alternatives
                for alt in alternatives:
                    alt['current_price'] = 0
                    alt['cost_ratio'] = 0
                    alt['cost_implication'] = 'Not in system'
        
        except Exception as e:
            print(f"Warning: Could not calculate cost implications for alternatives: {e}")
            # Set default values if price calculation fails
            for alt in alternatives:
                alt['current_price'] = 0
                alt['cost_ratio'] = 0
                alt['cost_implication'] = 'Unknown'
        
        # Filter based on price threshold if specified
        if price_threshold is not None:
            alternatives = [
                alt for alt in alternatives 
                if abs(alt.get('cost_ratio', 1) - 1) <= price_threshold
            ]
        
        return alternatives
    
    def check_supply_disruption_risks(self, materials: List[str]) -> List[Dict]:
        """
        Check for potential supply disruptions based on various factors
        
        Args:
            materials: List of materials to check for disruption risks
        
        Returns:
            List of materials with disruption risk assessment
        """
        disruptions = []
        
        for material in materials:
            # Simulate supply disruption risk assessment
            disruption_risk = {
                'material': material,
                'disruption_risk_score': self._calculate_disruption_risk(material),
                'risk_factors': self._get_disruption_factors(material),
                'mitigation_strategies': self._get_mitigation_strategies(material),
                'alternative_sources': self._identify_alternative_sources(material),
                'recommended_actions': self._get_recommended_actions(material),
                'timestamp': datetime.now().isoformat()
            }
            
            disruptions.append(disruption_risk)
        
        return disruptions
    
    def _calculate_disruption_risk(self, material: str) -> int:
        """Calculate disruption risk score (0-100) for a material"""
        import random
        # Simulate various risk factors
        base_risk = random.randint(20, 60)  # Base risk level
        
        # Add material-specific factors
        if material.lower() in ['copper', 'aluminum']:
            # These materials might have higher geopolitical risks
            base_risk += random.randint(5, 15)
        elif material.lower() == 'steel':
            # Steel might have different risk profile
            base_risk += random.randint(0, 10)
        
        return min(base_risk, 100)
    
    def _get_disruption_factors(self, material: str) -> List[str]:
        """Get specific disruption factors for a material"""
        factor_templates = [
            f"Geopolitical tensions affecting {material} supply routes",
            f"Weather conditions impacting {material} production",
            f"Transportation disruptions in key {material} shipping lanes",
            f"Seasonal demand fluctuations for {material}",
            f"Currency fluctuations affecting {material} import costs"
        ]
        
        # Select 2-4 random factors
        import random
        num_factors = random.randint(2, min(4, len(factor_templates)))
        return random.sample(factor_templates, num_factors)
    
    def _get_mitigation_strategies(self, material: str) -> List[str]:
        """Get mitigation strategies for disruption risks"""
        strategies = [
            f"Diversify {material} suppliers across different regions",
            f"Increase safety stock levels for {material}",
            f"Negotiate flexible delivery schedules with {material} vendors",
            f"Explore alternative {material} sources or substitute materials",
            f"Establish strategic partnerships with key {material} suppliers"
        ]
        
        import random
        num_strategies = random.randint(2, min(3, len(strategies)))
        return random.sample(strategies, num_strategies)
    
    def _identify_alternative_sources(self, material: str) -> List[str]:
        """Identify alternative sources for the material"""
        source_options = {
            'Copper': ['Chile', 'Peru', 'China', 'United States', 'Australia'],
            'Aluminum': ['China', 'Russia', 'Canada', 'United States', 'India'],
            'Steel': ['China', 'India', 'Japan', 'United States', 'Russia']
        }
        
        sources = source_options.get(material, [f'{material} sources'])
        import random
        num_sources = random.randint(2, min(3, len(sources)))
        return random.sample(sources, num_sources)
    
    def _get_recommended_actions(self, material: str) -> List[str]:
        """Get recommended immediate actions"""
        actions = [
            f"Monitor {material} supply chain closely",
            f"Review {material} inventory levels and reorder points",
            f"Engage with {material} suppliers about potential disruptions",
            f"Research alternative {material} options or sources",
            f"Adjust {material} procurement strategy based on risk"
        ]
        
        import random
        num_actions = random.randint(1, min(2, len(actions)))
        return random.sample(actions, num_actions)
    
    def optimize_lead_times(self, vendors: List[Dict], material: str) -> List[Dict]:
        """
        Optimize lead times by analyzing delivery performance and costs
        
        Args:
            vendors: List of vendor information
            material: Material name for context
        
        Returns:
            List of vendors with optimized lead time recommendations
        """
        optimized_vendors = []
        
        for vendor in vendors:
            # Calculate total time and cost including delivery
            delivery_days = vendor.get('delivery_days', 7)
            unit_price = vendor.get('price', 1000)
            
            # Normalize delivery time to score (shorter = better)
            time_score = max(0, 100 - (delivery_days * 5))  # Each day = 5 points
            
            # Calculate cost efficiency score
            # Lower price = higher efficiency, normalized to 100 point scale
            # Assuming typical price range for normalization
            base_price = {
                'Copper': 8000,
                'Aluminum': 2200,
                'Steel': 750
            }.get(material, 1000)
            
            cost_efficiency = max(0, 100 - ((unit_price - base_price) / base_price * 50))
            
            # Combined score (time 60%, cost 40%)
            combined_score = (time_score * 0.6) + (cost_efficiency * 0.4)
            
            optimized_vendor = {
                'vendor_name': vendor['name'],
                'delivery_days': delivery_days,
                'unit_price': unit_price,
                'time_score': round(time_score, 2),
                'cost_efficiency_score': round(cost_efficiency, 2),
                'combined_score': round(combined_score, 2),
                'recommendation': self._get_lead_time_recommendation(combined_score, vendor),
                'optimal_order_timing': self._calculate_optimal_order_timing(delivery_days)
            }
            
            optimized_vendors.append(optimized_vendor)
        
        # Sort by combined score (best options first)
        optimized_vendors.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return optimized_vendors
    
    def _get_lead_time_recommendation(self, combined_score: float, vendor: Dict) -> str:
        """Get recommendation based on lead time optimization score"""
        if combined_score >= 80:
            return f"Highly recommended - Best time/cost balance for {vendor['name']}"
        elif combined_score >= 60:
            return f"Good option with balanced delivery and cost for {vendor['name']}"
        elif combined_score >= 40:
            return f"Consider {vendor['name']} if faster delivery is more important than cost"
        else:
            return f"{vendor['name']} has high delivery time or cost - consider alternatives"
    
    def _calculate_optimal_order_timing(self, delivery_days: int) -> str:
        """Calculate optimal order timing based on delivery time"""
        if delivery_days <= 5:
            return f"Order 1-2 days before needed (fast delivery: {delivery_days} days)"
        elif delivery_days <= 10:
            return f"Order 3-5 days before needed (medium delivery: {delivery_days} days)"
        else:
            return f"Order 1-2 weeks before needed (slow delivery: {delivery_days} days)"
    
    def get_supply_chain_insights(self, material: str, current_price: float, 
                                 vendor_list: List[Dict]) -> Dict:
        """
        Comprehensive supply chain insights for a material
        
        Args:
            material: Material name
            current_price: Current market price
            vendor_list: List of vendors for this material
        
        Returns:
            Dictionary with comprehensive supply chain insights
        """
        # Calculate risk scores for all vendors
        vendor_risks = [self.calculate_vendor_risk_score(vendor, material) for vendor in vendor_list]
        
        # Get alternative materials
        alternatives = self.get_alternative_materials(material)
        
        # Check disruption risks
        disruption_risks = self.check_supply_disruption_risks([material])
        
        # Optimize lead times
        lead_time_optimization = self.optimize_lead_times(vendor_list, material)
        
        # Calculate overall supply chain health score
        avg_vendor_risk = sum(vr['risk_score'] for vr in vendor_risks) / len(vendor_risks) if vendor_risks else 50
        disruption_score = disruption_risks[0]['disruption_risk_score'] if disruption_risks else 50
        
        # Overall health (lower risk = better health)
        overall_health = 100 - ((avg_vendor_risk + disruption_score) / 2)
        
        return {
            'material': material,
            'current_price': current_price,
            'supply_chain_health_score': round(overall_health, 2),
            'supply_chain_health_level': self._health_score_to_level(overall_health),
            'vendor_risk_analysis': vendor_risks,
            'alternative_materials': alternatives,
            'disruption_risks': disruption_risks,
            'lead_time_optimization': lead_time_optimization,
            'recommendations': {
                'vendor_selection': self._get_vendor_selection_recommendations(vendor_risks),
                'alternative_considerations': len(alternatives) > 0,
                'risk_mitigation': disruption_risks[0]['mitigation_strategies'] if disruption_risks else [],
                'procurement_timing': self._get_procurement_timing_advice(lead_time_optimization)
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _health_score_to_level(self, health_score: float) -> str:
        """Convert health score to health level"""
        if health_score >= 80:
            return "EXCELLENT"
        elif health_score >= 60:
            return "GOOD"
        elif health_score >= 40:
            return "FAIR"
        else:
            return "POOR"
    
    def _get_vendor_selection_recommendations(self, vendor_risks: List[Dict]) -> List[str]:
        """Get recommendations for vendor selection"""
        recommendations = []
        
        # Identify lowest risk vendor
        sorted_vendors = sorted(vendor_risks, key=lambda x: x['risk_score'])
        low_risk_vendor = sorted_vendors[0] if sorted_vendors else None
        
        if low_risk_vendor:
            recommendations.append(
                f"Primary recommendation: {low_risk_vendor['vendor_name']} "
                f"(Risk Score: {low_risk_vendor['risk_score']}, Level: {low_risk_vendor['risk_level']})"
            )
        
        # Identify medium risk alternatives
        medium_risk_vendors = [vr for vr in vendor_risks if 20 <= vr['risk_score'] < 50]
        if medium_risk_vendors:
            vendor_names = [vr['vendor_name'] for vr in medium_risk_vendors[:2]]
            recommendations.append(
                f"Secondary options: {', '.join(vendor_names)} (Medium risk - consider for diversification)"
            )
        
        return recommendations
    
    def _get_procurement_timing_advice(self, lead_time_optimization: List[Dict]) -> str:
        """Get procurement timing advice based on optimization"""
        if not lead_time_optimization:
            return "No lead time optimization data available"
        
        best_vendor = lead_time_optimization[0]
        return (
            f"Best option: {best_vendor['vendor_name']} with combined score of {best_vendor['combined_score']}. "
            f"Recommend ordering {best_vendor['optimal_order_timing']}."
        )


# Global instance
_supply_chain_analyzer = None

def get_supply_chain_analyzer():
    """Get or create global supply chain analyzer instance"""
    global _supply_chain_analyzer
    if _supply_chain_analyzer is None:
        _supply_chain_analyzer = SupplyChainAnalyzer()
    return _supply_chain_analyzer


if __name__ == '__main__':
    # Test the supply chain analyzer
    print("Testing Supply Chain Intelligence Module...")
    
    analyzer = SupplyChainAnalyzer()
    
    # Sample vendor data
    sample_vendors = [
        {
            'name': 'Global Metals Inc.',
            'price': 8450,
            'rating': 4.5,
            'delivery_days': 7,
            'payment_terms': 'Net 30',
            'reliability': 'High',
            'min_order': 100
        },
        {
            'name': 'Prime Suppliers Ltd.',
            'price': 8300,
            'rating': 3.8,
            'delivery_days': 12,
            'payment_terms': 'Net 60',
            'reliability': 'Medium',
            'min_order': 200
        },
        {
            'name': 'Elite Resources Group',
            'price': 8600,
            'rating': 4.8,
            'delivery_days': 5,
            'payment_terms': 'Advance',
            'reliability': 'High',
            'min_order': 50
        }
    ]
    
    material = 'Copper'
    
    print(f"\n1. Vendor Risk Analysis for {material}:")
    for vendor in sample_vendors:
        risk = analyzer.calculate_vendor_risk_score(vendor, material)
        print(f"  {vendor['name']}: Risk Score {risk['risk_score']} ({risk['risk_level']})")
        print(f"    Recommendation: {risk['recommendation']}")
        print()
    
    print(f"2. Alternative Materials for {material}:")
    alternatives = analyzer.get_alternative_materials(material)
    for alt in alternatives:
        print(f"  - {alt['substitute']}: {alt['substitution_feasibility']*100:.0f}% feasible")
        print(f"    Use case: {alt['typical_use_case']}")
        print(f"    Cost: ${alt.get('current_price', 'N/A')} ({alt.get('cost_implication', 'N/A')})")
        print()
    
    print(f"3. Supply Disruption Risks for {material}:")
    disruptions = analyzer.check_supply_disruption_risks([material])
    for disruption in disruptions:
        print(f"  Risk Score: {disruption['disruption_risk_score']}")
        print(f"  Risk Factors: {', '.join(disruption['risk_factors'][:2])}")
        print(f"  Mitigation: {', '.join(disruption['mitigation_strategies'][:2])}")
        print()
    
    print(f"4. Lead Time Optimization for {material}:")
    optimization = analyzer.optimize_lead_times(sample_vendors, material)
    for opt in optimization:
        print(f"  {opt['vendor_name']}: Combined Score {opt['combined_score']}")
        print(f"    Delivery: {opt['delivery_days']} days, Price: ${opt['unit_price']}")
        print(f"    Recommendation: {opt['recommendation']}")
        print()
    
    print(f"5. Comprehensive Supply Chain Insights for {material}:")
    insights = analyzer.get_supply_chain_insights(material, 8500, sample_vendors)
    print(f"  Overall Health: {insights['supply_chain_health_score']} ({insights['supply_chain_health_level']})")
    print(f"  Recommendations: {insights['recommendations']['vendor_selection'][0] if insights['recommendations']['vendor_selection'] else 'None'}")