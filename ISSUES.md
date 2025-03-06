# EPUBAR Development Issues

## Active Issues

1. **Docker Environment Compatibility**
   - Python 3.13 has compatibility issues with some packages like Pillow
   - Downgraded to Python 3.11 in Docker to resolve dependencies
   - Need to ensure consistent environments between development and production

2. **Application Structure Issues**
   - Initial application structure wasn't suitable for testing
   - Refactored to use Flask application factory pattern
   - Need to validate the new structure works with all tests

## Known Issues

1. **EPUB Format Compatibility**
   - Different EPUB versions (2.0, 3.0) have varying specifications
   - Some publishers use non-standard formatting or structure
   - Need comprehensive testing with diverse EPUB samples

2. **Pagination Consistency**
   - Ensuring consistent pagination across different device sizes
   - Handling dynamic content and embedded media in pagination
   - Preserving annotation positions when font size or spacing changes

3. **Performance Considerations**
   - Large EPUB files may cause slow loading or rendering
   - Memory usage for storing and retrieving annotations
   - Optimizing database queries for large libraries

4. **Cross-browser Compatibility**
   - Text selection behavior differs across browsers
   - CSS rendering inconsistencies between browsers
   - Touch vs. mouse interactions for highlighting

5. **Data Persistence**
   - Ensuring reliable storage of reading position and annotations
   - Handling concurrent read/write operations
   - Graceful recovery from database corruption or connection issues

## Implementation Challenges

1. **Text Selection and Highlighting**
   - Implementing reliable text selection across paginated content
   - Persisting highlight positions when text reflows
   - Creating an intuitive interface for highlight colors and annotation entry

2. **Content Normalization**
   - Standardizing diverse HTML/CSS in EPUB files
   - Handling embedded fonts and styling

## Fixed Issues

1. **API Integration Issues**
   - ✅ Fixed method name mismatch between code and tests (extract_spine → get_spine_items)
   - ✅ Corrected API response key mismatch ('idref' → 'id') in book spine API routes
   - ✅ Resolved content path construction in get_book_content route

2. **Content Processing**
   - ✅ Enhanced ContentProcessor to return complete HTML documents with proper html and body tags
   - ✅ Fixed image path resolution in EPUB content

3. **Test Environment Issues**
   - ✅ Fixed 'safe_join' import error by importing from werkzeug.utils instead of flask
   - ✅ Resolved path discrepancy in Docker container by updating paths in conftest.py
   - ✅ Fixed database access error in reader tests by using db fixture directly
   - ✅ Added missing 'sample_book' fixture to the testing configuration
   - Maintaining original formatting while enabling customization

3. **Monochrome Design**
   - Creating a visually appealing interface with limited color palette
   - Using typography, spacing, and contrast effectively
   - Integrating highlight colors without disrupting the monochrome aesthetic
