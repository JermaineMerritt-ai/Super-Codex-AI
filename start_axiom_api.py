#!/usr/bin/env python3
"""
AXIOM-FLAME API Startup Script
"""

import sys
import os
import uvicorn

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the AXIOM-FLAME API server"""
    print("🔥 Starting AXIOM-FLAME API...")
    print("📍 Server will be available at: http://localhost:8080")
    print("📖 API Documentation: http://localhost:8080/docs")
    print("🔧 Health Check: http://localhost:8080/health")
    print("-" * 50)
    
    # Run the server using import string for reload functionality
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8080,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )

if __name__ == "__main__":
    main()