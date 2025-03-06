"""EPUBAR - EPUB Library and Reader application module"""
import os
from flask import Flask
from app.models.db import db


def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                instance_relative_config=True,
                static_folder='static',
                template_folder='templates')
    
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///data/epubar.db'),
        UPLOAD_FOLDER=os.path.join(os.getcwd(), 'uploads'),
        MAX_CONTENT_LENGTH=50 * 1024 * 1024,  # 50MB max upload size
    )
    
    # Load test config if provided
    if test_config:
        app.config.update(test_config)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.library import library_bp
    from app.routes.reader import reader_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(library_bp, url_prefix='/library')
    app.register_blueprint(reader_bp, url_prefix='/reader')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
