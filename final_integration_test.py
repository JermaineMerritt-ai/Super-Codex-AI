#!/usr/bin/env python3
"""
Final comprehensive test of the Concord Hymn System
Tests both API endpoints and PowerShell upload script
"""

import json
import time
import subprocess
import requests
import threading
import signal
import sys
import os
from pathlib import Path
import uvicorn
from concord_hymn_system import app, hymn_registry

server_process = None

def start_server_in_background():
    """Start the FastAPI server in a subprocess"""
    global server_process
    try:
        # Start uvicorn in a subprocess
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "concord_hymn_system:app", 
            "--host", "127.0.0.1", 
            "--port", "8004"
        ], cwd=os.getcwd())
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server is running
        for attempt in range(10):
            try:
                response = requests.get("http://127.0.0.1:8004/")
                if response.status_code == 200:
                    print(f"✅ Server started successfully on http://127.0.0.1:8004")
                    return True
            except:
                time.sleep(1)
                
        print("❌ Server failed to start")
        return False
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def stop_server():
    """Stop the FastAPI server"""
    global server_process
    if server_process:
        server_process.terminate()
        server_process.wait()
        print("🛑 Server stopped")

def test_api_endpoints():
    """Test the server endpoints"""
    print("\n🧪 Testing API Endpoints...")
    
    base_url = "http://127.0.0.1:8004"
    
    try:
        # Test 1: Root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ System: {data['system']} v{data['version']}")
            print(f"   📊 Hymns Registered: {data['hymns_registered']}")
        
        # Test 2: Register a test hymn via API
        print("\n2. Testing hymn registration via API...")
        hymn_spec = {
            "artifactId": "api-test-hymn-" + str(int(time.time())),
            "title": "API Test Hymn",
            "version": "1.0.0",
            "type": "hymn",
            "audience": ["heirs"],
            "cycles": ["daily"],
            "files": {
                "text": "concord-hymn/concord_hymn.md"
            },
            "signing": {
                "sigil": "API-TEST-001",
                "signed_by": "Custodian",
                "heirs_chorus": True
            }
        }
        
        response = requests.post(f"{base_url}/ledger/continuum/hymn", json=hymn_spec)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Registered: {data['hymn_id']}")
            print(f"   📜 Title: {data['title']}")
            print(f"   🔐 Seal Created: {data['seal_created']}")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_upload_script():
    """Test the PowerShell upload script"""
    print("\n🔄 Testing PowerShell Upload Script...")
    
    try:
        cmd = [
            "powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "upload.ps1",
            "-ApiBase", "http://127.0.0.1:8004",
            "-Token", "test-sigil-bearer-token"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        print(f"   Exit Code: {result.returncode}")
        
        if result.stdout:
            print(f"   📤 Upload Output:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"      {line}")
        
        if result.stderr and result.stderr.strip():
            print(f"   ⚠️  Upload Errors:")
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    print(f"      {line}")
        
        # Check if upload was successful
        if result.returncode == 0:
            print("   ✅ Upload script completed successfully!")
            return True
        else:
            print(f"   ⚠️  Upload script exited with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Upload script timed out")
        return False
    except Exception as e:
        print(f"   ❌ Upload script failed: {e}")
        return False

def check_hymn_count():
    """Check how many hymns are registered"""
    try:
        response = requests.get("http://127.0.0.1:8004/hymns/list")
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Final Statistics:")
            print(f"   📚 Total Hymns: {data['total']}")
            for hymn in data['hymns']:
                print(f"   🎵 {hymn['title']} v{hymn['version']}")
                print(f"      🆔 ID: {hymn['artifact_id']}")
                print(f"      🎭 Performances: {hymn['performance_count']}")
                print(f"      🔐 SIGIL Protected: {'Yes' if hymn['has_sigil'] else 'No'}")
            return True
    except Exception as e:
        print(f"❌ Could not get hymn statistics: {e}")
        return False

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Interrupt received, shutting down...")
    stop_server()
    sys.exit(0)

if __name__ == "__main__":
    print("🚀 Concord Hymn System - Final Integration Test")
    print("=" * 80)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start server
        if not start_server_in_background():
            print("❌ Could not start server, aborting tests")
            sys.exit(1)
        
        # Run API tests
        api_success = test_api_endpoints()
        
        # Run upload script test
        upload_success = test_upload_script()
        
        # Check final hymn count
        stats_success = check_hymn_count()
        
        # Summary
        print(f"\n🏁 Test Summary:")
        print(f"   🔌 API Tests: {'✅ PASSED' if api_success else '❌ FAILED'}")
        print(f"   📤 Upload Script: {'✅ PASSED' if upload_success else '❌ FAILED'}")
        print(f"   📊 Statistics: {'✅ PASSED' if stats_success else '❌ FAILED'}")
        
        if api_success and upload_success and stats_success:
            print(f"\n🎉 All tests PASSED! Concord Hymn System is ready!")
            print(f"🌐 Server running at: http://127.0.0.1:8004")
            print(f"📖 API Documentation: http://127.0.0.1:8004/docs")
        else:
            print(f"\n⚠️  Some tests failed. Please review output above.")
            
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
    finally:
        # Cleanup
        stop_server()
        print("\n✨ Test suite complete!")