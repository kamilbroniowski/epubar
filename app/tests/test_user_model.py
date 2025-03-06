"""
Tests for the User model
"""
import json
import pytest
from app.models.user import User
from app.models.db import db

def test_new_user(db):
    """Test creating a new user"""
    # Create a new user
    user = User(
        username='newuser',
        email='new@example.com'
    )
    db.session.add(user)
    db.session.commit()
    
    # Verify user was created correctly
    fetched_user = User.query.filter_by(username='newuser').first()
    assert fetched_user is not None
    assert fetched_user.username == 'newuser'
    assert fetched_user.email == 'new@example.com'
    
    # Test default preferences are set
    preferences = fetched_user.user_preferences
    assert isinstance(preferences, dict)
    assert 'theme' in preferences
    assert 'font_family' in preferences
    assert 'font_size' in preferences
    assert 'line_spacing' in preferences
    assert 'margin' in preferences
    assert 'highlight_colors' in preferences

def test_user_preferences_getter_setter(db):
    """Test the getter and setter for user preferences"""
    # Create a new user
    user = User(
        username='prefuser',
        email='pref@example.com'
    )
    db.session.add(user)
    db.session.commit()
    
    # Test updating preferences
    new_preferences = {
        'theme': 'dark',
        'font_family': 'sans-serif',
        'font_size': 18,
        'line_spacing': 2.0,
        'margin': 1.5,
        'highlight_colors': ['#ff0000', '#00ff00', '#0000ff']
    }
    
    user.user_preferences = new_preferences
    db.session.commit()
    
    # Fetch the user and check preferences
    fetched_user = User.query.filter_by(username='prefuser').first()
    fetched_preferences = fetched_user.user_preferences
    
    assert fetched_preferences['theme'] == 'dark'
    assert fetched_preferences['font_family'] == 'sans-serif'
    assert fetched_preferences['font_size'] == 18
    assert fetched_preferences['line_spacing'] == 2.0
    assert fetched_preferences['margin'] == 1.5
    assert fetched_preferences['highlight_colors'] == ['#ff0000', '#00ff00', '#0000ff']

def test_invalid_preferences_type(db):
    """Test that setting invalid preferences raises an error"""
    user = User(
        username='invalidpref',
        email='invalid@example.com'
    )
    db.session.add(user)
    db.session.commit()
    
    # Test setting invalid preferences
    with pytest.raises(ValueError):
        user.user_preferences = "invalid"

def test_user_repr(db):
    """Test the string representation of a User object"""
    user = User(
        username='repruser',
        email='repr@example.com'
    )
    
    assert repr(user) == '<User repruser>'
