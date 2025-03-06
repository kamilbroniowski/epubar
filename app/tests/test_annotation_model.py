"""
Tests for the Annotation model
"""
import pytest
import json
from datetime import datetime
from app.models.annotation import Annotation, AnnotationType
from app.models.book import Book
from app.models.user import User
from app.models.db import db

@pytest.fixture
def test_book(db, test_user):
    """Create a test book for annotation tests"""
    book = Book(
        user_id=test_user.id,
        title='Annotation Test Book',
        author='Annotation Author',
        file_path='/uploads/annotation_test.epub',
        total_pages=250
    )
    db.session.add(book)
    db.session.commit()
    return book

def test_new_highlight_annotation(db, test_user, test_book):
    """Test creating a new highlight annotation"""
    # Create position data as it would be stored
    position_data = json.dumps({
        'startContainer': '/html/body/p[3]',
        'startOffset': 12,
        'endContainer': '/html/body/p[3]',
        'endOffset': 42,
        'text': 'This is the highlighted text'
    })
    
    # Create a new highlight annotation
    annotation = Annotation(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.HIGHLIGHT,
        color='#ffff00',  # Yellow
        position_data=position_data,
        chapter_index=2
    )
    db.session.add(annotation)
    db.session.commit()
    
    # Verify annotation was created correctly
    fetched_annotation = Annotation.query.filter_by(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.HIGHLIGHT
    ).first()
    
    assert fetched_annotation is not None
    assert fetched_annotation.user_id == test_user.id
    assert fetched_annotation.book_id == test_book.id
    assert fetched_annotation.type == AnnotationType.HIGHLIGHT
    assert fetched_annotation.color == '#ffff00'
    assert fetched_annotation.chapter_index == 2
    
    # Verify position data
    position = json.loads(fetched_annotation.position_data)
    assert position['text'] == 'This is the highlighted text'
    assert position['startOffset'] == 12
    assert position['endOffset'] == 42

def test_new_note_annotation(db, test_user, test_book):
    """Test creating a new note annotation"""
    # Create position data
    position_data = json.dumps({
        'startContainer': '/html/body/p[5]',
        'startOffset': 8,
        'endContainer': '/html/body/p[5]',
        'endOffset': 25,
        'text': 'Text with a note'
    })
    
    # Create a new note annotation
    annotation = Annotation(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.NOTE,
        content='This is a note about the selected text',
        position_data=position_data,
        chapter_index=3
    )
    db.session.add(annotation)
    db.session.commit()
    
    # Verify annotation was created correctly
    fetched_annotation = Annotation.query.filter_by(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.NOTE
    ).first()
    
    assert fetched_annotation is not None
    assert fetched_annotation.content == 'This is a note about the selected text'
    assert fetched_annotation.chapter_index == 3
    
    # Verify position data
    position = json.loads(fetched_annotation.position_data)
    assert position['text'] == 'Text with a note'

def test_new_bookmark_annotation(db, test_user, test_book):
    """Test creating a new bookmark annotation"""
    # Create position data
    position_data = json.dumps({
        'chapter': 'Chapter 4',
        'position': 'top',
        'elementId': 'chapter-4-header'
    })
    
    # Create a new bookmark annotation
    annotation = Annotation(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.BOOKMARK,
        content='Chapter 4 - Important section',
        position_data=position_data,
        chapter_index=4
    )
    db.session.add(annotation)
    db.session.commit()
    
    # Verify annotation was created correctly
    fetched_annotation = Annotation.query.filter_by(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.BOOKMARK
    ).first()
    
    assert fetched_annotation is not None
    assert fetched_annotation.content == 'Chapter 4 - Important section'
    assert fetched_annotation.chapter_index == 4

def test_annotation_relationships(db, test_user, test_book):
    """Test the relationships between Annotation, User, and Book"""
    # Create a new annotation
    annotation = Annotation(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.HIGHLIGHT,
        color='#90ee90',  # Light green
        position_data=json.dumps({'text': 'Relationship test'}),
        chapter_index=1
    )
    db.session.add(annotation)
    db.session.commit()
    
    # Test annotation-user relationship
    fetched_annotation = Annotation.query.filter_by(color='#90ee90').first()
    assert fetched_annotation.user == test_user
    assert fetched_annotation in test_user.annotations
    
    # Test annotation-book relationship
    assert fetched_annotation.book == test_book
    assert fetched_annotation in test_book.annotations

def test_annotation_repr(db, test_user, test_book):
    """Test the string representation of an Annotation object"""
    annotation = Annotation(
        user_id=test_user.id,
        book_id=test_book.id,
        type=AnnotationType.HIGHLIGHT,
        position_data=json.dumps({'text': 'Repr test'}),
        chapter_index=1
    )
    
    assert 'Annotation' in repr(annotation)
    assert 'HIGHLIGHT' in repr(annotation)
