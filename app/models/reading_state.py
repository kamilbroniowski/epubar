"""
ReadingState model for tracking user reading progress
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from app.models.db import db

class ReadingState(db.Model):
    """ReadingState model for tracking user reading progress and bookmarks"""
    __tablename__ = 'reading_states'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    current_position = Column(String(255))  # Can store chapter/page info in structured format
    progress_percent = Column(Float, default=0.0)
    is_finished = Column(Boolean, default=False)
    last_read_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='reading_states')
    book = relationship('Book', back_populates='reading_state')
    
    def __repr__(self):
        return f'<ReadingState {self.book_id} - {self.progress_percent}%>'
