#!/usr/bin/env python3
"""
Main Flask Application for Ecommerce Project
Integrates all components    app.run(debug=True, host='0.0.0.0', port=5005)and provides a complete working application
"""

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
import os
from datetime import datetime
from dotenv import load_dotenv

# Import our database utilities
from src.db import init_db, create_tables, DatabaseConfig

# Load environment variables
load_dotenv()

# app = Flask(__name__)
app = Flask(__name__, 
           template_folder='templates',
           static_folder='.',
           static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database using our db utilities
db = init_db(app)

# Import and register blueprints
from src.Administrator.Customer.route import customer_bp
from src.Administrator.ClassRoom.route import classroom_bp
from src.Administrator.Order.route import app as order_bp

app.register_blueprint(customer_bp, url_prefix='/administrator/customers')
app.register_blueprint(classroom_bp, url_prefix='/administrator/classrooms')
app.register_blueprint(order_bp, url_prefix='/administrator/orders')

if __name__ == '__main__':
    # app = create_app()
    print("🚀 Starting Flask Ecommerce Application")
    print("📍 Available routes:")
    print("   - http://localhost:5000/ (Dashboard)")
    print("   - http://localhost:5000/customers (Customer Management)")
    print("   - http://localhost:5000/customers/api (Customer API)")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
