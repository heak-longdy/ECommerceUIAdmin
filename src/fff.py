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


class Customerddddddddd(db.Model):
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
        address_parts = [
            self.address,
            self.city,
            self.state,
            self.zip_code,
            self.country
        ]
        return ', '.join([part for part in address_parts if part])
    
    @property
    def is_complete_profile(self):
        """Check if customer profile is complete"""
        required_fields = [
            self.first_name, 
            self.last_name, 
            self.email,
            self.phone,
            self.address,
            self.city,
            self.state,
            self.zip_code
        ]
        return all(field for field in required_fields)
    
    def to_dict(self):
        """Convert customer to dictionary representation"""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'newsletter_subscribed': self.newsletter_subscribed,
            'preferred_language': self.preferred_language,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'notes': self.notes,
            'tags': self.tags,
            'full_name': self.full_name,
            'full_address': self.full_address,
            'is_complete_profile': self.is_complete_profile
        }
    
    @classmethod
    def create(cls, **kwargs):
        """Class method to create a new customer"""
        customer = cls(**kwargs)
        db.session.add(customer)
        try:
            db.session.commit()
            return customer
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, **kwargs):
        """Update customer attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            return self
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Delete customer"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone:
            return True  # Phone is optional
        phone_pattern = r'^[\+]?[1-9]?[\d\s\-\(\)]{7,15}$'
        return re.match(phone_pattern, phone) is not None


# Event listeners for the Customer model
@event.listens_for(Customer, 'before_insert')
def before_insert(mapper, connection, target):
    """Before insert event listener"""
    if not target.uuid:
        target.uuid = str(uuid.uuid4())


@event.listens_for(Customer, 'before_update')
def before_update(mapper, connection, target):
    """Before update event listener"""
    target.updated_at = datetime.utcnow()


class CustomerService:
    """Service class for Customer operations"""
    
    def __init__(self, db_session=None):
        self.db = db_session or db
    
    
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        return Customer.query.get(customer_id)
    
    def get_customer_by_email(self, email):
        """Get customer by email"""
        return Customer.query.filter_by(email=email).first()
    
    def create_customer(self, customer_data):
        """Create new customer"""
        # Validate email
        if not Customer.validate_email(customer_data.get('email', '')):
            raise ValueError("Invalid email format")
        
        # Validate phone if provided
        if customer_data.get('phone') and not Customer.validate_phone(customer_data['phone']):
            raise ValueError("Invalid phone number format")
        
        # Check if email already exists
        if self.get_customer_by_email(customer_data['email']):
            raise ValueError("Customer with this email already exists")
        
        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()
        return customer
    
    def update_customer(self, customer_id, update_data):
        """Update customer"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        # Validate email if being updated
        if 'email' in update_data and update_data['email'] != customer.email:
            if not Customer.validate_email(update_data['email']):
                raise ValueError("Invalid email format")
            
            # Check if new email already exists
            existing_customer = self.get_customer_by_email(update_data['email'])
            if existing_customer and existing_customer.id != customer_id:
                raise ValueError("Customer with this email already exists")
        
        # Validate phone if being updated
        if 'phone' in update_data and not Customer.validate_phone(update_data['phone']):
            raise ValueError("Invalid phone number format")
        
        return customer.update(**update_data)
    
    def delete_customer(self, customer_id):
        """Delete customer"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        return customer.delete()
    
    def get_customer_stats(self):
        """Get customer statistics"""
        total_customers = Customer.query.count()
        active_customers = Customer.query.filter_by(is_active=True).count()
        verified_customers = Customer.query.filter_by(is_verified=True).count()
        subscribed_customers = Customer.query.filter_by(newsletter_subscribed=True).count()
        
        return {
            'total': total_customers,
            'active': active_customers,
            'inactive': total_customers - active_customers,
            'verified': verified_customers,
            'unverified': total_customers - verified_customers,
            'subscribed': subscribed_customers,
            'unsubscribed': total_customers - subscribed_customers
        }
