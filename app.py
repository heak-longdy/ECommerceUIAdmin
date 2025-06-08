#!/usr/bin/env python3
"""
Flask Ecommerce Application
A comprehensive Flask web server for the Ecommerce project with modular Jinja2 templates,
RESTful API endpoints, and advanced features.
"""

from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, flash, session, abort
import os
import json
from datetime import datetime, timedelta
import logging
from functools import wraps
import uuid
import random
from typing import Dict, List, Optional, Any
import time

# Initialize Flask app with proper template structure
app = Flask(__name__, 
           template_folder='templates',
           static_folder='.',
           static_url_path='')

# Enhanced Configuration
app.config.update({
    'DEBUG': True,
    'SECRET_KEY': 'ecommerce-secret-key-2025',
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file upload
    'TEMPLATES_AUTO_RELOAD': True
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enhanced sample data with more realistic information
SAMPLE_PRODUCTS = [
    {
        "id": 1, 
        "name": "MacBook Pro 14-inch", 
        "price": 1999.99, 
        "category": "Electronics", 
        "stock": 15,
        "description": "Apple M2 Pro chip, 16GB RAM, 512GB SSD",
        "image": "macbook-pro.jpg",
        "rating": 4.8,
        "reviews": 1247
    },
    {
        "id": 2, 
        "name": "iPhone 15 Pro", 
        "price": 999.99, 
        "category": "Electronics", 
        "stock": 25,
        "description": "6.1-inch display, A17 Pro chip, 256GB storage",
        "image": "iphone-15-pro.jpg",
        "rating": 4.7,
        "reviews": 2156
    },
    {
        "id": 3, 
        "name": "AirPods Pro (2nd Gen)", 
        "price": 249.99, 
        "category": "Audio", 
        "stock": 50,
        "description": "Active Noise Cancellation, Spatial Audio",
        "image": "airpods-pro.jpg",
        "rating": 4.6,
        "reviews": 892
    },
    {
        "id": 4, 
        "name": "iPad Pro 11-inch", 
        "price": 799.99, 
        "category": "Electronics", 
        "stock": 12,
        "description": "M2 chip, 11-inch Liquid Retina display, 128GB",
        "image": "ipad-pro.jpg",
        "rating": 4.9,
        "reviews": 654
    },
    {
        "id": 5, 
        "name": "Apple Watch Series 9", 
        "price": 399.99, 
        "category": "Wearables", 
        "stock": 30,
        "description": "45mm GPS, Always-On Retina display",
        "image": "apple-watch.jpg",
        "rating": 4.5,
        "reviews": 1034
    }
]

SAMPLE_ORDERS = [
    {
        "id": "ORD-001", 
        "customer": "John Doe", 
        "email": "john.doe@example.com",
        "total": 2249.98, 
        "status": "Shipped", 
        "date": "2025-06-01",
        "items": [
            {"product_id": 1, "quantity": 1, "price": 1999.99},
            {"product_id": 3, "quantity": 1, "price": 249.99}
        ],
        "shipping_address": "123 Main St, New York, NY 10001"
    },
    {
        "id": "ORD-002", 
        "customer": "Jane Smith", 
        "email": "jane.smith@example.com",
        "total": 1249.98, 
        "status": "Processing", 
        "date": "2025-06-05",
        "items": [
            {"product_id": 2, "quantity": 1, "price": 999.99},
            {"product_id": 3, "quantity": 1, "price": 249.99}
        ],
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90210"
    },
    {
        "id": "ORD-003", 
        "customer": "Bob Johnson", 
        "email": "bob.johnson@example.com",
        "total": 1199.98, 
        "status": "Delivered", 
        "date": "2025-06-03",
        "items": [
            {"product_id": 4, "quantity": 1, "price": 799.99},
            {"product_id": 5, "quantity": 1, "price": 399.99}
        ],
        "shipping_address": "789 Pine St, Chicago, IL 60601"
    }
]

# Purchase Order sample data
SAMPLE_PURCHASE_ORDERS = [
    {
        'id': 'PO-001',
        'vendor': 'Apple Inc.',
        'total': '15,299.99',
        'status': 'Pending',
        'date': '2025-06-05',
        'items_count': 8,
        'expected_delivery': '2025-06-15'
    },
    {
        'id': 'PO-002', 
        'vendor': 'Samsung Electronics',
        'total': '8,999.50',
        'status': 'Approved',
        'date': '2025-06-04',
        'items_count': 12,
        'expected_delivery': '2025-06-12'
    },
    {
        'id': 'PO-003',
        'vendor': 'Sony Corporation',
        'total': '4,299.00',
        'status': 'Delivered',
        'date': '2025-06-02',
        'items_count': 6,
        'expected_delivery': '2025-06-08'
    }
]

# System metrics for dashboard
SYSTEM_METRICS = {
    'hosting': {
        'downloads_7d': '2.8GB',
        'status': 'Active',
        'uptime': '99.9%',
        'deployed_by': 'longdyheak9999@gmail.com',
        'last_deployment': '2025-06-06 14:30:00'
    },
    'firestore': {
        'reads_current': 1247,
        'writes_current': 856,
        'active_connections': 12,
        'storage_used': '145MB',
        'queries_per_minute': 23
    },
    'authentication': {
        'active_users': 89,
        'signins_today': 234,
        'new_registrations': 5,
        'failed_attempts': 2
    }
}

# Utility decorators and functions
def api_key_required(f):
    """Decorator for API endpoints that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != 'ecommerce-api-key-2025':
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_dashboard_data():
    """Generate dynamic dashboard data"""
    total_revenue = sum(order["total"] for order in SAMPLE_ORDERS)
    total_orders = len(SAMPLE_ORDERS)
    total_products = len(SAMPLE_PRODUCTS)
    
    return {
        'total_revenue': f"${total_revenue:,.2f}",
        'total_orders': total_orders,
        'total_products': total_products,
        'avg_order_value': f"${total_revenue/total_orders:,.2f}" if total_orders > 0 else "$0.00",
        'low_stock_items': len([p for p in SAMPLE_PRODUCTS if p['stock'] < 20])
    }

def get_build_cards():
    """Generate build cards data for dashboard"""
    metrics = SYSTEM_METRICS
    
    return [
        {
            'title': 'Hosting',
            'stat': metrics['hosting']['downloads_7d'],
            'descriptions': [
                f'Downloads (7d total)',
                f'Status: <b>{metrics["hosting"]["status"]}</b>',
                f'Uptime: <b>{metrics["hosting"]["uptime"]}</b>',
                f'Deployed by: {metrics["hosting"]["deployed_by"]}'
            ]
        },
        {
            'title': 'Firestore Database',
            'stat': f'{metrics["firestore"]["reads_current"]:,}',
            'descriptions': [
                f'Reads (current)',
                f'Writes: <b>{metrics["firestore"]["writes_current"]:,}</b>',
                f'Active connections: <b>{metrics["firestore"]["active_connections"]}</b>',
                f'Storage used: <b>{metrics["firestore"]["storage_used"]}</b>'
            ]
        },
        {
            'title': 'Authentication',
            'stat': str(metrics['authentication']['active_users']),
            'descriptions': [
                'Active users (current)',
                f'Sign-ins today: <b>{metrics["authentication"]["signins_today"]}</b>',
                f'New registrations: <b>{metrics["authentication"]["new_registrations"]}</b>',
                f'Failed attempts: <b>{metrics["authentication"]["failed_attempts"]}</b>'
            ]
        }
    ]

# Template context processors
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'current_year': datetime.now().year,
        'app_version': '2.0.0',
        'environment': 'development' if app.debug else 'production'
    }

# Enhanced Session Management and Middleware
def init_session():
    """Initialize user session with default values"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['session_start'] = datetime.now().isoformat()
        session['page_views'] = 0
        session['cart'] = []
        session['preferences'] = {
            'theme': 'light',
            'currency': 'USD',
            'language': 'en'
        }

def track_page_view():
    """Track user page views for analytics"""
    init_session()
    session['page_views'] = session.get('page_views', 0) + 1
    session['last_activity'] = datetime.now().isoformat()

@app.before_request
def before_request():
    """Enhanced request preprocessing"""
    # Initialize session
    init_session()
    
    # Track request start time for performance monitoring
    request.start_time = time.time()
    
    # Log request details
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    # Security headers
    if request.endpoint and not request.endpoint.startswith('static'):
        track_page_view()

@app.after_request
def after_request(response):
    """Enhanced response post-processing with security headers and performance tracking"""
    # Calculate request duration
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        response.headers['X-Response-Time'] = f"{duration:.3f}s"
    
    # Enhanced Security Headers
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: https:",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        'X-Powered-By': 'Flask-Ecommerce-2.0'
    })
    
    # CORS headers for API endpoints
    if request.path.startswith('/api/'):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key'
        })
    
    return response

