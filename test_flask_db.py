#!/usr/bin/env python3
"""
Test the updated db.py with Flask integration
"""

import os
import sys
sys.path.append('/Users/longdy/Documents/Projects/Python/NewProject/Ecommerce')

from main_app import create_app
from src.db import test_flask_db_connection, backup_table_to_json

def test_flask_db_integration():
    """Test Flask database integration"""
    app = create_app()
    
    print("🧪 Testing Flask-SQLAlchemy integration...")
    
    # Test connection
    if test_flask_db_connection(app):
        print("✅ Flask-SQLAlchemy connection test passed!")
    else:
        print("❌ Flask-SQLAlchemy connection test failed!")
    
    # Test customer operations
    with app.app_context():
        try:
            from src.Customer.route import db, Customer
            import random
            
            # Check existing customers
            customers = Customer.query.all()
            print(f"📊 Found {len(customers)} existing customers in database")
            
            # Generate unique email for test
            random_id = random.randint(1000, 9999)
            test_email = f"test.user.{random_id}@example.com"
            
            # Check if test customer already exists and delete it
            existing_customer = Customer.query.filter_by(email=test_email).first()
            if existing_customer:
                db.session.delete(existing_customer)
                db.session.commit()
                print(f"🧹 Cleaned up existing test customer")
            
            # Try to create a new customer
            test_customer = Customer(
                first_name="Test",
                last_name="User",
                email=test_email,
                phone="555-TEST",
                city="Test City",
                state="TC",
                country="USA",
                is_active=True
            )
            
            db.session.add(test_customer)
            db.session.commit()
            
            print(f"✅ Successfully created test customer: {test_customer.full_name}")
            print(f"   ID: {test_customer.id}")
            print(f"   Email: {test_customer.email}")
            
            # Verify the customer was saved
            saved_customer = Customer.query.filter_by(email=test_email).first()
            if saved_customer:
                print(f"✅ Customer verification successful: {saved_customer.full_name}")
                
                # Clean up the test customer
                db.session.delete(saved_customer)
                db.session.commit()
                print(f"🧹 Test customer cleaned up from database")
            else:
                print("❌ Customer verification failed!")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing customer operations: {e}")
            # Try to rollback in case of error
            try:
                db.session.rollback()
            except:
                pass
            return False

def test_backup_functionality():
    """Test database backup functionality"""
    print("\n📋 Testing backup functionality...")
    
    try:
        # Backup customers table
        backup_file = "customers_backup.json"
        if backup_table_to_json("customers", backup_file):
            print(f"✅ Backup created successfully: {backup_file}")
            
            # Check if file exists and has content
            import os
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                print(f"✅ Backup file verified: {os.path.getsize(backup_file)} bytes")
                
                # Clean up test file
                os.remove(backup_file)
                print("🧹 Test backup file cleaned up")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Backup test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing Flask-integrated db.py functionality...")
    
    # Test Flask integration
    db_test_passed = test_flask_db_integration()
    
    # Test backup functionality
    backup_test_passed = test_backup_functionality()
    
    print(f"\n📊 Test Results:")
    print(f"   Flask DB Integration: {'✅ PASSED' if db_test_passed else '❌ FAILED'}")
    print(f"   Backup Functionality: {'✅ PASSED' if backup_test_passed else '❌ FAILED'}")
    
    if db_test_passed and backup_test_passed:
        print("\n🎉 All tests passed! db.py is working perfectly with Flask!")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
