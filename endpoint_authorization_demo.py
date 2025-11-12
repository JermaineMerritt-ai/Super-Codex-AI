# endpoint_authorization_demo.py
"""
Demo of individual endpoint authorization patterns
"""

from fastapi import FastAPI, Depends, HTTPException
from app.authz import require_roles, require_admin, require_council
from app.auth import get_user, User

app = FastAPI()

# Pattern 2: Individual endpoint protection
@app.post("/admin-functions", dependencies=[Depends(require_admin())])
async def admin_functions():
    """Admin-only endpoint using dependencies parameter"""
    return {"message": "Admin function executed", "access_level": "admin"}

@app.post("/council-decisions", dependencies=[Depends(require_council())])
async def council_decisions():
    """Council-only endpoint using dependencies parameter"""
    return {"message": "Council decision recorded", "access_level": "council"}

@app.post("/operator-tasks", dependencies=[Depends(require_roles("operator", "admin"))])
async def operator_tasks():
    """Operator or admin endpoint using dependencies parameter"""
    return {"message": "Operator task completed", "access_level": "operator_or_admin"}

# Pattern 3: Within function role checking
@app.post("/flexible-endpoint")
async def flexible_endpoint(user: User = Depends(get_user)):
    """Flexible endpoint with role-based logic inside function"""
    
    # Check admin access
    if user.has_role("admin"):
        return {
            "message": "Admin access granted",
            "features": ["full_control", "user_management", "system_config"],
            "access_level": "admin"
        }
    
    # Check operator access  
    if user.has_role("operator"):
        return {
            "message": "Operator access granted", 
            "features": ["workflow_control", "ceremony_management"],
            "access_level": "operator"
        }
    
    # Check council access
    if user.has_role("council"):
        return {
            "message": "Council access granted",
            "features": ["governance", "strategic_decisions"],
            "access_level": "council"
        }
    
    # Insufficient permissions
    raise HTTPException(403, "Insufficient role permissions")

@app.post("/conditional-access")
async def conditional_access(operation: str, user: User = Depends(get_user)):
    """Conditional access based on operation type and user roles"""
    
    # Critical operations require admin
    if operation in ["delete_user", "system_shutdown", "data_purge"]:
        if not user.has_role("admin"):
            raise HTTPException(403, "Critical operations require admin role")
    
    # Ceremonial operations require operator or higher
    elif operation.startswith("ceremony_"):
        if not user.has_any_role("operator", "admin", "council"):
            raise HTTPException(403, "Ceremonial operations require elevated privileges")
    
    # Standard operations require authentication only
    elif operation in ["view_data", "basic_query"]:
        pass  # Any authenticated user can perform these
    
    else:
        raise HTTPException(400, "Unknown operation type")
    
    return {
        "operation": operation,
        "user": user.sub,
        "authorized": True,
        "timestamp": "2025-11-11T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Individual endpoint authorization demo")
    print("Available endpoints:")
    print("  POST /admin-functions - Admin only")
    print("  POST /council-decisions - Council only")  
    print("  POST /operator-tasks - Operator or Admin")
    print("  POST /flexible-endpoint - Role-based response")
    print("  POST /conditional-access - Operation-based authorization")
    
    # Run on different port to avoid conflicts
    uvicorn.run(app, host="127.0.0.1", port=8020)