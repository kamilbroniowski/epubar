# Test Resources

This directory contains files used for testing the EPUBAR application.

## EPUB Test Files

### great_gatsby.epub
- **Description**: A Project Gutenberg edition of "The Great Gatsby" by F. Scott Fitzgerald
- **Source**: Project Gutenberg (https://www.gutenberg.org/ebooks/64317)
- **Purpose**: Real-world EPUB file used to test various EPUB processing functions:
  - Metadata extraction (title, author, language, etc.)
  - Spine item extraction for navigation
  - HTML content processing and normalization
  - Path resolution for embedded resources
  - JavaScript removal for security
  - Styling hook addition for consistent rendering

## Usage in Tests

When using these files in tests, reference them with the path relative to the Docker container:

```python
# Example test using Great Gatsby EPUB
def test_with_great_gatsby():
    epub_path = '/app/tests/resources/great_gatsby.epub'
    # Test code here
```

When running tests in Docker, make sure to mount this directory:

```bash
docker run --rm -v /home/mr/github/epubar/app/tests/resources:/app/tests/resources ... epubar pytest ...
```

## Adding New Test Files

When adding new test files to this directory:

1. Add a description in this README.md
2. Document the source and purpose of the file
3. Include any relevant licensing information
4. Update tests to properly reference the new files
