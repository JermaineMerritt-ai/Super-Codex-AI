#!/usr/bin/env python3
"""
Test Treasury Module - Sacred Resource Management Tests
=====================================================

Comprehensive test suite for the treasury binding system, covering:
- Resource allocation and management
- Treasury binding operations
- Abundance flow creation
- Balance calculations and auditing
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import treasury module components
from treasury import (
    TreasuryBinding, 
    ResourceType, 
    TreasuryOperation, 
    TreasuryEntry, 
    AbundanceFlow,
    create_treasury_binding,
    TwilioTreasuryNotifier
)


class TestTreasuryBinding:
    """Test suite for TreasuryBinding class"""
    
    def setup_method(self):
        """Set up test environment with temporary storage"""
        self.temp_dir = tempfile.mkdtemp()
        self.treasury = TreasuryBinding(storage_root=self.temp_dir)
        
    def teardown_method(self):
        """Clean up temporary storage"""
        shutil.rmtree(self.temp_dir)
    
    def test_treasury_initialization(self):
        """Test treasury binding initialization"""
        assert self.treasury.storage_root == Path(self.temp_dir)
        assert self.treasury.treasury_path.exists()
        assert self.treasury.abundance_path.exists()
        assert self.treasury.binding_path.exists()
    
    def test_resource_allocation(self):
        """Test sacred resource allocation"""
        entry = self.treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=1000.0,
            actor="Test_Custodian",
            realm="TEST-001",
            purpose="test_allocation"
        )
        
        assert isinstance(entry, TreasuryEntry)
        assert entry.resource_type == ResourceType.FLAME_ESSENCE
        assert entry.amount == 1000.0
        assert entry.actor == "Test_Custodian"
        assert entry.realm == "TEST-001"
        assert entry.operation == TreasuryOperation.ALLOCATION
        assert entry.entry_id.startswith("TRE-")
        assert len(entry.binding_hash) == 16
        assert entry.governance_seal.startswith("GS-")
    
    def test_abundance_flow_creation(self):
        """Test abundance flow between entities"""
        flow = self.treasury.create_abundance_flow(
            source_entity="Sacred_Treasury",
            target_entity="Ceremonial_Council",
            resource_type=ResourceType.CEREMONIAL_TOKENS,
            flow_amount=500.0,
            flow_purpose="council_operations",
            ceremonial_authority="Test_Custodian"
        )
        
        assert isinstance(flow, AbundanceFlow)
        assert flow.source_entity == "Sacred_Treasury"
        assert flow.target_entity == "Ceremonial_Council"
        assert flow.resource_type == ResourceType.CEREMONIAL_TOKENS
        assert flow.flow_amount == 500.0
        assert flow.flow_id.startswith("ABF-")
        assert len(flow.binding_signature) == 16
    
    def test_ceremonial_treasury_binding(self):
        """Test creating a ceremonial treasury with initial resources"""
        initial_resources = {
            ResourceType.FLAME_ESSENCE: 1000.0,
            ResourceType.CEREMONIAL_TOKENS: 500.0,
            ResourceType.SACRED_BONDS: 250.0
        }
        
        binding = self.treasury.bind_ceremonial_treasury(
            treasury_name="Test_Sacred_Treasury",
            initial_resources=initial_resources,
            binding_authority="Test_Custodian",
            realm="TEST-001"
        )
        
        assert binding["treasury_name"] == "Test_Sacred_Treasury"
        assert binding["binding_authority"] == "Test_Custodian"
        assert binding["realm"] == "TEST-001"
        assert binding["binding_status"] == "active"
        assert len(binding["initial_allocations"]) == 3
        assert binding["ceremonial_seal"].startswith("CS-")
    
    def test_treasury_balance_calculation(self):
        """Test treasury balance calculations"""
        # Create multiple allocations
        self.treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=1000.0,
            actor="Test_Entity",
            realm="TEST-001"
        )
        
        self.treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=500.0,
            actor="Test_Entity",
            realm="TEST-001"
        )
        
        self.treasury.allocate_resources(
            resource_type=ResourceType.CEREMONIAL_TOKENS,
            amount=250.0,
            actor="Test_Entity",
            realm="TEST-001"
        )
        
        balances = self.treasury.get_treasury_balance("Test_Entity")
        
        assert balances["flame_essence"] == 1500.0
        assert balances["ceremonial_tokens"] == 250.0
        
        # Test filtered balance
        flame_balance = self.treasury.get_treasury_balance(
            "Test_Entity", 
            ResourceType.FLAME_ESSENCE
        )
        assert flame_balance["flame_essence"] == 1500.0
        assert "ceremonial_tokens" not in flame_balance
    
    def test_treasury_audit(self):
        """Test treasury audit operations"""
        # Create test entries
        entry1 = self.treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=1000.0,
            actor="Test_Custodian",
            realm="TEST-001"
        )
        
        entry2 = self.treasury.allocate_resources(
            resource_type=ResourceType.CEREMONIAL_TOKENS,
            amount=500.0,
            actor="Test_Guardian",
            realm="TEST-002"
        )
        
        # Audit all operations
        audit_results = self.treasury.audit_treasury_operations()
        assert len(audit_results) == 2
        
        # Audit by actor
        custodian_audit = self.treasury.audit_treasury_operations(actor="Test_Custodian")
        assert len(custodian_audit) == 1
        assert custodian_audit[0]["actor"] == "Test_Custodian"
    
    def test_binding_hash_generation(self):
        """Test binding hash generation for integrity"""
        test_data = {
            "entry_id": "TEST-123",
            "resource_type": "flame_essence",
            "amount": 1000.0,
            "actor": "Test_Actor"
        }
        
        hash1 = self.treasury._generate_binding_hash(test_data)
        hash2 = self.treasury._generate_binding_hash(test_data)
        
        assert hash1 == hash2  # Same data should produce same hash
        assert len(hash1) == 16
        assert hash1.isupper()  # Should be uppercase
    
    def test_storage_persistence(self):
        """Test that treasury data persists to storage"""
        entry = self.treasury.allocate_resources(
            resource_type=ResourceType.SACRED_BONDS,
            amount=750.0,
            actor="Test_Actor",
            realm="TEST-001"
        )
        
        # Check that file was created
        entry_file = self.treasury.treasury_path / f"{entry.entry_id}.json"
        assert entry_file.exists()
        
        # Verify file content
        with open(entry_file, 'r') as f:
            stored_data = json.load(f)
        
        assert stored_data["entry_id"] == entry.entry_id
        assert stored_data["resource_type"] == "sacred_bonds"
        assert stored_data["amount"] == 750.0
        assert stored_data["actor"] == "Test_Actor"


class TestTwilioTreasuryNotifier:
    """Test suite for Twilio treasury notifications"""
    
    @patch('treasury.Client')
    def test_notifier_initialization_success(self, mock_client):
        """Test successful Twilio client initialization"""
        notifier = TwilioTreasuryNotifier(
            account_sid="test_sid",
            auth_token="test_token",
            from_whatsapp="whatsapp:+1234567890"
        )
        
        assert notifier.client is not None
        assert notifier.from_whatsapp == "whatsapp:+1234567890"
        mock_client.assert_called_once_with("test_sid", "test_token")
    
    @patch('treasury.Client', side_effect=ImportError)
    def test_notifier_initialization_no_twilio(self, mock_client):
        """Test initialization when Twilio is not available"""
        notifier = TwilioTreasuryNotifier(
            account_sid="test_sid",
            auth_token="test_token",
            from_whatsapp="whatsapp:+1234567890"
        )
        
        assert notifier.client is None
    
    @patch('treasury.Client')
    def test_treasury_notification_success(self, mock_client):
        """Test successful treasury operation notification"""
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        mock_messages.create.return_value = MagicMock()
        
        notifier = TwilioTreasuryNotifier(
            account_sid="test_sid",
            auth_token="test_token",
            from_whatsapp="whatsapp:+1234567890"
        )
        
        # Create a test treasury entry
        entry = TreasuryEntry(
            entry_id="TRE-TEST-123",
            timestamp="2025-11-12T12:00:00Z",
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=1000.0,
            operation=TreasuryOperation.ALLOCATION,
            actor="Test_Custodian",
            realm="TEST-001",
            capsule="Test_Capsule",
            governance_seal="GS-12345678",
            binding_hash="ABCD1234EFGH5678",
            metadata={"purpose": "test_notification"}
        )
        
        result = notifier.notify_treasury_operation(
            entry=entry,
            recipient_whatsapp="whatsapp:+0987654321"
        )
        
        assert result is True
        mock_messages.create.assert_called_once()
    
    def test_treasury_notification_no_client(self):
        """Test notification when client is not available"""
        notifier = TwilioTreasuryNotifier(
            account_sid="test_sid",
            auth_token="test_token",
            from_whatsapp="whatsapp:+1234567890"
        )
        notifier.client = None  # Simulate no client
        
        entry = TreasuryEntry(
            entry_id="TRE-TEST-123",
            timestamp="2025-11-12T12:00:00Z",
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=1000.0,
            operation=TreasuryOperation.ALLOCATION,
            actor="Test_Custodian",
            realm="TEST-001",
            capsule="Test_Capsule",
            governance_seal="GS-12345678",
            binding_hash="ABCD1234EFGH5678",
            metadata={"purpose": "test_notification"}
        )
        
        result = notifier.notify_treasury_operation(
            entry=entry,
            recipient_whatsapp="whatsapp:+0987654321"
        )
        
        assert result is False


class TestFactoryFunctions:
    """Test factory functions and utilities"""
    
    def test_create_treasury_binding_factory(self):
        """Test treasury binding factory function"""
        with tempfile.TemporaryDirectory() as temp_dir:
            treasury = create_treasury_binding(storage_root=temp_dir)
            
            assert isinstance(treasury, TreasuryBinding)
            assert treasury.storage_root == Path(temp_dir)
    
    def test_create_treasury_binding_default_storage(self):
        """Test treasury binding with default storage"""
        treasury = create_treasury_binding()
        
        assert isinstance(treasury, TreasuryBinding)
        assert treasury.storage_root == Path(".")


class TestResourceTypes:
    """Test resource type enums and validation"""
    
    def test_resource_type_values(self):
        """Test all resource type enum values"""
        expected_types = [
            "flame_essence",
            "ceremonial_tokens", 
            "dominion_credits",
            "honor_points",
            "wisdom_shares",
            "sacred_bonds"
        ]
        
        actual_types = [rt.value for rt in ResourceType]
        
        for expected in expected_types:
            assert expected in actual_types
    
    def test_treasury_operation_values(self):
        """Test all treasury operation enum values"""
        expected_operations = [
            "allocation",
            "transfer",
            "binding", 
            "release",
            "audit",
            "ceremonial_grant"
        ]
        
        actual_operations = [op.value for op in TreasuryOperation]
        
        for expected in expected_operations:
            assert expected in actual_operations


if __name__ == "__main__":
    pytest.main([__file__])