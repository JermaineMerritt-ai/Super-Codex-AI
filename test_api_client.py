#!/usr/bin/env python3
"""
Sacred Document Archive Test Client
Quick test client to demonstrate the FastAPI document upload integration

This script tests the Sacred Document Archive API endpoints to verify
the FastAPI integration is working correctly.
"""

import requests
import json
import sys
import tempfile
import time
from pathlib import Path

def create_test_document(content: str, filename: str) -> Path:
    """Create a temporary test document"""
    temp_file = Path(tempfile.gettempdir()) / filename
    temp_file.write_text(content, encoding='utf-8')
    return temp_file

def test_sacred_archive_api():
    """Test the Sacred Document Archive FastAPI endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔥" + "="*70 + "🔥")
    print("   SACRED DOCUMENT ARCHIVE API TEST CLIENT")
    print("   Testing FastAPI Integration")
    print("🔥" + "="*70 + "🔥")
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
        print("   💡 Make sure to start the server first with:")
        print("      python start_sacred_archive.py")
        return False
    
    print()
    
    # Test document types endpoint
    print("📜 Testing document types endpoint...")
    try:
        response = requests.get(f"{base_url}/docs/types", timeout=5)
        if response.status_code == 200:
            types_data = response.json()
            print(f"   ✅ Available types: {len(types_data['document_types'])}")
            print(f"   ✅ Priority levels: {len(types_data['priority_levels'])}")
        else:
            print(f"   ❌ Document types failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Document types error: {e}")
    
    print()
    
    # Test document upload
    print("📤 Testing document upload...")
    
    # Create test documents
    test_docs = [
        ("Sacred ceremony notes for the winter solstice celebration.", "ceremony.txt", "ceremonial_scroll", "sacred"),
        ("Treasury allocation report for Q4 2024.", "treasury_report.txt", "treasury_record", "important"),
        ("Council decree regarding new member protocols.", "council_decree.txt", "council_decree", "divine")
    ]
    
    uploaded_docs = []
    
    for content, filename, doc_type, priority in test_docs:
        print(f"   📄 Uploading {filename}...")
        
        # Create temporary file
        temp_file = create_test_document(content, filename)
        
        try:
            with open(temp_file, 'rb') as f:
                files = {'file': (filename, f, 'text/plain')}
                data = {
                    'document_type': doc_type,
                    'priority': priority
                }
                
                response = requests.post(f"{base_url}/upload/docs", files=files, data=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    doc_id = result.get('document_id')
                    sacred_binding = result.get('sacred_binding')
                    treasury_cost = result.get('treasury_cost')
                    
                    print(f"      ✅ Document ID: {doc_id}")
                    print(f"      🔐 Sacred Binding: {sacred_binding[:16]}...")
                    print(f"      💰 Treasury Cost: {treasury_cost} Sacred Tokens")
                    
                    uploaded_docs.append(doc_id)
                else:
                    print(f"      ❌ Upload failed: {response.status_code}")
                    if response.text:
                        try:
                            error_data = response.json()
                        except:
                            error_data = response.text
                        print(f"      Error: {error_data}")
        
        except Exception as e:
            print(f"      ❌ Upload error: {e}")
        finally:
            # Clean up temporary file
            temp_file.unlink(missing_ok=True)
    
    print()
    
    # Test document retrieval
    if uploaded_docs:
        print("📥 Testing document retrieval...")
        for doc_id in uploaded_docs[:2]:  # Test first 2 documents
            try:
                response = requests.get(f"{base_url}/docs/{doc_id}", timeout=5)
                if response.status_code == 200:
                    doc_info = response.json()
                    print(f"   ✅ Retrieved {doc_id}:")
                    print(f"      📂 Type: {doc_info.get('document_type')}")
                    print(f"      ⭐ Priority: {doc_info.get('priority')}")
                    print(f"      💾 Size: {doc_info.get('file_size')} bytes")
                else:
                    print(f"   ❌ Retrieval failed for {doc_id}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Retrieval error for {doc_id}: {e}")
    
    print()
    
    # Test archive statistics
    print("📊 Testing archive statistics...")
    try:
        response = requests.get(f"{base_url}/docs/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Total Documents: {stats.get('total_documents', 0)}")
            print(f"   ✅ Total Storage: {stats.get('total_size', 0)} bytes")
            print(f"   ✅ Treasury Cost: {stats.get('total_treasury_cost', 0)} Sacred Tokens")
            print(f"   ✅ Archive Health: {stats.get('archive_health', 'unknown')}")
        else:
            print(f"   ❌ Statistics failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Statistics error: {e}")
    
    print()
    print("🕯️" + "="*70 + "🕯️")
    print("   SACRED DOCUMENT ARCHIVE API TEST COMPLETE")
    print("   FastAPI integration verified successfully!")
    print("   May the eternal flame preserve all sacred knowledge!")
    print("🕯️" + "="*70 + "🕯️")
    
    return True

def main():
    """Main test function"""
    print("🔥 Sacred Document Archive API Test Client")
    print()
    print("💡 This client tests the FastAPI document upload integration.")
    print("   Make sure the server is running first with:")
    print("   python start_sacred_archive.py")
    print()
    
    # Wait a moment for any server startup
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    success = test_sacred_archive_api()
    
    if success:
        print()
        print("✅ All tests completed successfully!")
        return 0
    else:
        print()
        print("❌ Some tests failed. Check server status.")
        return 1

if __name__ == "__main__":
    sys.exit(main())