"""
Tests for processing a real EPUB file (The Great Gatsby)
"""
import os
import pytest
from bs4 import BeautifulSoup

from app.utils.epub.processor import EPUBProcessor
from app.utils.epub.metadata import MetadataExtractor
from app.utils.epub.content import ContentProcessor

def test_process_great_gatsby(sample_epub):
    """Test processing the Great Gatsby EPUB file"""
    # Path to the Great Gatsby EPUB file from the fixture
    epub_path = sample_epub
    
    # Create the EPUBProcessor and extract the EPUB
    processor = EPUBProcessor()
    extracted_path = processor.extract(epub_path)
    
    # Verify successful extraction
    assert os.path.exists(extracted_path)
    assert os.path.exists(os.path.join(extracted_path, 'META-INF/container.xml'))
    
    # Extract metadata
    extractor = MetadataExtractor()
    container_path = os.path.join(extracted_path, 'META-INF/container.xml')
    opf_relative_path = extractor.get_opf_path(container_path)
    opf_full_path = os.path.join(extracted_path, opf_relative_path)
    metadata = extractor.extract_from_opf(opf_full_path)
    
    # Print metadata for verification
    print("\nEPUB Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
    # Get spine items
    spine = extractor.get_spine_items(opf_full_path)
    
    # Print spine for verification
    print("\nSpine Items:")
    for item in spine:
        print(f"{item['id']} - {item['href']}")
    
    # Process content of the first HTML file in the spine
    if spine:
        content_processor = ContentProcessor()
        # Use the spine item path directly as it's already a full path
        first_chapter_path = spine[0]['href']
        
        if os.path.exists(first_chapter_path):
            # Process the HTML
            normalized_html = content_processor.normalize_html(first_chapter_path, base_path=extracted_path)
            
            # Save the processed HTML to a file in the project directory
            output_dir = '/app/output'
            os.makedirs(output_dir, exist_ok=True)
            
            # Save the original HTML
            original_filename = os.path.basename(first_chapter_path)
            with open(os.path.join(output_dir, f"original_{original_filename}"), 'w', encoding='utf-8') as f:
                with open(first_chapter_path, 'r', encoding='utf-8') as original:
                    f.write(original.read())
            
            # Save the processed HTML
            with open(os.path.join(output_dir, f"processed_{original_filename}"), 'w', encoding='utf-8') as f:
                f.write(normalized_html)
            
            print(f"\nOriginal and processed HTML saved to {output_dir}")
    
    # Clean up
    processor.cleanup()
