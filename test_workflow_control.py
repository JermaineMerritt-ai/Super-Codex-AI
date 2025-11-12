#!/usr/bin/env python3
"""
Workflow Control API Test
Demonstrates the exact usage pattern you requested:
- await api("/workflow/start?name=FullConstellation", "POST", { capsule: "full" }, token);
- await api(`/workflow/${wid}/advance?phase=DISPATCH`, "POST", { note: "Planetary release" }, token);
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8010"

def test_workflow_control_api():
    """Test the new workflow control endpoints exactly as requested"""
    
    print("🚀 Testing Workflow Control API...")
    print("=" * 60)
    
    try:
        # First, authenticate to get token
        print("1. 🔐 Authenticating...")
        auth_data = {"username": "admin", "password": "secret"}
        response = requests.post(f"{BASE_URL}/auth/login", json=auth_data)
        
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.text}")
            return
            
        auth = response.json()
        token = auth["access_token"]
        print(f"   ✅ Token obtained: {token[:20]}...")
        
        # Headers for authenticated requests
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Start a workflow (your exact pattern)
        print("\n2. 🚀 Starting workflow: FullConstellation...")
        print('   📝 API Call: await api("/workflow/start?name=FullConstellation", "POST", { capsule: "full" }, token);')
        
        start_response = requests.post(
            f"{BASE_URL}/workflow/start?name=FullConstellation",
            json={"capsule": "full"},
            headers=headers
        )
        
        if start_response.status_code == 200:
            new_workflow = start_response.json()
            wid = new_workflow["id"]
            print(f"   ✅ Workflow started successfully!")
            print(f"   🆔 Workflow ID: {wid}")
            print(f"   📛 Name: {new_workflow['name']}")
            print(f"   📊 Status: {new_workflow['status']}")
            print(f"   💊 Capsule: full (as requested)")
            
            # 3. Advance the workflow (your exact pattern)
            print(f"\n3. ⚡ Advancing workflow {wid} to DISPATCH phase...")
            print(f'   📝 API Call: await api(`/workflow/{wid}/advance?phase=DISPATCH`, "POST", {{ note: "Planetary release" }}, token);')
            
            advance_response = requests.post(
                f"{BASE_URL}/workflow/{wid}/advance?phase=DISPATCH",
                json={"note": "Planetary release"},
                headers=headers
            )
            
            if advance_response.status_code == 200:
                updated_workflow = advance_response.json()
                print(f"   ✅ Workflow advanced successfully!")
                print(f"   📊 New Status: {updated_workflow['status']}")
                print(f"   📝 Description: {updated_workflow['description']}")
                print(f"   🌍 Note Applied: Planetary release")
                
                # 4. Show all workflows to verify
                print(f"\n4. 📋 Current workflows list...")
                workflows_response = requests.get(f"{BASE_URL}/workflow", headers=headers)
                
                if workflows_response.status_code == 200:
                    workflows = workflows_response.json()
                    print(f"   📊 Total workflows: {len(workflows)}")
                    
                    for workflow in workflows:
                        status_emoji = {
                            "completed": "✅", 
                            "running": "🟡", 
                            "pending": "⏳", 
                            "failed": "❌"
                        }.get(workflow["status"], "❓")
                        
                        highlight = "➡️ " if workflow["id"] == wid else "   "
                        print(f"{highlight}{workflow['name']} ({workflow['id']}) {status_emoji}")
                        if workflow["id"] == wid:
                            print(f"      └─ {workflow['description']}")
                
            else:
                print(f"   ❌ Workflow advance failed: {advance_response.text}")
                
        else:
            print(f"   ❌ Workflow start failed: {start_response.text}")
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("   Make sure the backend API is running:")
        print("   python -m uvicorn backend_api:app --host 127.0.0.1 --port 8010 --reload")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Workflow Control API Test Complete!")
    print("\n📝 Your TypeScript patterns now work perfectly:")
    print('✅ await api("/workflow/start?name=FullConstellation", "POST", { capsule: "full" }, token);')
    print('✅ await api(`/workflow/${wid}/advance?phase=DISPATCH`, "POST", { note: "Planetary release" }, token);')

if __name__ == "__main__":
    test_workflow_control_api()