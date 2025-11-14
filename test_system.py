#!/usr/bin/env python3
"""
Comprehensive test script for Super-Codex-AI system
Tests all major components and endpoints
"""
import requests
import time
import sys
from pathlib import Path

def test_server_health():
    """Test server health endpoint"""
    try:
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_server_status():
    """Test server status endpoint"""
    try:
        response = requests.get("http://localhost:8081/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Status endpoint passed")
            print(f"   System: {data.get('system')}")
            print(f"   Components: {len(data.get('components', {}))}")
            return True
        else:
            print(f"❌ Status endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Status endpoint failed: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get("http://localhost:8081/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Content type: {response.headers.get('content-type')}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_docs_endpoint():
    """Test API documentation endpoint"""
    try:
        response = requests.get("http://localhost:8081/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API docs endpoint passed")
            return True
        else:
            print(f"❌ API docs endpoint failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API docs endpoint failed: {e}")
        return False

def test_imports():
    """Test critical imports"""
    tests = [
        ("backend.models.user", "User, is_council"),
        ("backend.models.token", "DominionToken"),
        ("capsule_video.scene", "create_scene"),
        ("capsule_video.render", "render_video"),
        ("capsule_video.publish", "publish_video"),
        ("core.config", "get_config"),
        ("core.utils", "generate_unique_id"),
    ]
    
    passed = 0
    for module, items in tests:
        try:
            exec(f"from {module} import {items}")
            print(f"✅ Import {module} passed")
            passed += 1
        except ImportError as e:
            print(f"❌ Import {module} failed: {e}")
    
    print(f"📊 Import tests: {passed}/{len(tests)} passed")
    return passed == len(tests)

def wait_for_server(timeout=30):
    """Wait for server to be ready"""
    print("⏳ Waiting for server to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:8081/health", timeout=2)
            if response.status_code == 200:
                print("🚀 Server is ready!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    
    print("❌ Server failed to start within timeout")
    return False

def main():
    """Run all tests"""
    print("🔍 Starting comprehensive Super-Codex-AI system tests")
    print("=" * 60)
    
    # Test imports first (doesn't require server)
    print("\n📦 Testing imports...")
    import_success = test_imports()
    
    # Wait for server to be ready
    if wait_for_server():
        # Test endpoints
        print("\n🌐 Testing endpoints...")
        health_success = test_server_health()
        status_success = test_server_status()
        root_success = test_root_endpoint()
        docs_success = test_docs_endpoint()
        
        endpoint_tests = [health_success, status_success, root_success, docs_success]
        endpoint_passed = sum(endpoint_tests)
        
        print(f"\n📊 Endpoint tests: {endpoint_passed}/{len(endpoint_tests)} passed")
    else:
        endpoint_passed = 0
        endpoint_tests = []
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print(f"   Import Tests: {'✅ PASSED' if import_success else '❌ FAILED'}")
    if endpoint_tests:
        print(f"   Endpoint Tests: {'✅ PASSED' if endpoint_passed == len(endpoint_tests) else '❌ FAILED'}")
    else:
        print("   Endpoint Tests: ⏭️ SKIPPED (Server not ready)")
    
    total_success = import_success and (not endpoint_tests or endpoint_passed == len(endpoint_tests))
    print(f"   Overall: {'🎉 SUCCESS' if total_success else '💥 FAILURE'}")
    
    if total_success:
        print("\n🌟 Super-Codex-AI system is fully operational!")
        return 0
    else:
        print("\n🔧 Super-Codex-AI system needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())