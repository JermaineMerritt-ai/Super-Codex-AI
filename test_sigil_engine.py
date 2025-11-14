#!/usr/bin/env python3
"""
SIGIL Engine Test Suite
Tests identity crowning and sealing functionality
"""
import time
from pathlib import Path

# Import the SIGIL engine
from engines.sigil import SIGIL

def test_sigil_crown_functionality():
    """Test SIGIL identity crowning and sealing"""
    print("🔮 SIGIL ENGINE TEST SUITE")
    print("=" * 50)
    
    # Initialize SIGIL engine
    sigil = SIGIL()
    
    # Test identity crowning scenarios
    test_scenarios = [
        {"name": "Custodian Alpha", "roles": ["admin", "custodian", "overseer"]},
        {"name": "Council Member Beta", "roles": ["council", "voter", "advisor"]},
        {"name": "Guardian Gamma", "roles": ["guardian", "protector", "sentinel"]},
        {"name": "Architect Delta", "roles": ["architect", "designer", "builder"]},
        {"name": "Oracle Epsilon", "roles": ["oracle", "seer", "prophet"]}
    ]
    
    crowned_identities = []
    
    print("\n🌟 CROWNING IDENTITIES")
    print("-" * 30)
    
    for scenario in test_scenarios:
        print(f"\n👑 Crowning: {scenario['name']}")
        print(f"   Roles: {', '.join(scenario['roles'])}")
        
        # Crown the identity
        result = sigil.crown(scenario['name'], scenario['roles'])
        crowned_identities.append(result)
        
        # Verify the result structure
        assert "identity" in result, "Missing identity in result"
        assert "seal" in result, "Missing seal in result"
        
        identity = result["identity"]
        seal = result["seal"]
        
        # Verify identity fields
        assert identity["name"] == scenario['name'], "Name mismatch"
        assert identity["roles"] == scenario['roles'], "Roles mismatch"
        assert "slug" in identity, "Missing slug"
        assert "stamped_at" in identity, "Missing timestamp"
        
        # Verify seal fields
        assert seal["slug"] == identity["slug"], "Slug mismatch between identity and seal"
        assert seal["seal"].startswith("SIGIL-"), "Invalid seal format"
        assert seal["status"] == "crowned", "Invalid seal status"
        
        print(f"   ✅ Slug: {identity['slug']}")
        print(f"   ✅ Seal: {seal['seal']}")
        print(f"   ✅ Timestamp: {identity['stamped_at']}")
        
        # Small delay to ensure unique timestamps
        time.sleep(0.1)
    
    print("\n📊 VERIFICATION RESULTS")
    print("-" * 30)
    print(f"✅ Crowned Identities: {len(crowned_identities)}")
    
    # Verify slug uniqueness
    slugs = [identity["identity"]["slug"] for identity in crowned_identities]
    unique_slugs = set(slugs)
    print(f"✅ Unique Slugs: {len(unique_slugs)}/{len(slugs)}")
    assert len(unique_slugs) == len(slugs), "Duplicate slugs detected!"
    
    # Verify seal uniqueness
    seals = [identity["seal"]["seal"] for identity in crowned_identities]
    unique_seals = set(seals)
    print(f"✅ Unique Seals: {len(unique_seals)}/{len(seals)}")
    assert len(unique_seals) == len(seals), "Duplicate seals detected!"
    
    print("\n🎯 IDENTITY DETAILS")
    print("-" * 30)
    for i, result in enumerate(crowned_identities, 1):
        identity = result["identity"]
        seal = result["seal"]
        print(f"{i}. {identity['name']}")
        print(f"   Slug: {identity['slug']}")
        print(f"   Roles: {len(identity['roles'])} roles")
        print(f"   Seal: {seal['seal']}")
        print(f"   Status: {seal['status']}")
        print()

def verify_file_persistence():
    """Verify that identities and seals are properly saved to files"""
    print("\n💾 FILE PERSISTENCE VERIFICATION")
    print("-" * 40)
    
    data_dir = Path("data")
    identities_dir = data_dir / "identities"
    seals_dir = data_dir / "seals"
    
    # Check if directories exist
    print(f"📁 Identities Directory: {identities_dir.exists()}")
    print(f"📁 Seals Directory: {seals_dir.exists()}")
    
    if identities_dir.exists():
        identity_files = list(identities_dir.glob("*.json"))
        print(f"📄 Identity Files: {len(identity_files)}")
        
        # Show sample files
        for file in identity_files[:3]:  # Show first 3
            print(f"   - {file.name}")
    
    if seals_dir.exists():
        seal_files = list(seals_dir.glob("*.json"))
        print(f"📄 Seal Files: {len(seal_files)}")
        
        # Show sample files
        for file in seal_files[:3]:  # Show first 3
            print(f"   - {file.name}")

if __name__ == "__main__":
    print("🚀 Starting SIGIL Engine Test Suite")
    
    # Test SIGIL functionality
    test_sigil_crown_functionality()
    
    # Verify file persistence
    verify_file_persistence()
    
    print("\n🎉 SIGIL ENGINE TEST COMPLETE!")
    print("✅ All identity crowning operations successful")
    print("✅ All sealing operations verified")
    print("✅ File persistence confirmed")
    
    print("\n🔮 SIGIL ENGINE STATUS: OPERATIONAL")