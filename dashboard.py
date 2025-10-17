"""
Streamlit Dashboard for Smart Procurement System - Clean Version
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import json
import time

import config

# Page configuration
st.set_page_config(
    page_title="Smart Procurement Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Recommendation Badges */
    .buy-now {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .wait {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
    
    .monitor {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Alert Styles */
    .alert-critical {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #991b1b;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #78350f;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #b45309;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1e40af;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_BASE_URL = f"http://localhost:{config.FLASK_PORT}/api"

# Helper functions
@st.cache_data(ttl=60)
def fetch_data(endpoint):
    """Fetch data from API with caching"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def get_recommendation_color(recommendation):
    """Get color for recommendation badge"""
    colors = {
        'BUY NOW': '#10b981',
        'WAIT': '#f59e0b',
        'MONITOR': '#3b82f6'
    }
    return colors.get(recommendation, '#6c757d')

def create_price_chart(material, historical_data, forecast_data=None):
    """Create interactive price chart with forecast"""
    fig = go.Figure()
    
    # Historical prices
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['price'],
        mode='lines+markers',
        name='Historical Price',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    ))
    
    # Forecast
    if forecast_data and 'forecast' in forecast_data:
        forecast_df = pd.DataFrame(forecast_data['forecast'])
        forecast_df['date'] = pd.to_datetime(forecast_df['date'])
        
        # Predicted price
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['predicted_price'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#f59e0b', width=3, dash='dash'),
            marker=dict(size=6)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['date'].tolist() + forecast_df['date'].tolist()[::-1],
            y=forecast_df['upper_bound'].tolist() + forecast_df['lower_bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(245, 158, 11, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval',
            showlegend=True
        ))
    
    fig.update_layout(
        title=f'{material} Price Trend & Forecast',
        xaxis_title='Date',
        yaxis_title='Price (INR/ton)',
        hovermode='x unified',
        template='plotly_white',
        height=450,
        xaxis=dict(
            tickformat='%m/%d',
            tickangle=-45,
            dtick=86400000.0  # 1 day in milliseconds
        )
    )
    
    return fig

def create_inventory_gauge(material, inventory_data):
    """Create gauge chart for inventory level"""
    current = inventory_data['current_stock']
    max_capacity = inventory_data['max_capacity']
    threshold = inventory_data['min_threshold']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{material} Stock Level (tons)"},
        delta={'reference': threshold, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, max_capacity]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, threshold], 'color': "lightcoral"},
                {'range': [threshold, max_capacity * 0.8], 'color': "lightgreen"},
                {'range': [max_capacity * 0.8, max_capacity], 'color': "lightyellow"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold
            }
        }
    ))
    
    fig.update_layout(height=250)
    return fig

