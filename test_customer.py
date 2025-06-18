#!/usr/bin/env python3
"""
Simple test script to verify customer creation works
"""

import os
import sys
sys.path.append('/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce')

from main_app import create_app

def test_customer_creation():
    """Test creating a customer"""
    app = create_app()
    
    with app.app_context():
        # Import the Customer model
        import src.Customer.routes_simple as customer_routes
        Customer = customer_routes.Customer
        
        # Try to create a test customer
        try:
            test_customer = Customer(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="555-1234",
                city="New York",
                state="NY",
                country="USA",
                is_active=True
            )
            
            customer_routes.db.session.add(test_customer)
            customer_routes.db.session.commit()
            
            print(f"✅ Successfully created customer: {test_customer.full_name}")
            print(f"   ID: {test_customer.id}")
            print(f"   Email: {test_customer.email}")
            print(f"   Created at: {test_customer.created_at}")
            
            # Query to verify
            customers = Customer.query.all()
            print(f"📊 Total customers in database: {len(customers)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating customer: {e}")
            customer_routes.db.session.rollback()
            return False

if __name__ == '__main__':
    print("🧪 Testing customer creation...")
    success = test_customer_creation()
    if success:
        print("✅ Test passed!")
    else:
        print("❌ Test failed!")
