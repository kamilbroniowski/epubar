"""
Main routes for EPUBAR application
"""
from flask import Blueprint, render_template, current_app, redirect, url_for
from app.models.db import db
from app.models.user import User
from app.models.book import Book
from app.models.reading_state import ReadingState

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the application home page"""
    # Get recent books for the current user
    # For simplicity, we're using a default user_id for now
    user_id = 1
    
    # Get books with recent reading activity
    recent_states = ReadingState.query.filter_by(user_id=user_id)\
        .order_by(ReadingState.last_read_at.desc())\
        .limit(4).all()
        
    recent_books = []
    for state in recent_states:
        book = db.session.get(Book, state.book_id)
        if book:
            # Add reading progress
            state_parts = state.current_position.split(':')
            if len(state_parts) >= 2:
                current_spine = int(state_parts[0])
                # We'd need to get the total number of spine items for accurate progress
                # This is a simplified calculation
                book.reading_state = state
                book.reading_state.progress_percent = min(int(current_spine * 100 / 10), 100)  # Assuming 10 chapters
            recent_books.append(book)
    
    return render_template('main/index.html', recent_books=recent_books)

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
