#!/usr/bin/env python3
"""
Basic Functionality Tests for Codex-Flame Package
=================================================

Simple tests that verify the basic import and core functionality
of the ceremonial modules without testing complex features.
"""

import pytest
import tempfile
import shutil
import sys
import os
from pathlib import Path

# Add codex-flame to Python path for imports
codex_flame_path = Path(__file__).parent.parent
sys.path.insert(0, str(codex_flame_path))


class TestBasicImports:
    """Test that all modules can be imported successfully"""
    
    def test_treasury_import(self):
        """Test treasury module import"""
        from treasury import create_treasury_binding, ResourceType, TreasuryOperation
        
        # Basic enum verification
        assert hasattr(ResourceType, 'FLAME_ESSENCE')
        assert hasattr(ResourceType, 'CEREMONIAL_TOKENS')
        assert hasattr(ResourceType, 'SACRED_BONDS')
        
        assert hasattr(TreasuryOperation, 'ALLOCATION')
        assert hasattr(TreasuryOperation, 'TRANSFER')
    
    def test_radiant_concord_import(self):
        """Test radiant concord module import"""
        from radiant_concord import RadiantConcordSystem, ConcordType, RadianceLevel
        
        # Basic enum verification
        assert hasattr(ConcordType, 'HARMONY_BINDING')
        assert hasattr(ConcordType, 'SACRED_ALLIANCE')
        
        assert hasattr(RadianceLevel, 'EMBER')
        assert hasattr(RadianceLevel, 'FLAME')
        assert hasattr(RadianceLevel, 'TRANSCENDENT')
    
    def test_flamekeepers_import(self):
        """Test flamekeepers module import"""
        from flamekeepers_scroll import FlameKeepersScroll, FlameKeeperRank, FlameType, DutyType
        
        # Basic enum verification
        assert hasattr(FlameKeeperRank, 'INITIATE_KEEPER')
        assert hasattr(FlameKeeperRank, 'GUARDIAN_KEEPER')
        
        assert hasattr(FlameType, 'ETERNAL_FLAME')
        assert hasattr(FlameType, 'CEREMONIAL_FLAME')
        
        assert hasattr(DutyType, 'FLAME_TENDING')
        assert hasattr(DutyType, 'CEREMONIAL_LIGHTING')


