# EPUBAR

A minimalist, in-browser EPUB library and reader application built with Flask, Jinja2, HTMX, and SQLite.

## Features

- **EPUB Processing**: Extract and render EPUB content with full format support
- **Library Management**: Upload, organize, and search your EPUB collection
- **Reading Experience**: Customizable pagination, fonts, themes, and spacing
- **Text Interaction**: Highlighting, annotations, and bookmarking
- **Minimalist Design**: Content-focused monochrome interface

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

## Architecture

EPUBAR follows a modular architecture with clear separation of concerns:

- **EPUB Processing**: Utilities for extracting and parsing EPUB files
- **Content Rendering**: HTML/CSS normalization for consistent display
- **Text Interaction**: Selection, highlighting, and annotation systems
- **Database Layer**: Clean interfaces for efficient data operations

## License

See the [LICENSE](LICENSE) file for details.