# Enhanced Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Enhanced 404 error handler with template"""
    return render_template('index.html',
                         active_page='error',
                         project_name='Page Not Found',
                         plan_type='Pro Plan',
                         error_message="The requested page could not be found.",
                         error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    """Enhanced 500 error handler with logging"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('index.html',
                         active_page='error',
                         project_name='Server Error',
                         plan_type='Pro Plan',
                         error_message="An internal server error occurred.",
                         error_code=500), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Enhanced 403 error handler"""
    return render_template('index.html',
                         active_page='error',
                         project_name='Access Denied',
                         plan_type='Pro Plan',
                         error_message="Access to this resource is forbidden.",
                         error_code=403), 403

# Cart Management Functions
def get_cart_items():
    """Get current user's cart items"""
    cart_ids = session.get('cart', [])
    cart_items = []
    for item_id in cart_ids:
        product = next((p for p in SAMPLE_PRODUCTS if p['id'] == item_id), None)
        if product:
            cart_items.append(product)
    return cart_items

def calculate_cart_total():
    """Calculate total price of items in cart"""
    cart_items = get_cart_items()
    return sum(item['price'] for item in cart_items)

# Template context processors
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'current_year': datetime.now().year,
        'app_version': '2.0.0',
        'environment': 'development' if app.debug else 'production'
    }

