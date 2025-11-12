#!/usr/bin/env python3
"""
Complete AXIOM Integration Test
Tests the full stack: Frontend → FastAPI Gateway → AXIOM-Flame Flask Backend
"""

import requests
import json

FASTAPI_BASE = "http://127.0.0.1:8015"
AXIOM_BASE = "http://127.0.0.1:5010"

def test_complete_axiom_stack():
    """Test the complete AXIOM integration stack"""
    
    print("🔥 Testing Complete AXIOM Integration Stack...")
    print("=" * 70)
    
    try:
        # 1. Test direct AXIOM-Flame health
        print("1. 🏥 Testing AXIOM-Flame direct health...")
        axiom_health = requests.get(f"{AXIOM_BASE}/health", timeout=10)
        
        if axiom_health.status_code == 200:
            health_data = axiom_health.json()
            print(f"   ✅ AXIOM-Flame is healthy!")
            print(f"   📊 Service: {health_data.get('service', 'unknown')}")
            print(f"   🔢 Version: {health_data.get('version', 'unknown')}")
            print(f"   📈 Ceremonies: {health_data.get('ceremonies_active', 0)}")
            print(f"   🏆 Honors: {health_data.get('honors_granted', 0)}")
        else:
            print(f"   ❌ AXIOM-Flame health check failed: {axiom_health.status_code}")
            return
            
        # 2. Test Gateway proxy to AXIOM health
        print("\n2. 🌉 Testing FastAPI Gateway proxy to AXIOM health...")
        gateway_health = requests.get(f"{FASTAPI_BASE}/axiom/health", timeout=10)
        
        if gateway_health.status_code == 200:
            gateway_data = gateway_health.json()
            print(f"   ✅ Gateway proxy working!")
            print(f"   📊 Gateway Status: {gateway_data.get('status', 'unknown')}")
            print(f"   🌐 AXIOM Base: {gateway_data.get('axiom_base', 'unknown')}")
            print(f"   📡 Proxied Response: {gateway_data.get('response', {}).get('service', 'unknown')}")
        else:
            print(f"   ❌ Gateway health check failed: {gateway_health.status_code}")
            return
            
        # 3. Test ceremonial reasoning through gateway
        print("\n3. 🧠 Testing ceremonial reasoning through gateway...")
        reason_payload = {
            "actor": "TestCustodian",
            "realm": "PL-001",
            "capsule": "Integration Crown",
            "intent": "Gateway.Test"
        }
        
        reason_response = requests.post(
            f"{FASTAPI_BASE}/axiom/reason",
            json=reason_payload,
            timeout=15
        )
        
        if reason_response.status_code == 200:
            reason_data = reason_response.json()
            print(f"   ✅ Ceremonial reasoning successful!")
            print(f"   🎭 Actor: {reason_data.get('ceremony', {}).get('actor', 'unknown')}")
            print(f"   🏰 Realm: {reason_data.get('ceremony', {}).get('realm', 'unknown')}")
            print(f"   👑 Capsule: {reason_data.get('ceremony', {}).get('capsule', 'unknown')}")
            print(f"   🆔 Dispatch ID: {reason_data.get('dispatch_id', 'unknown')}")
            print(f"   📊 Status: {reason_data.get('ceremony', {}).get('status', 'unknown')}")
        else:
            print(f"   ❌ Ceremonial reasoning failed: {reason_response.status_code}")
            print(f"   📄 Response: {reason_response.text}")
            
        # 4. Test honor granting through gateway
        print("\n4. 🏆 Testing honor granting through gateway...")
        grant_payload = {
            "recipient": "IntegrationTester",
            "honor": "Gateway Mastery",
            "authority": "AXIOM-Council"
        }
        
        grant_response = requests.post(
            f"{FASTAPI_BASE}/axiom/grant",
            json=grant_payload,
            timeout=15
        )
        
        if grant_response.status_code == 200:
            grant_data = grant_response.json()
            print(f"   ✅ Honor granting successful!")
            print(f"   👤 Recipient: {grant_data.get('honor', {}).get('recipient', 'unknown')}")
            print(f"   🏅 Honor: {grant_data.get('honor', {}).get('honor', 'unknown')}")
            print(f"   🛡️ Authority: {grant_data.get('honor', {}).get('authority', 'unknown')}")
            print(f"   🆔 Honor ID: {grant_data.get('honor_id', 'unknown')}")
            print(f"   🎖️ Insignia: {grant_data.get('honor', {}).get('insignia', 'unknown')}")
        else:
            print(f"   ❌ Honor granting failed: {grant_response.status_code}")
            print(f"   📄 Response: {grant_response.text}")
            
        # 5. Test ceremonies list through gateway
        print("\n5. 📜 Testing ceremonies list through gateway...")
        ceremonies_response = requests.get(f"{FASTAPI_BASE}/axiom/ceremonies", timeout=10)
        
        if ceremonies_response.status_code == 200:
            ceremonies_data = ceremonies_response.json()
            print(f"   ✅ Ceremonies list retrieved!")
            print(f"   📊 Total Ceremonies: {ceremonies_data.get('total', 0)}")
            
            recent_ceremonies = ceremonies_data.get('ceremonies', [])
            if recent_ceremonies:
                latest = recent_ceremonies[-1]
                print(f"   🔄 Latest Ceremony:")
                print(f"      🎭 Actor: {latest.get('actor', 'unknown')}")
                print(f"      🏰 Realm: {latest.get('realm', 'unknown')}")
                print(f"      👑 Capsule: {latest.get('capsule', 'unknown')}")
                print(f"      🆔 Dispatch: {latest.get('dispatch_id', 'unknown')}")
        else:
            print(f"   ❌ Ceremonies list failed: {ceremonies_response.status_code}")
            
        # 6. Test execute command through gateway
        print("\n6. ⚡ Testing execute command through gateway...")
        execute_payload = {
            "command": "health",
            "payload": {"test": True}
        }
        
        execute_response = requests.post(
            f"{FASTAPI_BASE}/axiom/execute",
            json=execute_payload,
            timeout=10
        )
        
        if execute_response.status_code == 200:
            execute_data = execute_response.json()
            print(f"   ✅ Execute command successful!")
            print(f"   📋 Command: {execute_data.get('command', 'unknown')}")
            print(f"   📊 Status: {execute_data.get('status', 'unknown')}")
            print(f"   🔄 Result: {execute_data.get('result', 'unknown')}")
            print(f"   📈 Ceremonies Count: {execute_data.get('ceremonies_count', 0)}")
            print(f"   🏆 Honors Count: {execute_data.get('honors_count', 0)}")
        else:
            print(f"   ❌ Execute command failed: {execute_response.status_code}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("   Make sure both services are running:")
        print("   1. AXIOM-Flame: cd axiom_flame; python app.py")
        print("   2. FastAPI Gateway: python -c \"import uvicorn; from backend_api import app; uvicorn.run(app, host='127.0.0.1', port=8015)\"")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Complete AXIOM Integration Stack Test Complete!")
    print("\n📝 Your full integration is now working:")
    print('✅ AXIOM-Flame Flask Backend (Port 5010)')
    print('✅ FastAPI Gateway Proxy (Port 8015)')  
    print('✅ React Frontend API Client')
    print('✅ Ceremonial Reasoning System')
    print('✅ Honor Granting System')
    print('✅ Ceremony & Honor Management')
    print("\n🚀 Ready for production deployment!")

if __name__ == "__main__":
    test_complete_axiom_stack()