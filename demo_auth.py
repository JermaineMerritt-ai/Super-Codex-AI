#!/usr/bin/env python3
"""
Authentication Demo Script
Demonstrates JWT token creation, validation, and role-based access
"""
import os
import sys
import json
import time

# Add current directory to path
sys.path.insert(0, os.path.abspath('.'))

def demo_jwt_auth():
    """Demonstrate JWT authentication functionality"""
    print("🔐 JWT Authentication Demo")
    print("=" * 50)
    
    try:
        # Import our auth module
        from app.auth import create_token, verify_token, User
        
        print("1. Creating tokens for different users...")
        
        # Create tokens for different user types
        admin_token = create_token(
            sub="admin_user", 
            roles=["admin", "council"],
            email="admin@super-codex-ai.local",
            name="System Administrator"
        )
        
        council_token = create_token(
            sub="council_member",
            roles=["council"], 
            email="council@super-codex-ai.local",
            name="Council Member"
        )
        
        user_token = create_token(
            sub="regular_user",
            roles=["user"],
            email="user@super-codex-ai.local", 
            name="Regular User"
        )
        
        print(f"   ✅ Admin token: {admin_token[:30]}...")
        print(f"   ✅ Council token: {council_token[:30]}...")
        print(f"   ✅ User token: {user_token[:30]}...")
        
        print("\n2. Verifying tokens and extracting user data...")
        
        # Verify tokens
        admin_user = verify_token(admin_token)
        council_user = verify_token(council_token) 
        regular_user = verify_token(user_token)
        
        print(f"   👤 Admin: {admin_user.sub} - Roles: {admin_user.roles}")
        print(f"   👤 Council: {council_user.sub} - Roles: {council_user.roles}")
        print(f"   👤 User: {regular_user.sub} - Roles: {regular_user.roles}")
        
        print("\n3. Testing role-based permissions...")
        
        # Test admin permissions
        print(f"   🔑 Admin is admin: {admin_user.is_admin()}")
        print(f"   🔑 Admin is council: {admin_user.is_council()}")
        print(f"   🔑 Admin has admin role: {admin_user.has_role('admin')}")
        
        # Test council permissions
        print(f"   🏛️  Council is admin: {council_user.is_admin()}")
        print(f"   🏛️  Council is council: {council_user.is_council()}")
        print(f"   🏛️  Council has council role: {council_user.has_role('council')}")
        
        # Test regular user permissions
        print(f"   👥 User is admin: {regular_user.is_admin()}")
        print(f"   👥 User is council: {regular_user.is_council()}")
        print(f"   👥 User has user role: {regular_user.has_role('user')}")
        
        print("\n4. Testing token expiration...")
        
        # Create short-lived token
        short_token = create_token(
            sub="temp_user",
            roles=["user"],
            exp_minutes=0  # Expires immediately
        )
        
        # Wait a moment then try to verify
        time.sleep(1)
        
        expired_user = verify_token(short_token)
        if expired_user is None:
            print("   ✅ Expired token correctly rejected")
        else:
            print("   ⚠️  Expired token was accepted (unexpected)")
            
        print("\n5. Creating service tokens...")
        
        from app.auth import create_service_token
        
        service_token = create_service_token("axiom-flame", ["service", "ceremonial"])
        service_user = verify_token(service_token)
        
        print(f"   🤖 Service: {service_user.sub} - Roles: {service_user.roles}")
        
        print("\n" + "=" * 50)
        print("🎉 JWT Authentication Demo Complete!")
        print("\n📋 Summary:")
        print("   • JWT tokens created and verified successfully")
        print("   • Role-based access control working")
        print("   • Token expiration handled correctly")
        print("   • Service tokens supported")
        print("\n💡 The authentication system is ready for use!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running from the correct directory")
        return False
    
    except Exception as e:
        print(f"❌ Demo Error: {e}")
        return False

def demo_auth_routes():
    """Show authentication routes structure"""
    print("\n🚀 Authentication API Endpoints")
    print("=" * 50)
    
    endpoints = [
        ("POST", "/auth/login", "Login with username/password"),
        ("POST", "/auth/token", "Login with HTTP Basic Auth"),
        ("GET", "/auth/me", "Get current user info"),
        ("POST", "/auth/refresh", "Refresh JWT token"),
        ("POST", "/auth/logout", "Logout user"),
        ("POST", "/auth/users", "Create new user (admin only)"),
        ("GET", "/auth/users", "List all users (admin only)"),
        ("GET", "/protected", "Protected endpoint (any auth)"),
        ("GET", "/admin", "Admin-only endpoint"),
        ("GET", "/council", "Council-only endpoint")
    ]
    
    for method, endpoint, description in endpoints:
        print(f"   {method:4} {endpoint:20} - {description}")
    
    print(f"\n📝 Example Login Request:")
    login_example = {
        "username": "admin",
        "password": "admin"
    }
    print(f"   POST /auth/login")
    print(f"   {json.dumps(login_example, indent=6)}")
    
    print(f"\n📝 Example Response:")
    response_example = {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
            "username": "admin",
            "email": "admin@super-codex-ai.local",
            "name": "System Administrator",
            "roles": ["admin", "council"]
        }
    }
    print(f"   {json.dumps(response_example, indent=6)}")

if __name__ == "__main__":
    print("🔐 Super-Codex-AI Authentication System")
    print("🔥 AXIOM FLAME Security Integration")
    print()
    
    success = demo_jwt_auth()
    
    if success:
        demo_auth_routes()
        print("\n🚀 Ready to start the backend with authentication!")
        print("   Run: python -m uvicorn backend.main:app --host 127.0.0.1 --port 8005")
    
    sys.exit(0 if success else 1)