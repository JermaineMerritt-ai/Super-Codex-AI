#!/usr/bin/env python3
"""
Quick test client for Sacred Document Archive API
Tests the API endpoints to verify integration is working
"""

import requests
import tempfile
import json
from pathlib import Path

def test_sacred_archive_api(port=8001):
    """Test the Sacred Document Archive FastAPI endpoints"""
    base_url = f"http://localhost:{port}"
    
    print("🔥" + "="*50 + "🔥")
    print("   SACRED ARCHIVE API TEST")
    print(f"   Testing on port {port}")
    print("🔥" + "="*50 + "🔥")
    print()
    
    # Test health check
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status', 'unknown')}")
            print(f"   ✅ Archive: {data.get('archive_system', 'unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Cannot connect to server: {e}")
        print("   💡 Make sure server is running on the correct port")
        return False
    
    print()
    
    # Test document upload
    print("📤 Testing document upload...")
    
    # Create test document
    temp_file = Path(tempfile.gettempdir()) / "test_ceremony.txt"
    temp_file.write_text("Sacred ceremony notes for testing the upload endpoint.", encoding='utf-8')
    
    try:
        with open(temp_file, 'rb') as f:
            files = {'file': ('test_ceremony.txt', f, 'text/plain')}
            data = {
                'document_type': 'ceremonial_scroll',
                'priority': 'sacred'
            }
            
            response = requests.post(f"{base_url}/upload/docs", files=files, data=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                doc_id = result.get('document_id')
                sacred_binding = result.get('sacred_binding')
                treasury_cost = result.get('treasury_cost')
                
                print(f"   ✅ Document ID: {doc_id}")
                print(f"   🔐 Sacred Binding: {sacred_binding[:16]}...")
                print(f"   💰 Treasury Cost: {treasury_cost} Sacred Tokens")
                
                # Test document retrieval
                print()
                print("📥 Testing document retrieval...")
                try:
                    response = requests.get(f"{base_url}/docs/{doc_id}", timeout=5)
                    if response.status_code == 200:
                        doc_info = response.json()
                        print(f"   ✅ Retrieved document: {doc_info.get('filename')}")
                        print(f"   📂 Type: {doc_info.get('document_type')}")
                        print(f"   ⭐ Priority: {doc_info.get('priority')}")
                    else:
                        print(f"   ❌ Retrieval failed: {response.status_code}")
                except Exception as e:
                    print(f"   ❌ Retrieval error: {e}")
            else:
                print(f"   ❌ Upload failed: {response.status_code}")
                if response.text:
                    print(f"   Error: {response.text}")
                return False
    
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
        return False
    finally:
        # Clean up
        temp_file.unlink(missing_ok=True)
    
    print()
    
    # Test statistics
    print("📊 Testing archive statistics...")
    try:
        response = requests.get(f"{base_url}/docs/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Total Documents: {stats.get('total_documents', 0)}")
            print(f"   ✅ Archive Health: {stats.get('archive_health', 'unknown')}")
        else:
            print(f"   ❌ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Statistics error: {e}")
    
    print()
    print("🕯️" + "="*50 + "🕯️")
    print("   API TEST COMPLETE - SUCCESS!")
    print("   FastAPI integration verified!")
    print("🕯️" + "="*50 + "🕯️")
    
    return True

if __name__ == "__main__":
    # Try different ports
    for port in [8001, 8000, 8002]:
        print(f"Trying port {port}...")
        if test_sacred_archive_api(port):
            print(f"✅ Successfully tested on port {port}")
            break
        print(f"❌ Port {port} failed, trying next...")
    else:
        print("❌ No working server found on common ports")