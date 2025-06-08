#!/usr/bin/env python3
"""
Flask Development Server Runner
Easy script to run the Flask Ecommerce application with auto-reload and debug mode.
"""

import subprocess
import sys
import os
import webbrowser
import time
import threading

def check_flask_installed():
    """Check if Flask is installed"""
    try:
        import flask
        print(f"✅ Flask {flask.__version__} is installed")
        return True
    except ImportError:
        print("❌ Flask is not installed")
        return False

def install_requirements():
    """Install requirements from requirements.txt"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def open_browser(url, delay=3):
    """Open browser after a short delay"""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    """Main function to run the Flask development server"""
    
    print("🚀 Flask Ecommerce Development Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Make sure you're in the Ecommerce directory")
        sys.exit(1)
    
    print(f"📁 Project Directory: {os.getcwd()}")
    
    # Check if Flask is installed
    if not check_flask_installed():
        print("\n💡 Installing Flask and dependencies...")
        if not install_requirements():
            print("❌ Failed to install Flask. Please run manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    
    # Configuration
    server_url = "http://localhost:5000"
    dashboard_url = f"{server_url}/dashboard"
    
    print(f"\n🌐 Server URLs:")
    print(f"   • Main: {server_url}")
    print(f"   • Dashboard: {dashboard_url}")
    print(f"   • Purchase Order: {server_url}/purchase-order")
    print(f"   • API Products: {server_url}/api/products")
    print(f"   • API Orders: {server_url}/api/orders")
    print(f"   • Health Check: {server_url}/health")
    
    print("\n💡 Features:")
    print("   • Auto-reload on file changes")
    print("   • Debug mode enabled")
    print("   • API endpoints for data")
    print("   • Error handling")
    print("   • Static file serving")
    
    print("\n🛠 Controls:")
    print("   • Press Ctrl+C to stop")
    print("   • Edit files and they'll auto-reload")
    print("   • Check terminal for errors")
    
    # Open browser in a separate thread
    print(f"\n🌐 Opening browser to {dashboard_url}...")
    browser_thread = threading.Thread(target=open_browser, args=(dashboard_url,))
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n" + "=" * 50)
    print("🚀 Starting Flask server...")
    print("=" * 50)
    
    try:
        # Run Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error running Flask app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
