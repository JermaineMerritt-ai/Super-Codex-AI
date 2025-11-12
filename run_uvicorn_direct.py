#!/usr/bin/env python3
"""
Direct execution of: python -m uvicorn app.main:app --host 0.0.0.0 --port 8010
This script bypasses PowerShell interaction issues by running uvicorn directly
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Execute the exact uvicorn command requested"""
    
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🚀 Executing: python -m uvicorn app.main:app --host 0.0.0.0 --port 8010")
    print(f"📂 Working Directory: {script_dir}")
    print("🌐 Server will be available at: http://localhost:8010")
    print("=" * 60)
    
    # Set environment variables
    env = os.environ.copy()
    env['PYTHONPATH'] = str(script_dir)
    env['PYTHONUNBUFFERED'] = '1'
    
    # Kill any existing processes on port 8010
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, check=False)
    except Exception:
        pass
    
    # Build the command exactly as requested
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'app.main:app',
        '--host', '0.0.0.0',
        '--port', '8010'
    ]
    
    try:
        print(f"🎯 Running command: {' '.join(cmd)}")
        print("🔥 Starting server...")
        
        # Execute the command
        result = subprocess.run(cmd, env=env, cwd=script_dir)
        
        print(f"✅ Server exited with code: {result.returncode}")
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"❌ Error running server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())