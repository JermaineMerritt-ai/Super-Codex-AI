#!/usr/bin/env python3
"""
Quick Server Status Check for Super-Codex-AI
"""
import requests
import time

def check_port(port):
    """Check if server is running on given port"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"✅ PORT {port}: {data.get('status', 'unknown')} - {data.get('message', '')}"
        else:
            return f"⚠️ PORT {port}: HTTP {response.status_code}"
    except Exception as e:
        return f"❌ PORT {port}: {str(e)}"

def main():
    print("🔍 SUPER-CODEX-AI SERVER STATUS CHECK")
    print("=" * 50)
    
    # Check common ports
    ports = [8080, 8081, 8082, 8083]
    
    for port in ports:
        status = check_port(port)
        print(status)
    
    print("\n🌐 AVAILABLE INTERFACES:")
    for port in [8080, 8082]:  # Known working ports
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                print(f"   🔗 http://localhost:{port}/ - Main Interface")
                print(f"   📊 http://localhost:{port}/health - Health Check") 
                print(f"   📚 http://localhost:{port}/docs - API Documentation")
                print(f"   🔥 http://localhost:{port}/ceremonial - Ceremonial Interface")
                print(f"   📈 http://localhost:{port}/status - System Status")
                print()
                break
        except:
            continue
    
    print("🎯 RECOMMENDED ACTION:")
    print("   Try accessing: http://localhost:8080")
    print("   If that fails, try: http://localhost:8082")

if __name__ == "__main__":
    main()