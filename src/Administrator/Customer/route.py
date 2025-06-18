"""
Customer Routes
Defines Flask routes for customer management using Flask-SQLAlchemy
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime


from src.db import db, DatabaseConfig

from src.Models.Customer import Customer
# Import customer forms
from .form import CustomerForm, CustomerSearchForm, CustomerQuickForm, CustomerDeleteForm, CustomerBulkActionForm

# This will be set by the main app
# db = None
# Customer = None
# CustomerService = None

# def init_routes(database, customer_model, customer_service_class):
#     """Initialize routes with database, model, and service instances"""
#     global db, Customer, CustomerService
#     db = database
#     Customer = customer_model
#     CustomerService = customer_service_class

# Create blueprint for customer routes
customer_bp = Blueprint('customer_bp', __name__, url_prefix='/customers')

@customer_bp.route('/')
@customer_bp.route('/list')
def customer_list():
    """Customer list page with search and pagination"""
    try:
        
        # QueryData = db.session.query(Customer).all()
        # print(f"Total customers in database: {QueryData}")
        
        
        search_form = CustomerSearchForm()
        
        # Get search parameters
        search_query = request.args.get('search', '')
        status_filter = request.args.get('status', 'all')
        page = request.args.get('page', 1, type=int)
        per_page = 1
        
        # Create service instance and get customers
        # service = CustomerService(db)
        result = Customer.get_all_customers(
            page=page,
            per_page=per_page,
            search=search_query if search_query else None,
            status_filter=status_filter if status_filter != 'all' else None
        )
        
        # print(f"Customers foun @@@@@@: {len(result['customers'])}")
        
        return render_template('customers/index.html', 
                             customers=result, 
                             search_form=search_form,
                             search_query=search_query,
                             status_filter=status_filter)
                             
    except Exception as e:
        return str(e)
        # current_app.logger.error(f'Error loading customers: {str(e)}')
        # flash(f'Error loading customers: {str(e)}', 'error')
        # return render_template('customers/index.html', 
        #                      customers={'customers': [], 'total': 0, 'page': 1, 'pages': 0}, 
        #                      search_form=CustomerSearchForm(),
        #                      search_query='',
        #                      status_filter='all')

@customer_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create new customer with improved Flask practices"""
    form = CustomerForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Create service instance
                # service = CustomerService(db)
                
                # # Prepare customer data with better validation
                customer_data = _prepare_customer_data(form)
                
                # # Create customer using service
                # customer = service.create_customer(customer_data)
                
                if not Customer.validate_email(customer_data.get('email', '')):
                    raise ValueError("Invalid email format")
                
                # Validate phone if provided
                if customer_data.get('phone') and not Customer.validate_phone(customer_data['phone']):
                    raise ValueError("Invalid phone number format")
                
                # Check if email already exists
                # if self.get_customer_by_email(customer_data['email']):
                #     raise ValueError("Customer with this email already exists")
                
                customer = Customer(**customer_data)
                db.session.add(customer)
                db.session.commit()
                # return customer
                
                # Log the successful creation
                current_app.logger.info(f'Customer created: {customer.email} (ID: {customer.id})')
                
                # Flash success message with better formatting
                flash(f'✅ Success! Customer "{customer.full_name}" has been created successfully.', 'success')
                
                # Redirect to customer view page instead of list for better UX
                return redirect(url_for('customer_bp.view', customer_id=customer.id))
                
            except ValueError as e:
                current_app.logger.warning(f'Validation error creating customer: {str(e)}')
                flash(f'❌ Validation Error: {str(e)}', 'error')
            except IntegrityError as e:
                current_app.logger.error(f'Database integrity error: {str(e)}')
                db.session.rollback()
                flash('❌ Error: A customer with this email already exists.', 'error')
            except Exception as e:
                current_app.logger.error(f'Unexpected error creating customer: {str(e)}')
                db.session.rollback()
                flash(f'❌ Unexpected Error: {str(e)}', 'error')
        else:
            # Display form validation errors with better formatting
            _flash_form_errors(form)
    
    # Render the form (GET request or failed POST)
    return render_template('customers/create.html', form=form, title='Create New Customer')

@customer_bp.route('/<int:customer_id>')
def view(customer_id):
    """View customer details"""
    try:
        service = CustomerService(db)
        customer = service.get_customer_by_id(customer_id)
        
        if not customer:
            flash('Customer not found', 'error')
            return redirect(url_for('customer_bp.customer_list'))
            
        return render_template('customers/view.html', customer=customer)
    except Exception as e:
        flash(f'Error loading customer: {str(e)}', 'error')
        return redirect(url_for('customer_bp.customer_list'))

