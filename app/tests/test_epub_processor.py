"""
Tests for the EPUB processing utilities
"""
import os
import pytest
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

# Import the modules we're going to test
from app.utils.epub.processor import EPUBProcessor
from app.utils.epub.metadata import MetadataExtractor
from app.utils.epub.content import ContentProcessor

@pytest.fixture
def sample_epub():
    """Create a minimal valid EPUB file for testing"""
    tmp_dir = tempfile.mkdtemp()
    epub_path = os.path.join(tmp_dir, 'sample.epub')
    
    # Create a minimal EPUB structure
    with zipfile.ZipFile(epub_path, 'w') as epub:
        # Add mimetype file (must be first and uncompressed)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # Add META-INF directory with container.xml
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
            <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
               <rootfiles>
                  <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
               </rootfiles>
            </container>'''
        epub.writestr('META-INF/container.xml', container_xml)
        
        # Add OPF file
        opf_content = '''<?xml version="1.0" encoding="UTF-8"?>
            <package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId">
               <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
                  <dc:title>Test Book</dc:title>
                  <dc:creator>Test Author</dc:creator>
                  <dc:identifier id="BookId">urn:isbn:1234567890</dc:identifier>
                  <dc:language>en</dc:language>
                  <dc:publisher>Test Publisher</dc:publisher>
                  <dc:date>2023-01-01</dc:date>
                  <dc:description>A test book for EPUB processor tests</dc:description>
               </metadata>
               <manifest>
                  <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
                  <item id="css" href="style.css" media-type="text/css"/>
                  <item id="cover" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>
               </manifest>
               <spine>
                  <itemref idref="chapter1"/>
               </spine>
            </package>'''
        epub.writestr('OEBPS/content.opf', opf_content)
        
        # Add a chapter
        chapter1 = '''<?xml version="1.0" encoding="UTF-8"?>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
               <head>
                  <title>Chapter 1</title>
                  <link rel="stylesheet" type="text/css" href="style.css"/>
                  <script type="text/javascript">document.body.style.color = 'red';</script>
               </head>
               <body xml:lang="en">
                  <h1 epub:type="title">Chapter 1</h1>
                  <p style="color: blue;">This is the first paragraph of the test book.</p>
                  <p>This is the second paragraph with some <strong>bold text</strong> and <em>italic text</em>.</p>
                  <div class="section">
                    <h2>Section 1.1</h2>
                    <p>This is a section with an <img src="cover.jpg" alt="Cover Image"/> embedded.</p>
                  </div>
               </body>
            </html>'''
        epub.writestr('OEBPS/chapter1.xhtml', chapter1)
        
        # Add CSS file
        css = '''body { font-family: serif; }
            h1 { font-size: 2em; }
            p { line-height: 1.5em; }'''
        epub.writestr('OEBPS/style.css', css)
        
        # Add a cover image (as a tiny 1x1 JPEG)
        cover_jpg = bytes([
            0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 0x01, 0x01, 0x00, 0x48,
            0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC2, 0x00, 0x0B, 0x08, 0x00,
            0x01, 0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x14, 0x10, 0x01, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xDA, 0x00,
            0x08, 0x01, 0x01, 0x00, 0x01, 0x3F, 0x10
        ])
        epub.writestr('OEBPS/cover.jpg', cover_jpg)
    
    yield epub_path
    
    # Cleanup
    os.remove(epub_path)
    os.rmdir(tmp_dir)


class TestEPUBProcessor:
    """Test cases for EPUB extraction and validation"""
    
    def test_epub_extraction(self, sample_epub):
        """Test extracting contents from an EPUB file"""
        processor = EPUBProcessor()
        extracted_path = processor.extract(sample_epub)
        
        # Verify extraction worked and required files exist
        assert os.path.exists(extracted_path)
        assert os.path.exists(os.path.join(extracted_path, 'mimetype'))
        assert os.path.exists(os.path.join(extracted_path, 'META-INF/container.xml'))
        assert os.path.exists(os.path.join(extracted_path, 'OEBPS/content.opf'))
        assert os.path.exists(os.path.join(extracted_path, 'OEBPS/chapter1.xhtml'))
        assert os.path.exists(os.path.join(extracted_path, 'OEBPS/style.css'))
        assert os.path.exists(os.path.join(extracted_path, 'OEBPS/cover.jpg'))
        
        # Clean up
        processor.cleanup()
        
    def test_epub_validation(self, sample_epub):
        """Test validating an EPUB file"""
        processor = EPUBProcessor()
        is_valid, errors = processor.validate(sample_epub)
        
        assert is_valid
        assert len(errors) == 0
        
        # Test with invalid EPUB
        with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as invalid_file:
            invalid_file.write(b'This is not a valid EPUB file')
            invalid_path = invalid_file.name
        
        is_valid, errors = processor.validate(invalid_path)
        
        assert not is_valid
        assert len(errors) > 0
        
        os.remove(invalid_path)

class TestMetadataExtractor:
    """Test cases for EPUB metadata extraction"""
    
    def test_extract_metadata_from_opf(self, sample_epub):
        """Test extracting metadata from an OPF file"""
        processor = EPUBProcessor()
        extracted_path = processor.extract(sample_epub)
        
        extractor = MetadataExtractor()
        opf_path = os.path.join(extracted_path, 'OEBPS/content.opf')
        metadata = extractor.extract_from_opf(opf_path)
        
        # Verify metadata
        assert metadata['title'] == 'Test Book'
        assert metadata['creator'] == 'Test Author'
        assert metadata['identifier'] == 'urn:isbn:1234567890'
        assert metadata['language'] == 'en'
        assert metadata['publisher'] == 'Test Publisher'
        assert metadata['date'] == '2023-01-01'
        assert metadata['description'] == 'A test book for EPUB processor tests'
        
        # Verify cover image is identified
        assert 'cover' in metadata
        # The cover path should end with 'OEBPS/cover.jpg'
        assert metadata['cover'].endswith('OEBPS/cover.jpg')
        
        # Clean up
        processor.cleanup()
    
    def test_get_spine_items(self, sample_epub):
        """Test extracting spine items for navigation"""
        processor = EPUBProcessor()
        extracted_path = processor.extract(sample_epub)
        
        extractor = MetadataExtractor()
        opf_path = os.path.join(extracted_path, 'OEBPS/content.opf')
        spine = extractor.get_spine_items(opf_path)
        
        # Verify spine items
        assert len(spine) == 1
        assert spine[0]['id'] == 'chapter1'
        # The href should end with 'OEBPS/chapter1.xhtml'
        assert spine[0]['href'].endswith('OEBPS/chapter1.xhtml')
        
        # Clean up
        processor.cleanup()

class TestContentProcessor:
    """Test cases for EPUB content processing"""
    
    def test_save_processed_html(self, sample_epub):
        """Test saving processed HTML to a persistent location"""
        processor = EPUBProcessor()
        extracted_path = processor.extract(sample_epub)
        
        content_processor = ContentProcessor()
        chapter_path = os.path.join(extracted_path, 'OEBPS/chapter1.xhtml')
        
        normalized_html = content_processor.normalize_html(chapter_path, base_path=extracted_path)
        
        # Save the processed HTML to a file in the project directory
        output_dir = '/app/output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the original HTML
        with open(os.path.join(output_dir, 'original_chapter1.html'), 'w', encoding='utf-8') as f:
            with open(chapter_path, 'r', encoding='utf-8') as original:
                f.write(original.read())
        
        # Save the processed HTML
        with open(os.path.join(output_dir, 'processed_chapter1.html'), 'w', encoding='utf-8') as f:
            f.write(normalized_html)
        
        print(f"Original and processed HTML saved to {output_dir}")
        assert os.path.exists(os.path.join(output_dir, 'processed_chapter1.html'))
    
    def test_normalize_html(self, sample_epub):
        """Test normalizing HTML content for rendering"""
        processor = EPUBProcessor()
        extracted_path = processor.extract(sample_epub)
        
        content_processor = ContentProcessor()
        chapter_path = os.path.join(extracted_path, 'OEBPS/chapter1.xhtml')
        
        normalized_html = content_processor.normalize_html(chapter_path, base_path=extracted_path)
        
        # Verify that the HTML was normalized correctly
        assert normalized_html is not None
        assert len(normalized_html) > 0
        
        # Check for styling hooks
        assert 'epubar-content' in normalized_html
        assert 'epubar-heading' in normalized_html
        assert 'epubar-paragraph' in normalized_html
        assert 'data-epubar-id' in normalized_html
        
        # Make sure scripts and non-standard attributes were removed
        assert '<script>' not in normalized_html.lower()
        assert 'xml:' not in normalized_html
        assert 'epub:' not in normalized_html
        
        # Check that styles were removed
        assert 'style="color: blue;"' not in normalized_html
        
        # Check image paths were properly adjusted
        soup = BeautifulSoup(normalized_html, 'html.parser')
        img = soup.find('img')
        assert img is not None
        assert img['src'].endswith('cover.jpg')
        
        # Verify headings have appropriate classes
        h1 = soup.find('h1')
        assert 'epubar-heading' in h1['class']
        assert 'epubar-h1' in h1['class']
        
        h2 = soup.find('h2')
        assert 'epubar-heading' in h2['class']
        assert 'epubar-h2' in h2['class']
        
        # Clean up
        processor.cleanup()
