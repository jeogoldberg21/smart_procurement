"""
Startup script to run both Flask backend and Streamlit dashboard
"""
import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_flask():
    """Run Flask backend"""
    print("🚀 Starting Flask backend...")
    subprocess.run([sys.executable, "app.py"])

def run_streamlit():
    """Run Streamlit dashboard"""
    print("🎨 Starting Streamlit dashboard...")
    time.sleep(3)  # Wait for Flask to start
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

def main():
    """Main startup function"""
    print("=" * 60)
    print("🏭 Smart Procurement System - Startup")
    print("=" * 60)
    print()
    
    # Check if data exists
    if not os.path.exists('data/material_prices.csv'):
        print("📊 Generating initial data...")
        from utils.data_generator import initialize_data
        initialize_data()
        print("✓ Data generated successfully\n")
    
    print("Starting services...")
    print()
    print("📡 Flask Backend: http://localhost:5000")
    print("🎨 Streamlit Dashboard: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop all services")
    print("=" * 60)
    print()
    
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait a bit for Flask to start
    time.sleep(5)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8501')
    except:
        pass
    
    # Run Streamlit in main thread
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Smart Procurement System...")
        print("✓ All services stopped")

if __name__ == "__main__":
    main()
