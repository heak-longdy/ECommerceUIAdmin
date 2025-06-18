#!/usr/bin/env python3
"""
Simple Flask app runner to test customer functionality with success alerts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from src.Customer.route import customer_bp, init_routes
from src.Customer.model import Customer, CustomerService
from src.db import db

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Initialize customer routes
    init_routes(db, Customer, CustomerService)
    
    # Register blueprints
    app.register_blueprint(customer_bp)
    
    # Home route
    @app.route('/')
    def index():
        return '''
        <h1>Ecommerce Customer Management</h1>
        <p>Welcome to the Customer Management System</p>
        <ul>
            <li><a href="/customers">View All Customers</a></li>
            <li><a href="/customers/create">Create New Customer</a></li>
        </ul>
        '''
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app

def main():
    """Main function to run the app"""
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database tables created successfully!")
    
    print("🚀 Starting Flask development server...")
    print("📋 Available routes:")
    print("   - Home: http://localhost:5000/")
    print("   - Customers List: http://localhost:5000/customers")
    print("   - Create Customer: http://localhost:5000/customers/create")
    print("   - View Customer: http://localhost:5000/customers/<id>")
    print("   - Edit Customer: http://localhost:5000/customers/<id>/edit")
    print("")
    print("✅ Customer creation will show success alerts!")
    print("💡 Create a customer to test the success alert functionality")
    print("")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
