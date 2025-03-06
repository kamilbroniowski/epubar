"""
EPUB Processor module for extracting and validating EPUB files.
"""
import os
import shutil
import tempfile
import zipfile
from typing import Tuple, List, Optional


class EPUBProcessor:
    """
    Utility class for processing EPUB files.
    
    This class handles the extraction, validation, and cleanup of EPUB files.
    """
    
    def __init__(self):
        """Initialize the EPUB processor."""
        self.temp_dir = None
        self.extracted_path = None
    
    def extract(self, epub_path: str) -> str:
        """
        Extract the contents of an EPUB file to a temporary directory.
        
        Args:
            epub_path: Path to the EPUB file to extract
            
        Returns:
            Path to the directory containing the extracted contents
        
        Raises:
            ValueError: If the file is not a valid EPUB file
        """
        # Create a temporary directory for extraction
        self.temp_dir = tempfile.mkdtemp(prefix='epubar_')
        self.extracted_path = os.path.join(self.temp_dir, 'epub_content')
        os.makedirs(self.extracted_path, exist_ok=True)
        
        # Extract the EPUB file
        try:
            with zipfile.ZipFile(epub_path, 'r') as epub:
                # Check if the first file is mimetype with proper content
                if epub.namelist()[0] != 'mimetype':
                    raise ValueError("Invalid EPUB: mimetype file must be first in the archive")
                
                # Extract all files
                epub.extractall(self.extracted_path)
                
                # Verify required structure exists
                if not os.path.exists(os.path.join(self.extracted_path, 'META-INF/container.xml')):
                    raise ValueError("Invalid EPUB: Missing META-INF/container.xml")
                
        except zipfile.BadZipFile:
            self.cleanup()
            raise ValueError("Invalid EPUB: Not a valid ZIP file")
        
        return self.extracted_path
    
    def validate(self, epub_path: str) -> Tuple[bool, List[str]]:
        """
        Validate an EPUB file.
        
        Args:
            epub_path: Path to the EPUB file to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Check if it's a valid ZIP file
            if not zipfile.is_zipfile(epub_path):
                errors.append("Not a valid ZIP file")
                return False, errors
            
            with zipfile.ZipFile(epub_path, 'r') as epub:
                # Check for required files
                file_list = epub.namelist()
                
                # Check mimetype
                if 'mimetype' not in file_list:
                    errors.append("Missing mimetype file")
                elif file_list[0] != 'mimetype':
                    errors.append("mimetype file is not the first file in the archive")
                else:
                    mimetype = epub.read('mimetype').decode('utf-8')
                    if mimetype != 'application/epub+zip':
                        errors.append(f"Invalid mimetype: {mimetype}")
                
                # Check container.xml
                if 'META-INF/container.xml' not in file_list:
                    errors.append("Missing META-INF/container.xml")
                
                # Extract and check OPF file
                if 'META-INF/container.xml' in file_list:
                    container_xml = epub.read('META-INF/container.xml').decode('utf-8')
                    # Simple check for rootfile reference
                    if 'full-path=' not in container_xml or 'media-type="application/oebps-package+xml"' not in container_xml:
                        errors.append("Invalid container.xml: missing OPF reference")
        
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            return False, errors
        
        return len(errors) == 0, errors
    
    def cleanup(self) -> None:
        """
        Clean up temporary files and directories.
        """
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
            self.extracted_path = None