# Enhanced Configuration
app.config.update({
    'DEBUG': True,
    'SECRET_KEY': 'ecommerce-secret-key-2025',
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file upload
    'TEMPLATES_AUTO_RELOAD': True
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enhanced sample data with more realistic information
SAMPLE_PRODUCTS = [
    {
        "id": 1, 
        "name": "MacBook Pro 14-inch", 
        "price": 1999.99, 
        "category": "Electronics", 
        "stock": 15,
        "description": "Apple M2 Pro chip, 16GB RAM, 512GB SSD",
        "image": "macbook-pro.jpg",
        "rating": 4.8,
        "reviews": 1247
    },
    {
        "id": 2, 
        "name": "iPhone 15 Pro", 
        "price": 999.99, 
        "category": "Electronics", 
        "stock": 25,
        "description": "6.1-inch display, A17 Pro chip, 256GB storage",
        "image": "iphone-15-pro.jpg",
        "rating": 4.7,
        "reviews": 2156
    },
    {
        "id": 3, 
        "name": "AirPods Pro (2nd Gen)", 
        "price": 249.99, 
        "category": "Audio", 
        "stock": 50,
        "description": "Active Noise Cancellation, Spatial Audio",
        "image": "airpods-pro.jpg",
        "rating": 4.6,
        "reviews": 892
    },
    {
        "id": 4, 
        "name": "iPad Pro 11-inch", 
        "price": 799.99, 
        "category": "Electronics", 
        "stock": 12,
        "description": "M2 chip, 11-inch Liquid Retina display, 128GB",
        "image": "ipad-pro.jpg",
        "rating": 4.9,
        "reviews": 654
    },
    {
        "id": 5, 
        "name": "Apple Watch Series 9", 
        "price": 399.99, 
        "category": "Wearables", 
        "stock": 30,
        "description": "45mm GPS, Always-On Retina display",
        "image": "apple-watch.jpg",
        "rating": 4.5,
        "reviews": 1034
    }
]

SAMPLE_ORDERS = [
    {
        "id": "ORD-001", 
        "customer": "John Doe", 
        "email": "john.doe@example.com",
        "total": 2249.98, 
        "status": "Shipped", 
        "date": "2025-06-01",
        "items": [
            {"product_id": 1, "quantity": 1, "price": 1999.99},
            {"product_id": 3, "quantity": 1, "price": 249.99}
        ],
        "shipping_address": "123 Main St, New York, NY 10001"
    },
    {
        "id": "ORD-002", 
        "customer": "Jane Smith", 
        "email": "jane.smith@example.com",
        "total": 1249.98, 
        "status": "Processing", 
        "date": "2025-06-05",
        "items": [
            {"product_id": 2, "quantity": 1, "price": 999.99},
            {"product_id": 3, "quantity": 1, "price": 249.99}
        ],
        "shipping_address": "456 Oak Ave, Los Angeles, CA 90210"
    },
    {
        "id": "ORD-003", 
        "customer": "Bob Johnson", 
        "email": "bob.johnson@example.com",
        "total": 1199.98, 
        "status": "Delivered", 
        "date": "2025-06-03",
        "items": [
            {"product_id": 4, "quantity": 1, "price": 799.99},
            {"product_id": 5, "quantity": 1, "price": 399.99}
        ],
        "shipping_address": "789 Pine St, Chicago, IL 60601"
    }
]

# Purchase Order sample data
SAMPLE_PURCHASE_ORDERS = [
    {
        'id': 'PO-001',
        'vendor': 'Apple Inc.',
        'total': '15,299.99',
        'status': 'Pending',
        'date': '2025-06-05',
        'items_count': 8,
        'expected_delivery': '2025-06-15'
    },
    {
        'id': 'PO-002', 
        'vendor': 'Samsung Electronics',
        'total': '8,999.50',
        'status': 'Approved',
        'date': '2025-06-04',
        'items_count': 12,
        'expected_delivery': '2025-06-12'
    },
    {
        'id': 'PO-003',
        'vendor': 'Sony Corporation',
        'total': '4,299.00',
        'status': 'Delivered',
        'date': '2025-06-02',
        'items_count': 6,
        'expected_delivery': '2025-06-08'
    }
]

# System metrics for dashboard
SYSTEM_METRICS = {
    'hosting': {
        'downloads_7d': '2.8GB',
        'status': 'Active',
        'uptime': '99.9%',
        'deployed_by': 'longdyheak9999@gmail.com',
        'last_deployment': '2025-06-06 14:30:00'
    },
    'firestore': {
        'reads_current': 1247,
        'writes_current': 856,
        'active_connections': 12,
        'storage_used': '145MB',
        'queries_per_minute': 23
    },
    'authentication': {
        'active_users': 89,
        'signins_today': 234,
        'new_registrations': 5,
        'failed_attempts': 2
    }
}

# Utility decorators and functions
def api_key_required(f):
    """Decorator for API endpoints that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != 'ecommerce-api-key-2025':
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_dashboard_data():
    """Generate dynamic dashboard data"""
    total_revenue = sum(order["total"] for order in SAMPLE_ORDERS)
    total_orders = len(SAMPLE_ORDERS)
    total_products = len(SAMPLE_PRODUCTS)
    
    return {
        'total_revenue': f"${total_revenue:,.2f}",
        'total_orders': total_orders,
        'total_products': total_products,
        'avg_order_value': f"${total_revenue/total_orders:,.2f}" if total_orders > 0 else "$0.00",
        'low_stock_items': len([p for p in SAMPLE_PRODUCTS if p['stock'] < 20])
    }

def get_build_cards():
    """Generate build cards data for dashboard"""
    metrics = SYSTEM_METRICS
    
    return [
        {
            'title': 'Hosting',
            'stat': metrics['hosting']['downloads_7d'],
            'descriptions': [
                f'Downloads (7d total)',
                f'Status: <b>{metrics["hosting"]["status"]}</b>',
                f'Uptime: <b>{metrics["hosting"]["uptime"]}</b>',
                f'Deployed by: {metrics["hosting"]["deployed_by"]}'
            ]
        },
        {
            'title': 'Firestore Database',
            'stat': f'{metrics["firestore"]["reads_current"]:,}',
            'descriptions': [
                f'Reads (current)',
                f'Writes: <b>{metrics["firestore"]["writes_current"]:,}</b>',
                f'Active connections: <b>{metrics["firestore"]["active_connections"]}</b>',
                f'Storage used: <b>{metrics["firestore"]["storage_used"]}</b>'
            ]
        },
        {
            'title': 'Authentication',
            'stat': str(metrics['authentication']['active_users']),
            'descriptions': [
                'Active users (current)',
                f'Sign-ins today: <b>{metrics["authentication"]["signins_today"]}</b>',
                f'New registrations: <b>{metrics["authentication"]["new_registrations"]}</b>',
                f'Failed attempts: <b>{metrics["authentication"]["failed_attempts"]}</b>'
            ]
        }
    ]

# Template context processors
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'current_year': datetime.now().year,
        'app_version': '2.0.0',
        'environment': 'development' if app.debug else 'production'
    }

# Enhanced Session Management and Middleware
def init_session():
    """Initialize user session with default values"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['session_start'] = datetime.now().isoformat()
        session['page_views'] = 0
        session['cart'] = []
        session['preferences'] = {
            'theme': 'light',
            'currency': 'USD',
            'language': 'en'
        }

def track_page_view():
    """Track user page views for analytics"""
    init_session()
    session['page_views'] = session.get('page_views', 0) + 1
    session['last_activity'] = datetime.now().isoformat()

@app.before_request
def before_request():
    """Enhanced request preprocessing"""
    # Initialize session
    init_session()
    
    # Track request start time for performance monitoring
    request.start_time = time.time()
    
    # Log request details
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    # Security headers
    if request.endpoint and not request.endpoint.startswith('static'):
        track_page_view()

@app.after_request
def after_request(response):
    """Enhanced response post-processing with security headers and performance tracking"""
    # Calculate request duration
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        response.headers['X-Response-Time'] = f"{duration:.3f}s"
    
    # Enhanced Security Headers
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: https:",
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        'X-Powered-By': 'Flask-Ecommerce-2.0'
    })
    
    # CORS headers for API endpoints
    if request.path.startswith('/api/'):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-API-Key'
        })
    
    return response

