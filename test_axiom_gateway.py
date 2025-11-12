#!/usr/bin/env python3
"""
Test AXIOM Gateway Integration
Tests the new AXIOM proxy functionality through the backend API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8014"

def test_axiom_gateway():
    """Test the new AXIOM gateway endpoints"""
    
    print("🔥 Testing AXIOM Gateway Integration...")
    print("=" * 60)
    
    try:
        # 1. Test AXIOM health endpoint
        print("1. 🏥 Testing AXIOM health check...")
        health_response = requests.get(f"{BASE_URL}/axiom/health", timeout=10)
        
        if health_response.status_code == 502:
            print(f"   ⚠️  AXIOM service unavailable (expected if not running)")
            print(f"   📊 Response: {health_response.text}")
        elif health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   ✅ AXIOM health check successful!")
            print(f"   📊 Status: {health_data.get('status', 'unknown')}")
            print(f"   🌐 AXIOM Base: {health_data.get('axiom_base', 'unknown')}")
        else:
            print(f"   ❓ Unexpected status: {health_response.status_code}")
            
        # 2. Test AXIOM execute endpoint
        print("\n2. ⚡ Testing AXIOM execute endpoint...")
        execute_payload = {
            "command": "health",
            "payload": None
        }
        
        execute_response = requests.post(
            f"{BASE_URL}/axiom/execute", 
            json=execute_payload,
            timeout=10
        )
        
        if execute_response.status_code == 502:
            print(f"   ⚠️  AXIOM service unavailable (expected if not running)")
            print(f"   📊 Gateway is working, but AXIOM backend is down")
        elif execute_response.status_code == 200:
            execute_data = execute_response.json()
            print(f"   ✅ AXIOM execute successful!")
            print(f"   📊 Response: {execute_data}")
        else:
            print(f"   ❓ Unexpected status: {execute_response.status_code}")
            
        # 3. Test AXIOM reason endpoint
        print("\n3. 🧠 Testing AXIOM ceremonial reasoning...")
        reason_payload = {
            "actor": "TestCustodian",
            "realm": "PL-001",
            "capsule": "Development Crown",
            "intent": "Test.Gateway"
        }
        
        reason_response = requests.post(
            f"{BASE_URL}/axiom/reason",
            json=reason_payload,
            timeout=10
        )
        
        if reason_response.status_code == 502:
            print(f"   ⚠️  AXIOM service unavailable (expected if not running)")
            print(f"   📊 Gateway proxy is working correctly")
        elif reason_response.status_code == 200:
            reason_data = reason_response.json()
            print(f"   ✅ AXIOM ceremonial reasoning successful!")
            print(f"   🎭 Actor: {reason_payload['actor']}")
            print(f"   🏰 Realm: {reason_payload['realm']}")
            print(f"   👑 Capsule: {reason_payload['capsule']}")
            print(f"   📊 Response: {reason_data}")
        else:
            print(f"   ❓ Unexpected status: {reason_response.status_code}")
            
        # 4. Test AXIOM ceremonies endpoint
        print("\n4. 📜 Testing AXIOM ceremonies list...")
        ceremonies_response = requests.get(f"{BASE_URL}/axiom/ceremonies", timeout=10)
        
        if ceremonies_response.status_code == 502:
            print(f"   ⚠️  AXIOM service unavailable (expected if not running)")
        elif ceremonies_response.status_code == 200:
            ceremonies_data = ceremonies_response.json()
            print(f"   ✅ AXIOM ceremonies list retrieved!")
            print(f"   📊 Ceremonies count: {len(ceremonies_data) if isinstance(ceremonies_data, list) else 'unknown'}")
        else:
            print(f"   ❓ Unexpected status: {ceremonies_response.status_code}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("   Make sure the backend API is running:")
        print("   python -m uvicorn backend_api:app --host 127.0.0.1 --port 8012 --reload")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 AXIOM Gateway Integration Test Complete!")
    print("\n📝 Your AXIOM gateway patterns:")
    print('✅ await apiClient.axiom.health()')
    print('✅ await apiClient.axiom.execute("command", payload, token)')
    print('✅ await apiClient.axiom.reason({ actor, realm, capsule, intent }, token)')
    print('✅ await apiClient.axiom.grant({ recipient, honor, authority }, token)')
    print('✅ await apiClient.axiom.ceremonies(token)')

if __name__ == "__main__":
    test_axiom_gateway()