@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit(customer_id):
    """Edit customer"""
    try:
        service = CustomerService(db)
        customer = service.get_customer_by_id(customer_id)
        
        if not customer:
            flash('Customer not found', 'error')
            return redirect(url_for('customer_bp.customer_list'))
        
        form = CustomerForm(obj=customer)
        
        if form.validate_on_submit():
            try:
                # Prepare update data using helper function
                update_data = _prepare_customer_data(form)
                
                # Update customer using service
                updated_customer = service.update_customer(customer_id, update_data)
                
                # Log the successful update
                _log_customer_action('updated', customer_id=customer_id, email=updated_customer.email)
                
                # Flash success message with better formatting
                flash(f'✅ Success! Customer "{updated_customer.full_name}" has been updated successfully.', 'success')
                return redirect(url_for('customer_bp.view', customer_id=customer_id))
                
            except ValueError as e:
                current_app.logger.warning(f'Validation error updating customer {customer_id}: {str(e)}')
                flash(f'❌ Validation Error: {str(e)}', 'error')
            except IntegrityError as e:
                current_app.logger.error(f'Database integrity error updating customer {customer_id}: {str(e)}')
                db.session.rollback()
                flash('❌ Error: Email address is already in use by another customer.', 'error')
            except Exception as e:
                current_app.logger.error(f'Unexpected error updating customer {customer_id}: {str(e)}')
                db.session.rollback()
                flash(f'❌ Unexpected Error: {str(e)}', 'error')
        else:
            # Display form validation errors
            _flash_form_errors(form)
        
        return render_template('customers/edit.html', form=form, customer=customer, title=f'Edit Customer: {customer.full_name}')
        
    except Exception as e:
        flash(f'Error loading customer: {str(e)}', 'error')
        return redirect(url_for('customer_bp.customer_list'))

@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
def delete(customer_id):
    """Delete customer with improved error handling"""
    try:
        service = CustomerService(db)
        customer = service.get_customer_by_id(customer_id)
        
        if not customer:
            flash('❌ Error: Customer not found.', 'error')
            return redirect(url_for('customer_bp.customer_list'))
        
        # Store customer info for logging before deletion
        customer_name = customer.full_name
        customer_email = customer.email
        
        # Check if it should be a hard delete or soft delete
        hard_delete = request.form.get('hard_delete', 'false').lower() == 'true'
        
        # Perform deletion
        service.delete_customer(customer_id, hard_delete=hard_delete)
        
        # Log the deletion
        delete_type = 'hard deleted' if hard_delete else 'soft deleted'
        _log_customer_action(delete_type, customer_id=customer_id, email=customer_email)
        
        # Flash success message
        delete_message = 'permanently deleted' if hard_delete else 'deactivated'
        flash(f'✅ Success! Customer "{customer_name}" has been {delete_message}.', 'success')
        
    except ValueError as e:
        current_app.logger.warning(f'Validation error deleting customer {customer_id}: {str(e)}')
        flash(f'❌ Validation Error: {str(e)}', 'error')
    except Exception as e:
        current_app.logger.error(f'Unexpected error deleting customer {customer_id}: {str(e)}')
        db.session.rollback()
        flash(f'❌ Error deleting customer: {str(e)}', 'error')
    
    return redirect(url_for('customer_bp.customer_list'))

@customer_bp.route('/<int:customer_id>/toggle-status', methods=['POST'])
def toggle_status(customer_id):
    """Toggle customer active status"""
    try:
        service = CustomerService(db)
        customer = service.toggle_customer_status(customer_id)
        
        status = 'activated' if customer.is_active else 'deactivated'
        flash(f'Customer {customer.full_name} {status} successfully!', 'success')
        
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error updating customer status: {str(e)}', 'error')
    
    return redirect(url_for('customer_bp.customer_list'))

@customer_bp.route('/<int:customer_id>/verify', methods=['POST'])
def verify(customer_id):
    """Verify customer"""
    try:
        service = CustomerService(db)
        customer = service.verify_customer(customer_id)
        
        flash(f'Customer {customer.full_name} verified successfully!', 'success')
        
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error verifying customer: {str(e)}', 'error')
    
    return redirect(url_for('customer_bp.view', customer_id=customer_id))

@customer_bp.route('/<int:customer_id>/unverify', methods=['POST'])
def unverify(customer_id):
    """Unverify customer"""
    try:
        service = CustomerService(db)
        customer = service.unverify_customer(customer_id)
        
        flash(f'Customer {customer.full_name} unverified successfully!', 'success')
        
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
    except Exception as e:
        flash(f'Error unverifying customer: {str(e)}', 'error')
    
    return redirect(url_for('customer_bp.view', customer_id=customer_id))

