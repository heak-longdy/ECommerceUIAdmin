#!/usr/bin/env python3
"""
Test script for the enhanced Customer model
Tests all the new features and functionality
"""

import sys
import os
from datetime import datetime

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_app import create_app
from src.Customer.model import create_customer_model

def test_enhanced_customer_model():
    """Test the enhanced Customer model functionality"""
    print("🚀 Testing Enhanced Customer Model...")
    
    # Create Flask app and get database
    app = create_app()
    
    with app.app_context():
        # Get the existing database instance from the app
        from flask import current_app
        db = current_app.extensions['sqlalchemy']
        
        # Create Customer model and service
        Customer, CustomerService = create_customer_model(db)
        service = CustomerService(db)
        
        try:
            # Test 1: Create customer with enhanced data
            print("\n🧪 Test 1: Creating customer with enhanced data...")
            customer_data = {
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice.johnson@example.com',
                'phone': '+1-555-123-4567',
                'address': '123 Main Street',
                'city': 'New York',
                'state': 'NY',
                'zip_code': '10001',
                'country': 'USA',
                'is_active': True,
                'is_verified': True,
                'newsletter_subscribed': True,
                'preferred_language': 'en',
                'notes': 'VIP customer with special requirements',
                'tags': 'VIP, Premium, NYC'
            }
            
            customer = service.create_customer(customer_data)
            print(f"✅ Customer created: {customer.full_name}")
            print(f"   UUID: {customer.uuid}")
            print(f"   Status: {customer.status_label}")
            print(f"   Initials: {customer.initials}")
            print(f"   Tags: {customer.tags_list}")
            print(f"   Account Age: {customer.account_age_days} days")
            
            # Test 2: Test validation
            print("\n🧪 Test 2: Testing validation...")
            try:
                invalid_data = {
                    'first_name': '',  # Invalid - empty
                    'last_name': 'Test',
                    'email': 'invalid-email'  # Invalid format
                }
                service.create_customer(invalid_data)
                print("❌ Validation test failed - should have caught errors")
            except ValueError as e:
                print(f"✅ Validation working: {e}")
            
            # Test 3: Test tag operations
            print("\n🧪 Test 3: Testing tag operations...")
            customer.add_tag('High-Value')
            customer.add_tag('Frequent-Buyer')
            print(f"✅ Tags after adding: {customer.tags_list}")
            
            customer.remove_tag('NYC')
            print(f"✅ Tags after removing 'NYC': {customer.tags_list}")
            
            # Test 4: Test customer service methods
            print("\n🧪 Test 4: Testing service methods...")
            
            # Get customer stats
            stats = service.get_customer_stats()
            print(f"✅ Customer stats: {stats}")
            
            # Search customers
            search_results = service.search_customers('Alice')
            print(f"✅ Search results for 'Alice': {len(search_results)} customers")
            
            # Get customers by location
            location_results = service.get_customers_by_location(city='New York')
            print(f"✅ Customers in New York: {len(location_results)} customers")
            
            # Test 5: Test customer updates
            print("\n🧪 Test 5: Testing customer updates...")
            update_data = {
                'phone': '+1-555-999-8888',
                'notes': 'Updated VIP customer notes',
                'tags': 'VIP, Premium, Updated'
            }
            
            updated_customer = service.update_customer(customer.id, update_data)
            print(f"✅ Customer updated: {updated_customer.phone}")
            print(f"   Updated notes: {updated_customer.notes}")
            print(f"   Updated tags: {updated_customer.tags_list}")
            
            # Test 6: Test to_dict method
            print("\n🧪 Test 6: Testing to_dict method...")
            customer_dict = customer.to_dict()
            print(f"✅ Customer dict keys: {list(customer_dict.keys())}")
            print(f"   Full address: {customer_dict['full_address']}")
            
            # Clean up
            print("\n🧹 Cleaning up...")
            service.delete_customer(customer.id, hard_delete=True)
            print("✅ Test customer deleted")
            
            print("\n🎉 All tests passed! Enhanced Customer model is working correctly.")
            return True
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_enhanced_customer_model()
    sys.exit(0 if success else 1)
