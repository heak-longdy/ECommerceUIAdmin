#!/usr/bin/env python3
"""
Test PostgreSQL customer creation
"""

import os
import sys
sys.path.append('/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce')

from main_app import create_app

def test_postgresql_customer():
    """Test creating a customer in PostgreSQL"""
    app = create_app()
    
    with app.app_context():
        # Get the database and customer model from the route module
        from src.Customer.route import db, Customer
        
        # Try to create a test customer
        try:
            test_customer = Customer(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone="555-5678",
                city="San Francisco",
                state="CA",
                country="USA",
                is_active=True
            )
            
            db.session.add(test_customer)
            db.session.commit()
            
            print(f"✅ Successfully created customer in PostgreSQL: {test_customer.full_name}")
            print(f"   ID: {test_customer.id}")
            print(f"   Email: {test_customer.email}")
            print(f"   Created at: {test_customer.created_at}")
            
            # Query to verify
            customers = Customer.query.all()
            print(f"📊 Total customers in PostgreSQL database: {len(customers)}")
            
            for customer in customers:
                print(f"   - {customer.full_name} ({customer.email})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating customer: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🧪 Testing PostgreSQL customer creation...")
    success = test_postgresql_customer()
    if success:
        print("✅ PostgreSQL test passed!")
    else:
        print("❌ PostgreSQL test failed!")
