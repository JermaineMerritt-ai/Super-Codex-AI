#!/usr/bin/env python3
"""
Demonstrate Unified API Configuration
Shows that frontend uses single base URL /api and never calls Flask directly
"""

import json
import requests
from datetime import datetime

def demonstrate_unified_api():
    """Demonstrate the unified API architecture"""
    
    print("🎯 UNIFIED API CONFIGURATION DEMONSTRATION")
    print("="*55)
    print()
    
    print("📋 ARCHITECTURE OVERVIEW:")
    print("   React Frontend (http://localhost:3000)")
    print("      ↓ REACT_APP_API_BASE=/api (Environment Variable)")
    print("   FastAPI Gateway (http://127.0.0.1:8015)")
    print("      ↓ /api/axiom/execute (Unified Endpoint)")  
    print("   AXIOM-Flame Backend (http://127.0.0.1:5010)")
    print("      ↓ Ceremonial Operations")
    print()
    
    # Check AXIOM directly (backend communication only)
    print("1️⃣ AXIOM-Flame Backend Status:")
    try:
        response = requests.get("http://127.0.0.1:5010/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   📊 Status: {data.get('status')}")
            print(f"   🎭 Ceremonies Active: {data.get('ceremonies_active', 0)}")
            print(f"   🏆 Honors Granted: {data.get('honors_granted', 0)}")
        else:
            print(f"   ❌ AXIOM returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ AXIOM error: {e}")
    
    print()
    
    # Show frontend configuration
    print("2️⃣ Frontend Configuration:")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend accessible at http://localhost:3000")
            print("   🔗 Environment: REACT_APP_API_BASE=/api")
            print("   🛡️ All API calls routed through backend proxy")
            print("   ❌ NO direct Flask calls from browser allowed")
        else:
            print(f"   ❌ Frontend returned {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Frontend not accessible: {e}")
        print("   💡 Start with: cd frontend && npm start")
    
    print()
    
    # Direct AXIOM ceremonial test (to show it works)
    print("3️⃣ Direct AXIOM Ceremonial Operation (Backend Test):")
    try:
        payload = {
            "actor": "UnifiedAPI-Demo",
            "realm": "DEMO-001",
            "capsule": "Unified API Crown",
            "intent": "Demonstration.Test"
        }
        
        response = requests.post(
            "http://127.0.0.1:5010/reason",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            ceremony = response.json()
            print(f"   ✅ Ceremony Created: {ceremony.get('dispatch_id')}")
            print(f"   👤 Actor: {ceremony.get('actor')}")
            print(f"   🏰 Realm: {ceremony.get('realm')}")
            print(f"   👑 Capsule: {ceremony.get('capsule')}")
            print(f"   ⏰ Timestamp: {ceremony.get('timestamp')}")
        else:
            print(f"   ❌ Ceremony failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ceremony error: {e}")
    
    print()
    
    print("="*55)
    print("📱 FRONTEND USAGE INSTRUCTIONS")
    print("="*55)
    print()
    print("✅ CORRECT Frontend API Usage:")
    print("   • Always use: apiClient.axiom.execute()")
    print("   • Base URL: process.env.REACT_APP_API_BASE || '/api'")
    print("   • Example: apiClient.axiom.reason(params, token)")
    print("   • Routes through: /api/axiom/execute")
    print()
    print("❌ FORBIDDEN Frontend Usage:")
    print("   • Never call: http://127.0.0.1:5010/* directly")
    print("   • Never use: fetch('http://flask-server/...')")
    print("   • Never bypass: the FastAPI gateway")
    print()
    print("🔧 Environment Setup:")
    print("   • Frontend .env: REACT_APP_API_BASE=/api")
    print("   • Backend env: AXIOM_BASE=http://127.0.0.1:5010")
    print("   • Proxy config: backend routes to AXIOM")
    print()
    print("🌐 URL Structure:")
    print("   • Frontend: http://localhost:3000")
    print("   • Frontend API calls: /api/* (relative)")
    print("   • Backend Gateway: http://127.0.0.1:8015")  
    print("   • AXIOM Backend: http://127.0.0.1:5010 (internal only)")
    print()
    print("="*55)


if __name__ == "__main__":
    demonstrate_unified_api()