class TestBasicFunctionality:
    """Test basic functionality of each module"""
    
    def setup_method(self):
        """Set up test environment with temporary storage"""
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up temporary storage"""
        shutil.rmtree(self.temp_dir)
    
    def test_treasury_basic_function(self):
        """Test basic treasury functionality"""
        from treasury import create_treasury_binding, ResourceType
        
        treasury = create_treasury_binding(storage_root=self.temp_dir)
        assert treasury is not None
        assert treasury.storage_root == Path(self.temp_dir)
        
        # Test basic allocation
        entry = treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=100.0,
            actor="Test_Actor",
            realm="TEST-001",
            purpose="basic_test"
        )
        
        assert entry is not None
        assert entry.entry_id.startswith("TRE-")
        assert entry.amount == 100.0
        assert entry.actor == "Test_Actor"
    
    def test_concord_basic_function(self):
        """Test basic radiant concord functionality"""
        from radiant_concord import RadiantConcordSystem, ConcordType, RadianceLevel
        
        concord_system = RadiantConcordSystem(storage_root=self.temp_dir)
        assert concord_system is not None
        assert concord_system.storage_root == Path(self.temp_dir)
        
        # Test basic concord initiation
        concord = concord_system.initiate_radiant_concord(
            concord_type=ConcordType.HARMONY_BINDING,
            participants=["Entity_A", "Entity_B"],
            radiance_level=RadianceLevel.FLAME,
            ceremonial_purpose="basic_test"
        )
        
        assert concord is not None
        assert concord.concord_id.startswith("RC-")
        assert len(concord.participants) == 2
        assert concord.radiance_level == RadianceLevel.FLAME
    
    def test_flamekeepers_basic_function(self):
        """Test basic flamekeepers functionality"""
        from flamekeepers_scroll import FlameKeepersScroll, FlameKeeperRank
        
        scroll = FlameKeepersScroll(storage_root=self.temp_dir)
        assert scroll is not None
        assert scroll.storage_root == Path(self.temp_dir)
        
        # Test basic flame keeper ordination
        keeper = scroll.ordain_flame_keeper(
            keeper_name="Test_Guardian",
            rank=FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["basic_tending"],
            mentor="Test_Elder"
        )
        
        assert keeper is not None
        assert keeper.keeper_id.startswith("FKP-")
        assert keeper.keeper_name == "Test_Guardian"
        assert keeper.rank == FlameKeeperRank.GUARDIAN_KEEPER


class TestStorageSetup:
    """Test that storage directories are created properly"""
    
    def test_treasury_storage_setup(self):
        """Test treasury storage directory creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            from treasury import TreasuryBinding
            
            treasury = TreasuryBinding(storage_root=temp_dir)
            
            assert treasury.treasury_path.exists()
            assert treasury.abundance_path.exists()
            assert treasury.binding_path.exists()
    
    def test_concord_storage_setup(self):
        """Test concord storage directory creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            from radiant_concord import RadiantConcordSystem
            
            concord_system = RadiantConcordSystem(storage_root=temp_dir)
            
            assert concord_system.concord_path.exists()
            assert concord_system.harmony_path.exists()
            assert concord_system.ceremony_path.exists()
    
    def test_flamekeepers_storage_setup(self):
        """Test flamekeepers storage directory creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            from flamekeepers_scroll import FlameKeepersScroll
            
            scroll = FlameKeepersScroll(storage_root=temp_dir)
            
            assert scroll.keepers_path.exists()
            assert scroll.monitoring_path.exists()
            assert scroll.duties_path.exists()
            assert scroll.protocols_path.exists()


class TestEnumValues:
    """Test that enum values are correctly defined"""
    
    def test_resource_type_enum(self):
        """Test ResourceType enum values"""
        from treasury import ResourceType
        
        expected_values = {
            'FLAME_ESSENCE': 'flame_essence',
            'CEREMONIAL_TOKENS': 'ceremonial_tokens',
            'DOMINION_CREDITS': 'dominion_credits',
            'HONOR_POINTS': 'honor_points',
            'WISDOM_SHARES': 'wisdom_shares',
            'SACRED_BONDS': 'sacred_bonds'
        }
        
        for attr_name, expected_value in expected_values.items():
            assert hasattr(ResourceType, attr_name)
            assert getattr(ResourceType, attr_name).value == expected_value
    
    def test_concord_type_enum(self):
        """Test ConcordType enum values"""
        from radiant_concord import ConcordType
        
        expected_values = {
            'HARMONY_BINDING': 'harmony_binding',
            'SACRED_ALLIANCE': 'sacred_alliance',
            'TRANSCENDENT_UNION': 'transcendent_union',
            'ELEMENTAL_FUSION': 'elemental_fusion',
            'CEREMONIAL_CONVERGENCE': 'ceremonial_convergence'
        }
        
        for attr_name, expected_value in expected_values.items():
            assert hasattr(ConcordType, attr_name)
            assert getattr(ConcordType, attr_name).value == expected_value
    
    def test_flame_keeper_rank_enum(self):
        """Test FlameKeeperRank enum values"""
        from flamekeepers_scroll import FlameKeeperRank
        
        expected_values = {
            'INITIATE_KEEPER': 'initiate_keeper',
            'APPRENTICE_KEEPER': 'apprentice_keeper',
            'GUARDIAN_KEEPER': 'guardian_keeper',
            'MASTER_KEEPER': 'master_keeper',
            'ELDER_KEEPER': 'elder_keeper',
            'SUPREME_KEEPER': 'supreme_keeper'
        }
        
        for attr_name, expected_value in expected_values.items():
            assert hasattr(FlameKeeperRank, attr_name)
            assert getattr(FlameKeeperRank, attr_name).value == expected_value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])