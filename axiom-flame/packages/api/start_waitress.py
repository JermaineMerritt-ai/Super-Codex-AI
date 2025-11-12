#!/usr/bin/env python3
"""
Waitress startup script for Axiom-Flame API
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from waitress import serve
    import app
    
    print(f"[WAITRESS] Starting Axiom-Flame API on 127.0.0.1:8087...")
    print(f"[INFO] Using waitress WSGI server")
    print(f"[CONFIG] Current directory: {current_dir}")
    
    serve(app.app, host='127.0.0.1', port=8087)
    
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Server failed to start: {e}")
    sys.exit(1)