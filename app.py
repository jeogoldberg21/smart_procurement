"""
Flask Backend for Smart Procurement System
"""
import warnings
import logging
import sys
import os

# Suppress Prophet's matplotlib warning by temporarily redirecting stderr
_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
try:
    from models.forecast_model import PriceForecastModel
finally:
    sys.stderr.close()
    sys.stderr = _stderr

from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import threading

from utils.notifications import NotificationManager
from utils.data_generator import initialize_data
from utils.price_scraper import get_scraper, CommodityPriceScraper
from utils.po_generator import get_po_generator
from utils.supply_chain_analyzer import get_supply_chain_analyzer
from utils.usp_analyzer import get_usp_analyzer
from utils.preferred_supplier_analyzer import PreferredSupplierAnalyzer

# Try to import PDF exporter, fallback to simple version
try:
    from utils.pdf_exporter import get_pdf_exporter
except ImportError:
    from utils.simple_pdf_exporter import get_simple_pdf_exporter as get_pdf_exporter
    print("⚠️ Using simple PDF exporter (reportlab not available)")

import config

app = Flask(__name__)
CORS(app)

# Global variables
price_data = None
inventory_data = None
vendor_data = None
forecast_model = None
notification_manager = None
price_scraper = None
forecast_results = {}
last_update = None
last_scrape_time = None
preferred_supplier_analyzer = None

# Thread lock for data updates
data_lock = threading.Lock()

def convert_to_serializable(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def load_data():
    """Load all data from files"""
    global price_data, inventory_data, vendor_data
    
    with data_lock:
        # Load price data
        if os.path.exists(config.MATERIAL_PRICES_CSV):
            price_data = pd.read_csv(config.MATERIAL_PRICES_CSV)
        else:
            print("Initializing data...")
            initialize_data(config.DATA_DIR)
            price_data = pd.read_csv(config.MATERIAL_PRICES_CSV)
        
        # Load inventory
        if os.path.exists(config.INVENTORY_JSON):
            with open(config.INVENTORY_JSON, 'r') as f:
                inventory_data = json.load(f)
        
        # Load vendors
        if os.path.exists(config.VENDORS_JSON):
            with open(config.VENDORS_JSON, 'r') as f:
                vendor_data = json.load(f)

def update_forecasts():
    """Update price forecasts"""
    global forecast_results, last_update
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Updating forecasts...")
    
    with data_lock:
        try:
            # Train models and generate forecasts
            results = forecast_model.train_all_materials(price_data, config.MATERIALS)
            forecast_results = results
            last_update = datetime.now()
            
            print(f"[SUCCESS] Forecasts updated successfully")
            
            # Check for alerts
            check_alerts()
            
        except Exception as e:
            print(f"[ERROR] Error updating forecasts: {str(e)}")

def check_alerts():
    """Check for price and inventory alerts"""
    try:
        # Get current prices
        current_prices = {}
        for material in config.MATERIALS:
            latest_price = price_data[price_data['material'] == material]['price'].iloc[-1]
            current_prices[material] = float(latest_price)
        
        # Get previous prices (from 1 day ago)
        previous_prices = {}
        for material in config.MATERIALS:
            material_prices = price_data[price_data['material'] == material]['price']
            if len(material_prices) > 1:
                previous_prices[material] = float(material_prices.iloc[-2])
        
        # Check price alerts
        notification_manager.check_price_alerts(
            current_prices, 
            previous_prices, 
            threshold=config.PRICE_DROP_THRESHOLD
        )
        
        # Check inventory alerts
        notification_manager.check_inventory_alerts(
            inventory_data,
            threshold=config.INVENTORY_THRESHOLD
        )
        
        # Check forecast-based alerts
        if forecast_results:
            notification_manager.check_forecast_alerts(forecast_results)
            notification_manager.check_reorder_alerts(inventory_data, forecast_results)
        
        # Clean up old alerts (keep last 30 days)
        notification_manager.clear_old_alerts(days=30)
        
    except Exception as e:
        print(f"Error checking alerts: {str(e)}")

def scrape_real_time_prices():
    """Scrape real-time prices from web sources"""
    global price_data, last_scrape_time
    
    if not config.ENABLE_REAL_TIME_SCRAPING:
        # Fall back to simulation if scraping is disabled
        simulate_price_update()
        return
    
    with data_lock:
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scraping real-time prices...")
            
            # Use the scraper to update price data
            price_data = price_scraper.update_price_data(price_data)
            last_scrape_time = datetime.now()
            
            # Save updated data
            price_data.to_csv(config.MATERIAL_PRICES_CSV, index=False)
            
            # Log current prices for verification
            print(f"[OK] Real-time prices updated successfully")
            for material in config.MATERIALS:
                latest = price_data[price_data['material'] == material].iloc[-1]
                print(f"  → {material}: ${float(latest['price']):.2f}/ton (date: {latest['date']})")
            
        except Exception as e:
            print(f"✗ Error scraping prices: {str(e)}")
            import traceback
            traceback.print_exc()
            if config.USE_FALLBACK_ON_SCRAPE_FAIL:
                print("  Falling back to simulated update...")
                simulate_price_update()

def simulate_price_update():
    """Simulate real-time price updates (fallback method)"""
    import numpy as np
    
    with data_lock:
        try:
            # Add small random changes to latest prices
            for material in config.MATERIALS:
                latest_row = price_data[price_data['material'] == material].iloc[-1].copy()
                
                # Small random change
                change_pct = np.random.uniform(-0.5, 0.5)
                new_price = latest_row['price'] * (1 + change_pct / 100)
                
                # Update the latest price
                price_data.loc[price_data['material'] == material, 'price'] = \
                    price_data.loc[price_data['material'] == material, 'price'].iloc[:-1].tolist() + [new_price]
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Prices updated (simulated)")
            
        except Exception as e:
            print(f"Error updating prices: {str(e)}")

# API Endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'last_update': last_update.isoformat() if last_update else None,
        'last_scrape': last_scrape_time.isoformat() if last_scrape_time else None,
        'scraping_enabled': config.ENABLE_REAL_TIME_SCRAPING
    })

