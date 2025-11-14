#!/usr/bin/env python3
"""
Environment Variable Verification Script
Shows the Six Engines constellation environment variables set by run.ps1
"""

import os

def display_env_vars():
    """Display the Six Engines environment variables"""
    
    env_vars = [
        ("VECTOR_DIR", "./data/vectors"),
        ("VECTOR_NAME", "index.faiss"),
        ("CORPUS_DIR", "./data/corpus"),
        ("AUDIT_LOG_PATH", "./data/audit.log"),
        ("REPLAY_DIR", "./data/replay"),
        ("IDENTITIES_DIR", "./data/identities"),
        ("SEALS_DIR", "./data/seals")
    ]
    
    print("🔥 Six Engines Constellation Environment Variables")
    print("=" * 55)
    
    all_set = True
    for var_name, expected_value in env_vars:
        actual_value = os.environ.get(var_name)
        status = "✅" if actual_value == expected_value else "❌"
        
        if actual_value:
            print(f"{status} {var_name:<18} = {actual_value}")
        else:
            print(f"{status} {var_name:<18} = NOT SET")
            all_set = False
    
    print("=" * 55)
    if all_set:
        print("🎯 All environment variables are properly configured!")
    else:
        print("⚠️  Some environment variables are missing or incorrect")
        print("💡 Run: .\\ops\\scripts\\run.ps1 to set them")

if __name__ == "__main__":
    display_env_vars()