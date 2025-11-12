#!/usr/bin/env python3
"""
Rollup script for codex-flame API operations.

This script performs maintenance operations like generating annals,
cleaning up temporary files, and summarizing ledger activity.
"""

from pathlib import Path
import sys
import os

# Add the scripts directory to the path so we can import generate_annals
BASE = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = BASE / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

def main():
    """Run rollup operations."""
    print("=== CODEX-FLAME API Rollup Operations ===")
    
    # Import and run annals generation
    try:
        from generate_annals import run as generate_annals
        print("📊 Generating monthly annals from ledger entries...")
        generate_annals()
        print("✅ Annals generation complete")
    except Exception as e:
        print(f"❌ Annals generation failed: {e}")
    
    # Additional rollup operations can be added here
    print("\n🎯 Rollup operations complete!")

if __name__ == "__main__":
    main()