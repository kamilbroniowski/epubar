# EPUBAR Development Tasks

## Core Infrastructure

- [x] Setup project structure and Docker configuration
- [x] Define database models
- [x] Implement Flask application factory pattern for better testing
- [x] Create route blueprints (main, library, reader, api)
- [x] Create test fixtures and test database configuration
- [x] Implement testing framework for TDD approach
- [x] Run all tests in Docker environment

## EPUB Processing

- [x] Write tests for EPUB extraction functionality
- [x] Implement EPUB extraction from ZIP archives
- [x] Write tests for OPF file parsing
- [x] Implement OPF parser for book metadata
- [x] Write tests for HTML/CSS content processing
- [x] Implement HTML/CSS processor for rendering
- [x] Test with real-world EPUB files (Great Gatsby)
- [x] Verify CSS path resolution and resource loading
- [ ] Write tests for image handling
- [ ] Implement image extraction and processing

## Library Management

- [x] Write tests for upload functionality
- [x] Implement EPUB file upload and validation
- [x] Write tests for metadata extraction
- [x] Implement metadata extraction and storage
- [x] Write tests for library view
- [x] Implement library view with book cards and progress tracking
- [x] Implement recent books section on homepage
- [ ] Write tests for search functionality
- [ ] Implement search functionality
- [ ] Add sorting and filtering options

## Reading Experience

- [x] Write tests for EPUB content rendering
- [x] Implement EPUB content renderer with spine navigation
- [x] Implement reading state persistence
- [x] Write tests for theme and font customization
- [x] Implement theme switching (Light, Dark, Sepia)
- [x] Implement font size adjustment
- [ ] Write tests for pagination system
- [ ] Implement pagination with smooth transitions
- [ ] Write tests for bookmarking functionality
- [ ] Implement bookmarking system

## Text Interaction

- [x] Write tests for text selection mechanism
- [x] Implement text selection with contextual menu
- [x] Write tests for highlighting functionality
- [x] Implement highlighting with color options
- [x] Write tests for annotation system
- [x] Implement annotation creation and display
- [x] Write tests for annotation persistence
- [x] Implement annotation storage and retrieval via API
- [ ] Add annotation filtering and searching
- [ ] Implement annotation sharing

## UI/UX

- [x] Write tests for responsive layout
- [x] Implement responsive monochrome interface
- [x] Implement reader controls for navigation
- [x] Create minimalist reader interface
- [x] Implement settings for theme and font size
- [ ] Add animation tests for UI transitions
- [ ] Implement user preferences panel
- [ ] Add keyboard shortcuts for navigation
- [ ] Implement statistics dashboard for reading progress

## Documentation

- [x] Update README.md with project overview
- [x] Document architecture decisions in LOG.md
- [x] Create comprehensive test suite documentation
- [x] Document API endpoints for front-end developers
- [ ] Create user documentation
- [ ] Write developer onboarding guide

## Deployment

- [x] Configure Docker environment for development
- [ ] Set up production-ready Docker configuration
- [ ] Configure CI/CD pipeline for automated testing
- [ ] Create database migration scripts
- [ ] Set up automatic backups for user data
- [ ] Implement monitoring and logging

## Testing and Quality Assurance

- [x] Set up pytest framework
- [x] Implement test database configuration with fixtures
- [x] Write comprehensive unit tests for all models
- [x] Implement functional tests for API endpoints
- [x] Fix API method name mismatches (extract_spine → get_spine_items)
- [x] Fix API response key mismatches (idref → id)
- [x] Fix content path construction issues
- [x] Enhance HTML processing for reader content
- [ ] Address SQLAlchemy deprecation warnings
- [ ] Implement end-to-end tests with Selenium
- [ ] Achieve >90% overall test coverage
