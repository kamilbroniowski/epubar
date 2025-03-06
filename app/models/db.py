"""
Database configuration and initialization module
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

# Initialize SQLAlchemy instance
db = SQLAlchemy()
Base = declarative_base()
