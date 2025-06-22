#!/usr/bin/env python3
"""
Main Flask Application for Ecommerce Project
Integrates all components    app.run(debug=True, host='0.0.0.0', port=5005)and provides a complete working application
"""

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager


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
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')

# Initialize database using our db utilities
db = init_db(app)
jwt = JWTManager(app)

# Website
# Import and register blueprints
from src.Website.home import home_bp

app.register_blueprint(home_bp, url_prefix='/')


# Admin
# Import and register blueprints
from src.Administrator.Customer.route import customer_bp
from src.Administrator.ClassRoom.route import classroom_bp
from src.Administrator.Order.route import app as order_bp
from src.Administrator.Admin.route import admin_bp
from src.Administrator.Auth.route import auth_bp

app.register_blueprint(customer_bp, url_prefix='/administrator/customers')
app.register_blueprint(classroom_bp, url_prefix='/administrator/classrooms')
app.register_blueprint(order_bp, url_prefix='/administrator/orders')
app.register_blueprint(admin_bp, url_prefix='/administrator/admins')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.before_request
def make_session_permanent():
    session.permanent = True

if __name__ == '__main__':
    # app = create_app()
    print("🚀 Starting Flask Ecommerce Application")
    print("📍 Available routes:")
    print("   - http://localhost:5002/ (Dashboard)")
    print("   - http://localhost:5002/customers (Customer Management)")
    print("   - http://localhost:5002/customers/api (Customer API)")
    
    app.run(debug=True, host='0.0.0.0', port=5002)
