"""
Tests for the Book model
"""
import pytest
from datetime import datetime
from app.models.book import Book
from app.models.user import User
from app.models.db import db

def test_new_book(db, test_user):
    """Test creating a new book"""
    # Create a new book
    book = Book(
        user_id=test_user.id,
        title='Test Book',
        author='Test Author',
        publisher='Test Publisher',
        language='en',
        identifier='978-3-16-148410-0',
        publication_date='2023-01-01',
        description='A test book description',
        file_path='/uploads/test.epub',
        cover_path='/uploads/covers/test.jpg',
        file_size=1024000,
        total_pages=200
    )
    db.session.add(book)
    db.session.commit()
    
    # Verify book was created correctly
    fetched_book = Book.query.filter_by(title='Test Book').first()
    assert fetched_book is not None
    assert fetched_book.title == 'Test Book'
    assert fetched_book.author == 'Test Author'
    assert fetched_book.publisher == 'Test Publisher'
    assert fetched_book.language == 'en'
    assert fetched_book.identifier == '978-3-16-148410-0'
    assert fetched_book.publication_date == '2023-01-01'
    assert fetched_book.description == 'A test book description'
    assert fetched_book.file_path == '/uploads/test.epub'
    assert fetched_book.cover_path == '/uploads/covers/test.jpg'
    assert fetched_book.file_size == 1024000
    assert fetched_book.total_pages == 200
    assert fetched_book.user_id == test_user.id

def test_book_user_relationship(db, test_user):
    """Test the relationship between Book and User"""
    # Create a new book for the test user
    book = Book(
        user_id=test_user.id,
        title='Relationship Test Book',
        author='Relationship Author',
        file_path='/uploads/relationship_test.epub'
    )
    db.session.add(book)
    db.session.commit()
    
    # Test book-user relationship
    fetched_book = Book.query.filter_by(title='Relationship Test Book').first()
    assert fetched_book.user == test_user
    assert book in test_user.books

def test_book_timestamps(db, test_user):
    """Test that timestamps are created correctly"""
    # Create a new book
    book = Book(
        user_id=test_user.id,
        title='Timestamp Test Book',
        author='Timestamp Author',
        file_path='/uploads/timestamp_test.epub'
    )
    db.session.add(book)
    db.session.commit()
    
    # Verify timestamps
    fetched_book = Book.query.filter_by(title='Timestamp Test Book').first()
    assert isinstance(fetched_book.created_at, datetime)
    assert isinstance(fetched_book.updated_at, datetime)
    
    # created_at and updated_at should be very close on creation
    assert (datetime.utcnow() - fetched_book.created_at).total_seconds() < 60
    # Check if timestamps are within 1 millisecond of each other
    time_diff = abs((fetched_book.created_at - fetched_book.updated_at).total_seconds())
    assert time_diff < 0.001, f"Timestamps differ by {time_diff} seconds"

def test_book_repr(db, test_user):
    """Test the string representation of a Book object"""
    book = Book(
        user_id=test_user.id,
        title='Repr Test Book',
        author='Repr Author',
        file_path='/uploads/repr_test.epub'
    )
    
    assert repr(book) == '<Book Repr Test Book by Repr Author>'
