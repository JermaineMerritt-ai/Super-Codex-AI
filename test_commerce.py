#!/usr/bin/env python3
"""
Simple test script for Sovereign Commerce Platform
Tests basic endpoints without importing the main module
"""

import requests
import time
import json

# Test configuration
BASE_URL = "http://127.0.0.1:8081"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_homepage():
    """Test the homepage"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Homepage loads successfully")
            return True
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Homepage error: {e}")
        return False

def test_api_docs():
    """Test API documentation"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API docs accessible")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Sovereign Commerce Platform")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Homepage", test_homepage),
        ("API Documentation", test_api_docs)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        if test_func():
            passed += 1
        time.sleep(0.5)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"🏆 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Sovereign Commerce Platform is operational.")
        print(f"🌐 Access your platform at: {BASE_URL}")
        print(f"📚 API documentation: {BASE_URL}/docs")
        return True
    else:
        print("⚠️  Some tests failed. Please check server logs.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)