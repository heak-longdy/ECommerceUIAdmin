"""
Sample Flask Application with Customer Management
Demonstrates how to use the Customer functionality
"""

from flask import Flask, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import customer components
from src.Customer import customer_bp, Customer, CustomerService
from src.db import engine, Base, get_db_session

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'ecommerce_db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register customer blueprint
app.register_blueprint(customer_bp)

@app.route('/')
def index():
    """Home page with links to customer management"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ecommerce Customer Management</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; }
            .feature-card { transition: transform 0.3s; }
            .feature-card:hover { transform: translateY(-5px); }
        </style>
    </head>
    <body>
        <div class="hero">
            <div class="container text-center">
                <h1 class="display-4">Customer Management System</h1>
                <p class="lead">Complete customer management with PostgreSQL integration</p>
            </div>
        </div>
        
        <div class="container my-5">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body">
                            <h5 class="card-title">👥 Customer List</h5>
                            <p class="card-text">View all customers with search and pagination</p>
                            <a href="/customers/" class="btn btn-primary">View Customers</a>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body">
                            <h5 class="card-title">➕ Add Customer</h5>
                            <p class="card-text">Create new customer with complete information</p>
                            <a href="/customers/create" class="btn btn-success">Add Customer</a>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 mb-4">
                    <div class="card feature-card h-100">
                        <div class="card-body">
                            <h5 class="card-title">🔧 API Access</h5>
                            <p class="card-text">RESTful API for customer management</p>
                            <a href="/customers/api" class="btn btn-info">View API</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-5">
                <div class="col-12">
                    <h3>🚀 Quick Start</h3>
                    <div class="card">
                        <div class="card-body">
                            <h6>API Endpoints:</h6>
                            <ul>
                                <li><code>GET /customers/api</code> - List all customers</li>
                                <li><code>POST /customers/api/create</code> - Create new customer</li>
                                <li><code>GET /customers/api/&lt;id&gt;</code> - Get customer by ID</li>
                                <li><code>PUT /customers/api/&lt;id&gt;/edit</code> - Update customer</li>
                                <li><code>DELETE /customers/&lt;id&gt;/delete</code> - Delete customer</li>
                            </ul>
                            
                            <h6>Example API Usage:</h6>
                            <pre class="bg-light p-3"><code>curl -X POST http://localhost:5000/customers/api/create \\
  -H "Content-Type: application/json" \\
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA"
  }'</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with get_db_session() as session:
            # Try a simple query
            session.execute("SELECT 1")
            
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'features': [
                'Customer Management',
                'PostgreSQL Integration',
                'RESTful API',
                'Form Validation'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

@app.route('/setup')
def setup():
    """Setup database tables"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        return jsonify({
            'success': True,
            'message': 'Database tables created successfully',
            'tables': ['customers']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/sample-data')
def create_sample_data():
    """Create sample customer data"""
    try:
        with get_db_session() as session:
            customer_service = CustomerService(session)
            
            # Sample customers
            sample_customers = [
                {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'phone': '555-0123',
                    'address': '123 Main St',
                    'city': 'New York',
                    'state': 'NY',
                    'zip_code': '10001',
                    'country': 'USA'
                },
                {
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'email': 'jane.smith@example.com',
                    'phone': '555-0456',
                    'address': '456 Oak Ave',
                    'city': 'Los Angeles',
                    'state': 'CA',
                    'zip_code': '90210',
                    'country': 'USA'
                },
                {
                    'first_name': 'Bob',
                    'last_name': 'Johnson',
                    'email': 'bob.johnson@example.com',
                    'phone': '555-0789',
                    'address': '789 Pine Rd',
                    'city': 'Chicago',
                    'state': 'IL',
                    'zip_code': '60601',
                    'country': 'USA'
                }
            ]
            
            created_customers = []
            for customer_data in sample_customers:
                try:
                    customer = customer_service.create_customer(customer_data)
                    created_customers.append(customer.to_dict())
                except ValueError:
                    # Customer already exists, skip
                    pass
            
            return jsonify({
                'success': True,
                'message': f'Created {len(created_customers)} sample customers',
                'customers': created_customers
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Customer Management System")
    print("=" * 50)
    
    # Check database connection
    try:
        with get_db_session() as session:
            session.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your database configuration in .env file")
    
    print("\n📋 Available endpoints:")
    print("- Home: http://localhost:5000/")
    print("- Customers: http://localhost:5000/customers/")
    print("- Health: http://localhost:5000/health")
    print("- Setup: http://localhost:5000/setup")
    print("- Sample Data: http://localhost:5000/sample-data")
    
    print(f"\n🌐 Starting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
