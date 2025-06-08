#!/usr/bin/env python3
"""
Jinja2 Template Demo
Demonstrates the new modular template structure with sidebar and base extension.
"""

from flask import Flask, render_template
import os

# Initialize Flask app with templates folder
app = Flask(__name__, 
           template_folder='templates',
           static_folder='.',
           static_url_path='')

app.config['DEBUG'] = True

@app.route('/')
def home():
    """Main dashboard using Jinja2 templates"""
    return render_template('index.html', 
                         active_page='overview',
                         project_name='Ecommerce',
                         plan_type='Pro plan',
                         expanded_sections=['ai'],
                         user_email='longdyheak9999@gmail.com')

@app.route('/dashboard')
def dashboard():
    """Dashboard with dynamic data"""
    build_cards = [
        {
            'title': 'Hosting',
            'stat': '2.5GB',
            'descriptions': [
                'Downloads (7d total)',
                'Deployment history: <b>Deployed</b>',
                'Deployed by: longdyheak9999@gmail.com'
            ]
        },
        {
            'title': 'Firestore',
            'stat': '1,247',
            'descriptions': [
                'Reads (current)',
                'Writes (current)',
                'Active connections: <b>12</b>'
            ]
        },
        {
            'title': 'Authentication',
            'stat': '89',
            'descriptions': [
                'Active users',
                'Total sign-ins today: <b>234</b>',
                'New registrations: <b>5</b>'
            ]
        }
    ]
    
    return render_template('index.html',
                         active_page='overview',
                         project_name='Ecommerce Pro',
                         plan_type='Enterprise plan',
                         expanded_sections=['ai', 'build'],
                         build_cards=build_cards,
                         user_email='longdyheak9999@gmail.com')

@app.route('/purchase-order')
def purchase_order():
    """Purchase order page with sample data"""
    recent_orders = [
        {
            'id': 'PO-001',
            'vendor': 'Tech Supplies Inc.',
            'total': '1,299.99',
            'status': 'Pending',
            'date': '2025-06-05'
        },
        {
            'id': 'PO-002', 
            'vendor': 'Office Equipment Co.',
            'total': '899.50',
            'status': 'Approved',
            'date': '2025-06-04'
        },
        {
            'id': 'PO-003',
            'vendor': 'Software Solutions Ltd.',
            'total': '2,499.00',
            'status': 'Delivered',
            'date': '2025-06-02'
        }
    ]
    
    return render_template('PurchaseOrder.html',
                         active_page='purchase-order',
                         project_name='Ecommerce',
                         plan_type='Pro plan',
                         expanded_sections=['build'],
                         recent_orders=recent_orders)

@app.route('/analytics')
def analytics():
    """Example of another page extending the base template"""
    return render_template('index.html',
                         active_page='analytics',
                         project_name='Ecommerce Analytics',
                         plan_type='Pro plan',
                         expanded_sections=['analytics'],
                         user_email='longdyheak9999@gmail.com')

@app.route('/hosting')
def hosting():
    """Hosting page example"""
    return render_template('index.html',
                         active_page='hosting',
                         project_name='Ecommerce Hosting',
                         plan_type='Pro plan',
                         expanded_sections=['build'],
                         user_email='longdyheak9999@gmail.com')

if __name__ == '__main__':
    print("🚀 Starting Jinja2 Template Demo Server...")
    print("📁 Templates are located in: /templates/")
    print("🎨 Available routes:")
    print("   - / (Home)")
    print("   - /dashboard (Dashboard with data)")
    print("   - /purchase-order (Purchase Order form)")
    print("   - /analytics (Analytics page)")
    print("   - /hosting (Hosting page)")
    print("🌐 Server running at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
