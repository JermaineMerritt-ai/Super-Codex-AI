# app/authz.py
# Role-based authorization system for protecting API endpoints

from fastapi import Depends, HTTPException, status
from app.auth import get_user
from typing import List, Union

def require_roles(*roles: str):
    """
    Create a dependency that requires the user to have at least one of the specified roles.
    
    Args:
        *roles: Variable number of role names that are allowed access
        
    Returns:
        FastAPI dependency function that validates user roles
        
    Usage:
        @app.get("/protected", dependencies=[Depends(require_roles("admin", "operator"))])
        async def protected_endpoint():
            return {"message": "Access granted"}
    """
    def role_dependency(user = Depends(get_user)):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
            
        # Check if user has any of the required roles
        user_roles = getattr(user, 'roles', []) or getattr(user, 'role', '').split(',')
        
        # Handle single role string or list of roles
        if isinstance(user_roles, str):
            user_roles = [user_roles]
            
        # Normalize roles for comparison (lowercase, strip whitespace)
        normalized_user_roles = [role.strip().lower() for role in user_roles if role.strip()]
        normalized_required_roles = [role.strip().lower() for role in roles]
        
        if not any(role in normalized_user_roles for role in normalized_required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(roles)}"
            )
        return user
    return role_dependency

def require_admin():
    """Convenience function to require admin role only."""
    return require_roles("admin")

def require_operator():
    """Convenience function to require operator role only."""
    return require_roles("operator")

def require_council():
    """Convenience function to require council role only."""
    return require_roles("council", "custodian")

def require_any_elevated():
    """Require any elevated role (admin, operator, council, custodian)."""
    return require_roles("admin", "operator", "council", "custodian")

# Optional: More granular permission checking
def check_permission(user, required_permission: str) -> bool:
    """
    Check if user has a specific permission.
    Can be extended for more complex permission systems.
    """
    user_permissions = getattr(user, 'permissions', [])
    return required_permission in user_permissions

def require_permission(permission: str):
    """
    Create a dependency that requires a specific permission.
    """
    def permission_dependency(user = Depends(get_user)):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
            
        if not check_permission(user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}"
            )
        return user
    return permission_dependency