@app.route('/api/materials', methods=['GET'])
def get_materials():
    """Get list of tracked materials"""
    return jsonify({
        'materials': config.MATERIALS,
        'count': len(config.MATERIALS)
    })

@app.route('/api/prices/current', methods=['GET'])
def get_current_prices():
    """Get current prices for all materials"""
    with data_lock:
        current_prices = []
        
        for material in config.MATERIALS:
            material_df = price_data[price_data['material'] == material]
            latest = material_df.iloc[-1]
            
            # Calculate 24h change
            if len(material_df) > 1:
                prev_price = material_df.iloc[-2]['price']
                change_pct = ((latest['price'] - prev_price) / prev_price) * 100
            else:
                change_pct = 0
            
            current_prices.append({
                'material': material,
                'price': round(latest['price'], 2),
                'date': latest['date'],
                'change_24h': round(change_pct, 2),
                'volume': int(latest['volume']),
                'source': latest['source']
            })
        
        return jsonify({
            'prices': current_prices,
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/prices/historical/<material>', methods=['GET'])
def get_historical_prices(material):
    """Get historical prices for a specific material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        material_df = price_data[price_data['material'] == material].copy()
        material_df = material_df.sort_values('date')
        
        # Convert to native Python types for JSON serialization
        history = []
        for _, row in material_df.iterrows():
            history.append({
                'date': str(row['date']),
                'material': str(row['material']),
                'price': float(row['price']),
                'volume': int(row['volume']),
                'source': str(row['source'])
            })
        
        return jsonify({
            'material': material,
            'history': history,
            'count': len(history)
        })

@app.route('/api/forecast/<material>', methods=['GET'])
def get_forecast(material):
    """Get price forecast for a specific material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    if material not in forecast_results or forecast_results[material] is None:
        return jsonify({'error': 'Forecast not available'}), 503
    
    result = forecast_results[material]
    forecast_df = result['forecast']
    
    # Get future predictions only
    future_forecast = forecast_df.tail(config.FORECAST_DAYS)
    
    # Convert to native Python types for JSON serialization
    forecast_list = []
    for _, row in future_forecast.iterrows():
        forecast_list.append({
            'date': row['ds'].strftime('%Y-%m-%d'),
            'predicted_price': float(round(row['yhat'], 2)),
            'lower_bound': float(round(row['yhat_lower'], 2)),
            'upper_bound': float(round(row['yhat_upper'], 2))
        })
    
    forecast_data = {
        'material': material,
        'forecast': forecast_list,
        'recommendation': convert_to_serializable(result['recommendation'])
    }
    
    return jsonify(forecast_data)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get buy/wait recommendations for all materials"""
    recommendations = []
    
    for material in config.MATERIALS:
        if material in forecast_results and forecast_results[material]:
            rec = forecast_results[material]['recommendation']
            recommendations.append(convert_to_serializable(rec))
    
    return jsonify({
        'recommendations': recommendations,
        'timestamp': datetime.now().isoformat(),
        'last_update': last_update.isoformat() if last_update else None
    })

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get current inventory levels"""
    with data_lock:
        return jsonify({
            'inventory': inventory_data,
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/inventory/<material>', methods=['GET'])
def get_material_inventory(material):
    """Get inventory for specific material"""
    if material not in inventory_data:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        return jsonify({
            'material': material,
            'inventory': inventory_data[material]
        })

@app.route('/api/vendors/<material>', methods=['GET'])
def get_vendors(material):
    """Get vendor comparison for a material"""
    if material not in vendor_data:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        return jsonify({
            'material': material,
            'vendors': vendor_data[material]
        })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 10, type=int)
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    alerts = notification_manager.get_recent_alerts(limit=limit, unread_only=unread_only)
    summary = notification_manager.get_alert_summary()
    
    return jsonify({
        'alerts': alerts,
        'summary': summary
    })

@app.route('/api/alerts/<int:alert_id>/read', methods=['POST'])
def mark_alert_read(alert_id):
    """Mark an alert as read"""
    try:
        success = notification_manager.mark_as_read(alert_id)
        if success:
            return jsonify({
                'success': True, 
                'message': f'Alert {alert_id} marked as read',
                'alert_id': alert_id
            })
        else:
            return jsonify({
                'success': False, 
                'error': f'Alert {alert_id} not found'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alerts/mark-all-read', methods=['POST'])
def mark_all_alerts_read():
    """Mark all alerts as read"""
    try:
        count = notification_manager.mark_all_as_read()
        return jsonify({
            'success': True, 
            'message': f'Marked {count} alerts as read',
            'count': count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alerts/trigger', methods=['POST'])
def trigger_alert_check():
    """Manually trigger alert checking"""
    try:
        check_alerts()
        return jsonify({'success': True, 'message': 'Alert check completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    """Get complete dashboard summary"""
    with data_lock:
        # Current prices
        current_prices = []
        for material in config.MATERIALS:
            latest = price_data[price_data['material'] == material].iloc[-1]
            current_prices.append({
                'material': material,
                'price': float(round(latest['price'], 2))
            })
        
        # Recommendations (convert numpy types to native Python types)
        recommendations = []
        for material in config.MATERIALS:
            if material in forecast_results and forecast_results[material]:
                rec = forecast_results[material]['recommendation']
                recommendations.append(convert_to_serializable(rec))
        
        # Inventory status
        low_stock_items = [
            material for material, data in inventory_data.items()
            if data['current_stock'] < data['min_threshold']
        ]
        
        # Recent alerts
        recent_alerts = notification_manager.get_recent_alerts(limit=5)
        
        return jsonify({
            'current_prices': current_prices,
            'recommendations': recommendations,
            'inventory': {
                'total_materials': len(inventory_data),
                'low_stock_count': len(low_stock_items),
                'low_stock_items': low_stock_items
            },
            'alerts': {
                'recent': recent_alerts,
                'summary': notification_manager.get_alert_summary()
            },
            'last_update': last_update.isoformat() if last_update else None,
            'timestamp': datetime.now().isoformat()
        })

# Purchase Order Endpoints

def convert_to_json_serializable(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

@app.route('/api/po/generate', methods=['POST'])
def generate_purchase_order():
    """Generate a new purchase order"""
    try:
        data = request.json
        
        material = data.get('material')
        quantity = data.get('quantity', 100)
        requester = data.get('requester', 'Procurement Manager')
        
        if not material or material not in config.MATERIALS:
            return jsonify({'error': 'Invalid material'}), 400
        
        # Get recommendation
        if material not in forecast_results or forecast_results[material] is None:
            return jsonify({'error': 'Forecast not available'}), 503
        
        recommendation = forecast_results[material]['recommendation']
        
        # Get vendor data
        if material not in vendor_data:
            return jsonify({'error': 'Vendor data not available'}), 404
        
        # Use best vendor (first in sorted list)
        vendor = convert_to_json_serializable(vendor_data[material][0])
        
        # Get inventory data
        if material not in inventory_data:
            return jsonify({'error': 'Inventory data not available'}), 404
        
        inventory = convert_to_json_serializable(inventory_data[material])
        
        # Generate PO
        po_generator = get_po_generator()
        po = po_generator.generate_po(
            material=material,
            recommendation=recommendation,
            vendor=vendor,
            quantity=quantity,
            inventory_data=inventory,
            requester=requester
        )
        
        return jsonify({
            'success': True,
            'po': po,
            'message': f'Purchase order {po["po_number"]} generated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/po/list', methods=['GET'])
def list_purchase_orders():
    """List all purchase orders"""
    try:
        status = request.args.get('status')
        limit = request.args.get('limit', 50, type=int)
        
        po_generator = get_po_generator()
        pos = po_generator.list_pos(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'purchase_orders': pos,
            'count': len(pos)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/po/<po_number>', methods=['GET'])
def get_purchase_order(po_number):
    """Get a specific purchase order"""
    try:
        po_generator = get_po_generator()
        po = po_generator.get_po(po_number)
        
        if po:
            return jsonify({
                'success': True,
                'po': po
            })
        else:
            return jsonify({'success': False, 'error': 'PO not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/po/<po_number>/pdf', methods=['GET'])
def export_po_to_pdf(po_number):
    """Export PO to PDF"""
    try:
        po_generator = get_po_generator()
        po = po_generator.get_po(po_number)
        
        if not po:
            return jsonify({'success': False, 'error': 'PO not found'}), 404
        
        # Generate PDF
        pdf_exporter = get_pdf_exporter()
        pdf_path = pdf_exporter.export_po_to_pdf(po)
        
        # Return file path
        return jsonify({
            'success': True,
            'pdf_path': pdf_path,
            'message': f'PDF generated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/po/<po_number>/status', methods=['PUT'])
def update_po_status(po_number):
    """Update PO status"""
    try:
        data = request.json
        new_status = data.get('status')
        updated_by = data.get('updated_by', 'System')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        po_generator = get_po_generator()
        success = po_generator.update_po_status(po_number, new_status, updated_by)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'PO {po_number} status updated to {new_status}'
            })
        else:
            return jsonify({'success': False, 'error': 'PO not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Supply Chain Intelligence Endpoints

@app.route('/api/supply-chain/vendor-risk/<material>', methods=['GET'])
def get_vendor_risk_analysis(material):
    """Get comprehensive vendor risk analysis for a material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        try:
            # Get vendor data
            if material not in vendor_data:
                return jsonify({'error': 'Vendor data not available'}), 404
            
            vendors = convert_to_json_serializable(vendor_data[material])
            
            # Calculate risk scores
            analyzer = get_supply_chain_analyzer()
            risk_analysis = []
            
            for vendor in vendors:
                risk_data = analyzer.calculate_vendor_risk_score(vendor, material)
                risk_analysis.append(risk_data)
            
            return jsonify({
                'material': material,
                'vendor_risk_analysis': risk_analysis,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/supply-chain/alternatives/<material>', methods=['GET'])
def get_alternative_materials(material):
    """Get alternative materials for substitution"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    try:
        analyzer = get_supply_chain_analyzer()
        alternatives = analyzer.get_alternative_materials(material)
        
        return jsonify({
            'material': material,
            'alternatives': alternatives,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/supply-chain/disruption-risk/<material>', methods=['GET'])
def get_supply_disruption_risk(material):
    """Get supply disruption risk assessment for a material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    try:
        analyzer = get_supply_chain_analyzer()
        disruption_risks = analyzer.check_supply_disruption_risks([material])
        
        return jsonify({
            'material': material,
            'disruption_risks': disruption_risks,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/supply-chain/lead-time-optimization/<material>', methods=['GET'])
def get_lead_time_optimization(material):
    """Get lead time optimization recommendations for vendors"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        try:
            # Get vendor data
            if material not in vendor_data:
                return jsonify({'error': 'Vendor data not available'}), 404
            
            vendors = convert_to_json_serializable(vendor_data[material])
            
            # Get current price for context
            material_df = price_data[price_data['material'] == material].iloc[-1]
            current_price = float(material_df['price'])
            
            # Optimize lead times
            analyzer = get_supply_chain_analyzer()
            optimization = analyzer.optimize_lead_times(vendors, material)
            
            return jsonify({
                'material': material,
                'current_price': current_price,
                'lead_time_optimization': optimization,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/supply-chain/insights/<material>', methods=['GET'])
def get_supply_chain_insights(material):
    """Get comprehensive supply chain insights for a material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        try:
            # Get vendor data
            if material not in vendor_data:
                return jsonify({'error': 'Vendor data not available'}), 404
            
            vendors = convert_to_json_serializable(vendor_data[material])
            
            # Get current price
            material_df = price_data[price_data['material'] == material].iloc[-1]
            current_price = float(material_df['price'])
            
            # Get comprehensive insights
            analyzer = get_supply_chain_analyzer()
            insights = analyzer.get_supply_chain_insights(material, current_price, vendors)
            
            return jsonify(insights)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/usp/opportunity-score/<material>', methods=['GET'])
def get_opportunity_score(material):
    """Get Procurement Opportunity Score for a material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404

    with data_lock:
        try:
            # 1. Get price forecast data
            price_forecast = forecast_results.get(material, {})

            # 2. Get inventory data
            material_inventory = inventory_data.get(material, {})

            # 3. Get vendor data
            material_vendors = vendor_data.get(material, [])

            # 4. Get supply chain insights
            supply_chain_analyzer = get_supply_chain_analyzer()
            current_price = price_data[price_data['material'] == material]['price'].iloc[-1]
            supply_chain_insights = supply_chain_analyzer.get_supply_chain_insights(material, float(current_price), material_vendors)

            # 5. Calculate opportunity score
            usp_analyzer = get_usp_analyzer()
            opportunity_score = usp_analyzer.calculate_opportunity_score(
                material,
                price_forecast,
                inventory_data, # Passing full inventory data
                material_vendors,
                supply_chain_insights
            )

            return jsonify(opportunity_score)

        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Preferred Supplier Analytics Endpoints

@app.route('/api/preferred-supplier/<material>', methods=['GET'])
def get_preferred_supplier_analysis(material):
    """Get preferred supplier analysis for a specific material"""
    if material not in config.MATERIALS:
        return jsonify({'error': 'Material not found'}), 404
    
    with data_lock:
        try:
            # Update the analyzer with current data
            current_analyzer = PreferredSupplierAnalyzer(price_data, vendor_data)
            
            # Get comparison for the specific material
            comparison = current_analyzer.compare_prices(material)
            
            return jsonify(comparison)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/preferred-supplier', methods=['GET'])
def get_all_preferred_supplier_analysis():
    """Get preferred supplier analysis for all materials"""
    with data_lock:
        try:
            # Update the analyzer with current data
            current_analyzer = PreferredSupplierAnalyzer(price_data, vendor_data)
            
            # Get comparison for all materials
            comparisons = current_analyzer.get_all_materials_comparison()
            
            return jsonify({
                'preferred_supplier_analysis': comparisons,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/preferred-supplier/negotiations', methods=['GET'])
def get_negotiation_recommendations():
    """Get materials where negotiation with preferred supplier is recommended"""
    with data_lock:
        try:
            # Update the analyzer with current data
            current_analyzer = PreferredSupplierAnalyzer(price_data, vendor_data)
            
            # Get materials where negotiation is recommended
            recommendations = current_analyzer.get_negotiation_recommendations()
            
            return jsonify({
                'negotiation_recommendations': recommendations,
                'count': len(recommendations),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def initialize_app():
    """Initialize application components"""
    global forecast_model, notification_manager, price_scraper, preferred_supplier_analyzer
    
    print("[Initializing Smart Procurement System...]")
    
    # Create data directory
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    # Initialize price scraper
    if config.ENABLE_REAL_TIME_SCRAPING:
        # Pass API key if available
        api_key = config.METAL_PRICE_API_KEY or '3b30bd59dfac506681cc7c57e3af9101'
        price_scraper = get_scraper(metal_api_key=api_key)
        print(f"[OK] Real-time price scraper initialized (API key: {'configured' if api_key else 'not set'})")
    
    # Load data
    load_data()
    print("[OK] Data loaded")
    
    # Initialize forecast model
    forecast_model = PriceForecastModel()
    print("[OK] Forecast model initialized")
    
    # Initialize notification manager
    notification_manager = NotificationManager()
    print("[OK] Notification manager initialized")
    
    # Initialize preferred supplier analyzer
    preferred_supplier_analyzer = PreferredSupplierAnalyzer(price_data, vendor_data)
    print("[OK] Preferred supplier analyzer initialized")
    
    # Generate initial forecasts
    update_forecasts()
    print("[OK] Initial forecasts generated")
    
    # Setup scheduler for periodic updates
    scheduler = BackgroundScheduler()
    
    # Update forecasts every hour
    scheduler.add_job(
        update_forecasts,
        'interval',
        seconds=config.FORECAST_UPDATE_INTERVAL,
        id='update_forecasts'
    )
    
    # Scrape real-time prices or simulate updates
    price_update_func = scrape_real_time_prices if config.ENABLE_REAL_TIME_SCRAPING else simulate_price_update
    scheduler.add_job(
        price_update_func,
        'interval',
        seconds=config.SCRAPING_INTERVAL if config.ENABLE_REAL_TIME_SCRAPING else config.PRICE_UPDATE_INTERVAL,
        id='update_prices'
    )
    
    scheduler.start()
    print("[OK] Background scheduler started")
    
    print(f"\n[Smart Procurement System ready!]")
    print(f"[Tracking {len(config.MATERIALS)} materials: {', '.join(config.MATERIALS)}]")
    print(f"[Forecast updates: every {config.FORECAST_UPDATE_INTERVAL}s]")
    if config.ENABLE_REAL_TIME_SCRAPING:
        print(f"[Real-time price scraping: every {config.SCRAPING_INTERVAL}s]")
    else:
        print(f"[Price updates (simulated): every {config.PRICE_UPDATE_INTERVAL}s]")
    print()

if __name__ == '__main__':
    initialize_app()
    app.run(debug=config.FLASK_DEBUG, port=config.FLASK_PORT, threaded=True)
