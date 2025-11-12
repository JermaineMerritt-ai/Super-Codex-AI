#!/usr/bin/env python3
"""
Simple startup script for AXIOM Integrated Backend
"""
import subprocess
import sys
import os
from pathlib import Path

def start_server():
    """Start the integrated server"""
    print("🚀 Starting AXIOM Integrated Backend Server...")
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Start uvicorn directly
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "axiom_integrated_backend:app",
        "--host", "127.0.0.1",
        "--port", "8006",
        "--reload"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    start_server()