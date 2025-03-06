"""
Tests for the reader functionality in EPUBAR
"""
import pytest
from flask import url_for
from app.models.book import Book
from app.models.reading_state import ReadingState


def test_reader_page_loads(client, app, test_user, sample_book, db):
    """Test that the reader page loads properly for a valid book"""
    with app.app_context():
        # Create a test book
        book = Book(
            user_id=test_user.id,
            title="Test Book",
            author="Test Author",
            file_path=sample_book,
            language="en"
        )
        db.session.add(book)
        db.session.commit()
        
        # Create an initial reading state
        reading_state = ReadingState(
            user_id=test_user.id,
            book_id=book.id,
            current_position="0:0"
        )
        db.session.add(reading_state)
        db.session.commit() 
        # Test that the reader page loads
        response = client.get(f"/reader/{book.id}")
        assert response.status_code == 200
        assert book.title in response.data.decode('utf-8')
        
        # Check that the reading state and book info are in the page
        assert "bookId = " + str(book.id) in response.data.decode('utf-8')
        assert "currentPosition = " in response.data.decode('utf-8')


def test_reader_404_for_invalid_book(client):
    """Test that the reader returns 404 for an invalid book ID"""
    response = client.get("/reader/999999")  # Using a very high ID that shouldn't exist
    assert response.status_code == 404


def test_api_get_book_spine(client, app, test_user, sample_book, db):
    """Test the API endpoint for getting book spine"""
    with app.app_context():
        # Create a test book
        book = Book(
            user_id=test_user.id,
            title="Test Book",
            author="Test Author",
            file_path=sample_book,
            language="en"
        )
        db.session.add(book)
        db.session.commit()
        
        # Test the API endpoint
        response = client.get(f"/api/books/{book.id}/spine")
        assert response.status_code == 200
        
        # Parse the JSON response
        json_data = response.get_json()
        assert 'book_id' in json_data
        assert 'spine' in json_data
        assert isinstance(json_data['spine'], list)
        assert json_data['book_id'] == book.id


def test_api_get_book_content(client, app, test_user, sample_book, db):
    """Test the API endpoint for getting book content"""
    with app.app_context():
        # Create a test book
        book = Book(
            user_id=test_user.id,
            title="Test Book",
            author="Test Author",
            file_path=sample_book,
            language="en"
        )
        db.session.add(book)
        db.session.commit()
        
        # First get the spine to find an item ID
        response = client.get(f"/api/books/{book.id}/spine")
        json_data = response.get_json()
        
        # Make sure we have at least one spine item
        assert len(json_data['spine']) > 0
        
        # Get the first spine item ID
        item_id = json_data['spine'][0]['id']
        
        # Test the content API
        response = client.get(f"/api/books/{book.id}/content/{item_id}")
        assert response.status_code == 200
        
        # Make sure we got HTML content
        content = response.data.decode('utf-8')
        assert '<html' in content.lower() or '<body' in content.lower()


def test_update_reading_state(client, app, test_user, sample_book, db):
    """Test updating the reading state"""
    with app.app_context():
        # Create a test book
        book = Book(
            user_id=test_user.id,
            title="Test Book",
            author="Test Author",
            file_path=sample_book,
            language="en"
        )
        db.session.add(book)
        db.session.commit()
        
        # Create an initial reading state
        reading_state = ReadingState(
            user_id=test_user.id,
            book_id=book.id,
            current_position="0:0"
        )
        db.session.add(reading_state)
        db.session.commit()
        
        # Update the reading state
        new_position = "1:150"
        response = client.post(
            f"/reader/{book.id}/state",
            json={
                'position': new_position,
                'is_finished': False
            }
        )
        
        assert response.status_code == 200
        
        # Verify the state was updated in the database
        updated_state = ReadingState.query.filter_by(
            user_id=test_user.id,
            book_id=book.id
        ).first()
        
        assert updated_state.current_position == new_position
        assert updated_state.is_finished is False
