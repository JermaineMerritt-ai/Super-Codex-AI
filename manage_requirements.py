#!/usr/bin/env python3
"""
Alternative to pip-tools for Python 3.14 compatibility
Manages requirements.in -> requirements.txt workflow
"""
import subprocess
import sys
from pathlib import Path

def install_from_requirements_in():
    """Install packages from requirements.in"""
    requirements_in = Path("requirements.in")
    if not requirements_in.exists():
        print("❌ requirements.in not found")
        return False
    
    print("📦 Installing packages from requirements.in...")
    with open(requirements_in) as f:
        lines = f.readlines()
    
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            packages.append(line)
    
    if packages:
        cmd = [sys.executable, "-m", "pip", "install"] + packages
        result = subprocess.run(cmd)
        return result.returncode == 0
    return True

def generate_requirements_txt():
    """Generate requirements.txt from current environment"""
    print("📝 Generating requirements.txt...")
    cmd = [sys.executable, "-m", "pip", "freeze"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        with open("requirements.txt", "w") as f:
            f.write(result.stdout)
        print("✅ requirements.txt generated successfully")
        return True
    else:
        print("❌ Failed to generate requirements.txt")
        return False

def sync_requirements():
    """Synchronize environment with requirements.txt"""
    requirements_txt = Path("requirements.txt")
    if not requirements_txt.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("🔄 Synchronizing environment with requirements.txt...")
    cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    result = subprocess.run(cmd)
    return result.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "compile":
            if install_from_requirements_in():
                generate_requirements_txt()
        elif sys.argv[1] == "sync":
            sync_requirements()
        else:
            print("Usage: python manage_requirements.py [compile|sync]")
    else:
        print("🔧 Super-Codex-AI Requirements Manager")
        print("Available commands:")
        print("  compile - Install from requirements.in and generate requirements.txt")
        print("  sync    - Synchronize environment with requirements.txt")