# Enhanced Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Enhanced 404 error handler with template"""
    return render_template('index.html',
                         active_page='error',
                         project_name='Page Not Found',
                         plan_type='Pro Plan',
                         error_message="The requested page could not be found.",
                         error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    """Enhanced 500 error handler with logging"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('index.html',
                         active_page='error',
                         project_name='Server Error',
                         plan_type='Pro Plan',
                         error_message="An internal server error occurred.",
                         error_code=500), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Enhanced 403 error handler"""
    return render_template('index.html',
                         active_page='error',
                         project_name='Access Denied',
                         plan_type='Pro Plan',
                         error_message="Access to this resource is forbidden.",
                         error_code=403), 403

# Cart Management Functions
def get_cart_items():
    """Get current user's cart items"""
    cart_ids = session.get('cart', [])
    cart_items = []
    for item_id in cart_ids:
        product = next((p for p in SAMPLE_PRODUCTS if p['id'] == item_id), None)
        if product:
            cart_items.append(product)
    return cart_items

def calculate_cart_total():
    """Calculate total price of items in cart"""
    cart_items = get_cart_items()
    return sum(item['price'] for item in cart_items)

# Cart and Session API Routes
@app.route('/api/cart')
def api_get_cart():
    """Get current user's cart"""
    try:
        cart_items = get_cart_items()
        total = calculate_cart_total()
        return jsonify({
            'success': True,
            'cart': cart_items,
            'total': total,
            'count': len(cart_items),
            'session_id': session.get('user_id')
        })
    except Exception as e:
        logger.error(f"Cart retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve cart'}), 500

@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        
        # Check if product exists
        product = next((p for p in SAMPLE_PRODUCTS if p['id'] == product_id), None)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Add to cart
        cart = session.get('cart', [])
        if product_id not in cart:
            cart.append(product_id)
            session['cart'] = cart
            
            return jsonify({
                'success': True,
                'message': f'{product["name"]} added to cart',
                'cart_count': len(cart)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Product already in cart'
            }), 409
            
    except Exception as e:
        logger.error(f"Add to cart error: {str(e)}")
        return jsonify({'error': 'Failed to add item to cart'}), 500

@app.route('/api/cart/remove', methods=['POST'])
def api_remove_from_cart():
    """Remove item from cart"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400
        
        cart = session.get('cart', [])
        if product_id in cart:
            cart.remove(product_id)
            session['cart'] = cart
            
            return jsonify({
                'success': True,
                'message': 'Item removed from cart',
                'cart_count': len(cart)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Item not found in cart'
            }), 404
            
    except Exception as e:
        logger.error(f"Remove from cart error: {str(e)}")
        return jsonify({'error': 'Failed to remove item from cart'}), 500

@app.route('/api/cart/clear', methods=['POST'])
def api_clear_cart():
    """Clear all items from cart"""
    try:
        session['cart'] = []
        return jsonify({
            'success': True,
            'message': 'Cart cleared successfully'
        })
    except Exception as e:
        logger.error(f"Clear cart error: {str(e)}")
        return jsonify({'error': 'Failed to clear cart'}), 500

@app.route('/api/session')
def api_session_info():
    """Get current session information"""
    try:
        return jsonify({
            'success': True,
            'session': {
                'user_id': session.get('user_id'),
                'session_start': session.get('session_start'),
                'page_views': session.get('page_views', 0),
                'last_activity': session.get('last_activity'),
                'cart_count': len(session.get('cart', [])),
                'preferences': session.get('preferences', {})
            }
        })
    except Exception as e:
        logger.error(f"Session info error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve session info'}), 500

# Main Page Routes
@app.route('/')
def home():
    """Main dashboard - redirect to dashboard"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Enhanced dashboard page with real-time data and cart info"""
    try:
        dashboard_data = get_dashboard_data()
        build_cards = get_build_cards()
        cart_items = get_cart_items()
        cart_total = calculate_cart_total()
        
        return render_template('index.html',
                             active_page='overview',
                             project_name='Ecommerce Dashboard',
                             plan_type='Pro Plan',
                             expanded_sections=['ai'],
                             build_cards=build_cards,
                             dashboard_data=dashboard_data,
                             cart_items=cart_items,
                             cart_total=cart_total,
                             cart_count=len(cart_items),
                             user_email='longdyheak9999@gmail.com')
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return render_template('index.html',
                             active_page='overview',
                             error_message="Failed to load dashboard data")

@app.route('/purchase-order')
def purchase_order():
    """Enhanced purchase order page with detailed data"""
    try:
        return render_template('PurchaseOrder.html',
                             active_page='purchase-order',
                             project_name='Purchase Orders',
                             plan_type='Pro Plan',
                             expanded_sections=['build'],
                             recent_orders=SAMPLE_PURCHASE_ORDERS,
                             cart_count=len(session.get('cart', [])))
    except Exception as e:
        logger.error(f"Purchase order page error: {str(e)}")
        return render_template('PurchaseOrder.html',
                             active_page='purchase-order',
                             error_message="Failed to load purchase orders")

@app.route('/products')
def products_page():
    """Products listing page with cart integration"""
    try:
        cart_items = get_cart_items()
        return render_template('index.html',
                             active_page='products',
                             project_name='Product Catalog',
                             plan_type='Pro Plan',
                             expanded_sections=['build'],
                             products=SAMPLE_PRODUCTS,
                             cart_items=cart_items,
                             cart_count=len(cart_items))
    except Exception as e:
        logger.error(f"Products page error: {str(e)}")
        return render_template('index.html',
                             active_page='products',
                             error_message="Failed to load products")

@app.route('/orders')
def orders_page():
    """Orders management page with enhanced order details"""
    return render_template('order/index.html',
                         active_page='orders',
                         project_name='Order Management',
                         plan_type='Pro Plan',
                         expanded_sections=['build'],
                         recent_orders=SAMPLE_ORDERS,
                         cart_count=len(session.get('cart', [])))
@app.route('/orders/Create')
def orders_create():
    """Orders management page with enhanced order details"""
    return render_template('order/create.html',
                         active_page='orders',
                         project_name='Order Management',
                         plan_type='Pro Plan',
                         expanded_sections=['build'],
                         recent_orders=SAMPLE_ORDERS,
                         cart_count=len(session.get('cart', [])))
@app.route('/analytics')
def analytics():
    """Analytics dashboard page with enhanced metrics"""
    try:
        # Generate analytics data
        analytics_data = {
            'revenue_trend': [1200, 1350, 1450, 1600, 1750, 1900, 2100],
            'order_trend': [15, 18, 22, 25, 28, 32, 35],
            'top_products': SAMPLE_PRODUCTS[:3],
            'conversion_rate': 3.2,
            'cart_abandonment_rate': 12.5,
            'avg_session_duration': '4:32'
        }
        
        return render_template('index.html',
                             active_page='analytics',
                             project_name='Analytics Dashboard',
                             plan_type='Pro Plan',
                             expanded_sections=['analytics'],
                             analytics_data=analytics_data,
                             cart_count=len(session.get('cart', [])))
    except Exception as e:
        logger.error(f"Analytics page error: {str(e)}")
        return render_template('index.html',
                             active_page='analytics',
                             error_message="Failed to load analytics")

@app.route('/search')
def search_page():
    """Search results page"""
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        
        results = []
        if query:
            # Simple search in product names and descriptions
            results = [p for p in SAMPLE_PRODUCTS 
                      if query.lower() in p['name'].lower() 
                      or query.lower() in p['description'].lower()]
        
        if category:
            results = [p for p in results if p['category'].lower() == category.lower()]
        
        return render_template('index.html',
                             active_page='search',
                             project_name=f'Search Results for "{query}"',
                             plan_type='Pro Plan',
                             search_query=query,
                             search_category=category,
                             search_results=results,
                             results_count=len(results),
                             cart_count=len(session.get('cart', [])))
    except Exception as e:
        logger.error(f"Search page error: {str(e)}")
        return render_template('index.html',
                             active_page='search',
                             error_message="Search failed")

# Enhanced API Routes with better error handling and validation
@app.route('/api/search')
def api_search():
    """Search products API with advanced filtering"""
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_rating = request.args.get('min_rating', type=float)
        sort_by = request.args.get('sort_by', 'name')  # name, price, rating
        sort_order = request.args.get('sort_order', 'asc')  # asc, desc
        
        results = SAMPLE_PRODUCTS.copy()
        
        # Apply text search filter
        if query:
            results = [p for p in results 
                      if query.lower() in p['name'].lower() 
                      or query.lower() in p['description'].lower()
                      or query.lower() in p['category'].lower()]
        
        # Apply category filter
        if category:
            results = [p for p in results if p['category'].lower() == category.lower()]
        
        # Apply price filters
        if min_price is not None:
            results = [p for p in results if p['price'] >= min_price]
        if max_price is not None:
            results = [p for p in results if p['price'] <= max_price]
        
        # Apply rating filter
        if min_rating is not None:
            results = [p for p in results if p['rating'] >= min_rating]
        
        # Apply sorting
        reverse = sort_order == 'desc'
        if sort_by == 'price':
            results.sort(key=lambda x: x['price'], reverse=reverse)
        elif sort_by == 'rating':
            results.sort(key=lambda x: x['rating'], reverse=reverse)
        elif sort_by == 'name':
            results.sort(key=lambda x: x['name'], reverse=reverse)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'query': query,
            'filters': {
                'category': category,
                'min_price': min_price,
                'max_price': max_price,
                'min_rating': min_rating
            },
            'sort': {
                'by': sort_by,
                'order': sort_order
            }
        })
        
    except Exception as e:
        logger.error(f"Search API error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/products')
def api_products():
    """Get all products with filtering and pagination"""
    try:
        # Get query parameters
        category = request.args.get('category', '').strip()
        search = request.args.get('search', '').strip().lower()
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 100)  # Max 100 items per page
        
        # Filter products
        filtered_products = SAMPLE_PRODUCTS
        
        if category:
            filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
        
        if search:
            filtered_products = [p for p in filtered_products 
                               if search in p['name'].lower() or search in p['description'].lower()]
        
        # Pagination
        start = (page - 1) * per_page
        end = start + per_page
        paginated_products = filtered_products[start:end]
        
        return jsonify({
            "success": True,
            "data": paginated_products,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(filtered_products),
                "pages": (len(filtered_products) + per_page - 1) // per_page
            },
            "filters": {
                "category": category,
                "search": search
            }
        })
    except ValueError as e:
        return jsonify({"success": False, "error": "Invalid pagination parameters"}), 400
    except Exception as e:
        logger.error(f"Products API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/products/<int:product_id>')
def api_product_detail(product_id):
    """Get specific product details with enhanced information"""
    try:
        product = next((p for p in SAMPLE_PRODUCTS if p["id"] == product_id), None)
        if product:
            # Add additional product details
            enhanced_product = product.copy()
            enhanced_product['availability'] = 'In Stock' if product['stock'] > 0 else 'Out of Stock'
            enhanced_product['stock_level'] = 'Low' if product['stock'] < 10 else 'Good'
            enhanced_product['last_updated'] = datetime.now().isoformat()
            
            return jsonify({"success": True, "data": enhanced_product})
        return jsonify({"success": False, "error": "Product not found"}), 404
    except Exception as e:
        logger.error(f"Product detail API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/orders')
def api_orders():
    """Get all orders with filtering"""
    try:
        status = request.args.get('status', '').strip()
        customer = request.args.get('customer', '').strip().lower()
        
        filtered_orders = SAMPLE_ORDERS
        
        if status:
            filtered_orders = [o for o in filtered_orders if o['status'].lower() == status.lower()]
        
        if customer:
            filtered_orders = [o for o in filtered_orders if customer in o['customer'].lower()]
        
        return jsonify({
            "success": True,
            "data": filtered_orders,
            "count": len(filtered_orders),
            "filters": {
                "status": status,
                "customer": customer
            }
        })
    except Exception as e:
        logger.error(f"Orders API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """Create a new order with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['customer', 'email', 'total', 'items']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({"success": False, "error": "Invalid email format"}), 400
        
        # Create new order
        new_order = {
            "id": f"ORD-{len(SAMPLE_ORDERS) + 1:03d}",
            "customer": data['customer'],
            "email": data['email'],
            "total": float(data['total']),
            "status": "Processing",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "items": data['items'],
            "shipping_address": data.get('shipping_address', ''),
            "created_at": datetime.now().isoformat()
        }
        
        SAMPLE_ORDERS.append(new_order)
        
        return jsonify({"success": True, "data": new_order, "message": "Order created successfully"}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": "Invalid data format"}), 400
    except Exception as e:
        logger.error(f"Create order API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/orders/<order_id>', methods=['PUT'])
def api_update_order(order_id):
    """Update order status"""
    try:
        data = request.get_json()
        
        order = next((o for o in SAMPLE_ORDERS if o["id"] == order_id), None)
        if not order:
            return jsonify({"success": False, "error": "Order not found"}), 404
        
        # Update allowed fields
        allowed_fields = ['status', 'shipping_address']
        for field in allowed_fields:
            if field in data:
                order[field] = data[field]
        
        order['updated_at'] = datetime.now().isoformat()
        
        return jsonify({"success": True, "data": order, "message": "Order updated successfully"})
    except Exception as e:
        logger.error(f"Update order API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/stats')
def api_stats():
    """Get comprehensive dashboard statistics"""
    try:
        total_products = len(SAMPLE_PRODUCTS)
        total_orders = len(SAMPLE_ORDERS)
        total_revenue = sum(order["total"] for order in SAMPLE_ORDERS)
        total_stock = sum(product["stock"] for product in SAMPLE_PRODUCTS)
        
        # Calculate additional metrics
        low_stock_products = [p for p in SAMPLE_PRODUCTS if p['stock'] < 10]
        orders_this_week = [o for o in SAMPLE_ORDERS 
                           if (datetime.now() - datetime.strptime(o['date'], "%Y-%m-%d")).days <= 7]
        
        # Category breakdown
        categories = {}
        for product in SAMPLE_PRODUCTS:
            cat = product['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'total_stock': 0}
            categories[cat]['count'] += 1
            categories[cat]['total_stock'] += product['stock']
        
        return jsonify({
            "success": True,
            "data": {
                "overview": {
                    "total_products": total_products,
                    "total_orders": total_orders,
                    "total_revenue": total_revenue,
                    "total_stock": total_stock,
                    "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
                },
                "alerts": {
                    "low_stock_count": len(low_stock_products),
                    "low_stock_products": [p['name'] for p in low_stock_products]
                },
                "recent_activity": {
                    "orders_this_week": len(orders_this_week),
                    "revenue_this_week": sum(o['total'] for o in orders_this_week)
                },
                "categories": categories,
                "generated_at": datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Stats API error: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/api/purchase-orders', methods=['GET', 'POST'])
def api_purchase_orders():
    """Handle purchase orders API"""
    if request.method == 'GET':
        try:
            status = request.args.get('status', '').strip()
            filtered_pos = SAMPLE_PURCHASE_ORDERS
            
            if status:
                filtered_pos = [po for po in filtered_pos if po['status'].lower() == status.lower()]
            
            return jsonify({
                "success": True,
                "data": filtered_pos,
                "count": len(filtered_pos)
            })
        except Exception as e:
            logger.error(f"Purchase orders GET API error: {str(e)}")
            return jsonify({"success": False, "error": "Internal server error"}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['vendor', 'total', 'items_count']
            for field in required_fields:
                if field not in data:
                    return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
            
            new_po = {
                'id': f'PO-{len(SAMPLE_PURCHASE_ORDERS) + 1:03d}',
                'vendor': data['vendor'],
                'total': data['total'],
                'status': 'Pending',
                'date': datetime.now().strftime("%Y-%m-%d"),
                'items_count': int(data['items_count']),
                'expected_delivery': data.get('expected_delivery', 
                                            (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
            }
            
            SAMPLE_PURCHASE_ORDERS.append(new_po)
            
            return jsonify({"success": True, "data": new_po, "message": "Purchase order created successfully"}), 201
        except ValueError as e:
            return jsonify({"success": False, "error": "Invalid data format"}), 400
        except Exception as e:
            logger.error(f"Purchase orders POST API error: {str(e)}")
            return jsonify({"success": False, "error": "Internal server error"}), 500

# Enhanced Static file routes with caching and security
@app.route('/css/<path:filename>')
def css_files(filename):
    """Serve CSS files with proper headers"""
    response = send_from_directory('css', filename)
    response.headers['Content-Type'] = 'text/css'
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response

@app.route('/js/<path:filename>')
def js_files(filename):
    """Serve JavaScript files with proper headers"""
    response = send_from_directory('js', filename)
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    return response

@app.route('/assets/<path:filename>')
def asset_files(filename):
    """Serve asset files with proper headers"""
    response = send_from_directory('assets', filename)
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
    return response

@app.route('/images/<path:filename>')
def image_files(filename):
    """Serve image files with proper headers"""
    response = send_from_directory('images', filename)
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
    return response

@app.route('/logo.png')
def logo():
    """Serve logo file with caching"""
    response = send_from_directory('.', 'logo.png')
    response.headers['Cache-Control'] = 'public, max-age=86400'  # Cache for 24 hours
    return response

# Security headers middleware
@app.after_request
def after_request(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # CORS headers for API endpoints
    if request.path.startswith('/api/'):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
    
    return response

# Enhanced Error handlers with better user experience
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({
        "success": False,
        "error": "Bad Request",
        "message": "The request could not be understood by the server",
        "code": 400
    }), 400

@app.errorhandler(404)
def not_found(error):
    """Enhanced 404 error handler"""
    if request.path.startswith('/api/'):
        return jsonify({
            "success": False,
            "error": "Resource not found",
            "message": f"The requested resource '{request.path}' was not found",
            "code": 404,
            "available_endpoints": [
                "/api/products",
                "/api/orders", 
                "/api/stats",
                "/api/purchase-orders"
            ]
        }), 404
    else:
        # Redirect to dashboard for non-API 404s
        return redirect(url_for('dashboard'))

@app.errorhandler(500)
def internal_error(error):
    """Enhanced 500 error handler"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred on the server",
        "code": 500,
        "timestamp": datetime.now().isoformat()
    }), 500

@app.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limiting errors"""
    return jsonify({
        "success": False,
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later.",
        "code": 429
    }), 429

# Utility endpoints
@app.route('/health')
def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check system health
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "environment": "development" if app.debug else "production",
            "services": {
                "database": "connected",  # Would check real DB in production
                "api": "operational",
                "templates": "loaded"
            },
            "metrics": {
                "total_products": len(SAMPLE_PRODUCTS),
                "total_orders": len(SAMPLE_ORDERS),
                "uptime": "operational"
            }
        }
        
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/version')
def api_version():
    """API version information"""
    return jsonify({
        "api_version": "2.0.0",
        "flask_version": "2.3.3",
        "python_version": "3.9+",
        "features": [
            "Enhanced product management",
            "Order processing",
            "Purchase order management", 
            "Analytics dashboard",
            "Real-time statistics",
            "Template-based UI"
        ],
        "endpoints": {
            "products": "/api/products",
            "orders": "/api/orders",
            "stats": "/api/stats",
            "purchase_orders": "/api/purchase-orders",
            "health": "/health"
        }
    })

# Development helpers
@app.route('/api/reset-data', methods=['POST'])
def reset_sample_data():
    """Reset sample data - development only"""
    if not app.debug:
        return jsonify({"error": "Not available in production"}), 403
    
    global SAMPLE_ORDERS, SAMPLE_PURCHASE_ORDERS
    
    # Reset to original sample data
    SAMPLE_ORDERS = [
        {
            "id": "ORD-001", 
            "customer": "John Doe", 
            "email": "john.doe@example.com",
            "total": 2249.98, 
            "status": "Shipped", 
            "date": "2025-06-01",
            "items": [
                {"product_id": 1, "quantity": 1, "price": 1999.99},
                {"product_id": 3, "quantity": 1, "price": 249.99}
            ],
            "shipping_address": "123 Main St, New York, NY 10001"
        }
    ]
    
    SAMPLE_PURCHASE_ORDERS = [
        {
            'id': 'PO-001',
            'vendor': 'Apple Inc.',
            'total': '15,299.99',
            'status': 'Pending',
            'date': '2025-06-05',
            'items_count': 8,
            'expected_delivery': '2025-06-15'
        }
    ]
    
    return jsonify({
        "success": True,
        "message": "Sample data reset successfully",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced Flask Ecommerce Application")
    print("=" * 60)
    print(f"📁 Project Directory: {os.getcwd()}")
    print(f"📄 Templates Directory: {os.path.join(os.getcwd(), 'templates')}")
    print(f"🌐 Server URL: http://localhost:5001")
    print(f"📱 Main Dashboard: http://localhost:5001/dashboard")
    print(f"🛒 Purchase Orders: http://localhost:5001/purchase-order")
    print(f"📊 Analytics: http://localhost:5001/analytics")
    print(f"📦 Products: http://localhost:5001/products")
    print("-" * 60)
    print(f"🔗 Enhanced API Endpoints:")
    print(f"   • Products (GET/POST): http://localhost:5001/api/products")
    print(f"   • Orders (GET/POST/PUT): http://localhost:5001/api/orders")
    print(f"   • Purchase Orders: http://localhost:5001/api/purchase-orders")
    print(f"   • Statistics: http://localhost:5001/api/stats")
    print(f"   • Health Check: http://localhost:5001/health")
    print(f"   • API Version: http://localhost:5001/api/version")
    print("-" * 60)
    print("✨ New Features:")
    print("   • Modular Jinja2 templates with sidebar")
    print("   • Enhanced error handling and logging")
    print("   • API validation and filtering")
    print("   • Real-time dashboard metrics")
    print("   • Security headers and CORS")
    print("   • Comprehensive health checks")
    print("   • Development data reset endpoint")
    print("-" * 60)
    print("💡 Tips:")
    print("   • All pages use the new template structure")
    print("   • API endpoints support filtering and pagination")
    print("   • Check /health for system status")
    print("   • Use /api/reset-data to reset sample data")
    print("   • Press Ctrl+C to stop the server")
    print("🌐 Starting server...")
    
    # Run the enhanced Flask app
    try:
        app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"❌ Error: {str(e)}")
        print("💡 Try changing the port or check if another service is running on port 5001")
