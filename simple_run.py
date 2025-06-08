#!/usr/bin/env python3
"""
Ecommerce Flask Runner - Simplified Version
No external dependencies beyond Flask
"""

from flask import Flask, send_from_directory, jsonify
import webbrowser
import os
import sys
import threading
import time
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, 
            template_folder='html',
            static_folder='.',
            static_url_path='')

# Manual CORS headers (no external dependency needed)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Configuration
HOST = 'localhost'
PORT = 5000

# Routes
@app.route('/')
def index():
    return send_from_directory('html', 'index.html')

@app.route('/dashboard')
@app.route('/html/index.html')
def dashboard():
    return send_from_directory('html', 'index.html')

@app.route('/purchase-order')
@app.route('/html/PurchaseOrder.html')
def purchase_order():
    return send_from_directory('html', 'PurchaseOrder.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0'
    })

# Static file serving
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename, mimetype='text/css')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename, mimetype='application/javascript')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

def open_browser():
    time.sleep(1.5)
    try:
        webbrowser.open(f'http://{HOST}:{PORT}/dashboard')
        print(f"🌐 Browser opened: http://{HOST}:{PORT}/dashboard")
    except:
        pass

def main():
    print("🚀 Ecommerce Flask Server")
    print("=" * 40)
    print(f"📱 Dashboard: http://{HOST}:{PORT}/dashboard")
    print(f"🛒 Purchase Order: http://{HOST}:{PORT}/purchase-order")
    print(f"🔧 API Status: http://{HOST}:{PORT}/api/status")
    print("=" * 40)
    print("✅ Features: CORS enabled, Auto-reload, Static files")
    print("💡 Press Ctrl+C to stop")
    print()
    
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")
        if "Address already in use" in str(e):
            print(f"💡 Port {PORT} is busy. Try: lsof -ti:{PORT} | xargs kill -9")

if __name__ == "__main__":
    main()
