# App package for Super-Codex-AI
__version__ = "1.0.0"

# Import key modules
try:
    from .main import app
    from .auth import get_user, require_admin, require_council, User
    from .gateway import router as gateway_router
    from .health import router as health_router
    from .auth_routes import router as auth_router
except ImportError as e:
    print(f"Warning: Could not import app modules: {e}")
    app = None

__all__ = ["app", "get_user", "require_admin", "require_council", "User"]