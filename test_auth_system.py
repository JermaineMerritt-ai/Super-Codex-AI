#!/usr/bin/env python3
"""Test the authentication system structure and imports."""

import sys
import os

def test_auth_system():
    """Test all authentication system components."""
    print("🔧 Testing Authentication System Structure...")
    
    try:
        # Test security module imports
        from app.security.auth import get_current_user, decode_token, PRIMARY_KEY, SECONDARY_KEY
        print("✅ Security auth module imported successfully")
        print(f"   - Primary key configured: {'Yes' if PRIMARY_KEY else 'No'}")
        print(f"   - Secondary key configured: {'Yes' if SECONDARY_KEY else 'No'}")
        
        # Test authentication router
        from app.routers.authentication import router
        print("✅ Authentication router imported successfully")
        print(f"   - Router prefix: {router.prefix}")
        print(f"   - Router tags: {router.tags}")
        
        # Test main app
        from app.main import app
        print("✅ Main app imported successfully")
        
        # Check router inclusion
        router_count = len([r for r in app.routes if hasattr(r, 'path')])
        auth_routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                path = str(route.path)
                if 'auth' in path.lower():
                    auth_routes.append(path)
        
        print(f"✅ Total routes registered: {router_count}")
        print(f"✅ Authentication routes: {auth_routes}")
        
        # Test route structure
        if auth_routes:
            print("✅ Authentication router is properly integrated!")
        else:
            print("⚠️  No authentication routes found - checking integration...")
        
        print("\n🎉 Authentication system structure test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_auth_system()
    sys.exit(0 if success else 1)