"""
Metadata extractor for EPUB files.

This module provides functionality to extract metadata from EPUB OPF files.
"""
import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional


class MetadataExtractor:
    """
    Utility class for extracting metadata from EPUB files.
    
    This class handles parsing OPF files to extract book metadata and spine information.
    """
    
    # XML namespaces used in EPUB files
    NAMESPACES = {
        'opf': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'container': 'urn:oasis:names:tc:opendocument:xmlns:container'
    }
    
    def get_opf_path(self, container_path: str) -> str:
        """
        Extract the OPF file path from the container.xml file.
        
        Args:
            container_path: Path to the META-INF/container.xml file
            
        Returns:
            Path to the OPF file
            
        Raises:
            ValueError: If no rootfile is found in container.xml
        """
        try:
            tree = ET.parse(container_path)
            root = tree.getroot()
            
            # Find the rootfile element
            rootfile_element = root.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
            if rootfile_element is None:
                raise ValueError("No rootfile found in container.xml")
            
            # Get the full path attribute
            opf_path = rootfile_element.get('full-path')
            if opf_path is None:
                raise ValueError("No full-path attribute in rootfile element")
                
            return opf_path
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid container.xml: {str(e)}")
    
    def extract_from_opf(self, opf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from an OPF file.
        
        Args:
            opf_path: Path to the OPF file
            
        Returns:
            Dictionary containing the extracted metadata
        """
        metadata = {}
        
        try:
            tree = ET.parse(opf_path)
            root = tree.getroot()
            
            # Extract basic metadata (title, creator, etc.)
            metadata_element = root.find('.//{http://www.idpf.org/2007/opf}metadata')
            if metadata_element is not None:
                # Extract Dublin Core metadata
                dc_elements = [
                    'title', 'creator', 'language', 'identifier',
                    'publisher', 'date', 'description', 'subject',
                    'rights', 'contributor', 'type', 'format', 'source',
                    'relation', 'coverage'
                ]
                
                for element_name in dc_elements:
                    element = metadata_element.find(f'./{{http://purl.org/dc/elements/1.1/}}{element_name}')
                    if element is not None and element.text:
                        metadata[element_name] = element.text.strip()
            
            # Extract cover image reference
            manifest_element = root.find('.//{http://www.idpf.org/2007/opf}manifest')
            if manifest_element is not None:
                # Look for item with cover-image property or id="cover"
                cover_items = manifest_element.findall('.//{http://www.idpf.org/2007/opf}item[@properties="cover-image"]')
                if not cover_items:
                    cover_items = manifest_element.findall('.//{http://www.idpf.org/2007/opf}item[@id="cover"]')
                
                if cover_items:
                    cover_href = cover_items[0].get('href')
                    if cover_href:
                        # Get the directory of the OPF file
                        opf_dir = os.path.dirname(opf_path)
                        # Combine with the cover path
                        cover_path = os.path.normpath(os.path.join(opf_dir, cover_href))
                        metadata['cover'] = cover_path
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid OPF file: {str(e)}")
        
        return metadata
    
    def get_spine_items(self, opf_path: str) -> List[Dict[str, str]]:
        """
        Extract spine items for navigation.
        
        Args:
            opf_path: Path to the OPF file
            
        Returns:
            List of dictionaries containing spine items with id and href
        """
        spine_items = []
        
        try:
            tree = ET.parse(opf_path)
            root = tree.getroot()
            
            # Get the manifest for id to href mapping
            manifest_element = root.find('.//{http://www.idpf.org/2007/opf}manifest')
            id_to_href = {}
            
            if manifest_element is not None:
                for item in manifest_element.findall('.//{http://www.idpf.org/2007/opf}item'):
                    item_id = item.get('id')
                    item_href = item.get('href')
                    if item_id and item_href:
                        id_to_href[item_id] = item_href
            
            # Get spine items
            spine_element = root.find('.//{http://www.idpf.org/2007/opf}spine')
            if spine_element is not None:
                for itemref in spine_element.findall('.//{http://www.idpf.org/2007/opf}itemref'):
                    idref = itemref.get('idref')
                    if idref and idref in id_to_href:
                        # Get the directory of the OPF file
                        opf_dir = os.path.dirname(opf_path)
                        # Combine with the href path
                        href_path = os.path.normpath(os.path.join(opf_dir, id_to_href[idref]))
                        
                        spine_items.append({
                            'id': idref,
                            'href': href_path
                        })
        
        except ET.ParseError as e:
            raise ValueError(f"Invalid OPF file: {str(e)}")
        
        return spine_items
