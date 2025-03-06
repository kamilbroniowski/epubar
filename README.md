# EPUBAR

A minimalist, in-browser EPUB library and reader application built with Flask, Bootstrap, and SQLite.

![EPUBAR](https://example.com/screenshot.png)

> EPUBAR is a dedicated EPUB reading application designed to provide a clean, distraction-free reading experience with powerful annotation features.

## Features

- **EPUB Processing**: Extract and render EPUB content with full format support
- **Library Management**: Upload, organize, and track reading progress of your EPUB collection
- **Reading Experience**: Chapter-based navigation with customizable themes (Light, Dark, Sepia) and font sizes
- **Text Interaction**: Highlighting and annotation system for marking important passages
- **Progress Tracking**: Automatically remembers your reading position across sessions
- **Responsive Design**: Works on desktop and mobile devices

## Development

### Prerequisites

- Docker and Docker Compose
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/kamilbroniowski/epubar.git
cd epubar

# Start the application
docker-compose up
```

The application will be available at http://localhost:5000

### Testing

EPUBAR follows a test-driven development approach with comprehensive test coverage:

```bash
# Run the test suite
docker-compose run --rm app pytest

# Run with coverage report
docker-compose run --rm app pytest --cov=app
```

### Project Structure

```
epubar/
├── app/                  # Application code
│   ├── models/           # Database models
│   ├── routes/           # Route handlers
│   ├── static/           # Static assets
│   ├── templates/        # Jinja2 templates
│   ├── tests/            # Test suite
│   │   └── resources/    # Test EPUB files
│   └── utils/            # Utility modules
│       └── epub/         # EPUB processing utilities
├── docker/               # Docker configuration
└── uploads/              # Book storage directory
```

## Architecture

EPUBAR follows a modular architecture with clear separation of concerns:

- **EPUB Processing**: Utilities for extracting and parsing EPUB files using custom processors
- **Content Rendering**: HTML/CSS normalization for consistent display across devices
- **Text Interaction**: Selection, highlighting, and annotation systems with position tracking
- **Database Layer**: SQLAlchemy ORM models for books, reading states, annotations, and user preferences
- **API Layer**: RESTful endpoints for content retrieval and reading state management
- **Frontend**: JavaScript-driven reader interface with dynamic content loading

## Components

### Book Reader

The EPUB reader component provides:

- Chapter-by-chapter navigation through book content
- Theme switching (Light, Dark, Sepia) for comfortable reading
- Font size adjustment for better readability
- Text selection for creating highlights and annotations
- Automatic progress tracking and position saving

### Library Management

The library component offers:

- EPUB file upload with metadata extraction
- Reading progress tracking for each book
- Book cover display and metadata presentation
- Recently read books tracking
- Responsive grid layout for browsing books

## License

See the [LICENSE](LICENSE) file for details.
