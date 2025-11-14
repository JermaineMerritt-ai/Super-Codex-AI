#!/usr/bin/env python3
"""
Test the Dominion Command Center interface
"""
import requests
import time

def test_command_center():
    base_url = "http://127.0.0.1:8001"
    
    # Test endpoints
    endpoints = [
        "/health",
        "/dominion",
        "/dominion/ceremony", 
        "/dominion/command"
    ]
    
    print("🔥 Testing Dominion Command Center Interface")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅ SUCCESS" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
            print(f"{endpoint:<30} {status}")
        except requests.exceptions.RequestException as e:
            print(f"{endpoint:<30} ❌ ERROR: {str(e)}")
    
    print("\n🎯 Command Center Access URLs:")
    print(f"Main Interface:    {base_url}/dominion")
    print(f"Command Center:    {base_url}/dominion/command")
    print(f"Ceremony Dashboard: {base_url}/dominion/ceremony")

if __name__ == "__main__":
    test_command_center()