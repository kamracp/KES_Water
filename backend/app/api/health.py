"""
KES Water
Health Check API
"""

from datetime import datetime

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Application Health Check")
async def health_check() -> dict:
    """
    Basic application health endpoint.
    """
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }