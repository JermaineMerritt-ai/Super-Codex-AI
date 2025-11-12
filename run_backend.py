#!/usr/bin/env python3
"""
Simple server runner for the integrated backend
"""
import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Run the integrated backend server"""
    try:
        from integrated_backend import app
        print("🚀 Starting Super-Codex-AI Integrated Backend...")
        uvicorn.run(
            app,
            host="127.0.0.1", 
            port=8012,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()