"""
Test configuration for EPUBAR application
"""
import os
import tempfile
import pytest
from app import create_app
from app.models.db import db as _db
from app.models.user import User

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE_URL': f'sqlite:///{db_path}',
        'UPLOAD_FOLDER': tempfile.mkdtemp(),
        'WTF_CSRF_ENABLED': False,
    })
    
    # Create the database and the tables
    with app.app_context():
        _db.create_all()
        # Create a test user
        test_user = User(
            username='testuser',
            email='test@example.com'
        )
        _db.session.add(test_user)
        _db.session.commit()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)
    # Remove temporary upload folder
    os.rmdir(app.config['UPLOAD_FOLDER'])

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app"""
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    """Database session for testing"""
    with app.app_context():
        yield _db

@pytest.fixture
def test_user(db):
    """Get the test user"""
    user = User.query.filter_by(username='testuser').first()
    return user
