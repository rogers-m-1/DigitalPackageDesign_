"""Database models for comparison functionality."""
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class ComparisonSession(Base, TimestampMixin):
    """Model for storing comparison sessions."""
    __tablename__ = "comparison_sessions"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(255), nullable=False)  # Azure AD user
    uploaded_properties = Column(JSON, nullable=False)  # Extracted properties
    reference_design_id = Column(String(36), nullable=True)
    reference_design_name = Column(String(255), nullable=True)
    comparison_results = Column(JSON, nullable=False)  # Property deltas
    uploaded_file_name = Column(String(255), nullable=False)
    uploaded_file_blob_uri = Column(String(2048), nullable=False)


class DesignLibraryEntry(Base, TimestampMixin):
    """Model for reference library designs."""
    __tablename__ = "design_library_entries"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    properties = Column(JSON, nullable=False)  # Geometric properties
    source = Column(String(10), nullable=False)  # "stp" or "csv"
    source_file_blob_uri = Column(String(2048), nullable=True)
