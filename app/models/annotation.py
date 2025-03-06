"""
Annotation model for storing highlights, notes, and bookmarks
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.db import db

class AnnotationType(enum.Enum):
    """Enum for different types of annotations"""
    HIGHLIGHT = 'highlight'
    NOTE = 'note'
    BOOKMARK = 'bookmark'

class Annotation(db.Model):
    """Annotation model for managing highlights, notes, and bookmarks"""
    __tablename__ = 'annotations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    type = Column(Enum(AnnotationType), nullable=False)
    content = Column(Text)  # For notes and bookmarks
    color = Column(String(50))  # For highlights
    position_data = Column(Text, nullable=False)  # JSON string with selection position data
    chapter_index = Column(Integer)  # Chapter where the annotation is located
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='annotations')
    book = relationship('Book', back_populates='annotations')
    
    def __repr__(self):
        return f'<Annotation {self.id} - {self.type.name}>'
