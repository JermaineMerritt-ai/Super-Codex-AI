#!/usr/bin/env python3
"""
Simple production-like server startup test.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Super-Codex-AI server...")
    print("Server will be available at: http://127.0.0.1:8080")
    print("Press Ctrl+C to shut down")
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8080,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer shut down gracefully")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()