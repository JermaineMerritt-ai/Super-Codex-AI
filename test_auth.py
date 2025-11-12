#!/usr/bin/env python3
"""
Authentication System Test Suite
Tests JWT authentication, role-based access, and token management
"""
import requests
import json
import sys
from typing import Optional

# API Configuration
API_BASE = "http://127.0.0.1:8005"
TIMEOUT = 10

class AuthTestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def login(self, username: str, password: str) -> dict:
        """Login and store token"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        
        return data
    
    def get_current_user(self) -> dict:
        """Get current user info"""
        response = self.session.get(f"{self.base_url}/auth/me", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def test_protected_endpoint(self) -> dict:
        """Test protected endpoint"""
        response = self.session.get(f"{self.base_url}/protected", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def test_admin_endpoint(self) -> dict:
        """Test admin endpoint"""
        response = self.session.get(f"{self.base_url}/admin", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def test_council_endpoint(self) -> dict:
        """Test council endpoint"""
        response = self.session.get(f"{self.base_url}/council", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def test_health(self) -> dict:
        """Test health endpoint (no auth required)"""
        response = self.session.get(f"{self.base_url}/health", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

def test_auth_system():
    """Run comprehensive authentication tests"""
    print(f"🔐 Testing Authentication System on {API_BASE}")
    print("=" * 60)
    
    client = AuthTestClient(API_BASE)
    
    try:
        # Test 1: Health Check (no auth)
        print("1. Testing health endpoint (no auth required)...")
        health = client.test_health()
        print(f"   ✅ Health: {health.get('status', 'unknown')}")
        
        # Test 2: Admin Login
        print("\n2. Testing admin login...")
        admin_login = client.login("admin", "admin")
        print(f"   ✅ Admin logged in: {admin_login['user']['username']}")
        print(f"   📋 Roles: {', '.join(admin_login['user']['roles'])}")
        
        # Test 3: Protected endpoint with admin
        print("\n3. Testing protected endpoint with admin token...")
        protected = client.test_protected_endpoint()
        print(f"   ✅ Protected access: {protected['user']}")
        
        # Test 4: Admin endpoint
        print("\n4. Testing admin endpoint...")
        admin_data = client.test_admin_endpoint()
        print(f"   ✅ Admin access: {admin_data['message']}")
        
        # Test 5: Council endpoint (admin should have council role too)
        print("\n5. Testing council endpoint with admin...")
        council_data = client.test_council_endpoint()
        print(f"   ✅ Council access: {council_data['message']}")
        
        # Test 6: User info
        print("\n6. Testing user info endpoint...")
        user_info = client.get_current_user()
        print(f"   ✅ User: {user_info['username']} ({user_info['name']})")
        print(f"   📧 Email: {user_info['email']}")
        
        # Test 7: Council-only login
        print("\n7. Testing council member login...")
        council_client = AuthTestClient(API_BASE)
        council_login = council_client.login("council", "council")
        print(f"   ✅ Council logged in: {council_login['user']['username']}")
        
        # Test 8: Council access to council endpoint
        print("\n8. Testing council member accessing council endpoint...")
        council_access = council_client.test_council_endpoint()
        print(f"   ✅ Council access: {council_access['message']}")
        
        # Test 9: Council member trying admin endpoint (should fail)
        print("\n9. Testing council member accessing admin endpoint (should fail)...")
        try:
            council_client.test_admin_endpoint()
            print("   ❌ ERROR: Council member gained admin access!")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("   ✅ Correctly denied admin access (403 Forbidden)")
            else:
                print(f"   ⚠️  Unexpected error: {e}")
        
        # Test 10: Regular user login
        print("\n10. Testing regular user login...")
        user_client = AuthTestClient(API_BASE)
        user_login = user_client.login("user", "user")
        print(f"    ✅ User logged in: {user_login['user']['username']}")
        
        # Test 11: Regular user accessing protected endpoint
        print("\n11. Testing regular user accessing protected endpoint...")
        user_protected = user_client.test_protected_endpoint()
        print(f"    ✅ Protected access: {user_protected['user']}")
        
        # Test 12: Regular user trying admin endpoint (should fail)
        print("\n12. Testing regular user accessing admin endpoint (should fail)...")
        try:
            user_client.test_admin_endpoint()
            print("    ❌ ERROR: Regular user gained admin access!")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("    ✅ Correctly denied admin access (403 Forbidden)")
            else:
                print(f"    ⚠️  Unexpected error: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 All authentication tests passed!")
        print("\n💡 Default credentials:")
        print("   • Admin: username=admin, password=admin")
        print("   • Council: username=council, password=council") 
        print("   • User: username=user, password=user")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Connection Error: {e}")
        print(f"Make sure the backend is running on {API_BASE}")
        return False
    
    except Exception as e:
        print(f"\n❌ Test Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_auth_system()
    sys.exit(0 if success else 1)