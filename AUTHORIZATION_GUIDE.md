# Authorization Quick Reference Guide

## 🔐 Role-Based Authorization System

### Basic Usage

```python
from app.authz import require_roles, require_admin, require_council, require_any_elevated
from fastapi import Depends

# Router-level protection (protects all routes in the router)
app.include_router(
    axiom_router, 
    dependencies=[Depends(require_roles("operator", "admin"))]
)

# Individual endpoint protection
@app.get("/admin-only", dependencies=[Depends(require_admin())])
async def admin_endpoint():
    return {"message": "Admin access"}
```

### Available Authorization Functions

| Function | Required Roles | Usage |
|----------|---------------|--------|
| `require_roles("role1", "role2")` | Any of the specified roles | Custom role combinations |
| `require_admin()` | admin | Administrative functions |
| `require_council()` | council, custodian | Council operations |
| `require_operator()` | operator | Operator functions |
| `require_any_elevated()` | admin, operator, council, custodian | Any privileged user |

### Implementation Examples

#### 1. Protect Entire Router (Your Current Setup)
```python
# app/main.py
from app.authz import require_roles

app.include_router(
    axiom_router, 
    dependencies=[
        Depends(require_api_key),
        Depends(require_roles("operator", "admin"))
    ]
)
```

#### 2. Individual Endpoint Protection
```python
@app.post("/ceremony/invoke", dependencies=[Depends(require_roles("operator", "admin"))])
async def invoke_ceremony(data: dict):
    return {"status": "invoked"}
```

#### 3. Role Checking Within Function
```python
@app.get("/user-dashboard")
async def dashboard(user: User = Depends(get_user)):
    if user.has_role("admin"):
        return {"admin_panel": True, "data": "admin_data"}
    elif user.has_role("operator"):
        return {"operator_panel": True, "data": "operator_data"}
    else:
        return {"basic_panel": True, "data": "basic_data"}
```

#### 4. Multiple Authorization Layers
```python
@app.post("/critical-operation")
async def critical_op(
    data: dict,
    user: User = Depends(require_admin()),  # Must be admin
    api_key: str = Depends(require_api_key)  # Must have API key
):
    return {"status": "completed"}
```

### Error Responses

When authorization fails, the system returns:

```json
// 401 Unauthorized (no token or invalid token)
{
    "detail": "Authentication required"
}

// 403 Forbidden (valid token, insufficient role)
{
    "detail": "Insufficient permissions. Required roles: operator, admin"
}
```

### User Object Methods

The `User` object provides convenient role checking:

```python
user.has_role("admin")                    # Check single role
user.has_any_role("admin", "operator")    # Check multiple roles
user.is_admin()                          # Convenience method
user.is_council()                        # Convenience method
```

### Token Creation for Testing

```python
from app.auth import create_token

# Create test tokens
admin_token = create_token("admin_user", ["admin"])
operator_token = create_token("operator_user", ["operator"])
council_token = create_token("council_user", ["council"])
```

### Common Patterns

#### Pattern 1: Hierarchical Access
```python
# Admin can do everything, operators have limited access
@app.post("/workflow/{workflow_id}/advance")
async def advance_workflow(workflow_id: str, user: User = Depends(get_user)):
    if user.has_role("admin"):
        # Admin can advance any workflow
        return advance_any_workflow(workflow_id)
    elif user.has_role("operator"):
        # Operators can only advance their own workflows
        return advance_own_workflow(workflow_id, user.sub)
    else:
        raise HTTPException(403, "Insufficient permissions")
```

#### Pattern 2: Feature Flags by Role
```python
@app.get("/features")
async def get_features(user: User = Depends(get_user)):
    features = ["basic_dashboard"]
    
    if user.has_role("operator"):
        features.extend(["workflow_management", "ceremony_invoke"])
    
    if user.has_role("admin"):
        features.extend(["user_management", "system_config"])
    
    if user.has_role("council"):
        features.extend(["council_ceremonies", "honor_granting"])
    
    return {"features": features}
```

### Security Best Practices

1. **Always validate both authentication AND authorization**
2. **Use router-level protection for entire API sections**
3. **Principle of least privilege - grant minimum required roles**
4. **Log authorization failures for security monitoring**
5. **Use specific role combinations rather than broad permissions**

### Current AXIOM Protection

Your AXIOM routes are now protected with:
- **Authentication**: Valid JWT token required
- **Authorization**: Must have "operator" OR "admin" role
- **API Key**: Valid API key also required

This means only authenticated users with elevated privileges can access ceremonial operations, providing appropriate security for sensitive AXIOM functions.