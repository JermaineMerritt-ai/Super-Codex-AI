"""
Server Reload Script - Including WooCommerce Integration
========================================================

Restart the server with all ceremonial components including
the new WooCommerce integration.
"""

import subprocess
import time
import sys
import os

def restart_server_with_woocommerce():
    """Restart the server with WooCommerce integration."""
    print("🔥 Restarting Super-Codex-AI Server with WooCommerce Integration")
    print("=" * 60)
    
    # Kill existing processes on port 8080
    try:
        print("🛑 Stopping existing server processes...")
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True, check=False)
        time.sleep(3)
        print("✅ Processes terminated")
    except Exception as e:
        print(f"⚠️ Process cleanup: {e}")
    
    # Start server with WooCommerce integration
    try:
        print("🚀 Starting server with ceremonial commerce...")
        
        # Use the virtual environment Python
        python_path = r".\.venv\Scripts\python.exe"
        if os.path.exists(python_path):
            print(f"🐍 Using virtual environment: {python_path}")
        else:
            python_path = "python"
            print("🐍 Using system Python")
        
        # Start the server
        server_command = [
            python_path, "-m", "uvicorn", 
            "simple_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8080",
            "--reload"
        ]
        
        print(f"🎭 Starting command: {' '.join(server_command)}")
        print("🔥 Server starting with:")
        print("   📊 Health monitoring")
        print("   🎭 Ceremonial interfaces")
        print("   🛒 WooCommerce integration")
        print("   📜 Covenant management")
        print("   👑 Sovereignty verification")
        print("")
        print("🌐 Available endpoints:")
        print("   http://localhost:8080/health")
        print("   http://localhost:8080/dominion")
        print("   http://localhost:8080/woocommerce/")
        print("   http://localhost:8080/docs")
        print("")
        print("🔥 The flame burns sovereign with ceremonial commerce!")
        print("=" * 60)
        
        # Start the process
        subprocess.run(server_command)
        
    except KeyboardInterrupt:
        print("\n🛑 Server shutdown requested")
    except Exception as e:
        print(f"❌ Server start error: {e}")

if __name__ == "__main__":
    restart_server_with_woocommerce()