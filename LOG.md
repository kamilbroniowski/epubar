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

### 2025-03-06 20:05: EPUB Metadata Extraction Tests
- Implemented and enabled tests for EPUB metadata extraction functionality
- Successfully tested extraction of basic metadata (title, author, etc.) from OPF files
- Verified cover image identification within the EPUB package
- Implemented spine item extraction for navigation
- All tests now passing in our Docker testing environment

### 2025-03-06 20:13: HTML/CSS Content Processing
- Implemented ContentProcessor class for normalizing HTML content
- Added styling hooks and data attributes for annotation support
- Created tests for HTML normalization and verified functionality
- Implemented path fixing for relative URLs in HTML content
- Saved processed output to persistent storage for verification
- Successfully transformed EPUB HTML content for web rendering

### 2025-03-06 20:18: Real-world EPUB Testing
- Tested HTML/CSS processing with The Great Gatsby EPUB file
- Successfully extracted metadata (title, author, publication date, etc.)
- Verified spine item extraction for navigation
- Processed HTML content with proper path resolution
- Removed potentially harmful JavaScript
- Added styling hooks for consistent rendering
- All tests passing with both sample and real-world EPUB files

### 2025-03-06 20:22: Test Organization Improvements
- Created dedicated test resources directory for EPUB test files
- Moved Great Gatsby EPUB to app/tests/resources/ for better organization
- Updated test code to use the new file paths
- Enhanced Docker container setup with proper volume mounts for tests
- Improved project structure following testing best practices

### Text Interaction
- Designing selection mechanism compatible with pagination
- Implementing position tracking system for reliable annotation placement
- Creating color-coding system for different types of highlights

### 2025-03-06 20:34: EPUB Reader Implementation
- Created reader interface with chapter navigation and page controls
- Implemented theme switching (light, dark, and sepia modes)
- Added font size adjustments for better reading experience
- Designed annotation system for highlighting and taking notes
- Built JavaScript functionality for loading book content dynamically
- Implemented persistent reading state to remember user's position
- Added API endpoints for spine retrieval and content processing

### 2025-03-06 20:38: Library Management
- Created library interface for book management
- Implemented book upload with EPUB processing
- Added reading progress tracking on book cards
- Created homepage with recent books section
- Implemented responsive design for all screen sizes
- Added metadata extraction on book upload
