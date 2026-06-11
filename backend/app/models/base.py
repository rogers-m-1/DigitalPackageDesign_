"""SQLAlchemy declarative base and mixins."""
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import DateTime
from datetime import datetime
from typing import Any


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    @declared_attr
    def created_at(cls) -> Any:
        return DateTime(timezone=True), datetime.utcnow()

    @declared_attr
    def updated_at(cls) -> Any:
        return DateTime(timezone=True), datetime.utcnow()
