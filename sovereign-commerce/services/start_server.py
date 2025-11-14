#!/usr/bin/env python3
"""
Startup script for Sovereign Commerce Platform
"""
import subprocess
import sys
from pathlib import Path

def main():
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent
    print(f"📂 Starting server from: {script_dir}")
    
    # Change to the services directory
    import os
    os.chdir(script_dir)
    
    # Start uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "sovereign_main:app",
        "--host", "127.0.0.1",
        "--port", "8080",
        "--reload"
    ]
    
    print("🚀 Starting Sovereign Commerce Platform...")
    print("🌐 Server will be available at: http://127.0.0.1:8080")
    print("📚 API docs available at: http://127.0.0.1:8080/sacred/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()