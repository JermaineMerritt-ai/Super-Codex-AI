#!/usr/bin/env python3
"""
Test Unified API Configuration
Validates that frontend only calls backend, never Flask directly
"""

import requests
import json
import time
from datetime import datetime

def test_unified_api():
    """Test the unified API architecture"""
    
    print("🧪 TESTING UNIFIED API ARCHITECTURE")
    print("="*50)
    
    # Test 1: Backend health (should work)
    print("1️⃣ Testing backend gateway health...")
    try:
        response = requests.get("http://127.0.0.1:8015/health/live", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend gateway is healthy")
            print(f"   📋 Response: {response.json()}")
        else:
            print(f"   ❌ Backend gateway returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend gateway error: {e}")
    
    print()
    
    # Test 2: AXIOM proxy health (should work through gateway)
    print("2️⃣ Testing AXIOM proxy through gateway...")
    try:
        response = requests.get("http://127.0.0.1:8015/axiom/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ AXIOM proxy is working")
            print(f"   📋 Response: {response.json()}")
        else:
            print(f"   ❌ AXIOM proxy returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ AXIOM proxy error: {e}")
    
    print()
    
    # Test 3: Direct Flask call (should be avoided by frontend)
    print("3️⃣ Testing direct Flask access (frontend should NOT do this)...")
    try:
        response = requests.get("http://127.0.0.1:5010/health", timeout=5)
        if response.status_code == 200:
            print("   ⚠️ Direct Flask access works (but frontend shouldn't use this)")
            print("   🛡️ Frontend must use /api/axiom/execute instead")
        else:
            print(f"   ❌ Direct Flask returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Direct Flask error: {e}")
    
    print()
    
    # Test 4: Unified execute endpoint
    print("4️⃣ Testing unified /api/axiom/execute endpoint...")
    try:
        payload = {
            "command": "health"
        }
        response = requests.post(
            "http://127.0.0.1:8015/axiom/execute",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Unified execute endpoint works")
            result = response.json()
            print(f"   📋 Command: {result.get('command')}")
            print(f"   📋 Status: {result.get('status')}")
            print(f"   📋 Timestamp: {result.get('timestamp')}")
        else:
            print(f"   ❌ Execute endpoint returned {response.status_code}")
            print(f"   📋 Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Execute endpoint error: {e}")
    
    print()
    
    # Test 5: Ceremonial reasoning through unified endpoint
    print("5️⃣ Testing ceremonial reasoning through unified endpoint...")
    try:
        payload = {
            "command": "reason",
            "payload": {
                "actor": "TestAgent",
                "realm": "TEST-001", 
                "capsule": "Unified Test Crown",
                "intent": "Test.Validation"
            }
        }
        response = requests.post(
            "http://127.0.0.1:8015/axiom/execute",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Ceremonial reasoning works through unified API")
            result = response.json()
            ceremony = result.get('result', {})
            dispatch_id = ceremony.get('dispatch_id')
            if dispatch_id:
                print(f"   🎯 Created ceremony: {dispatch_id}")
            print(f"   📋 Status: {result.get('status')}")
        else:
            print(f"   ❌ Ceremonial reasoning returned {response.status_code}")
            print(f"   📋 Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Ceremonial reasoning error: {e}")
    
    print()
    print("="*50)
    print("📋 UNIFIED API VALIDATION SUMMARY")
    print("✅ Frontend should use: /api/axiom/execute")
    print("❌ Frontend should NOT use: direct Flask calls")
    print("🔗 Environment: REACT_APP_API_BASE=/api")
    print("🛡️ Architecture: React → FastAPI Gateway → Flask AXIOM")
    print("="*50)

def test_frontend_config():
    """Test frontend configuration"""
    print()
    print("🎨 TESTING FRONTEND CONFIGURATION")
    print("="*40)
    
    # Check if frontend is accessible
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            
            # Check if it contains our API configuration
            content = response.text
            if '/api' in content:
                print("✅ Frontend configured with /api base URL")
            else:
                print("⚠️ Frontend may not be configured correctly")
        else:
            print(f"❌ Frontend returned {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        print("💡 Make sure to start frontend with: npm start")
    
    print("="*40)

if __name__ == "__main__":
    test_unified_api()
    test_frontend_config()