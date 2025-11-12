# complete_authorization_example.py
"""
Complete example showing all three authorization patterns working together
"""

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from app.authz import require_roles, require_admin, require_council
from app.auth import get_user, User
from app.deps import require_api_key

app = FastAPI(title="Complete Authorization Demo")

# Pattern 1: Router-level protection (like your AXIOM router)
secure_router = APIRouter(prefix="/secure")

# All routes in this router require operator or admin role
app.include_router(
    secure_router,
    dependencies=[
        Depends(require_api_key),  # API key required
        Depends(require_roles("operator", "admin"))  # Role required
    ]
)

@secure_router.get("/workflow")
async def secure_workflow():
    """This endpoint inherits router-level authorization"""
    return {"message": "Secure workflow accessed", "auth_level": "router_protected"}

@secure_router.post("/ceremony")
async def secure_ceremony():
    """Another endpoint with inherited router protection"""
    return {"message": "Ceremony initiated", "auth_level": "router_protected"}

# Pattern 2: Individual endpoint protection
@app.get("/admin-dashboard", dependencies=[Depends(require_admin())])
async def admin_dashboard():
    """Admin-only dashboard - uses endpoint-level dependency"""
    return {
        "message": "Admin dashboard accessed",
        "auth_level": "endpoint_protected",
        "features": ["user_management", "system_monitoring"]
    }

@app.get("/council-chamber", dependencies=[Depends(require_council())])
async def council_chamber():
    """Council-only area - uses endpoint-level dependency"""
    return {
        "message": "Council chamber accessed", 
        "auth_level": "endpoint_protected",
        "features": ["governance", "strategic_planning"]
    }

# Pattern 3: Function-level authorization with flexible logic
@app.post("/dynamic-operation")
async def dynamic_operation(
    operation_type: str,
    sensitive_data: bool = False,
    user: User = Depends(get_user)
):
    """
    Flexible authorization within the function based on parameters and user roles
    """
    
    # Sensitive operations require admin regardless of type
    if sensitive_data and not user.has_role("admin"):
        raise HTTPException(403, "Sensitive operations require admin role")
    
    # Different operation types have different requirements
    if operation_type == "data_export":
        if not user.has_any_role("admin", "operator"):
            raise HTTPException(403, "Data export requires admin or operator role")
            
    elif operation_type == "user_invite":
        if not user.has_any_role("admin", "council"):
            raise HTTPException(403, "User invites require admin or council role")
            
    elif operation_type == "system_backup":
        if not user.has_role("admin"):
            raise HTTPException(403, "System backup requires admin role")
            
    elif operation_type == "ceremony_review":
        if not user.has_any_role("admin", "council", "operator"):
            raise HTTPException(403, "Ceremony review requires elevated privileges")
    
    else:
        # Default: any authenticated user
        pass
    
    return {
        "operation": operation_type,
        "sensitive": sensitive_data,
        "user": user.sub,
        "roles": user.roles,
        "authorized": True,
        "auth_level": "function_logic"
    }

# Combining patterns - router + endpoint + function level
protected_router = APIRouter(prefix="/protected")

# Router level: requires authentication
app.include_router(
    protected_router,
    dependencies=[Depends(get_user)]  # Basic auth required
)

@protected_router.post(
    "/super-secure", 
    dependencies=[Depends(require_admin())]  # Endpoint level: admin required
)
async def super_secure_operation(
    data: dict,
    user: User = Depends(get_user)  # Function level: additional checks
):
    """Triple-protected endpoint: router auth + endpoint admin + function logic"""
    
    # Additional function-level checks
    operation = data.get("operation")
    
    if operation == "nuclear_option":
        # Even admins need special permission for this
        if not user.has_role("admin") or "nuclear_clearance" not in user.roles:
            raise HTTPException(403, "Nuclear operations require special clearance")
    
    return {
        "message": "Super secure operation completed",
        "operation": operation,
        "auth_levels": ["router", "endpoint", "function"],
        "user": user.sub
    }

# Health check - no auth required
@app.get("/health")
async def health_check():
    """Public health endpoint"""
    return {"status": "healthy", "auth_required": False}

# User info - shows different data based on roles
@app.get("/me")
async def get_current_user_info(user: User = Depends(get_user)):
    """Get current user info with role-based data"""
    
    info = {
        "username": user.sub,
        "roles": user.roles,
        "auth_level": "authenticated"
    }
    
    # Add role-specific information
    if user.has_role("admin"):
        info.update({
            "admin_features": ["user_management", "system_config", "full_access"],
            "can_access": ["/secure/*", "/admin-dashboard", "/super-secure"]
        })
    
    if user.has_role("operator"):
        info.update({
            "operator_features": ["workflow_management", "ceremony_control"],
            "can_access": ["/secure/*", "/dynamic-operation"]
        })
        
    if user.has_role("council"):
        info.update({
            "council_features": ["governance", "strategic_decisions"],
            "can_access": ["/council-chamber", "/dynamic-operation"]
        })
    
    return info

if __name__ == "__main__":
    import uvicorn
    
    print("🛡️  Complete Authorization System Demo")
    print("=" * 50)
    print("\n📋 Authorization Patterns:")
    print("1. Router-level: /secure/* - requires operator/admin")
    print("2. Endpoint-level: /admin-dashboard - requires admin") 
    print("3. Function-level: /dynamic-operation - flexible logic")
    print("\n🔗 Combined: /protected/super-secure - triple protection")
    print("\n🌐 Running on: http://127.0.0.1:8021")
    
    uvicorn.run(app, host="127.0.0.1", port=8021)