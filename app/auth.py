"""
Authentication module for Super-Codex-AI system
Provides JWT-based authentication with role-based access control
"""
import os
import time
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PRODUCTION")
JWT_ALGORITHM = "HS256"
DEFAULT_EXPIRY_MINUTES = 60

# Security scheme
security = HTTPBearer()

class User(BaseModel):
    """User model with subject and roles"""
    sub: str
    roles: List[str]
    email: Optional[str] = None
    name: Optional[str] = None
    
    def has_role(self, role: str) -> bool:
        """Check if user has a specific role"""
        return role in self.roles
    
    def has_any_role(self, *roles: str) -> bool:
        """Check if user has any of the specified roles"""
        return any(role in self.roles for role in roles)
    
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.has_role("admin")
    
    def is_council(self) -> bool:
        """Check if user is a council member"""
        return self.has_role("council")

def create_token(
    sub: str, 
    roles: List[str], 
    exp_minutes: int = DEFAULT_EXPIRY_MINUTES,
    email: Optional[str] = None,
    name: Optional[str] = None
) -> str:
    """
    Create a JWT token for the user
    
    Args:
        sub: Subject (user identifier)
        roles: List of user roles
        exp_minutes: Token expiry in minutes
        email: Optional user email
        name: Optional user name
    
    Returns:
        Encoded JWT token
    """
    payload = {
        "sub": sub,
        "roles": roles,
        "exp": int(time.time()) + exp_minutes * 60,
        "iat": int(time.time()),
        "iss": "super-codex-ai"
    }
    
    if email:
        payload["email"] = email
    if name:
        payload["name"] = name
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_user(creds: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Extract and validate user from JWT token
    
    Args:
        creds: HTTP Authorization credentials containing JWT token
    
    Returns:
        User object with validated claims
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Validate required fields
        if "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing subject claim"
            )
        
        return User(
            sub=payload["sub"],
            roles=payload.get("roles", []),
            email=payload.get("email"),
            name=payload.get("name")
        )
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )

def get_optional_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
    """
    Optionally extract user from JWT token (for endpoints that work with or without auth)
    
    Args:
        creds: Optional HTTP Authorization credentials
    
    Returns:
        User object if token is valid, None otherwise
    """
    if not creds:
        return None
    
    try:
        return get_user(creds)
    except HTTPException:
        return None

def require_roles(*required_roles: str):
    """
    Dependency factory for role-based access control
    
    Args:
        *required_roles: Variable number of role names that are allowed
    
    Returns:
        FastAPI dependency function that validates user roles
    """
    def wrapper(user: User = Depends(get_user)) -> User:
        if not user.has_any_role(*required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(required_roles)}"
            )
        return user
    return wrapper

def require_admin(user: User = Depends(get_user)) -> User:
    """
    Dependency that requires admin role
    
    Args:
        user: User from JWT token
    
    Returns:
        User object if admin
    
    Raises:
        HTTPException: If user is not an admin
    """
    if not user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

def require_council(user: User = Depends(get_user)) -> User:
    """
    Dependency that requires council role
    
    Args:
        user: User from JWT token
    
    Returns:
        User object if council member
    
    Raises:
        HTTPException: If user is not a council member
    """
    if not user.is_council():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Council access required"
        )
    return user

# Common role combinations
require_admin_or_council = require_roles("admin", "council")
require_any_authenticated = Depends(get_user)

# Utility functions for token management
def verify_token(token: str) -> Optional[User]:
    """
    Verify a token without FastAPI dependencies
    
    Args:
        token: JWT token string
    
    Returns:
        User object if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return User(
            sub=payload["sub"],
            roles=payload.get("roles", []),
            email=payload.get("email"),
            name=payload.get("name")
        )
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return None

def create_service_token(service_name: str, roles: List[str] = None) -> str:
    """
    Create a long-lived service token for internal API communications
    
    Args:
        service_name: Name of the service
        roles: List of roles for the service (defaults to ["service"])
    
    Returns:
        JWT token with extended expiry
    """
    if roles is None:
        roles = ["service"]
    
    return create_token(
        sub=f"service:{service_name}",
        roles=roles,
        exp_minutes=60 * 24 * 30  # 30 days
    )