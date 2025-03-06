"""
Tests for the ReadingState model
"""
import pytest
from datetime import datetime, timedelta
from app.models.reading_state import ReadingState
from app.models.book import Book
from app.models.user import User
from app.models.db import db

@pytest.fixture
def test_book(db, test_user):
    """Create a test book for reading state tests"""
    book = Book(
        user_id=test_user.id,
        title='Reading State Test Book',
        author='Reading State Author',
        file_path='/uploads/reading_state_test.epub',
        total_pages=300
    )
    db.session.add(book)
    db.session.commit()
    return book

def test_new_reading_state(db, test_user, test_book):
    """Test creating a new reading state"""
    # Create a new reading state
    reading_state = ReadingState(
        user_id=test_user.id,
        book_id=test_book.id,
        current_position='chapter-1',
        progress_percent=10.5
    )
    db.session.add(reading_state)
    db.session.commit()
    
    # Verify reading state was created correctly
    fetched_state = ReadingState.query.filter_by(book_id=test_book.id).first()
    assert fetched_state is not None
    assert fetched_state.user_id == test_user.id
    assert fetched_state.book_id == test_book.id
    assert fetched_state.current_position == 'chapter-1'
    assert fetched_state.progress_percent == 10.5
    assert isinstance(fetched_state.last_read_at, datetime)
    assert isinstance(fetched_state.created_at, datetime)
    assert isinstance(fetched_state.updated_at, datetime)

def test_reading_state_relationships(db, test_user, test_book):
    """Test the relationships between ReadingState, User, and Book"""
    # Create a new reading state
    reading_state = ReadingState(
        user_id=test_user.id,
        book_id=test_book.id,
        current_position='chapter-2',
        progress_percent=25.0
    )
    db.session.add(reading_state)
    db.session.commit()
    
    # Test reading_state-user relationship
    fetched_state = ReadingState.query.filter_by(book_id=test_book.id).first()
    assert fetched_state.user == test_user
    assert fetched_state in test_user.reading_states
    
    # Test reading_state-book relationship
    assert fetched_state.book == test_book
    assert test_book.reading_state == fetched_state

def test_update_reading_state(db, test_user, test_book):
    """Test updating a reading state"""
    # Create a new reading state
    reading_state = ReadingState(
        user_id=test_user.id,
        book_id=test_book.id,
        current_position='chapter-1',
        progress_percent=10.5
    )
    db.session.add(reading_state)
    db.session.commit()
    
    # Record the current timestamps
    initial_updated_at = reading_state.updated_at
    initial_last_read_at = reading_state.last_read_at
    
    # Wait a bit to ensure timestamps will be different
    import time
    time.sleep(0.1)
    
    # Update the reading state
    reading_state.current_position = 'chapter-3'
    reading_state.progress_percent = 35.8
    reading_state.last_read_at = datetime.utcnow()
    db.session.commit()
    
    # Verify updates
    fetched_state = ReadingState.query.filter_by(book_id=test_book.id).first()
    assert fetched_state.current_position == 'chapter-3'
    assert fetched_state.progress_percent == 35.8
    assert fetched_state.updated_at > initial_updated_at
    assert fetched_state.last_read_at > initial_last_read_at

def test_reading_state_repr(db, test_user, test_book):
    """Test the string representation of a ReadingState object"""
    reading_state = ReadingState(
        user_id=test_user.id,
        book_id=test_book.id,
        current_position='chapter-1',
        progress_percent=10.5
    )
    
    assert repr(reading_state) == f'<ReadingState {test_book.id} - 10.5%>'
