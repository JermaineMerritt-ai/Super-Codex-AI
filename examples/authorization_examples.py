# examples/authorization_examples.py
"""
Examples of applying role-based authorization in different scenarios
"""

from fastapi import FastAPI, Depends, APIRouter
from app.authz import require_roles, require_admin, require_council, require_any_elevated
from app.auth import get_user, User

# Example 1: Router-level protection (what you implemented)
axiom_router = APIRouter(prefix="/axiom")
app = FastAPI()

# All AXIOM routes require operator or admin roles
app.include_router(
    axiom_router, 
    dependencies=[Depends(require_roles("operator", "admin"))]
)

# Example 2: Individual endpoint protection
@app.get("/admin-only", dependencies=[Depends(require_admin())])
async def admin_only_endpoint():
    return {"message": "Admin access granted"}

@app.get("/council-only", dependencies=[Depends(require_council())])
async def council_only_endpoint():
    return {"message": "Council access granted"}

# Example 3: Multiple role options
@app.get("/elevated-users", dependencies=[Depends(require_any_elevated())])
async def elevated_users_endpoint():
    return {"message": "Elevated access granted"}

# Example 4: Using roles within the endpoint function
@app.get("/user-info")
async def get_user_info(user: User = Depends(get_user)):
    """Get user info - shows different responses based on roles"""
    
    info = {
        "username": user.sub,
        "roles": user.roles,
        "is_admin": user.has_role("admin"),
        "is_council": user.has_role("council")
    }
    
    # Add admin-only information
    if user.has_role("admin"):
        info["admin_features"] = ["user_management", "system_config"]
    
    # Add operator-specific information  
    if user.has_role("operator"):
        info["operator_features"] = ["ceremony_management", "workflow_control"]
        
    return info

# Example 5: Custom role checking in endpoint
@app.post("/ceremony/invoke")
async def invoke_ceremony(ceremony_data: dict, user: User = Depends(get_user)):
    """Invoke ceremony with role-based restrictions"""
    
    # Check if user can invoke ceremonies
    if not user.has_any_role("operator", "admin", "council"):
        raise HTTPException(403, "Ceremony invocation requires elevated privileges")
    
    # Admin and council can invoke any ceremony
    if user.has_any_role("admin", "council"):
        return {"status": "ceremony_invoked", "level": "unrestricted"}
    
    # Operators have restrictions
    if user.has_role("operator"):
        # Operators can only invoke certain ceremonies
        allowed_ceremonies = ["standard_blessing", "routine_maintenance"] 
        ceremony_type = ceremony_data.get("type")
        
        if ceremony_type not in allowed_ceremonies:
            raise HTTPException(403, f"Operator role cannot invoke {ceremony_type}")
            
        return {"status": "ceremony_invoked", "level": "operator_restricted"}

# Example 6: Conditional authorization based on resource ownership
@app.get("/workflow/{workflow_id}")
async def get_workflow(workflow_id: str, user: User = Depends(get_user)):
    """Get workflow with ownership-based access control"""
    
    # Admins can see all workflows
    if user.has_role("admin"):
        return {"workflow_id": workflow_id, "access": "admin_full"}
    
    # Council can see council workflows
    if user.has_role("council"):
        # Check if workflow belongs to council (simplified example)
        if workflow_id.startswith("council_"):
            return {"workflow_id": workflow_id, "access": "council_owned"}
        else:
            raise HTTPException(403, "Council can only access council workflows")
    
    # Operators can see their own workflows
    if user.has_role("operator"):
        # Check if workflow belongs to this operator (simplified example)
        if workflow_id.startswith(f"op_{user.sub}_"):
            return {"workflow_id": workflow_id, "access": "operator_owned"}
        else:
            raise HTTPException(403, "Operators can only access their own workflows")
    
    raise HTTPException(403, "Insufficient permissions to access workflow")

# Example 7: Different authorization for different HTTP methods
ceremony_router = APIRouter(prefix="/ceremonies")

# GET ceremonies - any authenticated user
@ceremony_router.get("/")
async def list_ceremonies(user: User = Depends(get_user)):
    return {"ceremonies": ["list_based_on_user_role"]}

# POST ceremonies - requires operator or higher
@ceremony_router.post("/", dependencies=[Depends(require_roles("operator", "admin", "council"))])
async def create_ceremony(ceremony_data: dict):
    return {"status": "ceremony_created"}

# DELETE ceremonies - admin only
@ceremony_router.delete("/{ceremony_id}", dependencies=[Depends(require_admin())])
async def delete_ceremony(ceremony_id: str):
    return {"status": "ceremony_deleted", "id": ceremony_id}

# Example 8: Combining multiple authorization checks
@app.post("/critical-operation")
async def critical_operation(
    data: dict,
    admin_user: User = Depends(require_admin()),  # Must be admin
    api_key_valid: bool = Depends(require_api_key)  # Must have valid API key
):
    """Critical operation requiring both admin role and API key"""
    return {
        "status": "critical_operation_completed",
        "operator": admin_user.sub,
        "timestamp": "2025-11-11T00:00:00Z"
    }

# Example 9: Hierarchical role checking
def require_role_hierarchy(*roles_in_order):
    """
    Require user to have at least one role from a hierarchy (ordered by privilege level)
    """
    def wrapper(user: User = Depends(get_user)):
        user_roles = set(user.roles)
        
        # Check roles in order of privilege (admin > council > operator > user)
        role_hierarchy = ["admin", "council", "operator", "user"]
        
        # Find highest role user has
        user_highest_role = None
        for role in role_hierarchy:
            if role in user_roles:
                user_highest_role = role
                break
                
        # Find minimum required role
        required_highest_role = None
        for role in role_hierarchy:
            if role in roles_in_order:
                required_highest_role = role
                break
                
        # Check if user's highest role meets requirement
        if not user_highest_role or not required_highest_role:
            raise HTTPException(403, "No valid roles found")
            
        user_level = role_hierarchy.index(user_highest_role)
        required_level = role_hierarchy.index(required_highest_role)
        
        if user_level > required_level:  # Higher index = lower privilege
            raise HTTPException(403, f"Requires {required_highest_role} role or higher")
            
        return user
    return wrapper

# Usage of hierarchical checking
@app.post("/hierarchical-endpoint", dependencies=[Depends(require_role_hierarchy("council", "admin"))])
async def hierarchical_endpoint():
    return {"message": "Access granted to council level or higher"}

if __name__ == "__main__":
    print("Authorization examples loaded successfully")
    print("Available role combinations:")
    print("- require_roles('operator', 'admin')")  
    print("- require_admin()")
    print("- require_council()")
    print("- require_any_elevated()")