# Main Dashboard
def main():
    # Header
    st.markdown('<div class="main-header">🏭 Smart Procurement Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">⚡ Real-Time Material Price Insights & AI-Powered Recommendations</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("🏭 Navigation")
        
        page = st.radio(
            "Select View",
            ["📊 Overview", "💰 Price Analysis", "📦 Inventory", "🔔 Alerts", "🏪 Vendors", "🤝 Preferred Supplier", "📋 Purchase Orders", "🚚 Supply Chain", "🎯 Opportunity Score"]
        )
        
        st.markdown("---")
        
        # System status
        st.subheader("🔌 System Status")
        health = fetch_data("health")
        if health:
            st.success("✅ System Online")
            if health.get('last_update'):
                update_time = datetime.fromisoformat(health['last_update'])
                st.info(f"🕒 Last Update: {update_time.strftime('%H:%M:%S')}")
        else:
            st.error("❌ System Offline")
            st.warning("Please start the Flask backend:\n```python app.py```")
        
        st.markdown("---")
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
        if auto_refresh:
            time.sleep(30)
            st.rerun()
        
        if st.button("🔄 Refresh Now"):
            st.cache_data.clear()
            st.rerun()
    
    # Main content based on selected page
    if page == "📊 Overview":
        show_overview()
    elif page == "💰 Price Analysis":
        show_price_analysis()
    elif page == "📦 Inventory":
        show_inventory()
    elif page == "🔔 Alerts":
        show_alerts()
    elif page == "🏪 Vendors":
        show_vendors()
    elif page == "🤝 Preferred Supplier":
        show_preferred_supplier()
    elif page == "📋 Purchase Orders":
        show_purchase_orders()
    elif page == "🚚 Supply Chain":
        show_supply_chain()
    elif page == "🎯 Opportunity Score":
        show_opportunity_score()

def show_overview():
    """Overview dashboard page"""
    st.header("📊 Dashboard Overview")
    
    # Fetch summary data
    summary = fetch_data("dashboard/summary")
    
    if not summary:
        st.error("Unable to fetch dashboard data. Please ensure the Flask backend is running.")
        return
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Materials Tracked", len(config.MATERIALS))
    
    with col2:
        buy_now_count = sum(1 for r in summary['recommendations'] if r['recommendation'] == 'BUY NOW')
        st.metric("Buy Recommendations", buy_now_count)
    
    with col3:
        low_stock = summary['inventory']['low_stock_count']
        st.metric("Low Stock Alerts", low_stock, delta=f"-{low_stock}" if low_stock > 0 else "0", delta_color="inverse")
    
    with col4:
        unread_alerts = summary['alerts']['summary'].get('unread', 0)
        st.metric("Unread Alerts", unread_alerts)
    
    st.markdown("---")
    
    # Current prices and recommendations
    st.subheader("💰 Current Prices & Recommendations")
    
    cols = st.columns(len(config.MATERIALS))
    
    for idx, material in enumerate(config.MATERIALS):
        with cols[idx]:
            # Get price
            price_info = next((p for p in summary['current_prices'] if p['material'] == material), None)
            
            # Get recommendation
            rec_info = next((r for r in summary['recommendations'] if r['material'] == material), None)
            
            if price_info and rec_info:
                st.markdown(f"### {material}")
                
                # Price display
                st.metric(
                    "Current Price",
                    f"₹{price_info['price']:,.2f}/ton",
                    delta=f"{price_info.get('change_24h', 0):.2f}%" if 'change_24h' in price_info else None
                )
                
                # Recommendation badge
                rec = rec_info['recommendation']
                rec_class = 'buy-now' if rec == 'BUY NOW' else 'wait' if rec == 'WAIT' else 'monitor'
                st.markdown(
                    f'<div class="{rec_class}" style="text-align: center; margin: 1rem 0;">{rec}</div>',
                    unsafe_allow_html=True
                )
                
                st.caption(rec_info['reason'])
                
                if rec_info['potential_savings'] > 0:
                    st.success(f"💰 Potential savings: ₹{rec_info['potential_savings']:,.2f}/ton")
    
    st.markdown("---")
    
    # Quick charts
    st.subheader("📈 Price Trends (Last 7 Days)")
    
    chart_cols = st.columns(len(config.MATERIALS))
    
    for idx, material in enumerate(config.MATERIALS):
        with chart_cols[idx]:
            historical = fetch_data(f"prices/historical/{material}")
            
            if historical:
                df = pd.DataFrame(historical['history'])
                df['date'] = pd.to_datetime(df['date'])
                # Group by date (day only) and take the mean price for each day
                df['date_day'] = df['date'].dt.date
                df = df.groupby('date_day')['price'].mean().reset_index()
                df['date'] = pd.to_datetime(df['date_day']) # Convert back to datetime for plotting
                df = df.tail(7)
                
                # Format date for better display
                df['date_str'] = df['date'].dt.strftime('%m/%d')
                
                fig = px.line(df, x='date_str', y='price', title=material, markers=True)
                fig.update_layout(
                    height=250, 
                    showlegend=False, 
                    xaxis_title="", 
                    yaxis_title="Price (INR/ton)",
                    xaxis=dict(tickangle=-45),
                    margin=dict(l=20, r=20, t=40, b=40)
                )
                fig.update_traces(line_color='#667eea', line_width=3, marker=dict(size=8, color='#764ba2'))
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent alerts
    st.subheader("🔔 Recent Alerts")
    
    if summary['alerts']['recent']:
        for alert in summary['alerts']['recent'][:5]:
            severity_class = f"alert-{alert['severity'].lower()}"
            st.markdown(
                f'<div class="{severity_class}">'
                f'<strong>{alert["type"]}</strong> - {alert["material"]}<br>'
                f'{alert["message"]}<br>'
                f'<small>{alert["timestamp"]}</small>'
                f'</div><br>',
                unsafe_allow_html=True
            )
    else:
        st.info("No recent alerts")

def show_price_analysis():
    """Price analysis page"""
    st.header("💰 Price Analysis & Forecasting")
    
    # Material selector
    material = st.selectbox("Select Material", config.MATERIALS)
    
    # Fetch data
    historical = fetch_data(f"prices/historical/{material}")
    forecast = fetch_data(f"forecast/{material}")
    
    if not historical:
        st.error("Unable to fetch price data")
        return
    
    # Price chart with forecast
    st.subheader(f"{material} Price Analysis")
    
    fig = create_price_chart(material, historical['history'], forecast)
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendation details
    if forecast and 'recommendation' in forecast:
        rec = forecast['recommendation']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Recommendation")
            
            rec_text = rec['recommendation']
            rec_class = 'buy-now' if rec_text == 'BUY NOW' else 'wait' if rec_text == 'WAIT' else 'monitor'
            
            st.markdown(
                f'<div class="{rec_class}" style="text-align: center; font-size: 1.5rem; padding: 1.5rem;">{rec_text}</div>',
                unsafe_allow_html=True
            )
            
            st.markdown(f"**Reason:** {rec['reason']}")
            st.markdown(f"**Confidence:** {rec['confidence']}")
            st.markdown(f"**Best day to buy:** Day {rec['best_day_to_buy']} (from today)")
        
        with col2:
            st.markdown("### 📊 Price Metrics")
            
            st.metric("Current Price", f"₹{rec['current_price']:,.2f}/ton")
            st.metric(
                "Avg Forecast Price (7d)",
                f"₹{rec['avg_forecast_price']:,.2f}/ton",
                delta=f"{rec['price_change_pct']:.2f}%"
            )
            st.metric("Min Forecast Price", f"₹{rec['min_forecast_price']:,.2f}/ton")
            
            if rec['potential_savings'] > 0:
                st.success(f"💰 Potential Savings: ₹{rec['potential_savings']:,.2f}/ton")
    
    # Historical statistics
    st.markdown("---")
    st.subheader("📈 Historical Statistics (30 Days)")
    
    df = pd.DataFrame(historical['history'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Price", f"${df['price'].mean():.2f}")
    
    with col2:
        st.metric("Highest Price", f"${df['price'].max():.2f}")
    
    with col3:
        st.metric("Lowest Price", f"${df['price'].min():.2f}")
    
    with col4:
        volatility = df['price'].std()
        st.metric("Volatility (σ)", f"${volatility:.2f}")
    
    # Price distribution
    st.subheader("📊 Price Distribution")
    fig = px.histogram(df, x='price', nbins=20, title=f"{material} Price Distribution", color_discrete_sequence=['#667eea'])
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_inventory():
    """Inventory management page"""
    st.header("📦 Inventory Management")
    
    # Fetch inventory data
    inventory = fetch_data("inventory")
    
    if not inventory:
        st.error("Unable to fetch inventory data")
        return
    
    inventory_data = inventory['inventory']
    
    # Inventory gauges
    st.subheader("Current Stock Levels")
    
    cols = st.columns(len(config.MATERIALS))
    
    for idx, material in enumerate(config.MATERIALS):
        with cols[idx]:
            if material in inventory_data:
                fig = create_inventory_gauge(material, inventory_data[material])
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed inventory table
    st.subheader("Inventory Details")
    
    inventory_list = []
    for material, data in inventory_data.items():
        days_remaining = data['current_stock'] / data['daily_consumption']
        
        inventory_list.append({
            'Material': material,
            'Current Stock': f"{data['current_stock']:.1f} {data['unit']}",
            'Min Threshold': f"{data['min_threshold']} {data['unit']}",
            'Daily Consumption': f"{data['daily_consumption']:.1f} {data['unit']}",
            'Days Remaining': f"{days_remaining:.1f} days",
            'Status': data['status'],
            'Location': data['location']
        })
    
    df = pd.DataFrame(inventory_list)
    st.dataframe(df, use_container_width=True)
    
    # Consumption forecast
    st.markdown("---")
    st.subheader("📉 Consumption Forecast")
    
    material_select = st.selectbox("Select Material for Forecast", config.MATERIALS, key="inv_material")
    
    if material_select in inventory_data:
        data = inventory_data[material_select]
        
        # Calculate projected stock levels
        days = 30
        current_stock = data['current_stock']
        daily_consumption = data['daily_consumption']
        
        projected_stock = [max(0, current_stock - (i * daily_consumption)) for i in range(days)]
        dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=projected_stock,
            mode='lines',
            name='Projected Stock',
            line=dict(color='#667eea', width=3)
        ))
        
        fig.add_hline(
            y=data['min_threshold'],
            line_dash="dash",
            line_color="red",
            annotation_text="Min Threshold"
        )
        
        fig.update_layout(
            title=f"{material_select} Stock Projection (30 Days)",
            xaxis_title="Date",
            yaxis_title="Stock Level (tons)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Reorder recommendation
        if current_stock < data['min_threshold']:
            st.error(f"⚠️ {material_select} stock is below minimum threshold. Immediate reorder recommended!")
        else:
            days_until_reorder = (current_stock - data['min_threshold']) / daily_consumption
            st.info(f"📅 Reorder {material_select} in approximately {days_until_reorder:.0f} days")

def show_alerts():
    """Alerts and notifications page"""
    st.header("🔔 Alerts & Notifications")
    
    # Fetch alerts
    alerts_data = fetch_data("alerts?limit=50")
    
    if not alerts_data:
        st.error("Unable to fetch alerts")
        return
    
    alerts = alerts_data['alerts']
    summary = alerts_data['summary']
    
    # Alert summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alerts", summary.get('total', 0))
    
    with col2:
        st.metric("Unread", summary.get('unread', 0))
    
    with col3:
        critical = summary.get('by_severity', {}).get('CRITICAL', 0)
        st.metric("Critical", critical)
    
    with col4:
        warning = summary.get('by_severity', {}).get('WARNING', 0)
        st.metric("Warnings", warning)
    
    st.markdown("---")
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        filter_type = st.multiselect(
            "Filter by Type",
            ["PRICE_DROP", "PRICE_INCREASE", "LOW_INVENTORY", "HIGH_INVENTORY", 
             "FORECAST_BUY", "FORECAST_WAIT", "REORDER_NOW", "REORDER_WAIT"],
            default=[]
        )
    
    with col2:
        filter_severity = st.multiselect(
            "Filter by Severity",
            ["CRITICAL", "WARNING", "INFO"],
            default=[]
        )
    
    # Filter alerts
    filtered_alerts = alerts
    
    if filter_type:
        filtered_alerts = [a for a in filtered_alerts if a['type'] in filter_type]
    
    if filter_severity:
        filtered_alerts = [a for a in filtered_alerts if a['severity'] in filter_severity]
    
    # Display alerts
    st.subheader(f"Alerts ({len(filtered_alerts)})")
    
    if filtered_alerts:
        for alert in filtered_alerts:
            severity_class = f"alert-{alert['severity'].lower()}"
            
            # Alert icon
            icon = "🔴" if alert['severity'] == 'CRITICAL' else "⚠️" if alert['severity'] == 'WARNING' else "ℹ️"
            
            st.markdown(
                f'<div class="{severity_class}">'
                f'{icon} <strong>{alert["type"]}</strong> - {alert["material"]}<br>'
                f'{alert["message"]}<br>'
                f'<small>🕒 {alert["timestamp"]}</small>'
                f'</div><br>',
                unsafe_allow_html=True
            )
    else:
        st.info("No alerts match the selected filters")

def show_vendors():
    """Vendor comparison page"""
    st.header("🏪 Vendor Comparison")
    
    # Material selector
    material = st.selectbox("Select Material", config.MATERIALS, key="vendor_material")
    
    # Fetch vendor data
    vendors_data = fetch_data(f"vendors/{material}")
    # Fetch preferred supplier analysis
    preferred_analysis = fetch_data(f"preferred-supplier/{material}")
    
    if not vendors_data:
        st.error("Unable to fetch vendor data")
        return
    
    vendors = vendors_data['vendors']
    
    # Show preferred supplier status if available
    if preferred_analysis and 'preferred_supplier' in preferred_analysis:
        preferred_supplier = preferred_analysis['preferred_supplier']
        market_average = preferred_analysis['market_average']
        preferred_price = preferred_analysis['preferred_price']
        price_diff_pct = preferred_analysis['price_difference_percent']
        needs_negotiation = preferred_analysis.get('negotiation_suggestion', False)
        
        st.info(f"🤝 **Your Preferred Supplier:** {preferred_supplier}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Preferred Price", f"₹{preferred_price:,.2f}/ton")
        
        with col2:
            st.metric("Market Average", f"₹{market_average:,.2f}/ton")
        
        with col3:
            diff_text = f"{price_diff_pct:+.2f}%"
            if needs_negotiation:
                st.metric("Difference", diff_text, delta_color="inverse")
            else:
                st.metric("Difference", diff_text)
        
        if needs_negotiation:
            st.warning(f"⚠️ **Negotiation Suggestion:** {preferred_analysis['suggestion_message']}")
        else:
            st.success(f"✅ Your preferred supplier's price is competitive")
    
    # Top recommendation
    if vendors:
        best_vendor = vendors[0]  # Already sorted by price
        
        st.success(f"🏆 **Recommended Vendor:** {best_vendor['name']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Best Price", f"₹{best_vendor['price']:,.2f}/ton")
        
        with col2:
            st.metric("Rating", f"{best_vendor['rating']}/5.0")
        
        with col3:
            st.metric("Delivery", f"{best_vendor['delivery_days']} days")
    
    st.markdown("---")
    
    # Vendor comparison table
    st.subheader("All Vendors")
    
    vendor_list = []
    for vendor in vendors:
        # Highlight preferred supplier
        if vendor['name'] == preferred_analysis.get('preferred_supplier', ''):
            vendor_name = f"🤝 {vendor['name']}"
        else:
            vendor_name = vendor['name']
        
        vendor_list.append({
            'Vendor': vendor_name,
            'Price (INR/ton)': f"₹{vendor['price']:,.2f}",
            'Rating': f"{'⭐' * int(vendor['rating'])} ({vendor['rating']})",
            'Delivery': f"{vendor['delivery_days']} days",
            'Min Order': f"{vendor['min_order']} tons",
            'Payment Terms': vendor['payment_terms'],
            'Reliability': vendor['reliability']
        })
    
    df = pd.DataFrame(vendor_list)
    st.dataframe(df, use_container_width=True)
    
    # Price comparison chart
    st.subheader("Price Comparison")
    
    vendor_names = [v['name'] for v in vendors]
    # Use original names for price extraction to match the vendor data structure
    original_vendor_names = [v['name'] for v in vendors]
    vendor_prices = [v['price'] for v in vendors]
    
    # Create a color map to highlight the preferred supplier
    color_map = {}
    for name in original_vendor_names:
        if name == preferred_analysis.get('preferred_supplier', ''):
            color_map[name] = '#f59e0b'  # Yellow for preferred supplier
        else:
            color_map[name] = '#667eea'  # Blue for others
    
    fig = px.bar(
        x=vendor_names,
        y=vendor_prices,
        labels={'x': 'Vendor', 'y': 'Price (INR/ton)'},
        title=f"{material} Price Comparison Across Vendors",
        color=vendor_names,
        color_discrete_map=color_map
    )
    
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Vendor details
    st.markdown("---")
    st.subheader("Vendor Details")
    
    selected_vendor = st.selectbox("Select Vendor for Details", vendor_names)
    
    # Extract original vendor name (without emojis)
    original_selected_vendor = selected_vendor.replace("🤝 ", "")
    
    vendor_detail = next((v for v in vendors if v['name'] == original_selected_vendor), None)
    
    if vendor_detail:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Vendor Information")
            if vendor_detail['name'] == preferred_analysis.get('preferred_supplier', ''):
                st.write(f"**Name:** 🤝 {vendor_detail['name']} (Your Preferred Supplier)")
            else:
                st.write(f"**Name:** {vendor_detail['name']}")
            st.write(f"**Price:** ₹{vendor_detail['price']:,.2f}/ton")
            st.write(f"**Rating:** {vendor_detail['rating']}/5.0")
            st.write(f"**Reliability:** {vendor_detail['reliability']}")
        
        with col2:
            st.markdown("### 📦 Order Information")
            st.write(f"**Minimum Order:** {vendor_detail['min_order']} tons")
            st.write(f"**Delivery Time:** {vendor_detail['delivery_days']} days")
            st.write(f"**Payment Terms:** {vendor_detail['payment_terms']}")
            
            # Calculate total cost for different quantities
            st.markdown("### 💰 Cost Calculator")
            quantity = st.number_input("Order Quantity (tons)", min_value=vendor_detail['min_order'], value=100, step=10)
            total_cost = quantity * vendor_detail['price']
            st.success(f"Total Cost: ₹{total_cost:,.2f}")

def show_purchase_orders():
    """Purchase Orders page"""
    st.header("📋 Purchase Order Management")
    
    # Tabs for different PO actions
    tab1, tab2, tab3 = st.tabs(["🆕 Generate New PO", "📜 View POs", "📊 PO Analytics"])
    
    with tab1:
        st.subheader("Generate Purchase Order")
        
        # Fetch recommendations for context
        recommendations_data = fetch_data("recommendations")
        
        if not recommendations_data:
            st.error("Unable to fetch recommendations. Please ensure the backend is running.")
            return
        
        recommendations = recommendations_data.get('recommendations', [])
        
        # Material selection
        col1, col2 = st.columns(2)
        
        with col1:
            material = st.selectbox("Select Material", config.MATERIALS)
            quantity = st.number_input("Quantity (tons)", min_value=10, value=100, step=10)
        
        with col2:
            requester = st.text_input("Requester Name", value="Procurement Manager")
        
        # Show recommendation context
        rec_info = next((r for r in recommendations if r['material'] == material), None)
        
        if rec_info:
            st.markdown("### 🤖 AI Recommendation Context")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rec = rec_info['recommendation']
                rec_class = 'buy-now' if rec == 'BUY NOW' else 'wait' if rec == 'WAIT' else 'monitor'
                st.markdown(
                    f'<div class="{rec_class}" style="text-align: center; padding: 1rem;">{rec}</div>',
                    unsafe_allow_html=True
                )
            
            with col2:
                st.metric("Current Price", f"₹{rec_info['current_price']:,.2f}/ton")
            
            with col3:
                st.metric("Forecast Change", f"{rec_info['price_change_pct']:+.2f}%")
            
            st.info(f"💡 {rec_info['reason']}")
        
        # Generate PO button
        st.markdown("---")
        
        if st.button("🚀 Generate Purchase Order", type="primary"):
            with st.spinner("Generating purchase order..."):
                try:
                    # Call API to generate PO
                    response = requests.post(
                        f"{API_BASE_URL}/po/generate",
                        json={
                            'material': material,
                            'quantity': quantity,
                            'requester': requester
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        po = result['po']
                        
                        st.success(f"✅ {result['message']}")
                        
                        # Display PO summary
                        st.markdown("### 📄 Purchase Order Summary")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("PO Number", po['po_number'])
                            st.metric("Status", po['status'])
                        
                        with col2:
                            st.metric("Total Amount", f"${po['financial']['total_amount']:,.2f}")
                            st.metric("Vendor", po['vendor']['name'])
                        
                        with col3:
                            st.metric("Expected Delivery", po['delivery']['expected_date'])
                            st.metric("Potential Savings", f"₹{po['financial']['potential_savings']:,.2f}")
                        
                        # Export to PDF button
                        if st.button("📥 Export to PDF"):
                            pdf_response = requests.get(
                                f"{API_BASE_URL}/po/{po['po_number']}/pdf",
                                timeout=10
                            )
                            
                            if pdf_response.status_code == 200:
                                pdf_result = pdf_response.json()
                                st.success(f"✅ PDF generated: {pdf_result['pdf_path']}")
                            else:
                                st.error("Failed to generate PDF")
                    
                    else:
                        st.error(f"Failed to generate PO: {response.json().get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("View Purchase Orders")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "DRAFT", "APPROVED", "SENT", "RECEIVED"])
        
        with col2:
            limit = st.number_input("Show", min_value=10, max_value=100, value=20, step=10)
        
        with col3:
            if st.button("🔄 Refresh"):
                st.cache_data.clear()
                st.rerun()
        
        # Fetch POs
        try:
            params = {'limit': limit}
            if status_filter != "All":
                params['status'] = status_filter
            
            response = requests.get(
                f"{API_BASE_URL}/po/list",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                pos = result.get('purchase_orders', [])
                
                if pos:
                    st.success(f"Found {len(pos)} purchase orders")
                    
                    # Display POs as cards
                    for po in pos:
                        with st.expander(f"📋 {po['po_number']} - {po['material']['name']} - {po['status']}"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Material:** {po['material']['name']}")
                                st.write(f"**Quantity:** {po['material']['quantity']} {po['material']['unit']}")
                                st.write(f"**Vendor:** {po['vendor']['name']}")
                            
                            with col2:
                                st.write(f"**Total Amount:** ${po['financial']['total_amount']:,.2f}")
                                st.write(f"**Created:** {po['created_date']}")
                                st.write(f"**Status:** {po['status']}")
                            
                            with col3:
                                st.write(f"**Expected Delivery:** {po['delivery']['expected_date']}")
                                st.write(f"**Recommendation:** {po['ai_recommendation']['recommendation']}")
                                st.write(f"**Savings:** ₹{po['financial']['potential_savings']:,.2f}")
                            
                            # Action buttons
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if st.button(f"📥 Export PDF", key=f"pdf_{po['po_number']}"):
                                    pdf_response = requests.get(
                                        f"{API_BASE_URL}/po/{po['po_number']}/pdf",
                                        timeout=10
                                    )
                                    if pdf_response.status_code == 200:
                                        st.success("PDF generated!")
                            
                            with col2:
                                if po['status'] == 'DRAFT':
                                    if st.button(f"✅ Approve", key=f"approve_{po['po_number']}"):
                                        update_response = requests.put(
                                            f"{API_BASE_URL}/po/{po['po_number']}/status",
                                            json={'status': 'APPROVED', 'updated_by': requester},
                                            timeout=10
                                        )
                                        if update_response.status_code == 200:
                                            st.success("PO Approved!")
                                            st.rerun()
                else:
                    st.info("No purchase orders found")
            
            else:
                st.error("Failed to fetch purchase orders")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with tab3:
        st.subheader("Purchase Order Analytics")
        
        try:
            response = requests.get(f"{API_BASE_URL}/po/list?limit=100", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                pos = result.get('purchase_orders', [])
                
                if pos:
                    # Convert to DataFrame
                    po_data = []
                    for po in pos:
                        po_data.append({
                            'PO Number': po['po_number'],
                            'Material': po['material']['name'],
                            'Quantity': po['material']['quantity'],
                            'Total Amount': po['financial']['total_amount'],
                            'Savings': po['financial']['potential_savings'],
                            'Status': po['status'],
                            'Recommendation': po['ai_recommendation']['recommendation']
                        })
                    
                    df = pd.DataFrame(po_data)
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total POs", len(df))
                    
                    with col2:
                        st.metric("Total Value", f"${df['Total Amount'].sum():,.2f}")
                    
                    with col3:
                        st.metric("Total Savings", f"₹{df['Savings'].sum():,.2f}")
                    
                    with col4:
                        savings_pct = (df['Savings'].sum() / df['Total Amount'].sum()) * 100
                        st.metric("Savings %", f"{savings_pct:.2f}%")
                    
                    st.markdown("---")
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # POs by Material
                        fig = px.pie(df, names='Material', title='POs by Material')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # POs by Status
                        fig = px.pie(df, names='Status', title='POs by Status')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Value by Material
                    material_value = df.groupby('Material')['Total Amount'].sum().reset_index()
                    fig = px.bar(material_value, x='Material', y='Total Amount', 
                                title='Total Value by Material', color='Total Amount')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Data table
                    st.markdown("### 📊 Detailed PO Data")
                    st.dataframe(df, use_container_width=True)
                
                else:
                    st.info("No purchase orders available for analytics")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

def show_supply_chain():
    """Supply Chain Intelligence page"""
    st.header("🚚 Supply Chain Intelligence")
    
    # Material selector
    material = st.selectbox("Select Material", config.MATERIALS, key="sc_material")
    
    if not material:
        st.info("Please select a material to view supply chain intelligence")
        return
    
    # Fetch supply chain insights
    with st.spinner(f"Analyzing supply chain for {material}..."):
        try:
            insights_response = requests.get(
                f"{API_BASE_URL}/supply-chain/insights/{material}",
                timeout=15
            )
            
            if insights_response.status_code == 200:
                insights = insights_response.json()
            else:
                st.error(f"Failed to fetch supply chain insights: {insights_response.status_code}")
                return
                
        except Exception as e:
            st.error(f"Error fetching supply chain insights: {str(e)}")
            return
    
    # Display overall health
    health_score = insights.get('supply_chain_health_score', 0)
    health_level = insights.get('supply_chain_health_level', 'UNKNOWN')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Supply Chain Health", f"{health_score}/100", delta=None)
    
    with col2:
        health_emoji = "🟢" if health_level in ["EXCELLENT", "GOOD"] else "🟡" if health_level == "FAIR" else "🔴"
        st.markdown(f"### {health_emoji} Health Level: {health_level}")
    
    with col3:
        if insights.get('recommendations', {}).get('alternative_considerations'):
            st.warning("🔄 Consider alternative materials")
        else:
            st.success("✅ Material supply is stable")
    
    st.markdown("---")
    
    # Vendor Risk Analysis
    st.subheader("🛡️ Vendor Risk Analysis")
    
    vendor_risks = insights.get('vendor_risk_analysis', [])
    if vendor_risks:
        # Create DataFrame for visualization
        risk_data = []
        for vr in vendor_risks:
            risk_data.append({
                'Vendor': vr['vendor_name'],
                'Risk Score': vr['risk_score'],
                'Risk Level': vr['risk_level'],
                'Recommendation': vr['recommendation'][:50] + "..." if len(vr['recommendation']) > 50 else vr['recommendation']
            })
        
        risk_df = pd.DataFrame(risk_data)
        
        # Color code based on risk level
        def color_risk(val):
            color = 'red' if val == 'CRITICAL' else 'orange' if val == 'HIGH' else 'yellow' if val == 'MEDIUM' else 'green'
            return f'background-color: {color}; color: white;'
        
        st.dataframe(risk_df.style.applymap(color_risk, subset=['Risk Level']))
        
        # Risk breakdown chart
        fig = px.bar(
            risk_df,
            x='Vendor',
            y='Risk Score',
            title='Vendor Risk Scores',
            color='Risk Level',
            color_discrete_map={'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'},
            range_y=[0, 100]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Disruption Risks
    st.subheader("⚠️ Supply Disruption Risks")
    
    disruption_risks = insights.get('disruption_risks', [])
    if disruption_risks:
        disruption = disruption_risks[0]  # Take first (should be only one for the material)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Disruption Risk Score", f"{disruption['disruption_risk_score']}/100")
        
        with col2:
            st.info(f"Risk Factors Identified: {len(disruption.get('risk_factors', []))}")
        
        # Show risk factors
        risk_factors = disruption.get('risk_factors', [])
        if risk_factors:
            st.write("**Potential Risk Factors:**")
            for factor in risk_factors:
                st.warning(f"⚠️ {factor}")
        
        # Show mitigation strategies
        mitigation_strategies = disruption.get('mitigation_strategies', [])
        st.write("**Mitigation Strategies:**")
        for strategy in mitigation_strategies[:3]:  # Show top 3
            st.success(f"✅ {strategy}")
    
    st.markdown("---")
    
    # Alternative Materials
    st.subheader("🔄 Alternative Materials")
    
    alternatives = insights.get('alternative_materials', [])
    if alternatives:
        st.write(f"Potential alternatives for {material}:")
        
        for alt in alternatives:
            with st.expander(f"{alt['substitute']} - {alt['substitution_feasibility']*100:.0f}% feasible"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Feasibility:** {alt['substitution_feasibility']*100:.0f}%")
                    st.write(f"**Use Case:** {alt['typical_use_case']}")
                
                with col2:
                    st.write(f"**Cost:** ${alt.get('current_price', 'N/A')}")
                    st.write(f"**Cost Impact:** {alt.get('cost_implication', 'Unknown')}")
        
        # Show if alternatives are recommended
        if any(alt['substitution_feasibility'] > 0.7 for alt in alternatives):
            st.success("🟢 High-feasibility alternatives available - consider for risk mitigation")
        else:
            st.info("ℹ️ Alternatives available but may require design changes")
    else:
        st.info(f"No suitable alternatives found for {material} within price threshold")
    
    st.markdown("---")
    
    # Lead Time Optimization
    st.subheader("⏱️ Lead Time Optimization")
    
    lead_time_opt = insights.get('lead_time_optimization', [])
    if lead_time_opt:
        # Show top 3 vendors by combined score
        top_vendors = lead_time_opt[:3]
        
        for vendor in top_vendors:
            with st.container():
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**{vendor['vendor_name']}**")
                    st.write(f"Combined Score: {vendor['combined_score']}")
                
                with col2:
                    st.metric("Delivery", f"{vendor['delivery_days']} days")
                    st.write(f"Unit Price: ${vendor['unit_price']:,}")
                
                with col3:
                    st.write(f"**Recommendation:** {vendor['recommendation'][:40]}...")
                    st.write(f"**Order Timing:** {vendor['optimal_order_timing']}")
                
                # Progress bar for score visualization
                score_pct = vendor['combined_score'] / 100
                st.progress(score_pct)
                st.markdown("---")
    
    st.markdown("---")
    
    # Recommendations Summary
    st.subheader("📋 Recommendations Summary")
    
    recommendations = insights.get('recommendations', {})
    
    if recommendations.get('vendor_selection'):
        st.write("**Vendor Selection:**")
        for rec in recommendations['vendor_selection']:
            st.info(f"ℹ️ {rec}")
    
    if recommendations.get('risk_mitigation'):
        st.write("**Risk Mitigation:**")
        for strategy in recommendations['risk_mitigation'][:3]:  # Top 3
            st.success(f"✅ {strategy}")
    
    if recommendations.get('procurement_timing'):
        st.write("**Procurement Timing:**")
        st.write(f"📅 {recommendations['procurement_timing']}")

def show_preferred_supplier():
    """Preferred supplier analytics page"""
    st.header("🤝 Preferred Supplier Analytics")
    
    # Fetch preferred supplier analysis data
    analysis_data = fetch_data("preferred-supplier")
    
    if not analysis_data:
        st.error("Unable to fetch preferred supplier analysis data")
        return
    
    comparisons = analysis_data.get('preferred_supplier_analysis', [])
    
    # Display summary
    if comparisons:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_materials = len(comparisons)
            st.metric("Tracked Materials", total_materials)
        
        with col2:
            # Count materials where negotiation is recommended
            negotiation_count = sum(1 for comp in comparisons if comp.get('negotiation_suggestion', False))
            st.metric("Needs Negotiation", negotiation_count)
        
        with col3:
            # Count materials where price is below market average
            below_market = sum(1 for comp in comparisons if comp.get('price_difference_percent', 0) < 0)
            st.metric("Below Market", below_market)
        
        with col4:
            # Count materials where price is above market average
            above_market = sum(1 for comp in comparisons if comp.get('price_difference_percent', 0) > 0)
            st.metric("Above Market", above_market)
        
        st.markdown("---")
        
        # Detailed comparison table
        st.subheader("📊 Price Comparison with Market Average")
        
        comparison_list = []
        for comparison in comparisons:
            if 'error' not in comparison:
                comparison_list.append({
                    'Material': comparison['material'],
                    'Preferred Supplier': comparison.get('preferred_supplier', 'Not Set'),
                    'Market Average': f"₹{comparison['market_average']:,.2f}/ton",
                    'Preferred Price': f"₹{comparison['preferred_price']:,.2f}/ton",
                    'Difference': f"₹{comparison['price_difference']:,.2f}/ton",
                    'Difference %': f"{comparison['price_difference_percent']:+.2f}%",
                    'Needs Negotiation': "✅ Yes" if comparison.get('negotiation_suggestion', False) else "❌ No"
                })
        
        if comparison_list:
            df = pd.DataFrame(comparison_list)
            st.dataframe(df, use_container_width=True)
        
        # Highlight materials needing negotiation
        negotiation_recs = fetch_data("preferred-supplier/negotiations")
        if negotiation_recs and negotiation_recs.get('negotiation_recommendations'):
            st.markdown("---")
            st.subheader("📋 Negotiation Recommendations")
            
            for rec in negotiation_recs['negotiation_recommendations']:
                with st.container():
                    st.warning(f"⚠️ **{rec['material']}** - {rec['suggestion_message']}")
                    st.markdown("---")
        
        # Detailed analytics by material
        st.markdown("---")
        st.subheader("🔍 Detailed Analytics by Material")
        
        material_tabs = st.tabs(config.MATERIALS)
        
        for i, material in enumerate(config.MATERIALS):
            with material_tabs[i]:
                # Find comparison for this material
                material_comparison = next((comp for comp in comparisons if comp['material'] == material), None)
                
                if material_comparison and 'error' not in material_comparison:
                    st.markdown(f"### {material}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Market Average", f"₹{material_comparison['market_average']:,.2f}/ton")
                    
                    with col2:
                        st.metric("Preferred Supplier Price", f"₹{material_comparison['preferred_price']:,.2f}/ton")
                    
                    with col3:
                        st.metric("Difference", f"{material_comparison['price_difference_percent']:+.2f}%")
                    
                    # Recommendation box
                    if material_comparison.get('negotiation_suggestion', False):
                        st.error(f"🔴 {material_comparison['suggestion_message']}")
                    else:
                        st.success(f"🟢 {material_comparison['suggestion_message']}")
                    
                    # Price comparison bar chart
                    comparison_df = pd.DataFrame({
                        'Supplier': ['Market Average', material_comparison.get('preferred_supplier', 'Preferred')],
                        'Price': [material_comparison['market_average'], material_comparison['preferred_price']]
                    })
                    
                    fig = px.bar(
                        comparison_df,
                        x='Supplier',
                        y='Price',
                        title=f'{material} - Price Comparison',
                        color='Supplier',
                        color_discrete_map={material_comparison.get('preferred_supplier', 'Preferred'): '#f59e0b', 'Market Average': '#667eea'}
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No data available for {material}")

def show_opportunity_score():
    """Procurement Opportunity Score page"""
    st.header("🎯 Procurement Opportunity Score")

    # Material selector
    material = st.selectbox("Select Material", config.MATERIALS, key="usp_material")

    if not material:
        st.info("Please select a material to view the opportunity score.")
        return

    # Fetch opportunity score
    with st.spinner(f"Calculating opportunity score for {material}..."):
        score_data = fetch_data(f"usp/opportunity-score/{material}")

    if not score_data:
        st.error("Unable to calculate opportunity score. Please ensure the backend is running correctly.")
        return

    score = score_data.get('opportunity_score', 0)
    breakdown = score_data.get('breakdown', {})
    recommendation = score_data.get('recommendation', "No recommendation available.")

    # Display gauge chart for the score
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{material} Opportunity Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': 'red'},
                {'range': [40, 60], 'color': 'orange'},
                {'range': [60, 80], 'color': 'yellow'},
                {'range': [80, 100], 'color': 'green'}
            ],
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

    # Display recommendation
    st.markdown(f"### Recommendation: {recommendation}")

    st.markdown("---")

    # Display score breakdown
    st.subheader("Score Breakdown")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Price Opportunity", f"{breakdown.get('price_opportunity', 0)}/100")
    with col2:
        st.metric("Inventory Need", f"{breakdown.get('inventory_need', 0)}/100")
    with col3:
        st.metric("Vendor Quality", f"{breakdown.get('vendor_quality', 0)}/100")
    with col4:
        st.metric("Market Stability", f"{breakdown.get('market_stability', 0)}/100")


if __name__ == "__main__":
    main()
