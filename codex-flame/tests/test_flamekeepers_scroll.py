#!/usr/bin/env python3
"""
Test Flamekeepers Scroll Module - Sacred Flame Custodian Tests
==============================================================

Comprehensive test suite for the flamekeepers scroll system, covering:
- Flame keeper ordination and rank management
- Duty assignments and specializations
- Sacred flame monitoring and protocols
- Flame status tracking and emergency response
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import flamekeepers scroll module components
from flamekeepers_scroll import (
    FlameKeepersScroll,
    FlameKeeperRank,
    FlameType,
    DutyType,
    FlameStatus,
    FlameKeeper,
    FlameMonitoringReport,
    DutyAssignment,
    FlameRecord
)


class TestFlameKeepersScroll:
    """Test suite for FlameKeepersScroll class"""
    
    def setup_method(self):
        """Set up test environment with temporary storage"""
        self.temp_dir = tempfile.mkdtemp()
        self.scroll = FlameKeepersScroll(storage_root=self.temp_dir)
        
    def teardown_method(self):
        """Clean up temporary storage"""
        shutil.rmtree(self.temp_dir)
    
    def test_scroll_initialization(self):
        """Test flamekeepers scroll initialization"""
        assert self.scroll.storage_root == Path(self.temp_dir)
        assert self.scroll.keepers_path.exists()
        assert self.scroll.monitoring_path.exists()
        assert self.scroll.duties_path.exists()
        assert self.scroll.protocols_path.exists()
    
    def test_flame_keeper_ordination(self):
        """Test ordaining a new flame keeper"""
        keeper = self.scroll.ordain_flame_keeper(
            keeper_name="Guardian_Pyrion",
            rank=FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["eternal_flame_tending", "ceremonial_lighting"],
            mentor="Elder_Ignis",
            ceremonial_authorities=["Sacred_Council"]
        )
        
        assert isinstance(keeper, FlameKeeper)
        assert keeper.keeper_name == "Guardian_Pyrion"
        assert keeper.rank == FlameKeeperRank.GUARDIAN_KEEPER
        assert len(keeper.specializations) == 2
        assert "eternal_flame_tending" in keeper.specializations
        assert "ceremonial_lighting" in keeper.specializations
        assert keeper.mentor == "Elder_Ignis"
        assert keeper.keeper_id.startswith("FKP-")
        assert keeper.keeper_seal.startswith("KS-")
    
    def test_flame_monitoring_assignment(self):
        """Test assigning flame monitoring duties"""
        monitoring = self.scroll.create_monitoring_report(
            flame_name="Eternal_Sanctuary_Flame",
            monitoring_keeper="Guardian_Pyrion",
            flame_type=FlameType.CEREMONIAL_FLAME,
            flame_status=FlameStatus.BURNING_BRIGHT,
            observations="All parameters nominal"
        )
        
        assert isinstance(monitoring, FlameMonitoringReport)
        assert monitoring.flame_name == "Eternal_Sanctuary_Flame"
        assert monitoring.monitoring_keeper == "Guardian_Pyrion"
        assert monitoring.flame_type == FlameType.CEREMONIAL_FLAME
        assert monitoring.flame_status == FlameStatus.BURNING_BRIGHT
        assert monitoring.report_id.startswith("FM-")
    
    def test_storage_persistence(self):
        """Test that flame keeper data persists to storage"""
        keeper = self.scroll.ordain_flame_keeper(
            keeper_name="Test_Keeper",
            rank=FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["test_specialty"]
        )
        
        # Check that file was created
        keeper_file = self.scroll.keepers_path / f"{keeper.keeper_id}.json"
        assert keeper_file.exists()
        
        # Verify file content
        with open(keeper_file, 'r') as f:
            stored_data = json.load(f)
        
        assert stored_data["keeper_id"] == keeper.keeper_id
        assert stored_data["keeper_name"] == "Test_Keeper"
        assert stored_data["rank"] == "guardian_keeper"
        assert "test_specialty" in stored_data["specializations"]


class TestFlameKeeperRanks:
    """Test flame keeper rank enums and validation"""
    
    def test_flame_keeper_rank_values(self):
        """Test all flame keeper rank enum values"""
        expected_ranks = [
            "initiate_keeper",
            "apprentice_keeper", 
            "guardian_keeper",
            "master_keeper",
            "elder_keeper",
            "supreme_keeper"
        ]
        
        actual_ranks = [rank.value for rank in FlameKeeperRank]
        
        for expected in expected_ranks:
            assert expected in actual_ranks
    
    def test_flame_type_values(self):
        """Test all flame type enum values"""
        expected_types = [
            "eternal_flame",
            "ceremonial_flame",
            "sacred_brazier",
            "ritual_candle",
            "beacon_fire",
            "meditation_flame"
        ]
        
        actual_types = [flame_type.value for flame_type in FlameType]
        
        for expected in expected_types:
            assert expected in actual_types
    
    def test_duty_type_values(self):
        """Test all duty type enum values"""
        expected_duties = [
            "flame_tending",
            "ceremonial_lighting",
            "sacred_monitoring",
            "ritual_preparation", 
            "knowledge_preservation",
            "apprentice_training",
            "emergency_response"
        ]
        
        actual_duties = [duty.value for duty in DutyType]
        
        for expected in expected_duties:
            assert expected in actual_duties
    
    def test_flame_status_values(self):
        """Test all flame status enum values"""
        expected_statuses = [
            "burning_bright",
            "steady_glow",
            "flickering",
            "dimming",
            "critical",
            "extinguished",
            "rekindled"
        ]
        
        actual_statuses = [status.value for status in FlameStatus]
        
        for expected in expected_statuses:
            assert expected in actual_statuses


class TestDataClassStructures:
    """Test data class structures and validation"""
    
    def test_flame_keeper_creation(self):
        """Test FlameKeeper data class creation"""
        keeper = FlameKeeper(
            keeper_id="FKP-TEST-123",
            timestamp="2025-11-12T12:00:00Z",
            keeper_name="Test_Guardian",
            rank=FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["eternal_flame_tending", "ceremonial_lighting"],
            sacred_oath="I solemnly swear to tend the sacred flames",
            keeper_seal="KS-ABCD1234",
            mentor="Elder_Master",
            ceremonial_authorities=["Sacred_Council"],
            ordination_ceremony="guardian_ascension"
        )
        
        assert keeper.keeper_id == "FKP-TEST-123"
        assert keeper.keeper_name == "Test_Guardian"
        assert keeper.rank == FlameKeeperRank.GUARDIAN_KEEPER
        assert len(keeper.specializations) == 2
        assert keeper.mentor == "Elder_Master"
    
    def test_flame_monitoring_creation(self):
        """Test FlameMonitoring data class creation"""
        monitoring = FlameMonitoring(
            monitoring_id="FM-TEST-456",
            timestamp="2025-11-12T12:00:00Z",
            flame_designation="Test_Sacred_Flame",
            monitoring_keeper="Test_Guardian",
            flame_type=FlameType.ETERNAL_FLAME,
            flame_status=FlameStatus.BURNING_BRIGHT,
            monitoring_frequency="continuous",
            last_status_check="2025-11-12T11:55:00Z",
            ceremonial_significance="sanctuary_blessing",
            monitoring_notes="All parameters nominal"
        )
        
        assert monitoring.monitoring_id == "FM-TEST-456"
        assert monitoring.flame_designation == "Test_Sacred_Flame"
        assert monitoring.flame_type == FlameType.ETERNAL_FLAME
        assert monitoring.flame_status == FlameStatus.BURNING_BRIGHT
    
    def test_duty_assignment_creation(self):
        """Test DutyAssignment data class creation"""
        duty = DutyAssignment(
            assignment_id="DA-TEST-789",
            timestamp="2025-11-12T12:00:00Z",
            assigned_keeper="Test_Guardian",
            duty_type=DutyType.CEREMONIAL_LIGHTING,
            duty_description="Light evening ceremonial flames",
            duty_schedule="daily_evening",
            assignment_status="active",
            ceremonial_importance="high",
            duty_location="Sacred_Sanctuary",
            ceremonial_notes="Requires ritual preparation"
        )
        
        assert duty.assignment_id == "DA-TEST-789"
        assert duty.assigned_keeper == "Test_Guardian"
        assert duty.duty_type == DutyType.CEREMONIAL_LIGHTING
        assert duty.assignment_status == "active"
    
    def test_sacred_protocol_creation(self):
        """Test SacredProtocol data class creation"""
        protocol = SacredProtocol(
            protocol_id="SP-TEST-101",
            timestamp="2025-11-12T12:00:00Z",
            protocol_name="Emergency_Revival",
            protocol_authority="Elder_Council",
            protocol_steps=[
                "Step 1: Assessment",
                "Step 2: Preparation", 
                "Step 3: Execution"
            ],
            protocol_status="established",
            emergency_contacts=["Elder_Contact", "Master_Contact"],
            protocol_classification="emergency_critical",
            ceremonial_requirements="Sacred vestments required"
        )
        
        assert protocol.protocol_id == "SP-TEST-101"
        assert protocol.protocol_name == "Emergency_Revival"
        assert len(protocol.protocol_steps) == 3
        assert len(protocol.emergency_contacts) == 2
        assert protocol.protocol_status == "established"


if __name__ == "__main__":
    pytest.main([__file__])