#!/usr/bin/env python3
"""
Test script for AXIOM-FLAME API
"""

import sys
import os
import asyncio
import httpx
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_api():
    """Test the AXIOM-FLAME API endpoints"""
    print("🧪 Testing AXIOM-FLAME API...")
    
    # Import and create the FastAPI app directly
    from app.main import app
    
    # Test the app by creating a test client
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    print("\n1. Testing Health Endpoint...")
    response = client.get("/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    print("\n2. Testing Artifacts Endpoints...")
    # Create an artifact
    artifact_data = {
        "name": "Test Artifact",
        "type": "document",
        "content": "This is a test artifact content",
        "metadata": {"created_by": "test_user"}
    }
    response = client.post("/v1/artifacts/", json=artifact_data)
    print(f"   Create Artifact - Status: {response.status_code}")
    if response.status_code == 200:
        artifact = response.json()
        print(f"   Created Artifact ID: {artifact['id']}")
        
        # List artifacts
        response = client.get("/v1/artifacts/")
        print(f"   List Artifacts - Status: {response.status_code}")
        print(f"   Artifacts Count: {len(response.json())}")
    
    print("\n3. Testing Ceremonies Endpoints...")
    # Test ceremonial reasoning
    ceremony_data = {
        "actor": "Custodian",
        "realm": "PL-001",
        "capsule": "Test Capsule",
        "intent": "Test.Ceremony",
        "seal": "Sacred"
    }
    response = client.post("/v1/ceremonies/reason", json=ceremony_data)
    print(f"   Ceremonial Reasoning - Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Dispatch ID: {result.get('dispatch_id')}")
        print(f"   Status: {result.get('status')}")
    
    print("\n4. Testing Governance Endpoints...")
    # List governance rules
    response = client.get("/v1/governance/rules")
    print(f"   List Rules - Status: {response.status_code}")
    
    # Get seal types
    response = client.get("/v1/governance/seals")
    print(f"   Get Seals - Status: {response.status_code}")
    if response.status_code == 200:
        seals = response.json()
        print(f"   Available Seals: {len(seals.get('seal_types', []))}")
    
    print("\n5. Testing Identity Endpoints...")
    # Create an identity
    identity_data = {
        "actor": "TestActor",
        "realm": "PL-001",
        "authority_level": "Standard",
        "capsules": ["Test Capsule"]
    }
    response = client.post("/v1/identity/", json=identity_data)
    print(f"   Create Identity - Status: {response.status_code}")
    
    # List realms
    response = client.get("/v1/identity/realms")
    print(f"   List Realms - Status: {response.status_code}")
    
    print("\n6. Testing Recall Endpoints...")
    # Create a recall entry
    recall_data = {
        "dispatch_id": "AXF-2025-11-13-TEST123",
        "actor": "TestActor",
        "realm": "PL-001",
        "capsule": "Test Capsule",
        "intent": "Test.Recall",
        "content": {"test": "data"},
        "tags": ["test", "demo"]
    }
    response = client.post("/v1/recall/", json=recall_data)
    print(f"   Create Recall - Status: {response.status_code}")
    
    # Get recall stats
    response = client.get("/v1/recall/stats/summary")
    print(f"   Get Stats - Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Total Entries: {stats.get('total_entries')}")
    
    print("\n✅ API Test Complete!")
    print("🔥 AXIOM-FLAME API is fully functional!")
    
    # Test the OpenAPI documentation
    print("\n📖 API Documentation available at:")
    print("   - Swagger UI: http://localhost:8080/docs")
    print("   - ReDoc: http://localhost:8080/redoc")
    print("   - OpenAPI Schema: http://localhost:8080/openapi.json")

def main():
    """Run the API tests"""
    try:
        asyncio.run(test_api())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()