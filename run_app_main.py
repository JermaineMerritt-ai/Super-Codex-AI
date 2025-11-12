#!/usr/bin/env python3
"""
FastAPI Application Runner for app.main:app
Runs on host 0.0.0.0 port 8010 as requested
"""
import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Run the FastAPI application"""
    try:
        # Ensure we're in the right directory
        os.chdir(Path(__file__).parent)
        
        print("🚀 Starting FastAPI Application (app.main:app)")
        print("📍 Host: 0.0.0.0")  
        print("🔌 Port: 8010")
        print("=" * 50)
        
        # Import the app
        from app.main import app
        
        # Run the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8010,
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