#!/usr/bin/env python3
"""
🔥 Sacred Document Archive Server Starter 🔥
Ceremonial FastAPI Document Management System

This script starts the Sacred Document Archive FastAPI server with proper
ceremonial bindings and treasury integration.
"""

import sys
import os
from pathlib import Path

def main():
    """Start the Sacred Document Archive server"""
    print("🔥" + "="*70 + "🔥")
    print("   SACRED DOCUMENT ARCHIVE SERVER")
    print("   Ceremonial Storage System for the Dominion")
    print("🔥" + "="*70 + "🔥")
    print()
    
    # Check if uvicorn is available
    try:
        import uvicorn
        print("✅ uvicorn server available")
    except ImportError:
        print("❌ uvicorn not found - installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"])
        import uvicorn
        print("✅ uvicorn installed and ready")
    
    # Check archive system
    try:
        from sacred_document_archive import app, archive
        print("✅ Sacred Document Archive system loaded")
        print(f"📁 Storage root: {archive.storage_root}")
    except Exception as e:
        print(f"❌ Failed to load Sacred Document Archive: {e}")
        return 1
    
    print()
    print("🌟 Starting Sacred Document Archive server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📜 API documentation at: http://localhost:8000/docs")
    print("🏥 Health check at: http://localhost:8000/health")
    print()
    print("🔗 Example endpoints:")
    print("  POST /upload/docs - Upload sacred documents")
    print("  GET  /docs/{id}   - Retrieve document information")
    print("  GET  /docs/stats  - Archive statistics")
    print("  GET  /docs/types  - Available document types")
    print()
    print("Press Ctrl+C to stop the sacred flame...")
    print("🕯️" + "="*70 + "🕯️")
    print()
    
    try:
        # Start the server
        uvicorn.run(
            "sacred_document_archive:app",
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload in production
            log_level="info"
        )
    except KeyboardInterrupt:
        print()
        print("🕯️ Sacred flame extinguished gracefully.")
        print("  May the eternal knowledge be preserved.")
        return 0
    except Exception as e:
        print(f"💥 Sacred archive encountered an error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())