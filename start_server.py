#!/usr/bin/env python3
"""
Fixed startup script for AXIOM-FLAME API server.
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Start the AXIOM-FLAME API server with proper configuration."""
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🚀 Starting AXIOM-FLAME API Server")
    print("=" * 50)
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌐 Server URL: http://localhost:8080")
    print(f"📚 API Documentation: http://localhost:8080/docs")
    print(f"🔄 Auto-reload: Enabled")
    print("=" * 50)
    
    try:
        # Use import string to fix reload issue
        uvicorn.run(
            "app.main:app",  # Import string instead of object
            host="0.0.0.0",
            port=8080,
            reload=True,
            reload_dirs=[str(script_dir)],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()