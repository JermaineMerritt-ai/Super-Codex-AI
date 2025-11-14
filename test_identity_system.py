#!/usr/bin/env python3
"""Test script for the streamlined identity and seal functions"""

from codex.core import save_identity, save_seal, settings
from pathlib import Path
import orjson

def main():
    print("🔐 Testing Identity & Seal Management")
    print("=" * 45)
    print(f"📂 Identities directory: {settings.IDENTITIES_DIR}")
    print(f"🔒 Seals directory: {settings.SEALS_DIR}")
    print("-" * 45)
    
    # Test 1: Save identity data
    print("1. Creating identity records...")
    
    # Custodian identity
    custodian_data = {
        "name": "Codex Custodian Alpha",
        "type": "custodian",
        "realm_access": ["PL-001", "ST-007", "MO-003"],
        "authority_level": 5,
        "capsule_permissions": ["Sovereign Crown", "Temporal Mirror", "Data Nexus"],
        "contact": "custodian.alpha@codex.ai",
        "created": "2025-11-12T16:00:00Z",
        "active": True
    }
    
    custodian_path = save_identity("custodian-alpha", custodian_data)
    print(f"   ✅ Custodian saved: {Path(custodian_path).name}")
    
    # Council member identity
    council_data = {
        "name": "Council Member Beta",
        "type": "council",
        "realm_access": ["PL-001", "PL-002"],
        "authority_level": 3,
        "capsule_permissions": ["Strategic Analysis"],
        "contact": "council.beta@codex.ai",
        "created": "2025-11-12T16:05:00Z", 
        "active": True
    }
    
    council_path = save_identity("council-beta", council_data)
    print(f"   ✅ Council member saved: {Path(council_path).name}")
    
    # Oracle identity
    oracle_data = {
        "name": "Oracle Gamma",
        "type": "oracle",
        "realm_access": ["MO-003", "AQ-012"],
        "authority_level": 7,
        "capsule_permissions": ["Wisdom Engine", "Prophecy Matrix"],
        "contact": "oracle.gamma@codex.ai",
        "created": "2025-11-12T16:10:00Z",
        "active": True
    }
    
    oracle_path = save_identity("oracle-gamma", oracle_data)
    print(f"   ✅ Oracle saved: {Path(oracle_path).name}")
    
    # Test 2: Save seal data
    print("\n2. Creating governance seals...")
    
    # High Authority Seal for Custodian
    custodian_seal = {
        "holder": "custodian-alpha",
        "seal_type": "High Authority",
        "classification": "Sovereign",
        "authority_grants": [
            "realm_administration",
            "capsule_deployment",
            "emergency_protocols",
            "system_governance"
        ],
        "valid_realms": ["PL-001", "ST-007", "MO-003"],
        "issued": "2025-11-12T16:15:00Z",
        "expires": "2026-11-12T16:15:00Z",
        "active": True
    }
    
    custodian_seal_path = save_seal("custodian-alpha", custodian_seal)
    print(f"   ✅ Custodian seal: {Path(custodian_seal_path).name}")
    
    # Council Seal
    council_seal = {
        "holder": "council-beta",
        "seal_type": "Council Authority", 
        "classification": "Strategic",
        "authority_grants": [
            "strategic_oversight",
            "policy_creation",
            "resource_allocation"
        ],
        "valid_realms": ["PL-001", "PL-002"],
        "issued": "2025-11-12T16:20:00Z",
        "expires": "2025-12-12T16:20:00Z",
        "active": True
    }
    
    council_seal_path = save_seal("council-beta", council_seal)
    print(f"   ✅ Council seal: {Path(council_seal_path).name}")
    
    # Oracle Seal
    oracle_seal = {
        "holder": "oracle-gamma",
        "seal_type": "Oracle Authority",
        "classification": "Mystical",
        "authority_grants": [
            "prophetic_analysis",
            "wisdom_dispensation", 
            "temporal_guidance",
            "mystical_operations"
        ],
        "valid_realms": ["MO-003", "AQ-012"],
        "issued": "2025-11-12T16:25:00Z",
        "expires": "2027-11-12T16:25:00Z",
        "active": True
    }
    
    oracle_seal_path = save_seal("oracle-gamma", oracle_seal)
    print(f"   ✅ Oracle seal: {Path(oracle_seal_path).name}")
    
    # Test 3: Verify file contents
    print("\n3. Verifying stored data...")
    
    # Check identity file
    with open(custodian_path, "rb") as f:
        stored_identity = orjson.loads(f.read())
        print(f"   📄 Identity type: {stored_identity['type']}")
        print(f"   📄 Authority level: {stored_identity['authority_level']}")
        print(f"   📄 Realm access: {len(stored_identity['realm_access'])} realms")
    
    # Check seal file  
    with open(custodian_seal_path, "rb") as f:
        stored_seal = orjson.loads(f.read())
        print(f"   🔒 Seal type: {stored_seal['seal_type']}")
        print(f"   🔒 Classification: {stored_seal['classification']}")
        print(f"   🔒 Authority grants: {len(stored_seal['authority_grants'])} grants")
    
    # Test 4: Directory listing
    print("\n4. Directory summary:")
    
    identities_dir = Path(settings.IDENTITIES_DIR)
    if identities_dir.exists():
        identity_files = list(identities_dir.glob("*.json"))
        print(f"   📁 Identity files: {len(identity_files)}")
        for file in identity_files:
            print(f"     - {file.name}")
    
    seals_dir = Path(settings.SEALS_DIR)
    if seals_dir.exists():
        seal_files = list(seals_dir.glob("*-seal.json"))
        print(f"   🔐 Seal files: {len(seal_files)}")
        for file in seal_files:
            print(f"     - {file.name}")
    
    print("\n✨ Identity & seal test completed!")
    print("💾 All data stored using high-performance orjson")
    print("🚀 Ready for production identity management")

if __name__ == "__main__":
    main()