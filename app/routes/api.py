"""
API routes for EPUBAR application
"""
import os
import json
from flask import Blueprint, jsonify, request, current_app, send_file, safe_join
from app.models.db import db
from app.models.book import Book
from app.models.annotation import Annotation
from app.models.reading_state import ReadingState
from app.utils.epub.processor import EPUBProcessor
from app.utils.epub.metadata import MetadataExtractor
from app.utils.epub.content import ContentProcessor

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


@api_bp.route('/books/<int:book_id>/spine', methods=['GET'])
def get_book_spine(book_id):
    """Get the spine (table of contents) for a book"""
    book = Book.query.get_or_404(book_id)
    
    # Initialize the EPUB processor
    processor = EPUBProcessor()
    extracted_path = processor.extract(book.file_path)
    
    # Get the container.xml path
    container_path = os.path.join(extracted_path, 'META-INF/container.xml')
    
    # Initialize the metadata extractor
    extractor = MetadataExtractor()
    opf_path = extractor.get_opf_path(container_path)
    opf_dir = os.path.dirname(os.path.join(extracted_path, opf_path))
    opf_full_path = os.path.join(extracted_path, opf_path)
    
    # Extract spine items
    spine_items = extractor.extract_spine(opf_full_path)
    
    # Format spine items for the API response
    result = []
    for i, item in enumerate(spine_items):
        result.append({
            'id': item['idref'],
            'index': i,
            'href': item['href'],
            'media_type': item.get('media-type', 'application/xhtml+xml'),
            'title': item.get('title', f'Chapter {i+1}')
        })
    
    return jsonify({
        'book_id': book_id,
        'spine': result
    })


@api_bp.route('/books/<int:book_id>/content/<string:item_id>', methods=['GET'])
def get_book_content(book_id, item_id):
    """Get the content for a specific spine item"""
    book = Book.query.get_or_404(book_id)
    
    # Initialize the EPUB processor
    processor = EPUBProcessor()
    extracted_path = processor.extract(book.file_path)
    
    # Get the container.xml path
    container_path = os.path.join(extracted_path, 'META-INF/container.xml')
    
    # Initialize the metadata extractor
    extractor = MetadataExtractor()
    opf_path = extractor.get_opf_path(container_path)
    opf_dir = os.path.dirname(os.path.join(extracted_path, opf_path))
    opf_full_path = os.path.join(extracted_path, opf_path)
    
    # Extract spine items to find the requested one
    spine_items = extractor.extract_spine(opf_full_path)
    
    # Find the requested item
    content_path = None
    for item in spine_items:
        if item['idref'] == item_id:
            content_path = os.path.join(opf_dir, item['href'])
            break
    
    if not content_path:
        return jsonify({'error': 'Item not found in book spine'}), 404
    
    # Process the content
    content_processor = ContentProcessor()
    processed_html = content_processor.process_content(
        content_path,
        opf_dir,
        add_data_attributes=True  # Add data attributes for annotation support
    )
    
    return processed_html


@api_bp.route('/books/<int:book_id>/annotations', methods=['POST'])
def create_book_annotation(book_id):
    """Create a new annotation for a book"""
    book = Book.query.get_or_404(book_id)
    data = request.json
    
    # Create the annotation
    annotation = Annotation(
        user_id=book.user_id,  # Use the book's user ID
        book_id=book_id,
        start_position=data['start_position'],
        end_position=data['end_position'],
        text=data.get('text', ''),
        note=data.get('note', ''),
        color=data.get('color', 'yellow')
    )
    
    db.session.add(annotation)
    db.session.commit()
    
    return jsonify({
        'id': annotation.id,
        'start_position': annotation.start_position,
        'end_position': annotation.end_position,
        'text': annotation.text,
        'note': annotation.note,
        'color': annotation.color,
        'created_at': annotation.created_at.isoformat() if annotation.created_at else None
    }), 201


@api_bp.route('/books/<int:book_id>/annotations/<int:annotation_id>', methods=['DELETE'])
def delete_book_annotation(book_id, annotation_id):
    """Delete an annotation for a book"""
    annotation = Annotation.query.filter_by(book_id=book_id, id=annotation_id).first_or_404()
    
    db.session.delete(annotation)
    db.session.commit()
    
    return jsonify({'status': 'success'}), 200


@api_bp.route('/books/<int:book_id>/cover', methods=['GET'])
def get_book_cover(book_id):
    """Get the cover image for a book"""
    book = Book.query.get_or_404(book_id)
    
    if not book.cover_path or not os.path.exists(book.cover_path):
        # Return a default cover
        return send_file(
            safe_join(current_app.static_folder, 'images/default-cover.jpg'),
            mimetype='image/jpeg'
        )
    
    return send_file(book.cover_path)
