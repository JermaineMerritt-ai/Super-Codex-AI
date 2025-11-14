from fastapi import APIRouter, Depends
from app.security.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/protected")
def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """
    A protected endpoint that requires authentication.
    """
    return {
        "message": "This is a protected endpoint",
        "user": current_user
    }