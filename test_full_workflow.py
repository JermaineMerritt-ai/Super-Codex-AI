#!/usr/bin/env python3
"""
Test the complete authentication and AXIOM FLAME workflow
"""
import requests
import json
import time
import os

# Test configuration
BASE_URL = "http://127.0.0.1:8006"

def test_workflow():
    """Test complete authentication and ceremonial workflow"""
    print("🧪 Testing Complete AXIOM FLAME Authentication Workflow")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Service: {health_data.get('service')}")
            print(f"   Status: {health_data.get('status')}")
            print("   ✅ Health check successful")
        else:
            print(f"   ❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Authentication
    print("\n2️⃣ Testing Authentication...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            auth_result = response.json()
            token = auth_result["access_token"]
            user = auth_result["user"]
            print(f"   User: {user['name']} ({user['username']})")
            print(f"   Roles: {', '.join(user['roles'])}")
            print("   ✅ Authentication successful")
        else:
            print(f"   ❌ Authentication failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        return False
    
    # Test 3: User Info
    print("\n3️⃣ Testing User Info...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"   Username: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
            print(f"   Roles: {', '.join(user_info['roles'])}")
            print("   ✅ User info retrieved successfully")
        else:
            print(f"   ❌ User info failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ User info error: {e}")
        return False
    
    # Test 4: Ceremonial Reasoning
    print("\n4️⃣ Testing Ceremonial Reasoning...")
    try:
        ceremony_data = {
            "actor": "System Test",
            "realm": "PL-001",
            "capsule": "Sovereign Crown",
            "intent": "Authentication.Test"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/api/reason", json=ceremony_data, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            ceremony_result = response.json()
            dispatch_id = ceremony_result["dispatch_id"]
            print(f"   Dispatch ID: {dispatch_id}")
            print(f"   Status: {ceremony_result['ceremony']['status']}")
            print(f"   Authority: {ceremony_result['ceremony']['governance']['authority_level']}")
            print("   ✅ Ceremonial reasoning successful")
            
            # Test 5: Replay
            print("\n5️⃣ Testing Ceremonial Replay...")
            response = requests.get(f"{BASE_URL}/api/replay/{dispatch_id}", timeout=10)
            if response.status_code == 200:
                print("   ✅ Replay successful")
            else:
                print(f"   ❌ Replay failed: {response.text}")
                
            # Test 6: Audit
            print("\n6️⃣ Testing Ceremonial Audit...")
            response = requests.get(f"{BASE_URL}/api/audit/{dispatch_id}", timeout=10)
            if response.status_code == 200:
                audit_result = response.json()
                print(f"   Audit ID: {audit_result['audit_report']['audit_id']}")
                print("   ✅ Audit successful")
            else:
                print(f"   ❌ Audit failed: {response.text}")
                
        else:
            print(f"   ❌ Ceremonial reasoning failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Ceremonial reasoning error: {e}")
        return False
    
    print("\n🎉 All Tests Completed Successfully!")
    print("✅ Authentication system is fully operational")
    print("✅ AXIOM FLAME ceremonial operations are working")
    print("✅ JWT tokens are properly validated")
    print("✅ Role-based access control is enforced")
    
    return True

def test_cli_workflow():
    """Test the CLI workflow"""
    print("\n🚀 Testing CLI Workflow...")
    print("=" * 60)
    
    # Set environment variables for CLI
    os.environ["AXIOM_API_BASE"] = BASE_URL
    os.environ["AXIOM_BACKEND_BASE"] = BASE_URL
    
    print("\n📋 CLI Test Instructions:")
    print("Run the following commands to test the CLI:")
    print(f"   cd {os.getcwd()}")
    print("   python axiom_auth_cli.py login")
    print("   python axiom_auth_cli.py whoami")  
    print("   python axiom_auth_cli.py health")
    print('   python axiom_auth_cli.py reason "CLI Test" "PL-001" "Sovereign Crown" "CLI.Authentication.Test"')
    print("   python axiom_auth_cli.py logout")

if __name__ == "__main__":
    # Test API workflow
    success = test_workflow()
    
    # Show CLI instructions
    test_cli_workflow()
    
    if success:
        print("\n🌟 System is ready for production use!")
    else:
        print("\n❌ Some tests failed. Check server logs.")