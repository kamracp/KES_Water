"""
KES Water
Database Engine & Session Management
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger()

# ---------------------------------------------------------------------
# SQLAlchemy Engine
# ---------------------------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# ---------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)

# ---------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency.

    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


logger.info("Database session initialized.")