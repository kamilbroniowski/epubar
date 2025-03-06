"""
Main routes for EPUBAR application
"""
from flask import Blueprint, render_template, current_app, redirect, url_for
from app.models.db import db
from app.models.user import User

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the application home page"""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@main_bp.route('/settings')
def settings():
    """Render the settings page"""
    # For simplicity, we're using a default user for now
    # In a real app, we would use authentication
    user = User.query.first()
    if not user:
        # Create default user if none exists
        user = User(
            username='default',
            email='default@example.com'
        )
        db.session.add(user)
        db.session.commit()
    
    return render_template('settings.html', user=user)
