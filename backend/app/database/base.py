"""
KES Water
Database Declarative Base

This module defines the SQLAlchemy Declarative Base used by
all ORM models across the application.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Every database model in KES Water must inherit from this class.
    """

    pass