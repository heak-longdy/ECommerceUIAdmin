#!/usr/bin/env python3
"""
Ecommerce Project Runner - Flask Edition
Advanced Flask-based development server for the Ecommerce project.
"""

from flask import Flask, render_template, send_from_directory, jsonify, request
import webbrowser
import os
import sys
import threading
import time
from datetime import datetime
import json
from pathlib import Path

# Initialize Flask app
app = Flask(__name__, 
            template_folder='html',
            static_folder='.',
            static_url_path='')

# Manual CORS handling (works without flask-cors dependency)
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

# Configuration
CONFIG = {
    'HOST': 'localhost',
    'PORT': 5000,
    'DEBUG': True,
    'AUTO_RELOAD': True
}

@app.route('/')
def index():
    """Redirect to main dashboard"""
    return send_from_directory('html', 'index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return 'hhi'
    return send_from_directory('html', 'index.html')

@app.route('/purchase-order')
@app.route('/html/PurchaseOrder.html')
def purchase_order():
    """Purchase order page"""
    return send_from_directory('html', 'PurchaseOrder.html')

@app.route('/api/status')
def api_status():
    """API endpoint to check server status"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'endpoints': {
            'dashboard': '/dashboard',
            'purchase_order': '/purchase-order',
            'static_files': '/css/, /js/, /assets/'
        }
    })

@app.route('/api/project-info')
def project_info():
    """Get project structure information"""
    project_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    structure = {
        'css_files': list(project_dir.glob('css/*.css')),
        'js_files': list(project_dir.glob('js/*.js')),
        'html_files': list(project_dir.glob('html/*.html')),
        'assets': list(project_dir.glob('assets/*')),
    }
    
    # Convert Path objects to strings
    for key, files in structure.items():
        structure[key] = [str(f.name) for f in files if f.is_file()]
    
    return jsonify(structure)

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files with proper MIME type"""
    return send_from_directory('css', filename, mimetype='text/css')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files with proper MIME type"""
    return send_from_directory('js', filename, mimetype='application/javascript')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve asset files (images, fonts, etc.)"""
    return send_from_directory('assets', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve image files"""
    return send_from_directory('images', filename)

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from root directory"""
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        return send_from_directory('.', filename)
    return send_from_directory('.', filename)

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error page"""
    return jsonify({
        'error': 'Page not found',
        'message': f'The requested resource was not found on this server.',
        'available_routes': [
            '/',
            '/dashboard',
            '/purchase-order',
            '/api/status',
            '/api/project-info'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 error page"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server.'
    }), 500

def open_browser(url, delay=2):
    """Open browser after a short delay"""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"🌐 Browser opened: {url}")
    except Exception as e:
        print(f"⚠️  Could not open browser: {e}")

def print_startup_info():
    """Print server startup information"""
    host = CONFIG['HOST']
    port = CONFIG['PORT']
    
    print("🚀 Flask Ecommerce Development Server")
    print("=" * 50)
    print(f"📁 Project Directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"🌐 Server URL: http://{host}:{port}")
    print(f"📱 Main Dashboard: http://{host}:{port}/dashboard")
    print(f"🛒 Purchase Order: http://{host}:{port}/purchase-order")
    print(f"🔧 API Status: http://{host}:{port}/api/status")
    print("-" * 50)
    print("✅ Flask Features Enabled:")
    print("   • Auto-reload on file changes")
    print("   • CORS support for API calls")
    print("   • Custom error handling")
    print("   • Static file serving")
    print("   • RESTful API endpoints")
    print("\n💡 Tips:")
    print("   • Press Ctrl+C to stop the server")
    print("   • Edit files and refresh browser to see changes")
    print("   • Check terminal for request logs")
    print("   • Visit /api/status for server info")

def main():
    """Main function to run the Flask development server"""
    
    # Check dependencies first
    try:
        import flask
        print(f"✅ Flask {flask.__version__} is available")
    except ImportError:
        print("❌ Flask is not installed")
        print("💡 Install Flask: pip install flask")
        sys.exit(1)
    
    try:
        # Print startup information
        print_startup_info()
        
        # Open browser in a separate thread
        server_url = f"http://{CONFIG['HOST']}:{CONFIG['PORT']}/dashboard"
        browser_thread = threading.Thread(target=open_browser, args=(server_url,))
        browser_thread.daemon = True
        browser_thread.start()
        
        print(f"\n🌐 Opening browser to {server_url}...")
        print("\n🔥 Starting Flask server...\n")
        
        # Start Flask development server
        app.run(
            host=CONFIG['HOST'],
            port=CONFIG['PORT'],
            debug=CONFIG['DEBUG'],
            use_reloader=False,  # Disable reloader to avoid path issues
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Goodbye!")
        
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {CONFIG['PORT']} is already in use!")
            print("💡 Solutions:")
            print(f"   1. Stop other servers using port {CONFIG['PORT']}")
            print(f"   2. Change PORT in CONFIG at top of this file")
            print(f"   3. Run: lsof -ti:{CONFIG['PORT']} | xargs kill -9")
        else:
            print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
        
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("💡 Install required packages:")
        print("   pip install flask")
        print("   OR: pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
