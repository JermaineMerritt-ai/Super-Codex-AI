#!/usr/bin/env python3
"""
Simple Working Test for Codex-Flame Modules
==========================================

This test verifies that the ceremonial modules work correctly
without complex package structure issues.
"""

import pytest
import tempfile
import shutil
import sys
import os
from pathlib import Path

# Add codex-flame to Python path for direct imports
codex_flame_path = os.path.abspath("codex-flame")
sys.path.insert(0, codex_flame_path)

# Change to the codex-flame directory to avoid import issues
old_cwd = os.getcwd()
os.chdir("codex-flame")


def test_treasury_import():
    """Test treasury module import and basic functionality"""
    import treasury
    
    # Test enum values
    assert treasury.ResourceType.FLAME_ESSENCE.value == "flame_essence"
    assert treasury.ResourceType.CEREMONIAL_TOKENS.value == "ceremonial_tokens"
    assert treasury.TreasuryOperation.ALLOCATION.value == "allocation"
    
    # Test factory function exists
    assert hasattr(treasury, 'create_treasury_binding')
    
    print("✅ Treasury module test passed")


def test_radiant_concord_import():
    """Test radiant concord module import and basic functionality"""
    import radiant_concord
    
    # Test enum values
    assert radiant_concord.ConcordType.HARMONY_BINDING.value == "harmony_binding"
    assert radiant_concord.ConcordType.SACRED_RESONANCE.value == "sacred_resonance"
    assert radiant_concord.RadianceLevel.EMBER.value == "ember"
    assert radiant_concord.RadianceLevel.FLAME.value == "flame"
    
    print("✅ Radiant concord module test passed")


def test_flamekeepers_import():
    """Test flamekeepers module import and basic functionality"""
    import flamekeepers_scroll
    
    # Test enum values
    assert flamekeepers_scroll.FlameKeeperRank.INITIATE_KEEPER.value == "initiate_keeper"
    assert flamekeepers_scroll.FlameKeeperRank.GUARDIAN_KEEPER.value == "guardian_keeper"
    assert flamekeepers_scroll.FlameType.ETERNAL_FLAME.value == "eternal_flame"
    assert flamekeepers_scroll.DutyType.FLAME_TENDING.value == "flame_tending"
    
    print("✅ Flamekeepers scroll module test passed")


def test_treasury_functionality():
    """Test basic treasury functionality"""
    import treasury
    
    with tempfile.TemporaryDirectory() as temp_dir:
        treasury_binding = treasury.create_treasury_binding(storage_root=temp_dir)
        assert treasury_binding is not None
        assert treasury_binding.storage_root == Path(temp_dir)
        
        # Test allocation
        entry = treasury_binding.allocate_resources(
            resource_type=treasury.ResourceType.FLAME_ESSENCE,
            amount=100.0,
            actor="Test_Actor",
            realm="TEST-001",
            purpose="validation_test"
        )
        
        assert entry is not None
        assert entry.entry_id.startswith("TRE-")
        assert entry.amount == 100.0
        assert entry.actor == "Test_Actor"
        assert entry.realm == "TEST-001"
        
    print("✅ Treasury functionality test passed")


def test_concord_functionality():
    """Test basic radiant concord functionality"""
    import radiant_concord
    
    with tempfile.TemporaryDirectory() as temp_dir:
        concord_system = radiant_concord.RadiantConcordSystem(storage_dir=temp_dir)
        assert concord_system is not None
        
        # Test concord initiation
        concord = concord_system.initiate_radiant_concord(
            concord_type=radiant_concord.ConcordType.HARMONY_BINDING,
            radiance_level=radiant_concord.RadianceLevel.FLAME,
            participants=["Entity_A", "Entity_B"],
            ceremonial_elements=["sacred_flame", "harmony_crystal"],
            sacred_intention="validation_test"
        )
        
        assert concord is not None
        assert concord.concord_id.startswith("RC-")
        assert len(concord.participants) == 2
        assert "Entity_A" in concord.participants
        assert "Entity_B" in concord.participants
        
    print("✅ Radiant concord functionality test passed")


def test_flamekeepers_functionality():
    """Test basic flamekeepers functionality"""
    import flamekeepers_scroll
    
    with tempfile.TemporaryDirectory() as temp_dir:
        scroll = flamekeepers_scroll.FlameKeepersScroll(storage_root=temp_dir)
        assert scroll is not None
        assert scroll.storage_root == Path(temp_dir)
        
        # Test keeper ordination
        keeper = scroll.ordain_flame_keeper(
            keeper_name="Test_Guardian",
            rank=flamekeepers_scroll.FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["ceremonial_tending"],
            mentor="Test_Elder"
        )
        
        assert keeper is not None
        assert keeper.keeper_id.startswith("FKP-")
        assert keeper.keeper_name == "Test_Guardian"
        assert keeper.rank == flamekeepers_scroll.FlameKeeperRank.GUARDIAN_KEEPER
        
    print("✅ Flamekeepers functionality test passed")


if __name__ == "__main__":
    print("Running Codex-Flame Module Tests...")
    print("=" * 50)
    
    try:
        test_treasury_import()
        test_radiant_concord_import()
        test_flamekeepers_import()
        test_treasury_functionality()
        test_concord_functionality()
        test_flamekeepers_functionality()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        print("The codex-flame ceremonial modules are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
    finally:
        # Restore original working directory
        os.chdir(old_cwd)