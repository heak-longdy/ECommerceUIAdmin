"""
ClassRoom Model for Flask-SQLAlchemy
Defines the ClassRoom database model and service for educational management
Enhanced with Flask-specific features, validation, and utilities
"""

from datetime import datetime
from sqlalchemy import func, event
from sqlalchemy.exc import IntegrityError
from flask import current_app
import re
import uuid
from src.db import db


class ClassRoom(db.Model):
    """
    ClassRoom model for storing classroom information
    Enhanced with validation, hooks, and utility methods
    """
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Unique identifier for external references
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # ClassRoom basic information
    name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    building = db.Column(db.String(50), nullable=True)
    floor = db.Column(db.Integer, nullable=True)
    
    # Capacity and specifications
    capacity = db.Column(db.Integer, nullable=False, default=30)
    current_occupancy = db.Column(db.Integer, nullable=False, default=0)
    
    # Equipment and features
    has_projector = db.Column(db.Boolean, default=False, nullable=False)
    has_whiteboard = db.Column(db.Boolean, default=True, nullable=False)
    has_computer = db.Column(db.Boolean, default=False, nullable=False)
    has_air_conditioning = db.Column(db.Boolean, default=True, nullable=False)
    has_audio_system = db.Column(db.Boolean, default=False, nullable=False)
    
    # Status and availability
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False, index=True)
    maintenance_status = db.Column(db.String(20), default='good', nullable=False)  # good, needs_repair, under_maintenance
    
    # Classification
    room_type = db.Column(db.String(30), default='lecture', nullable=False)  # lecture, lab, seminar, conference
    department = db.Column(db.String(50), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_used_at = db.Column(db.DateTime, nullable=True)
    
    # Additional information
    description = db.Column(db.Text, nullable=True)
    special_features = db.Column(db.Text, nullable=True)
    access_requirements = db.Column(db.String(255), nullable=True)
    
    def __init__(self, **kwargs):
        """Initialize ClassRoom instance"""
        super(ClassRoom, self).__init__(**kwargs)
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
    
    def __repr__(self):
        """String representation of ClassRoom"""
        return f'<ClassRoom {self.id}: {self.room_number}>'
    
    def __str__(self):
        """Human-readable string representation"""
        return f'{self.name} ({self.room_number})'
    
    @property
    def full_name(self):
        """Get classroom's full name with room number"""
        return f'{self.name} ({self.room_number})'
