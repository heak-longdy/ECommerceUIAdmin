#!/usr/bin/env python3
"""
Simple Ecommerce Project Runner
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import time
import threading

def main():
    PORT = 8000
    HOST = 'localhost'
    
    print("🚀 Starting Ecommerce Development Server")
    print(f"📁 Directory: {os.getcwd()}")
    print(f"🌐 Server: http://{HOST}:{PORT}")
    print(f"📱 Main Page: http://{HOST}:{PORT}/html/index.html")
    print("Press Ctrl+C to stop")
    print("-" * 40)
    
    try:
        # Create and start server
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((HOST, PORT), handler) as httpd:
            print(f"✅ Server running on port {PORT}")
            
            # Open browser after 2 seconds
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://{HOST}:{PORT}/html/index.html")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try: lsof -ti:8000 | xargs kill -9")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
