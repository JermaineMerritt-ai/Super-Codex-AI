#!/usr/bin/env python3
"""
Simple SIGIL Engine Test
Direct test without complex dependencies
"""
import time
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import directly from the SIGIL module
from engines.sigil import SIGIL

def test_sigil_basic():
    """Test basic SIGIL functionality"""
    print("🔮 SIGIL ENGINE BASIC TEST")
    print("=" * 40)
    
    # Initialize SIGIL engine
    sigil = SIGIL()
    
    # Test single identity crowning
    print("\n👑 Crowning Identity")
    result = sigil.crown("Test Custodian", ["admin", "custodian"])
    
    print(f"✅ Identity: {result['identity']['name']}")
    print(f"✅ Slug: {result['identity']['slug']}")
    print(f"✅ Roles: {result['identity']['roles']}")
    print(f"✅ Timestamp: {result['identity']['stamped_at']}")
    print(f"✅ Seal: {result['seal']['seal']}")
    print(f"✅ Status: {result['seal']['status']}")
    
    # Verify structure
    assert "identity" in result
    assert "seal" in result
    assert result['identity']['slug'] == result['seal']['slug']
    assert result['seal']['seal'].startswith('SIGIL-')
    assert result['seal']['status'] == 'crowned'
    
    print("\n🎉 SIGIL ENGINE TEST PASSED!")
    return result

if __name__ == "__main__":
    test_sigil_basic()