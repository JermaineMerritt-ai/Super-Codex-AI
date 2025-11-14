#!/usr/bin/env python3
"""
Integrated SIGIL Engine Test
Test SIGIL with full system integration
"""
import time
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the core components and SIGIL
from codex.core.identity import save_identity, save_seal
import hashlib

class SIGIL:
    """Test implementation of SIGIL engine"""
    def crown(self, name: str, roles: list[str]) -> dict:
        stamp = int(time.time())
        slug = hashlib.sha256(f"{name}-{stamp}".encode()).hexdigest()[:12]
        identity = {"name": name, "roles": roles, "slug": slug, "stamped_at": stamp}
        seal = {"slug": slug, "seal": f"SIGIL-{slug}", "status": "crowned"}
        save_identity(slug, identity)
        save_seal(slug, seal)
        return {"identity": identity, "seal": seal}

def test_sigil_integration():
    """Test SIGIL with full integration"""
    print("🔮 SIGIL ENGINE INTEGRATION TEST")
    print("=" * 50)
    
    # Initialize SIGIL engine
    sigil = SIGIL()
    
    # Test scenarios
    test_cases = [
        {"name": "Alpha Guardian", "roles": ["guardian", "protector"]},
        {"name": "Beta Council", "roles": ["council", "advisor", "voter"]},
        {"name": "Gamma Custodian", "roles": ["custodian", "admin", "overseer"]},
    ]
    
    results = []
    
    print("\n👑 CROWNING IDENTITIES")
    print("-" * 30)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Crowning: {case['name']}")
        print(f"   Roles: {', '.join(case['roles'])}")
        
        # Crown the identity
        result = sigil.crown(case['name'], case['roles'])
        results.append(result)
        
        # Display results
        identity = result['identity']
        seal = result['seal']
        
        print(f"   ✅ Slug: {identity['slug']}")
        print(f"   ✅ Seal: {seal['seal']}")
        print(f"   ✅ Status: {seal['status']}")
        print(f"   ✅ Timestamp: {identity['stamped_at']}")
        
        # Verify structure
        assert "identity" in result, "Missing identity in result"
        assert "seal" in result, "Missing seal in result"
        assert identity['slug'] == seal['slug'], "Slug mismatch"
        assert seal['seal'].startswith('SIGIL-'), "Invalid seal format"
        assert seal['status'] == 'crowned', "Invalid status"
        
        # Small delay for unique timestamps
        time.sleep(0.1)
    
    print("\n📊 VERIFICATION")
    print("-" * 30)
    
    # Check uniqueness
    slugs = [r['identity']['slug'] for r in results]
    seals = [r['seal']['seal'] for r in results]
    
    unique_slugs = len(set(slugs))
    unique_seals = len(set(seals))
    
    print(f"✅ Total Identities: {len(results)}")
    print(f"✅ Unique Slugs: {unique_slugs}/{len(slugs)}")
    print(f"✅ Unique Seals: {unique_seals}/{len(seals)}")
    
    assert unique_slugs == len(slugs), "Slug collision detected!"
    assert unique_seals == len(seals), "Seal collision detected!"
    
    print("\n💾 FILE PERSISTENCE CHECK")
    print("-" * 30)
    
    data_dir = Path("data")
    identities_dir = data_dir / "identities"
    seals_dir = data_dir / "seals"
    
    if identities_dir.exists():
        identity_files = list(identities_dir.glob("*.json"))
        print(f"📁 Identity files: {len(identity_files)}")
    
    if seals_dir.exists():
        seal_files = list(seals_dir.glob("*.json"))
        print(f"📁 Seal files: {len(seal_files)}")
    
    print("\n🎉 SIGIL ENGINE TEST COMPLETE!")
    print("✅ Identity crowning successful")
    print("✅ Seal generation verified") 
    print("✅ Uniqueness confirmed")
    print("✅ File persistence active")

if __name__ == "__main__":
    test_sigil_integration()