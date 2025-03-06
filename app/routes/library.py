"""
Library routes for EPUBAR application
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from app.models.db import db
from app.models.book import Book
from app.models.user import User
from app.models.reading_state import ReadingState
from app.utils.epub.processor import EPUBProcessor
from app.utils.epub.metadata import MetadataExtractor

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
    
    # Get all books with reading state information
    books = Book.query.filter_by(user_id=user.id).all()
    
    # Add reading state for each book
    for book in books:
        reading_state = ReadingState.query.filter_by(
            user_id=user.id,
            book_id=book.id
        ).first()
        
        if reading_state:
            book.reading_state = reading_state
            # Calculate progress percentage
            if reading_state.current_position:
                state_parts = reading_state.current_position.split(':')
                if len(state_parts) >= 2:
                    current_spine = int(state_parts[0])
                    # This is a simplified calculation
                    reading_state.progress_percent = min(int(current_spine * 100 / 10), 100)  # Assuming 10 chapters on average
                else:
                    reading_state.progress_percent = 0
            else:
                reading_state.progress_percent = 0
    
    return render_template('library/index.html', books=books, user=user)

@library_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle EPUB file uploads"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'epub_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['epub_file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        # Check file extension
        if not file.filename.lower().endswith('.epub'):
            flash('Only EPUB files are allowed', 'error')
            return redirect(request.url)
        
        # For simplicity, we're using a default user for now
        user = User.query.first()
        if not user:
            user = User(username='default', email='default@example.com')
            db.session.add(user)
            db.session.commit()
        
        # Save the file with a secure filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        try:
            # Process the EPUB file
            processor = EPUBProcessor()
            extracted_path = processor.extract(file_path)
            
            # Get metadata from the EPUB
            container_path = os.path.join(extracted_path, 'META-INF/container.xml')
            extractor = MetadataExtractor()
            opf_path = extractor.get_opf_path(container_path)
            opf_full_path = os.path.join(extracted_path, opf_path)
            metadata = extractor.extract_from_opf(opf_full_path)
            
            # Create book record in database
            book = Book(
                user_id=user.id,
                title=metadata.get('title', 'Unknown Title'),
                author=metadata.get('creator', 'Unknown Author'),
                file_path=file_path,
                language=metadata.get('language', 'en'),
                publisher=metadata.get('publisher', ''),
                publication_date=metadata.get('date', ''),
                description=metadata.get('description', ''),
                isbn=metadata.get('identifier', ''),
                cover_path=''  # We'll handle cover extraction separately in future
            )
            
            db.session.add(book)
            db.session.commit()
            
            # Create initial reading state
            reading_state = ReadingState(
                user_id=user.id,
                book_id=book.id,
                current_position="0:0",  # Start at the beginning
                is_finished=False
            )
            
            db.session.add(reading_state)
            db.session.commit()
            
            flash(f'Book "{book.title}" uploaded successfully', 'success')
            
            # Redirect to reader
            return redirect(url_for('reader.read', book_id=book.id))
            
        except Exception as e:
            flash(f'Error processing EPUB file: {str(e)}', 'error')
            # Clean up uploaded file if there was an error
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(request.url)
    
    return render_template('library/upload.html')

@library_bp.route('/book/<int:book_id>')
def view_book(book_id):
    """View book details"""
    book = Book.query.get_or_404(book_id)
    return render_template('library/book_details.html', book=book)
