"""
ClassRoom Forms for Flask-WTF
Defines forms for classroom management with validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp, ValidationError
from wtforms.widgets import TextArea
from src.db import db


class ClassRoomForm(FlaskForm):
    """Main form for creating and editing classrooms"""
    # ...existing code...
