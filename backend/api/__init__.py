"""
Backend API Package

Contains API routers and handlers for the Super-Codex-AI system.
"""

try:
    from .webhooks import router as webhooks_router
except ImportError:
    from fastapi import APIRouter
    webhooks_router = APIRouter()

try:
    from .upload import router as upload_router
except ImportError:
    from fastapi import APIRouter
    upload_router = APIRouter()

__all__ = ["webhooks_router", "upload_router"]