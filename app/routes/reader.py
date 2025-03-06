"""
Reader routes for EPUBAR application
"""
from flask import Blueprint, render_template, request, session, jsonify
from app.models.db import db
from app.models.book import Book
from app.models.reading_state import ReadingState
from app.models.annotation import Annotation

# Create blueprint
reader_bp = Blueprint('reader', __name__)

@reader_bp.route('/<int:book_id>')
def read(book_id):
    """Display the EPUB reader for a specific book"""
    book = Book.query.get_or_404(book_id)
    
    # Get or create reading state
    reading_state = ReadingState.query.filter_by(
        user_id=book.user_id, 
        book_id=book.id
    ).first()
    
    if not reading_state:
        reading_state = ReadingState(
            user_id=book.user_id,
            book_id=book.id,
            current_position="0:0",  # Format: spineIndex:elementIndex
            last_read_at=db.func.now()
        )
        db.session.add(reading_state)
        db.session.commit()
    
    # Get annotations for this book
    annotations = Annotation.query.filter_by(
        user_id=book.user_id,
        book_id=book.id
    ).all()
    
    return render_template('reader/index.html', 
                          book=book, 
                          reading_state=reading_state,
                          annotations=annotations)

@reader_bp.route('/<int:book_id>/state', methods=['POST'])
def update_state(book_id):
    """Update reading state for a book"""
    book = Book.query.get_or_404(book_id)
    data = request.json
    
    reading_state = ReadingState.query.filter_by(
        user_id=book.user_id,
        book_id=book.id
    ).first()
    
    if not reading_state:
        reading_state = ReadingState(
            user_id=book.user_id,
            book_id=book.id,
            current_position="0:0",
            last_read_at=db.func.now()
        )
        db.session.add(reading_state)
    
    # Update the reading state
    if 'position' in data:
        reading_state.current_position = data['position']
    
    if 'is_finished' in data:
        reading_state.is_finished = data['is_finished']
    
    # Update the last read timestamp
    reading_state.last_read_at = db.func.now()
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'position': reading_state.current_position,
        'is_finished': reading_state.is_finished
    })
