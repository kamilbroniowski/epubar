"""
User model for storing user data and preferences
"""
from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from app.models.db import db

class User(db.Model):
    """User model representing application users"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    preferences = Column(JSON, default=lambda: json.dumps({
        'theme': 'light',
        'font_family': 'serif',
        'font_size': 16,
        'line_spacing': 1.5,
        'margin': 1.0,
        'highlight_colors': ['#ffff00', '#90ee90', '#add8e6', '#ffc0cb']
    }))
    
    # Relationships
    books = relationship('Book', back_populates='user')
    annotations = relationship('Annotation', back_populates='user')
    reading_states = relationship('ReadingState', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def user_preferences(self):
        """Return the user preferences as a Python dictionary"""
        if isinstance(self.preferences, str):
            return json.loads(self.preferences)
        return self.preferences
    
    @user_preferences.setter
    def user_preferences(self, preferences_dict):
        """Set user preferences from a Python dictionary"""
        if isinstance(preferences_dict, dict):
            self.preferences = json.dumps(preferences_dict)
        else:
            raise ValueError("Preferences must be a dictionary")
