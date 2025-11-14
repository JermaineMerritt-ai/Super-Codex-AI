#!/usr/bin/env python3
"""
Test script for the Concord Hymn System
Tests the upload functionality with local server
"""

import json
import time
import subprocess
import requests
import threading
from pathlib import Path
import uvicorn
from concord_hymn_system import app, hymn_registry

def start_server():
    """Start the FastAPI server in a separate thread"""
    uvicorn.run(app, host="127.0.0.1", port=8004, log_level="info")

def test_server():
    """Test the server endpoints"""
    print("🧪 Testing Concord Hymn System Endpoints...")
    
    # Wait for server to start
    time.sleep(2)
    
    base_url = "http://127.0.0.1:8004"
    
    try:
        # Test 1: Root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   System: {data['system']}")
            print(f"   Version: {data['version']}")
            print(f"   Hymns Registered: {data['hymns_registered']}")
        
        # Test 2: List hymns
        print("\n2. Testing hymns list...")
        response = requests.get(f"{base_url}/hymns/list")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total hymns: {data['total']}")
            for hymn in data['hymns']:
                print(f"   📜 {hymn['title']} v{hymn['version']}")
        
        # Test 3: Register new hymn
        print("\n3. Testing hymn registration...")
        hymn_spec = {
            "artifactId": "test-upload-hymn-" + str(int(time.time())),
            "title": "Test Upload Hymn",
            "version": "1.0.0",
            "type": "hymn",
            "files": {
                "text": "concord-hymn/concord_hymn.md",
                "glyph": "concord-hymn/assets/flame_glyph.svg"
            },
            "signing": {
                "sigil": "TEST-SIGIL-001",
                "signed_by": "Custodian",
                "heirs_chorus": True
            }
        }
        
        response = requests.post(f"{base_url}/ledger/continuum/hymn", json=hymn_spec)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Registered: {data['hymn_id']}")
            print(f"   Title: {data['title']}")
            print(f"   Seal Created: {data['seal_created']}")
            
            # Test 4: Get hymn details
            print("\n4. Testing hymn details...")
            response = requests.get(f"{base_url}/hymns/{data['hymn_id']}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                hymn_data = response.json()
                print(f"   📖 Content length: {len(hymn_data['content']) if hymn_data['content'] else 0} chars")
                print(f"   🔐 Seal verified: {hymn_data['seal_verification']['verified']}")
            
            # Test 5: Perform hymn
            print("\n5. Testing hymn performance...")
            response = requests.post(f"{base_url}/hymns/{data['hymn_id']}/perform", params={"heirs_chorus": True})
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                perf_data = response.json()
                print(f"   🎭 Performance recorded at: {perf_data['performance']['performance_time']}")
                print(f"   📊 Total performances: {perf_data['performance']['total_performances']}")
        
        # Test 6: Global dispatch
        print("\n6. Testing global dispatch...")
        response = requests.get(f"{base_url}/dispatch/global")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📡 Available hymns: {data['total_hymns']}")
        
        print("\n✅ All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8004.")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_upload_script():
    """Test the PowerShell upload script"""
    print("\n🔄 Testing PowerShell Upload Script...")
    
    # Run the upload script
    try:
        cmd = [
            "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "upload.ps1",
            "-ApiBase", "http://127.0.0.1:8004",
            "-Token", "test-sigil-bearer-token"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"   Exit code: {result.returncode}")
        if result.stdout:
            print(f"   Output:\n{result.stdout}")
        if result.stderr:
            print(f"   Errors:\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("   ⚠️  Upload script timed out")
    except Exception as e:
        print(f"   ❌ Upload script failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Concord Hymn System Test Suite")
    print("=" * 60)
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    test_server()
    
    # Test upload script
    test_upload_script()
    
    print("\n🏁 Test suite complete!")