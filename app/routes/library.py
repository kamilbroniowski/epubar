"""
Library routes for EPUBAR application
"""
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models.db import db
from app.models.book import Book
from app.models.user import User

# Create blueprint
library_bp = Blueprint('library', __name__)

@library_bp.route('/')
def index():
    """Render the library main page with all books"""
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
    
    books = Book.query.filter_by(user_id=user.id).all()
    return render_template('library/index.html', books=books, user=user)

@library_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle EPUB file uploads"""
    if request.method == 'POST':
        # File upload handling will be implemented here
        return redirect(url_for('library.index'))
    
    return render_template('library/upload.html')

@library_bp.route('/book/<int:book_id>')
def view_book(book_id):
    """View book details"""
    book = Book.query.get_or_404(book_id)
    return render_template('library/book_details.html', book=book)
