"""
API routes for EPUBAR application
"""
from flask import Blueprint, jsonify, request
from app.models.db import db
from app.models.book import Book
from app.models.annotation import Annotation
from app.models.reading_state import ReadingState

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books for the current user"""
    # In a real app, we would use authentication to get the user
    # For now, we're assuming user_id = 1
    user_id = 1
    books = Book.query.filter_by(user_id=user_id).all()
    
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'cover_path': book.cover_path,
            'file_path': book.file_path,
            'added_at': book.created_at.isoformat()
        })
    
    return jsonify(result)

@api_bp.route('/annotations', methods=['POST'])
def create_annotation():
    """Create a new annotation"""
    data = request.json
    
    annotation = Annotation(
        user_id=data.get('user_id', 1),  # Default user_id for now
        book_id=data['book_id'],
        content=data.get('content', ''),
        cfi_range=data['cfi_range'],
        type=data.get('type', 'highlight'),
        color=data.get('color', '#ffff00'),
        text=data.get('text', '')
    )
    
    db.session.add(annotation)
    db.session.commit()
    
    return jsonify({
        'id': annotation.id,
        'status': 'success'
    }), 201

@api_bp.route('/annotations/<int:annotation_id>', methods=['DELETE'])
def delete_annotation(annotation_id):
    """Delete an annotation"""
    annotation = Annotation.query.get_or_404(annotation_id)
    
    db.session.delete(annotation)
    db.session.commit()
    
    return jsonify({'status': 'success'}), 200
