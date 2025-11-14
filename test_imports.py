#!/usr/bin/env python3
"""
CODEX-FLAME Import Test and Demo
Demonstrates importing and using the core ceremonial modules

Usage:
    python test_imports.py
"""

import sys
import os

# Add codex-flame to path for imports
codex_flame_path = os.path.join(os.path.dirname(__file__), 'codex-flame')
sys.path.insert(0, codex_flame_path)

# Import the ceremonial modules
from treasury import create_treasury_binding, ResourceType, TreasuryOperation
from radiant_concord import RadiantConcordSystem, ConcordType, RadianceLevel
from flamekeepers_scroll import FlameKeepersScroll, DutyType, FlameKeeperRank

def main():
    """Test the codex-flame imports and basic functionality"""
    print("🔥🔥🔥 CODEX-FLAME IMPORT TEST 🔥🔥🔥")
    print("=" * 50)
    
    # Test Treasury
    print("\n💰 Testing Treasury Module:")
    treasury = create_treasury_binding()
    treasury_entry = treasury.allocate_resources(
        resource_type=ResourceType.SACRED_BONDS,
        amount=500.0,
        actor="Test_Custodian",
        realm="TEST-001",
        purpose="Module testing"
    )
    print(f"✅ Treasury allocation created: {treasury_entry.entry_id}")
    
    # Test Radiant Concord
    print("\n🌟 Testing Radiant Concord Module:")
    concord_system = RadiantConcordSystem()
    concord = concord_system.initiate_radiant_concord(
        ConcordType.HARMONY_BINDING,
        RadianceLevel.FLAME,
        ["Test Keeper", "Test Guardian"],
        ["Sacred Flame", "Unity Crystal"],
        "Test Sacred Harmony"
    )
    print(f"✅ Radiant concord initiated: {concord.concord_id}")
    
    # Test Flamekeepers
    print("\n🔥 Testing Flamekeepers Module:")
    flamekeepers = FlameKeepersScroll()
    keeper = flamekeepers.ordain_flame_keeper(
        keeper_name="Test Guardian",
        rank=FlameKeeperRank.GUARDIAN_KEEPER,
        specializations=["eternal_flame_tending", "ceremonial_lighting"]
    )
    print(f"✅ Flame keeper ordained: {keeper.keeper_id}")
    
    print("\n" + "=" * 50)
    print("🌟 All imports and tests successful! 🌟")
    print("🔥 The Sacred Flame modules are operational! 🔥")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit_code = 1
    
    sys.exit(exit_code)