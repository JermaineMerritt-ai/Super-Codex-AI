#!/usr/bin/env python3
"""
API Test Script for AXIOM-FLAME API.
Tests all endpoints to ensure they're working correctly.
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8080"

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check connection failed: {e}")
        return False

def test_governance_endpoints():
    """Test governance endpoints."""
    print("\n🔍 Testing governance endpoints...")
    
    try:
        # Test list rules
        response = requests.get(f"{BASE_URL}/v1/governance/rules", timeout=5)
        if response.status_code == 200:
            print(f"✅ List rules: {len(response.json())} rules found")
        else:
            print(f"❌ List rules failed: {response.status_code}")
            return False
            
        # Test create rule
        rule_data = {
            "name": "Test Rule",
            "description": "Test Description",
            "authority_level": "Standard",
            "seal_type": "Sacred"
        }
        response = requests.post(f"{BASE_URL}/v1/governance/rules", json=rule_data, timeout=5)
        if response.status_code == 200:
            rule_id = response.json()["id"]
            print(f"✅ Create rule: {rule_id}")
            
            # Test get specific rule
            response = requests.get(f"{BASE_URL}/v1/governance/rules/{rule_id}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Get rule: {response.json()['name']}")
                return True
            else:
                print(f"❌ Get rule failed: {response.status_code}")
                return False
        else:
            print(f"❌ Create rule failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Governance test failed: {e}")
        return False

def test_identity_endpoints():
    """Test identity endpoints."""
    print("\n🔍 Testing identity endpoints...")
    
    try:
        # Test list identities
        response = requests.get(f"{BASE_URL}/v1/identity/", timeout=5)
        if response.status_code == 200:
            print(f"✅ List identities: {len(response.json())} identities found")
            return True
        else:
            print(f"❌ List identities failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Identity test failed: {e}")
        return False

def test_recall_endpoints():
    """Test recall endpoints."""
    print("\n🔍 Testing recall endpoints...")
    
    try:
        # Test list recall entries
        response = requests.get(f"{BASE_URL}/v1/recall/", timeout=5)
        if response.status_code == 200:
            print(f"✅ List recall entries: {len(response.json())} entries found")
            return True
        else:
            print(f"❌ List recall entries failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Recall test failed: {e}")
        return False

def test_artifacts_endpoints():
    """Test artifacts endpoints."""
    print("\n🔍 Testing artifacts endpoints...")
    
    try:
        # Test list artifacts
        response = requests.get(f"{BASE_URL}/v1/artifacts", timeout=5)
        if response.status_code == 200:
            print(f"✅ List artifacts: {len(response.json())} artifacts found")
            return True
        else:
            print(f"❌ List artifacts failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Artifacts test failed: {e}")
        return False

def main():
    """Run all API tests."""
    print("🧪 AXIOM-FLAME API Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_governance_endpoints,
        test_identity_endpoints,
        test_recall_endpoints,
        test_artifacts_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            break  # Stop on first failure
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! API is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check server logs.")
        return 1

if __name__ == "__main__":
    sys.exit(main())