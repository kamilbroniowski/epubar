"""
Content processor for EPUB files.

This module provides functionality to process and normalize HTML content from EPUB files
for rendering in a web application.
"""
import os
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urljoin


class ContentProcessor:
    """
    Utility class for processing EPUB content.
    
    This class handles normalizing HTML content, resolving relative URLs,
    and preparing content for web display.
    """
    
    def normalize_html(self, html_path: str, base_path: Optional[str] = None) -> str:
        """
        Normalize HTML content for rendering in the web application.
        
        Args:
            html_path: Path to the HTML file
            base_path: Optional base path for resolving relative URLs
            
        Returns:
            Normalized HTML content
        
        Raises:
            ValueError: If the HTML file cannot be read or parsed
        """
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Process relative URLs
            if base_path:
                self._fix_relative_urls(soup, html_path, base_path)
            
            # Add CSS classes for styling
            self._add_styling_hooks(soup)
            
            # Clean up unnecessary elements and attributes
            self._clean_html(soup)
            
            return str(soup)
            
        except Exception as e:
            raise ValueError(f"Error normalizing HTML: {str(e)}")
    
    def _fix_relative_urls(self, soup: BeautifulSoup, html_path: str, base_path: str) -> None:
        """
        Fix relative URLs in the HTML content.
        
        Args:
            soup: BeautifulSoup object
            html_path: Path to the HTML file
            base_path: Base path for resolving relative URLs
        """
        # Get the directory of the HTML file relative to the base path
        html_dir = os.path.dirname(os.path.relpath(html_path, os.path.dirname(base_path)))
        
        # Fix image sources
        for img in soup.find_all('img'):
            if img.get('src') and not img['src'].startswith(('http://', 'https://', '/')):
                img['src'] = os.path.normpath(os.path.join(html_dir, img['src']))
        
        # Fix CSS links
        for link in soup.find_all('link', rel='stylesheet'):
            if link.get('href') and not link['href'].startswith(('http://', 'https://', '/')):
                link['href'] = os.path.normpath(os.path.join(html_dir, link['href']))
    
    def _add_styling_hooks(self, soup: BeautifulSoup) -> None:
        """
        Add CSS classes and data attributes to elements for styling.
        
        Args:
            soup: BeautifulSoup object
        """
        # Add a class to the body element
        if soup.body:
            if 'class' in soup.body.attrs:
                soup.body['class'].append('epubar-content')
            else:
                soup.body['class'] = ['epubar-content']
        
        # Add classes to headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if 'class' in heading.attrs:
                heading['class'].append(f'epubar-heading epubar-{heading.name}')
            else:
                heading['class'] = [f'epubar-heading epubar-{heading.name}']
        
        # Add classes to paragraphs
        for paragraph in soup.find_all('p'):
            if 'class' in paragraph.attrs:
                paragraph['class'].append('epubar-paragraph')
            else:
                paragraph['class'] = ['epubar-paragraph']
        
        # Add data attribute for annotation support
        elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span'])
        for i, element in enumerate(elements):
            element['data-epubar-id'] = f'el-{i}'
    
    def _clean_html(self, soup: BeautifulSoup) -> None:
        """
        Clean up unnecessary elements and attributes.
        
        Args:
            soup: BeautifulSoup object
        """
        # Remove scripts
        for script in soup.find_all('script'):
            script.decompose()
        
        # Remove style attributes (we'll use our own CSS)
        for tag in soup.find_all(style=True):
            del tag['style']
        
        # Remove non-standard attributes
        for tag in soup.find_all():
            attrs_to_remove = []
            for attr in tag.attrs:
                if attr.startswith('epub:') or attr.startswith('xml:'):
                    attrs_to_remove.append(attr)
            
            for attr in attrs_to_remove:
                del tag[attr]
                
    def process_content(self, html_path: str, base_path: str, add_data_attributes: bool = False) -> str:
        """
        Process HTML content for rendering in the reader.
        
        This method normalizes the HTML, resolves relative URLs, adds styling hooks,
        and optionally adds data attributes for annotation support.
        
        Args:
            html_path: Path to the HTML file
            base_path: Base path for resolving relative URLs
            add_data_attributes: Whether to add data attributes for annotation support
            
        Returns:
            Processed HTML content ready for the reader
        """
        try:
            # Read the HTML file
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Process relative URLs
            self._fix_relative_urls(soup, html_path, base_path)
            
            # Add CSS classes for styling
            self._add_styling_hooks(soup)
            
            # Clean up unnecessary elements and attributes
            self._clean_html(soup)
            
            # Add data attributes for annotation support if requested
            if add_data_attributes:
                self._add_data_attributes(soup)
            
            # Extract just the body content (or the entire document if no body)
            body_content = soup.body or soup
            
            # Create a new HTML structure for the reader
            reader_html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>EPUBAR Reader</title>
            </head>
            <body>
                <div class="epubar-chapter-content">
                    {body_content.encode_contents().decode('utf-8')}
                </div>
            </body>
            </html>
            '''
            
            return reader_html
            
        except Exception as e:
            raise ValueError(f"Error processing HTML content: {str(e)}")
    
    def _add_data_attributes(self, soup: BeautifulSoup) -> None:
        """
        Add data attributes to elements for annotation support.
        
        Args:
            soup: BeautifulSoup object
        """
        # Add unique IDs to elements that might be annotated
        for i, element in enumerate(soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span', 'li'])):
            element['data-epubar-id'] = f'el-{i}'
