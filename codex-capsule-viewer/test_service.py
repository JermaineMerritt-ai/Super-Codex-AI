#!/usr/bin/env python3
"""
Test script for the Codex Capsule Viewer service
"""
import requests
import time
import subprocess
import sys
from pathlib import Path

def test_service():
    # Test if service is running
    try:
        response = requests.get("http://127.0.0.1:8082/health", timeout=5)
        print(f"✅ Health check successful: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_capsules_api():
    try:
        # Test list capsules
        response = requests.get("http://127.0.0.1:8082/api/capsules", timeout=5)
        capsules = response.json()
        print(f"✅ Found {len(capsules)} capsules")
        
        # Test get specific capsule
        if capsules:
            first_capsule_id = capsules[0]['id']
            response = requests.get(f"http://127.0.0.1:8082/api/capsules/{first_capsule_id}", timeout=5)
            capsule = response.json()
            print(f"✅ Retrieved capsule: {capsule['title']}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Capsules API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Codex Capsule Viewer Service...")
    
    if test_service():
        print("🧪 Running API tests...")
        test_capsules_api()
    else:
        print("💡 Service not running. Please start it manually:")
        print("   cd codex-capsule-viewer/services")
        print("   python main.py")