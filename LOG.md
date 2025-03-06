# EPUBAR Development LOG

## Architecture Decisions

### 2025-03-06 19:40: Initial Project Setup
- Implemented modular architecture with clear separation of concerns
- Selected Flask as the web framework for its simplicity and flexibility
- Using SQLAlchemy ORM for database operations with SQLite backend
- Adopting a monochrome design except for highlights/notes as specified
- Following Test-Driven Development methodology for all features

### 2025-03-06 19:42: Database Schema
- Created models for Users, Books, Annotations, and ReadingStates
- Using JSON field for user preferences to allow for flexible configuration
- Designed annotation system with position tracking for reliable retrieval
- Implemented efficient indexes for frequent queries

### 2025-03-06 19:46: Docker Environment
- Switched from Python 3.13 to Python 3.11 in Docker for better package compatibility
- Added explicit system dependencies for Pillow and other packages
- Configured proper image building process using pip wheel

### 2025-03-06 19:48: Application Structure
- Implemented Flask application factory pattern for better testability
- Organized routes into blueprint modules (main, library, reader, api)
- Centralized application configuration in app/__init__.py
- Created simplified app.py entry point

### 2025-03-06 19:51: Database Configuration Fix
- Updated Flask-SQLAlchemy configuration to use the correct keys
- Changed DATABASE_URL to SQLALCHEMY_DATABASE_URI in configuration
- Added SQLALCHEMY_TRACK_MODIFICATIONS setting
- Fixed import paths and application structure for better testability

### 2025-03-06 19:52: Test Suite Success
- Modified Book model test to be resilient to microsecond differences in timestamps
- Successfully running all tests in Docker environment
- 17 tests passing, 7 skipped (EPUB processor tests not yet implemented)

## Implementation Notes

### EPUB Processing
- Using ebooklib for EPUB extraction and parsing
- Implementing custom utilities for handling EPUB content rendering
- Supporting embedded images and formatting for a complete reading experience

### Text Interaction
- Designing selection mechanism compatible with pagination
- Implementing position tracking system for reliable annotation placement
- Creating color-coding system for different types of highlights
