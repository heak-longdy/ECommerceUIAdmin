#!/usr/bin/env python3
"""
Test script to verify customer creation with success alerts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.Customer.route import customer_bp, init_routes
from src.Customer.model import Customer, CustomerService
from src.db import db

def create_test_app():
    """Create test Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_customer.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    # Initialize database
    db.init_app(app)
    
    # Initialize routes
    init_routes(db, Customer, CustomerService)
    
    # Register blueprint
    app.register_blueprint(customer_bp)
    
    return app

def test_customer_creation():
    """Test customer creation functionality"""
    app = create_test_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Test client
        client = app.test_client()
        
        # Test GET request to create page
        response = client.get('/customers/create')
        print(f"GET /customers/create - Status: {response.status_code}")
        
        # Test POST request to create customer
        customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'country': 'USA'
        }
        
        response = client.post('/customers/create', data=customer_data, follow_redirects=True)
        print(f"POST /customers/create - Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check if success message is in response
            response_data = response.get_data(as_text=True)
            if 'Success!' in response_data and 'John Doe' in response_data:
                print("✅ SUCCESS: Customer creation with success alert working!")
                print("✅ Flash message displayed correctly")
            else:
                print("❌ WARNING: Success message may not be displayed properly")
        else:
            print(f"❌ ERROR: Customer creation failed with status {response.status_code}")
        
        # Clean up
        db.drop_all()

if __name__ == '__main__':
    print("Testing Customer Creation with Success Alerts...")
    print("=" * 50)
    test_customer_creation()
    print("=" * 50)
    print("Test completed!")
