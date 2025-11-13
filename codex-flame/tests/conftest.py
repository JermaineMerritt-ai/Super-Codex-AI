#!/usr/bin/env python3
"""
Test Configuration and Fixtures for Codex-Flame Package
======================================================

Shared pytest fixtures and configuration for testing the ceremonial modules.
Provides common setup for treasury, radiant concord, and flamekeepers testing.
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


@pytest.fixture
def temp_storage():
    """Provide temporary storage directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def treasury_system(temp_storage):
    """Provide a configured treasury binding system"""
    from treasury import TreasuryBinding
    return TreasuryBinding(storage_root=temp_storage)


@pytest.fixture
def concord_system(temp_storage):
    """Provide a configured radiant concord system"""
    from radiant_concord import RadiantConcordSystem
    return RadiantConcordSystem(storage_root=temp_storage)


@pytest.fixture
def flamekeepers_system(temp_storage):
    """Provide a configured flamekeepers scroll system"""
    from flamekeepers_scroll import FlameKeepersScroll
    return FlameKeepersScroll(storage_root=temp_storage)


@pytest.fixture
def sample_treasury_entry(treasury_system):
    """Provide a sample treasury entry for testing"""
    from treasury import ResourceType
    return treasury_system.allocate_resources(
        resource_type=ResourceType.FLAME_ESSENCE,
        amount=1000.0,
        actor="Test_Custodian",
        realm="TEST-001",
        purpose="fixture_test_allocation"
    )


@pytest.fixture
def sample_radiant_concord(concord_system):
    """Provide a sample radiant concord for testing"""
    from radiant_concord import ConcordType, RadianceLevel
    return concord_system.initiate_radiant_concord(
        concord_type=ConcordType.HARMONY_BINDING,
        participants=["Test_Entity_Alpha", "Test_Entity_Beta"],
        radiance_level=RadianceLevel.FLAME,
        ceremonial_purpose="fixture_test_concord"
    )


@pytest.fixture
def sample_flame_keeper(flamekeepers_system):
    """Provide a sample flame keeper for testing"""
    from flamekeepers_scroll import FlameKeeperRank
    return flamekeepers_system.ordain_flame_keeper(
        keeper_name="Test_Guardian",
        rank=FlameKeeperRank.GUARDIAN_KEEPER,
        specializations=["eternal_flame_tending", "ceremonial_lighting"],
        mentor="Test_Elder"
    )


@pytest.fixture
def sample_flame_monitoring(flamekeepers_system):
    """Provide a sample flame monitoring assignment for testing"""
    from flamekeepers_scroll import FlameType, FlameStatus
    return flamekeepers_system.create_monitoring_report(
        flame_name="Test_Sacred_Flame",
        monitoring_keeper="Test_Guardian",
        flame_type=FlameType.CEREMONIAL_FLAME,
        flame_status=FlameStatus.BURNING_BRIGHT,
        observations="fixture_test_monitoring"
    )


# Test data constants
TEST_REALMS = ["TEST-001", "TEST-002", "TEST-003"]
TEST_ACTORS = ["Test_Custodian", "Test_Guardian", "Test_Elder"]
TEST_PURPOSES = ["test_allocation", "test_ceremony", "test_monitoring"]


@pytest.fixture(params=TEST_REALMS)
def test_realm(request):
    """Parameterized fixture for test realms"""
    return request.param


@pytest.fixture(params=TEST_ACTORS)
def test_actor(request):
    """Parameterized fixture for test actors"""
    return request.param


@pytest.fixture(params=TEST_PURPOSES)
def test_purpose(request):
    """Parameterized fixture for test purposes"""
    return request.param


# Cleanup and validation helpers
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Auto-cleanup any test files created during testing"""
    yield
    # Post-test cleanup
    test_patterns = ["TEST-*", "*test*", "FKP-TEST-*", "RC-TEST-*", "TRE-TEST-*"]
    current_dir = Path.cwd()
    
    for pattern in test_patterns:
        for test_file in current_dir.rglob(pattern):
            if test_file.is_file() and "test" in test_file.name.lower():
                try:
                    test_file.unlink()
                except (OSError, PermissionError):
                    pass  # Ignore cleanup errors


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "treasury: marks tests as treasury module tests"
    )
    config.addinivalue_line(
        "markers", "concord: marks tests as radiant concord module tests"
    )
    config.addinivalue_line(
        "markers", "flamekeepers: marks tests as flamekeepers module tests"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )


# Custom assertions for ceremonial data
def assert_valid_ceremonial_id(ceremonial_id, prefix):
    """Assert that a ceremonial ID has the correct format"""
    assert ceremonial_id.startswith(prefix), f"ID should start with {prefix}"
    assert len(ceremonial_id) > len(prefix) + 1, "ID should have content after prefix"
    assert "-" in ceremonial_id, "ID should contain separators"


def assert_valid_timestamp(timestamp_str):
    """Assert that a timestamp string is in ISO format"""
    from datetime import datetime
    try:
        datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except ValueError:
        pytest.fail(f"Invalid timestamp format: {timestamp_str}")


def assert_valid_sacred_seal(seal, expected_prefix="🌟⚡", expected_suffix="🔥✨"):
    """Assert that a sacred seal has the correct ceremonial format"""
    assert seal.startswith(expected_prefix), f"Seal should start with {expected_prefix}"
    assert seal.endswith(expected_suffix), f"Seal should end with {expected_suffix}"


# Export assertion helpers for use in test modules
__all__ = [
    'assert_valid_ceremonial_id',
    'assert_valid_timestamp', 
    'assert_valid_sacred_seal'
]