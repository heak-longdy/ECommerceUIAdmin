"""
Customer Routes
Defines Flask routes for customer management using Flask-SQLAlchemy
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime


from src.db import db, DatabaseConfig

# Create blueprint for order routes
app = Blueprint('order_bp', __name__, url_prefix='/orders')
# Import order forms

# This will be set by the main app
# db = None
# Customer = None
# CustomerService = None

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

@app.route('/')
def orders_page():
    """Orders management page with enhanced order details"""
    return render_template('order/index.html',
                         active_page='orders',
                         project_name='Order Management',
                         plan_type='Pro Plan',
                         expanded_sections=['build'],
                         recent_orders=SAMPLE_ORDERS,
                         cart_count=0)
@app.route('/Create')
def orders_create():
    """Orders management page with enhanced order details"""
    return render_template('order/create.html',
                         active_page='orders',
                         project_name='Order Management',
                         plan_type='Pro Plan',
                         expanded_sections=['build'],
                         recent_orders=SAMPLE_ORDERS,
                         cart_count=9)