# API Routes
@customer_bp.route('/api')
@customer_bp.route('/api/list')
def api_list():
    """API endpoint for customer list"""
    try:
        service = CustomerService(db)
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search')
        status_filter = request.args.get('status')
        
        result = service.get_all_customers(
            page=page,
            per_page=per_page,
            search=search,
            status_filter=status_filter
        )
        
        return jsonify({
            'success': True,
            'customers': [customer.to_dict() for customer in result['customers']],
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'pages': result['pages'],
                'has_prev': result['has_prev'],
                'has_next': result['has_next']
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/api/create', methods=['POST'])
def api_create():
    """API endpoint for creating customer"""
    try:
        service = CustomerService(db)
        data = request.get_json()
        
        customer = service.create_customer(data)
        
        return jsonify({
            'success': True,
            'message': 'Customer created successfully',
            'customer': customer.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/api/<int:customer_id>', methods=['GET'])
def api_get(customer_id):
    """API endpoint for getting customer details"""
    try:
        service = CustomerService(db)
        customer = service.get_customer_by_id(customer_id)
        
        if not customer:
            return jsonify({
                'success': False,
                'error': 'Customer not found'
            }), 404
            
        return jsonify({
            'success': True,
            'customer': customer.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/api/<int:customer_id>', methods=['PUT'])
def api_update(customer_id):
    """API endpoint for updating customer"""
    try:
        service = CustomerService(db)
        data = request.get_json()
        
        customer = service.update_customer(customer_id, data)
        
        return jsonify({
            'success': True,
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@customer_bp.route('/api/<int:customer_id>', methods=['DELETE'])
def api_delete(customer_id):
    """API endpoint for deleting customer"""
    try:
        service = CustomerService(db)
        customer = service.get_customer_by_id(customer_id)
        
        if not customer:
            return jsonify({
                'success': False,
                'error': 'Customer not found'
            }), 404
            
        name = customer.full_name
        
        # Check if it should be a hard delete
        hard_delete = request.args.get('hard_delete', 'false').lower() == 'true'
        service.delete_customer(customer_id, hard_delete=hard_delete)
        
        delete_type = 'deleted permanently' if hard_delete else 'deactivated'
        return jsonify({
            'success': True,
            'message': f'Customer {name} {delete_type} successfully'
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Helper functions
def _prepare_customer_data(form):
    """
    Prepare customer data from form with proper validation and defaults
    """
    return {
        'first_name': form.first_name.data.strip(),
        'last_name': form.last_name.data.strip(),
        'email': form.email.data.strip().lower(),
        'phone': form.phone.data.strip() if form.phone.data else None,
        'address': form.address.data.strip() if hasattr(form, 'address') and form.address.data else None,
        'city': form.city.data.strip() if hasattr(form, 'city') and form.city.data else None,
        'state': form.state.data.strip() if hasattr(form, 'state') and form.state.data else None,
        'zip_code': form.zip_code.data.strip() if hasattr(form, 'zip_code') and form.zip_code.data else None,
        'country': form.country.data if hasattr(form, 'country') and form.country.data else 'USA',
        'is_active': form.is_active.data if hasattr(form, 'is_active') else True,
        'is_verified': form.is_verified.data if hasattr(form, 'is_verified') else False,
        'newsletter_subscribed': form.newsletter_subscribed.data if hasattr(form, 'newsletter_subscribed') else True,
        'preferred_language': form.preferred_language.data if hasattr(form, 'preferred_language') else 'en',
        'notes': form.notes.data.strip() if hasattr(form, 'notes') and form.notes.data else None,
        'tags': form.tags.data.strip() if hasattr(form, 'tags') and form.tags.data else None
    }

def _flash_form_errors(form):
    """
    Flash form validation errors with better formatting
    """
    for field_name, errors in form.errors.items():
        field_label = getattr(form[field_name], 'label', field_name).text if hasattr(form[field_name], 'label') else field_name.replace('_', ' ').title()
        for error in errors:
            flash(f'❌ {field_label}: {error}', 'error')

def _log_customer_action(action, customer_id=None, email=None, details=None):
    """
    Log customer-related actions for auditing
    """
    log_message = f'Customer {action}'
    if customer_id:
        log_message += f' (ID: {customer_id})'
    if email:
        log_message += f' (Email: {email})'
    if details:
        log_message += f' - {details}'
    
    current_app.logger.info(log_message)

# Template filters
@customer_bp.app_template_filter('customer_status_class')
def customer_status_class(is_active):
    """Template filter to get CSS class for customer status"""
    return 'active' if is_active else 'inactive'

@customer_bp.app_template_filter('customer_verification_class')
def customer_verification_class(is_verified):
    """Template filter to get CSS class for customer verification status"""
    return 'verified' if is_verified else 'unverified'
