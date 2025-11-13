"""
Test Ceremonial Modules - Integration Testing Suite
====================================================

This module provides integration tests for all the ceremonial modules
in the codex-flame directory to ensure they function correctly.
"""

import sys
import os
from pathlib import Path

# Add the codex-flame directory to the path for importing modules
codex_flame_path = Path(__file__).parent
sys.path.insert(0, str(codex_flame_path))

def test_treasury_module():
    """Test the treasury.py module"""
    try:
        from treasury import create_treasury_binding, ResourceType, TreasuryOperation
        
        print("🔥 Testing Treasury Module...")
        treasury = create_treasury_binding()
        
        # Test resource allocation
        allocation = treasury.allocate_resources(
            resource_type=ResourceType.FLAME_ESSENCE,
            amount=100.0,
            actor="Test Custodian",
            realm="TEST-001",
            purpose="module_testing"
        )
        
        print(f"✅ Treasury allocation created: {allocation.entry_id}")
        return True
        
    except Exception as e:
        print(f"❌ Treasury module test failed: {e}")
        return False

def test_eternal_recognition_module():
    """Test the ETERNAL_RECOGNITION_SCROLL.py module"""
    try:
        from ETERNAL_RECOGNITION_SCROLL import create_eternal_recognition_system, HonorType, RecognitionLevel
        
        print("🔥 Testing Eternal Recognition Module...")
        eternal_scrolls = create_eternal_recognition_system()
        
        # Test recognition bestowment
        recognition = eternal_scrolls.bestow_eternal_recognition(
            honoree_name="Test Guardian",
            honor_type=HonorType.FLAME_KEEPING,
            recognition_level=RecognitionLevel.KEEPER,
            bestower="Test Elder",
            realm="TEST-001",
            citation="Test citation for module verification",
            ceremonial_witness=["Test Witness 1", "Test Witness 2"]
        )
        
        print(f"✅ Eternal recognition created: {recognition.recognition_id}")
        return True
        
    except Exception as e:
        print(f"❌ Eternal Recognition module test failed: {e}")
        return False

def test_flamekeepers_module():
    """Test the flamekeepers_scroll.py module"""
    try:
        from flamekeepers_scroll import create_flamekeepers_scroll, FlameKeeperRank, FlameType
        
        print("🔥 Testing Flamekeepers Module...")
        flamekeepers = create_flamekeepers_scroll()
        
        # Test keeper ordination
        keeper = flamekeepers.ordain_flame_keeper(
            keeper_name="Test Keeper",
            rank=FlameKeeperRank.GUARDIAN_KEEPER,
            specializations=["test_tending", "test_monitoring"]
        )
        
        print(f"✅ Flame keeper ordained: {keeper.keeper_id}")
        return True
        
    except Exception as e:
        print(f"❌ Flamekeepers module test failed: {e}")
        return False

def test_liturgical_module():
    """Test the liturgical_scheduling.py module"""
    try:
        from liturgical_scheduling import create_liturgical_scheduler, CeremonyType, CeremonyPriority
        from datetime import datetime, timezone
        
        print("🔥 Testing Liturgical Scheduling Module...")
        scheduler = create_liturgical_scheduler()
        
        # Test ceremony scheduling
        ceremony = scheduler.schedule_ceremony(
            ceremony_name="Test Ceremony",
            ceremony_type=CeremonyType.DAILY_FLAME_TENDING,
            scheduled_datetime=datetime.now(timezone.utc).isoformat(),
            duration_minutes=60,
            location="Test Chamber",
            presider="Test Presider",
            participants=[{"name": "Test Participant", "role": "participant"}],
            ceremony_purpose="Testing ceremonial scheduling"
        )
        
        print(f"✅ Ceremony scheduled: {ceremony.ceremony_id}")
        return True
        
    except Exception as e:
        print(f"❌ Liturgical Scheduling module test failed: {e}")
        return False

def test_honors_module():
    """Test the honors.py module"""
    try:
        from honors import create_honors_system, HonorCategory, HonorLevel
        
        print("🔥 Testing Honors Module...")
        honors = create_honors_system()
        
        # Test honor bestowment
        honor = honors.bestow_sacred_honor(
            honor_name="Test Honor",
            honor_category=HonorCategory.CEREMONIAL_EXCELLENCE,
            honor_level=HonorLevel.RECOGNITION,
            recipient_name="Test Recipient",
            bestower="Test Bestower",
            honor_description="Test honor for module verification",
            ceremonial_context="Module testing ceremony",
            witness_signatures=["Test Witness 1", "Test Witness 2"]
        )
        
        print(f"✅ Honor bestowed: {honor.honor_id}")
        return True
        
    except Exception as e:
        print(f"❌ Honors module test failed: {e}")
        return False

def test_triumvirate_module():
    """Test the inscribe_sacred_triumvirate.py module"""
    try:
        from inscribe_sacred_triumvirate import create_sacred_triumvirate, TriumviratePosition, AuthorityDomain
        
        print("🔥 Testing Sacred Triumvirate Module...")
        triumvirate = create_sacred_triumvirate()
        
        # Test triumvirate member inscription
        member = triumvirate.inscribe_triumvirate_member(
            member_name="Test Triumvir",
            position=TriumviratePosition.FLAME_KEEPER_PRIME,
            appointing_authority="Test Authority",
            ceremonial_investiture="Test Investiture",
            authority_domains=[AuthorityDomain.SACRED_FLAMES]
        )
        
        print(f"✅ Triumvirate member inscribed: {member.member_id}")
        return True
        
    except Exception as e:
        print(f"❌ Sacred Triumvirate module test failed: {e}")
        return False

def test_contracts_appeals_module():
    """Test the contracts_appals.py module"""
    try:
        from contracts_appals import create_contracts_appeals_system, ContractType
        from datetime import datetime, timezone
        
        print("🔥 Testing Contracts & Appeals Module...")
        system = create_contracts_appeals_system()
        
        # Test contract creation
        contract = system.create_sacred_contract(
            contract_name="Test Contract",
            contract_type=ContractType.CEREMONIAL_SERVICE,
            parties=[{"name": "Test Party 1", "role": "contractor"}],
            contract_terms=["Test term 1", "Test term 2"],
            obligations={"Test Party 1": ["Test obligation"]},
            ceremonial_conditions=["Test condition"],
            effective_date=datetime.now(timezone.utc).isoformat()
        )
        
        print(f"✅ Contract created: {contract.contract_id}")
        return True
        
    except Exception as e:
        print(f"❌ Contracts & Appeals module test failed: {e}")
        return False

def run_all_tests():
    """Run all ceremonial module tests"""
    print("🔥🔥🔥 CODEX-FLAME CEREMONIAL MODULES INTEGRATION TESTS 🔥🔥🔥")
    print("=" * 70)
    
    tests = [
        test_treasury_module,
        test_eternal_recognition_module,
        test_flamekeepers_module,
        test_liturgical_module,
        test_honors_module,
        test_triumvirate_module,
        test_contracts_appeals_module
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 70)
    print(f"🔥 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌟 ALL CEREMONIAL MODULES FUNCTIONING CORRECTLY! 🌟")
        print("🔥 The Sacred Flame Architecture is operational! 🔥")
    else:
        print("⚠️  Some modules need attention for full functionality")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()