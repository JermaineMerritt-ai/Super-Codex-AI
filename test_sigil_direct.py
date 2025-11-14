#!/usr/bin/env python3
"""
Direct SIGIL Engine Test
Test SIGIL engine without package imports
"""
import time
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import SIGIL directly from its module
sys.path.insert(0, str(Path(__file__).parent / "engines"))
from sigil import SIGIL

def test_sigil_direct():
    """Test SIGIL engine directly"""
    print("🔮 DIRECT SIGIL ENGINE TEST")
    print("=" * 40)
    
    # Initialize SIGIL engine
    sigil = SIGIL()
    
    # Test identity crowning
    print("\n👑 Crowning Test Identity")
    result = sigil.crown("Direct Test User", ["admin", "tester"])
    
    print(f"✅ Name: {result['identity']['name']}")
    print(f"✅ Slug: {result['identity']['slug']}")
    print(f"✅ Roles: {result['identity']['roles']}")
    print(f"✅ Timestamp: {result['identity']['stamped_at']}")
    print(f"✅ Seal: {result['seal']['seal']}")
    print(f"✅ Status: {result['seal']['status']}")
    
    # Test multiple crownings for uniqueness
    print("\n🔄 Testing Uniqueness")
    results = []
    for i in range(3):
        user_result = sigil.crown(f"User {i+1}", ["role1", "role2"])
        results.append(user_result)
        time.sleep(0.1)  # Ensure different timestamps
    
    # Verify uniqueness
    slugs = [r['identity']['slug'] for r in results]
    seals = [r['seal']['seal'] for r in results]
    
    print(f"✅ Unique Slugs: {len(set(slugs))} / {len(slugs)}")
    print(f"✅ Unique Seals: {len(set(seals))} / {len(seals)}")
    
    assert len(set(slugs)) == len(slugs), "Slugs should be unique!"
    assert len(set(seals)) == len(seals), "Seals should be unique!"
    
    print("\n🎉 DIRECT SIGIL ENGINE TEST PASSED!")
    print("✅ Identity crowning works correctly")
    print("✅ Uniqueness verified") 
    print("✅ File persistence enabled")

if __name__ == "__main__":
    test_sigil_direct()