#!/usr/bin/env python3
"""
Axiom-Flame API Server Startup Script
"""
import os
import sys
import traceback
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def start_server():
    """Start the Axiom-Flame API server"""
    try:
        print("=" * 60)
        print("🔥 AXIOM-FLAME API SERVER STARTUP")
        print("=" * 60)
        
        # Import and setup
        print("📦 Importing modules...")
        from app import app, Config
        from waitress import serve
        
        print(f"✓ Flask app imported successfully")
        print(f"✓ Config loaded: HOST={Config.HOST}, PORT={Config.PORT}")
        
        # Initialize directories
        print("📁 Initializing directories...")
        Config.init_directories()
        print(f"✓ Storage directories created")
        
        # Test app configuration
        print("🔧 Testing app configuration...")
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✓ Health endpoint working")
            else:
                print(f"⚠ Health endpoint returned {response.status_code}")
        
        # Start server
        host = Config.HOST
        port = Config.PORT
        print(f"🚀 Starting Waitress WSGI server on {host}:{port}...")
        print(f"📊 Available routes: {len(app.url_map._rules)} endpoints")
        print(f"🌐 Server URL: http://{host}:{port}")
        print(f"💚 Health check: http://{host}:{port}/health")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Serve the application
        serve(app, host=host, port=port, threads=4)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        print("🔍 Traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_server()