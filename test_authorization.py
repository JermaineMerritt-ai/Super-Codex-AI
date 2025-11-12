# test_authorization.py
"""
Test script to demonstrate role-based authorization functionality
"""

import asyncio
from app.auth import create_token, User
from app.authz import require_roles, require_admin, require_council
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

class MockCredentials:
    """Mock credentials for testing"""
    def __init__(self, token: str):
        self.credentials = token

async def test_role_authorization():
    """Test role-based authorization with different user types"""
    
    print("🔐 Testing Role-Based Authorization System")
    print("=" * 50)
    
    # Create test tokens for different users
    admin_token = create_token("admin_user", ["admin", "operator"])
    operator_token = create_token("operator_user", ["operator"]) 
    council_token = create_token("council_user", ["council"])
    user_token = create_token("regular_user", ["user"])
    
    print(f"📋 Test Tokens Created:")
    print(f"  Admin: {admin_token[:50]}...")
    print(f"  Operator: {operator_token[:50]}...")
    print(f"  Council: {council_token[:50]}...")
    print(f"  User: {user_token[:50]}...")
    print()
    
    # Test different authorization scenarios
    scenarios = [
        ("Admin accessing operator endpoint", admin_token, require_roles("operator", "admin")),
        ("Operator accessing operator endpoint", operator_token, require_roles("operator", "admin")),
        ("Council accessing operator endpoint", council_token, require_roles("operator", "admin")),
        ("User accessing operator endpoint", user_token, require_roles("operator", "admin")),
        ("Admin accessing admin endpoint", admin_token, require_admin()),
        ("Operator accessing admin endpoint", operator_token, require_admin()),
        ("Council accessing council endpoint", council_token, require_council()),
        ("User accessing council endpoint", user_token, require_council()),
    ]
    
    print("🧪 Authorization Test Results:")
    print("-" * 30)
    
    for scenario_name, token, auth_dependency in scenarios:
        try:
            # Mock the FastAPI dependency injection
            mock_creds = MockCredentials(token)
            
            # This would normally be called by FastAPI's dependency system
            from app.auth import get_user
            user = get_user(mock_creds)
            
            # Call the authorization dependency
            authorized_user = auth_dependency(user)
            
            print(f"✅ {scenario_name}: ALLOWED")
            print(f"   User: {authorized_user.sub} | Roles: {authorized_user.roles}")
            
        except HTTPException as e:
            print(f"❌ {scenario_name}: DENIED")
            print(f"   Error: {e.detail}")
        except Exception as e:
            print(f"⚠️  {scenario_name}: ERROR")  
            print(f"   Exception: {str(e)}")
        print()

def test_user_role_methods():
    """Test User model role checking methods"""
    
    print("👤 Testing User Role Methods")
    print("=" * 30)
    
    # Create test users
    users = [
        User(sub="admin", roles=["admin", "operator"]),
        User(sub="operator", roles=["operator"]),
        User(sub="council", roles=["council", "custodian"]),
        User(sub="user", roles=["user"])
    ]
    
    for user in users:
        print(f"User: {user.sub}")
        print(f"  Roles: {user.roles}")
        print(f"  has_role('admin'): {user.has_role('admin')}")
        print(f"  has_role('operator'): {user.has_role('operator')}")
        print(f"  has_role('council'): {user.has_role('council')}")
        print(f"  has_any_role('admin', 'operator'): {user.has_any_role('admin', 'operator')}")
        print(f"  is_admin(): {user.is_admin()}")
        print(f"  is_council(): {user.is_council()}")
        print()

def test_authorization_patterns():
    """Test common authorization patterns"""
    
    print("🎭 Testing Common Authorization Patterns")
    print("=" * 40)
    
    # Pattern 1: AXIOM operations (your implementation)
    print("Pattern 1: AXIOM Operations")
    print("  Requirement: operator OR admin roles")
    print("  Implementation: require_roles('operator', 'admin')")
    print("  Usage: app.include_router(axiom_router, dependencies=[Depends(require_roles('operator', 'admin'))])")
    print()
    
    # Pattern 2: Administrative functions
    print("Pattern 2: Administrative Functions") 
    print("  Requirement: admin role only")
    print("  Implementation: require_admin()")
    print("  Usage: @app.post('/admin', dependencies=[Depends(require_admin())])")
    print()
    
    # Pattern 3: Council operations
    print("Pattern 3: Council Operations")
    print("  Requirement: council role")
    print("  Implementation: require_council()")
    print("  Usage: @app.post('/council', dependencies=[Depends(require_council())])")
    print()
    
    # Pattern 4: Any elevated user
    print("Pattern 4: Any Elevated User")
    print("  Requirement: admin, operator, council, or custodian")
    print("  Implementation: require_any_elevated()")
    print("  Usage: For general privileged operations")
    print()

if __name__ == "__main__":
    print("🚀 Role-Based Authorization System Test")
    print("=" * 50)
    
    # Run synchronous tests first
    test_user_role_methods()
    test_authorization_patterns()
    
    # Run async test
    print("Running async authorization tests...")
    asyncio.run(test_role_authorization())
    
    print("✅ All authorization tests completed!")
    print("\n📝 Integration Summary:")
    print("1. Created app/authz.py with role-based authorization")
    print("2. Updated app/main.py to protect AXIOM routes")
    print("3. AXIOM endpoints now require 'operator' or 'admin' roles")
    print("4. Multiple authorization patterns available")
    print("5. Comprehensive error handling and validation")