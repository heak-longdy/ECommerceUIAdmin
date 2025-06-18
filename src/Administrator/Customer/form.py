"""
Customer Forms
Defines forms for customer management using WTForms
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp
from wtforms.widgets import TextArea

class CustomerForm(FlaskForm):
    """
    Form for creating and editing customers
    """
    # Basic Information
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message="First name is required"),
            Length(min=2, max=50, message="First name must be between 2 and 50 characters")
        ],
        render_kw={"placeholder": "Enter first name", "class": "form-control"}
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Last name is required"),
            Length(min=2, max=50, message="Last name must be between 2 and 50 characters")
        ],
        render_kw={"placeholder": "Enter last name", "class": "form-control"}
    )
    
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={"placeholder": "Enter email address", "class": "form-control", "type": "email"}
    )
    
    phone = StringField(
        'Phone Numbekkkkr',
        render_kw={"placeholder": "Enter last name", "class": "form-control"}
    )
    
    # Address Information
    address = TextAreaField(
        'Street Address',
        validators=[Optional()],
        render_kw={"placeholder": "Enter street address", "class": "form-control", "rows": 3}
    )
    
    city = StringField(
        'City',
        validators=[
            Optional(),
            Length(max=50, message="City must be less than 50 characters")
        ],
        render_kw={"placeholder": "Enter city", "class": "form-control"}
    )
    
    state = StringField(
        'State/Province',
        validators=[
            Optional(),
            Length(max=50, message="State must be less than 50 characters")
        ],
        render_kw={"placeholder": "Enter state or province", "class": "form-control"}
    )
    
    zip_code = StringField(
        'ZIP/Postal Code',
        validators=[
            Optional(),
            Length(max=10, message="ZIP code must be less than 10 characters")
        ],
        render_kw={"placeholder": "Enter ZIP or postal code", "class": "form-control"}
    )
    
    country = SelectField(
        'Country',
        choices=[
            ('USA', 'United States'),
            ('Canada', 'Canada'),
            ('UK', 'United Kingdom'),
            ('Australia', 'Australia'),
            ('Germany', 'Germany'),
            ('France', 'France'),
            ('Japan', 'Japan'),
            ('China', 'China'),
            ('India', 'India'),
            ('Brazil', 'Brazil'),
            ('Mexico', 'Mexico'),
            ('Other', 'Other')
        ],
        default='USA',
        validators=[Optional()],
        render_kw={"class": "form-control"}
    )
    
    # Status fields (for admin use)
    is_active = BooleanField(
        'Active Customer',
        default=True,
        render_kw={"class": "form-check-input"}
    )
    
    is_verified = BooleanField(
        'Verified Customer',
        default=False,
        render_kw={"class": "form-check-input"}
    )
    
    # Newsletter and preferences
    newsletter_subscribed = BooleanField(
        'Newsletter Subscription',
        default=True,
        render_kw={"class": "form-check-input"}
    )
    
    preferred_language = SelectField(
        'Preferred Language',
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('it', 'Italian'),
            ('pt', 'Portuguese'),
            ('zh', 'Chinese'),
            ('ja', 'Japanese'),
            ('ko', 'Korean'),
            ('ar', 'Arabic')
        ],
        default='en',
        validators=[Optional()],
        render_kw={"class": "form-control"}
    )
    
    # Additional fields
    notes = TextAreaField(
        'Notes',
        validators=[Optional()],
        render_kw={"placeholder": "Internal notes about this customer", "class": "form-control", "rows": 3}
    )
    
    tags = StringField(
        'Tags',
        validators=[Optional()],
        render_kw={"placeholder": "Comma-separated tags (e.g., VIP, Wholesale, etc.)", "class": "form-control"}
    )
    
    # Submit button
    submit = SubmitField(
        'Save Customer',
        render_kw={"class": "btn btn-primary"}
    )
    
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
    
    def validate(self, extra_validators=None):
        """Custom validation"""
        if not super(CustomerForm, self).validate(extra_validators):
            return False
        
        # Additional custom validations can be added here
        return True


class CustomerSearchForm(FlaskForm):
    """
    Form for searching customers
    """
    search = StringField(
        'Search Customers',
        validators=[Optional()],
        render_kw={
            "placeholder": "Search by name or email...", 
            "class": "form-control",
            "autocomplete": "off"
        }
    )
    
    status = SelectField(
        'Status',
        choices=[
            ('all', 'All Customers'),
            ('active', 'Active Only'),
            ('inactive', 'Inactive Only'),
            ('verified', 'Verified Only'),
            ('unverified', 'Unverified Only')
        ],
        default='all',
        render_kw={"class": "form-control"}
    )
    
    country = SelectField(
        'Country',
        choices=[
            ('all', 'All Countries'),
            ('USA', 'United States'),
            ('Canada', 'Canada'),
            ('UK', 'United Kingdom'),
            ('Australia', 'Australia'),
            ('Germany', 'Germany'),
            ('France', 'France'),
            ('Japan', 'Japan'),
            ('China', 'China'),
            ('India', 'India'),
            ('Brazil', 'Brazil'),
            ('Mexico', 'Mexico'),
            ('Other', 'Other')
        ],
        default='all',
        render_kw={"class": "form-control"}
    )
    
    submit = SubmitField(
        'Search',
        render_kw={"class": "btn btn-outline-primary"}
    )


class CustomerQuickForm(FlaskForm):
    """
    Quick form for adding basic customer information
    """
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message="First name is required"),
            Length(min=2, max=50)
        ],
        render_kw={"placeholder": "First name", "class": "form-control form-control-sm"}
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Last name is required"),
            Length(min=2, max=50)
        ],
        render_kw={"placeholder": "Last name", "class": "form-control form-control-sm"}
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required")
        ],
        render_kw={"placeholder": "Email address", "class": "form-control form-control-sm"}
    )
    
    phone = StringField(
        'Phone',
        validators=[Optional()],
        render_kw={"placeholder": "Phone number", "class": "form-control form-control-sm"}
    )
    
    submit = SubmitField(
        'Add Customer',
        render_kw={"class": "btn btn-success btn-sm"}
    )


class CustomerDeleteForm(FlaskForm):
    """
    Form for confirming customer deletion
    """
    customer_id = StringField(
        'Customer ID',
        validators=[DataRequired()],
        render_kw={"type": "hidden"}
    )
    
    confirm = BooleanField(
        'I confirm that I want to delete this customer',
        validators=[DataRequired(message="Please confirm the deletion")],
        render_kw={"class": "form-check-input"}
    )
    
    submit = SubmitField(
        'Delete Customer',
        render_kw={"class": "btn btn-danger"}
    )


class CustomerBulkActionForm(FlaskForm):
    """
    Form for bulk actions on customers
    """
    action = SelectField(
        'Action',
        choices=[
            ('activate', 'Activate Selected'),
            ('deactivate', 'Deactivate Selected'),
            ('verify', 'Verify Selected'),
            ('unverify', 'Unverify Selected'),
            ('delete', 'Delete Selected')
        ],
        validators=[DataRequired(message="Please select an action")],
        render_kw={"class": "form-control"}
    )
    
    selected_customers = StringField(
        'Selected Customers',
        validators=[DataRequired(message="Please select at least one customer")],
        render_kw={"type": "hidden"}
    )
    
    submit = SubmitField(
        'Apply Action',
        render_kw={"class": "btn btn-warning"}
    )


# Form validation helper functions
def validate_customer_form_data(form_data):
    """
    Validate customer form data and return cleaned data
    """
    cleaned_data = {}
    
    # Clean and validate each field
    for field_name, field_value in form_data.items():
        if field_name in ['first_name', 'last_name', 'email']:
            # Required fields
            if not field_value or not field_value.strip():
                raise ValueError(f"{field_name.replace('_', ' ').title()} is required")
            cleaned_data[field_name] = field_value.strip()
        elif field_name in ['phone', 'address', 'city', 'state', 'zip_code', 'country']:
            # Optional fields
            cleaned_data[field_name] = field_value.strip() if field_value else None
        elif field_name in ['is_active', 'is_verified']:
            # Boolean fields
            cleaned_data[field_name] = bool(field_value)
    
    return cleaned_data


def prepare_form_choices():
    """
    Prepare dynamic choices for form fields (e.g., from database)
    This function can be expanded to load countries, states, etc. from database
    """
    countries = [
        ('USA', 'United States'),
        ('Canada', 'Canada'),
        ('UK', 'United Kingdom'),
        ('Australia', 'Australia'),
        ('Germany', 'Germany'),
        ('France', 'France'),
        ('Japan', 'Japan'),
        ('China', 'China'),
        ('India', 'India'),
        ('Brazil', 'Brazil'),
        ('Mexico', 'Mexico'),
        ('Other', 'Other')
    ]
    
    return {
        'countries': countries
    }
