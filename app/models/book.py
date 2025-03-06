"""
Book model for storing EPUB metadata and file information
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.db import db

class Book(db.Model):
    """Book model representing EPUB files in the library"""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    language = Column(String(50))
    identifier = Column(String(255))  # ISBN or other unique identifier
    publication_date = Column(String(50))
    description = Column(Text)
    file_path = Column(String(255), nullable=False)
    cover_path = Column(String(255))
    file_size = Column(Integer)  # in bytes
    total_pages = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='books')
    reading_state = relationship('ReadingState', back_populates='book', uselist=False)
    annotations = relationship('Annotation', back_populates='book')
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
