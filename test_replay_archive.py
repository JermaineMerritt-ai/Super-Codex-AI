#!/usr/bin/env python3
"""Test script for the archive functionality from codex.core.replay"""

from codex.core.replay import archive
from codex.core.config import settings
from pathlib import Path
import orjson

def main():
    print("🔄 Testing Archive Functionality")
    print(f"📁 Archive directory: {settings.REPLAY_DIR}")
    print("-" * 50)
    
    # Test 1: Archive user session data
    print("1. Archiving user session data...")
    path1 = archive("user-session", {"user_id": "123", "actions": ["login", "search"]})
    print(f"   ✅ Archived to: {Path(path1).name}")
    
    # Test 2: Archive AI response data
    print("2. Archiving AI response data...")
    path2 = archive("ai-response", {"query": "AI models", "response": "Here are the results..."})
    print(f"   ✅ Archived to: {Path(path2).name}")
    
    # Test 3: Archive vector update data
    print("3. Archiving vector update data...")
    path3 = archive("vector-update", {"index": "main", "documents": 1000})
    print(f"   ✅ Archived to: {Path(path3).name}")
    
    # Verify the archived files
    print("\n📊 Verification:")
    for i, path in enumerate([path1, path2, path3], 1):
        if Path(path).exists():
            with open(path, "rb") as f:
                data = orjson.loads(f.read())
            print(f"   {i}. {Path(path).name} - Contains: {list(data.keys())}")
        else:
            print(f"   {i}. ❌ File not found: {path}")
    
    # Show archive directory contents
    archive_dir = Path(settings.REPLAY_DIR)
    if archive_dir.exists():
        files = list(archive_dir.glob("*.json"))
        print(f"\n📂 Total files in archive directory: {len(files)}")
        print("   Recent files:")
        for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            print(f"   - {file.name}")
    
    print("\n✨ Archive test completed successfully!")

if __name__ == "__main__":
    main()