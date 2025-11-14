#!/usr/bin/env python3
"""
Test role-based Dominion system
"""
import requests
import time

def test_role_based_system():
    """Test the role-based access system"""
    base_url = "http://127.0.0.1:8002"
    
    # Test main role selector
    print("🧑‍🚀 Testing Role Selector...")
    try:
        response = requests.get(f"{base_url}/dominion/roles", timeout=5)
        print(f"✅ Role selector: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Role selector error: {e}")
    
    # Test each role type
    roles = ["contributor", "council", "heir", "general"]
    
    for role in roles:
        print(f"\n🎭 Testing {role.title()} Role...")
        try:
            # Test role page
            response = requests.get(f"{base_url}/dominion/role/{role}", timeout=5)
            print(f"✅ {role} interface: {response.status_code}")
            
            # Test role scrolls API
            response = requests.get(f"{base_url}/dominion/role/{role}/scrolls", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {role} scrolls: {len(data.get('recent_scrolls', []))} scrolls")
                print(f"   📜 Cadence: {len(data.get('scroll_cadence', []))} items")
            else:
                print(f"❌ {role} scrolls: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {role} error: {e}")
    
    # Test invalid role
    print("\n🚫 Testing Invalid Role...")
    try:
        response = requests.get(f"{base_url}/dominion/role/invalid", timeout=5)
        print(f"✅ Invalid role handling: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid role error: {e}")
    
    print("\n🌟 Role-Based System Test Complete!")
    print("Access the system at:")
    print(f"  🧑‍🚀 Role Selector: {base_url}/dominion/roles")
    print(f"  🧬 Contributor: {base_url}/dominion/role/contributor")
    print(f"  🏛️ Council: {base_url}/dominion/role/council")
    print(f"  🌠 Heir: {base_url}/dominion/role/heir")
    print(f"  🌌 General: {base_url}/dominion/role/general")

if __name__ == "__main__":
    print("🧑‍🚀 Super-Codex-AI Role-Based System Test")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    test_role_based_system()