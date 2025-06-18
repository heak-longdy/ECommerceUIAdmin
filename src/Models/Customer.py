"""
Customer Model for Flask-SQLAlchemy
Defines the Customer database model and service for Flask applications
Enhanced with Flask-specific features, validation, and utilities
"""

from datetime import datetime
from sqlalchemy import func, event
from sqlalchemy.exc import IntegrityError
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import re
import uuid
from src.db import db


class Customer(db.Model):
    """
    Customer model for storing customer information
    Enhanced with validation, hooks, and utility methods
    """
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Unique identifier for external references
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # Customer basic information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Address information
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50), nullable=True, default='USA')
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    # Customer preferences
    newsletter_subscribed = db.Column(db.Boolean, default=True, nullable=False)
    preferred_language = db.Column(db.String(5), default='en', nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(255), nullable=True)  # Comma-separated tags

    def __init__(self, **kwargs):
        """Initialize Customer instance"""
        super(Customer, self).__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        """String representation of Customer"""
        return f'<Customer {self.id}: {self.email}>'
    
    def __str__(self):
        """Human-readable string representation"""
        return f'{self.first_name} {self.last_name} ({self.email})'
    
    @property
    def full_name(self):
        """Get customer's full name"""
        return f'{self.first_name} {self.last_name}'.strip()
    
    @property
    def full_address(self):
        """Get formatted full address"""
        return f'{self.address}, {self.city}, {self.state}, {self.zip_code}, {self.country}'
    
    @staticmethod
    def get_all_customers(page=1, per_page=10, search=None, status_filter=None):
        """Get all customers with pagination and filtering"""
        query = Customer.query
        
        # Apply search filter
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Customer.first_name.ilike(search_filter),
                    Customer.last_name.ilike(search_filter),
                    Customer.email.ilike(search_filter),
                    Customer.phone.ilike(search_filter)
                )
            )
        
        # Apply status filter
        if status_filter == 'active':
            query = query.filter(Customer.is_active == True)
        elif status_filter == 'inactive':
            query = query.filter(Customer.is_active == False)
        elif status_filter == 'verified':
            query = query.filter(Customer.is_verified == True)
        elif status_filter == 'unverified':
            query = query.filter(Customer.is_verified == False)
        
        # Order by creation date (newest first)
        query = query.order_by(Customer.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'customers': pagination.items,
            'total': pagination.total,
            'page': page,
            'pages': pagination.pages,
            'per_page': per_page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num
        }
