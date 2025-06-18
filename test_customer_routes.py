#!/usr/bin/env python3
"""
Simple test script to verify customer functionality is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from src.db import init_db, create_tables
from src.Customer import customer_bp, Customer, CustomerService

def create_test_app():
    """Create test Flask app with SQLite for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_customer.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    # Initialize database
    init_db(app)
    
    # Register blueprint
    app.register_blueprint(customer_bp)
    
    return app

def test_customer_model():
    """Test customer model functionality"""
    app = create_test_app()
    
    with app.app_context():
        # Create tables
        create_tables(app)
        
        print("🧪 Testing Customer Model...")
        
        # Test customer creation
        service = CustomerService()
        
        try:
            customer_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '+1-555-0123',
                'address': '123 Main St',
                'city': 'Anytown',
                'state': 'CA',
                'zip_code': '12345'
            }
            
            customer = service.create_customer(customer_data)
            print(f"✅ Customer created: {customer}")
            print(f"   - ID: {customer.id}")
            print(f"   - Full Name: {customer.full_name}")
            print(f"   - Email: {customer.email}")
            print(f"   - UUID: {customer.uuid}")
            
            # Test getting all customers
            result = service.get_all_customers()
            print(f"✅ Total customers: {result['total']}")
            
            # Test customer update
            updated_customer = service.update_customer(customer.id, {'phone': '+1-555-9999'})
            print(f"✅ Customer updated: {updated_customer.phone}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def test_customer_routes():
    """Test customer routes"""
    app = create_test_app()
    
    with app.app_context():
        create_tables(app)
        
        print("\n🧪 Testing Customer Routes...")
        
        client = app.test_client()
        
        # Test customer list route
        response = client.get('/customers/')
        print(f"GET /customers/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Customer list route working")
        else:
            print(f"❌ Customer list route failed: {response.status_code}")
            return False
        
        return True

if __name__ == "__main__":
    print("🚀 Testing Customer Functionality...")
    
    # Test model
    model_success = test_customer_model()
    
    # Test routes
    route_success = test_customer_routes()
    
    if model_success and route_success:
        print("\n🎉 All tests passed! Customer functionality is working.")
    else:
        print("\n❌ Some tests failed. Check the output above.")
