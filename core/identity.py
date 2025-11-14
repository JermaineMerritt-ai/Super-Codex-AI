#!/usr/bin/env python3
"""
Core Identity Management System
Handles identity creation, storage, and seal management
"""

import json
import os
import hashlib
import time
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

# Create data directories
IDENTITY_DIR = Path("data/identities")
SEALS_DIR = Path("data/seals")
IDENTITY_DIR.mkdir(parents=True, exist_ok=True)
SEALS_DIR.mkdir(parents=True, exist_ok=True)

def save_identity(slug: str, identity: Dict) -> bool:
    """Save identity data to file system"""
    try:
        identity_file = IDENTITY_DIR / f"{slug}.json"
        with open(identity_file, 'w') as f:
            json.dump(identity, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving identity {slug}: {e}")
        return False

def save_seal(slug: str, seal: Dict) -> bool:
    """Save seal data to file system"""
    try:
        seal_file = SEALS_DIR / f"{slug}.json"
        with open(seal_file, 'w') as f:
            json.dump(seal, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving seal {slug}: {e}")
        return False

def load_identity(slug: str) -> Optional[Dict]:
    """Load identity data from file system"""
    try:
        identity_file = IDENTITY_DIR / f"{slug}.json"
        if identity_file.exists():
            with open(identity_file, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading identity {slug}: {e}")
        return None

def load_seal(slug: str) -> Optional[Dict]:
    """Load seal data from file system"""
    try:
        seal_file = SEALS_DIR / f"{slug}.json"
        if seal_file.exists():
            with open(seal_file, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading seal {slug}: {e}")
        return None

def list_identities() -> List[str]:
    """List all identity slugs"""
    try:
        return [f.stem for f in IDENTITY_DIR.glob("*.json")]
    except Exception as e:
        print(f"Error listing identities: {e}")
        return []

def list_seals() -> List[str]:
    """List all seal slugs"""
    try:
        return [f.stem for f in SEALS_DIR.glob("*.json")]
    except Exception as e:
        print(f"Error listing seals: {e}")
        return []

def generate_identity_slug(name: str, timestamp: Optional[int] = None) -> str:
    """Generate unique slug for identity"""
    if timestamp is None:
        timestamp = int(time.time())
    
    # Create slug from name and timestamp
    slug_data = f"{name}-{timestamp}"
    slug_hash = hashlib.sha256(slug_data.encode()).hexdigest()[:12]
    return slug_hash

def validate_identity(identity: Dict) -> bool:
    """Validate identity data structure"""
    required_fields = ["name", "roles", "slug", "stamped_at"]
    return all(field in identity for field in required_fields)

def validate_seal(seal: Dict) -> bool:
    """Validate seal data structure"""
    required_fields = ["slug", "seal", "status"]
    return all(field in seal for field in required_fields)

def create_identity_backup() -> str:
    """Create backup of all identities and seals"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backups/identity_backup_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup identities
        identities_backup = backup_dir / "identities"
        identities_backup.mkdir(exist_ok=True)
        for identity_file in IDENTITY_DIR.glob("*.json"):
            backup_file = identities_backup / identity_file.name
            backup_file.write_text(identity_file.read_text())
        
        # Backup seals
        seals_backup = backup_dir / "seals"
        seals_backup.mkdir(exist_ok=True)
        for seal_file in SEALS_DIR.glob("*.json"):
            backup_file = seals_backup / seal_file.name
            backup_file.write_text(seal_file.read_text())
        
        return str(backup_dir)
    except Exception as e:
        print(f"Error creating backup: {e}")
        return ""

def restore_identity_backup(backup_path: str) -> bool:
    """Restore identities and seals from backup"""
    try:
        backup_dir = Path(backup_path)
        if not backup_dir.exists():
            print(f"Backup directory {backup_path} does not exist")
            return False
        
        # Restore identities
        identities_backup = backup_dir / "identities"
        if identities_backup.exists():
            for backup_file in identities_backup.glob("*.json"):
                identity_file = IDENTITY_DIR / backup_file.name
                identity_file.write_text(backup_file.read_text())
        
        # Restore seals
        seals_backup = backup_dir / "seals"
        if seals_backup.exists():
            for backup_file in seals_backup.glob("*.json"):
                seal_file = SEALS_DIR / backup_file.name
                seal_file.write_text(backup_file.read_text())
        
        return True
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

def cleanup_old_identities(days_old: int = 30) -> int:
    """Clean up identities older than specified days"""
    try:
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        cleaned_count = 0
        
        for identity_slug in list_identities():
            identity = load_identity(identity_slug)
            if identity and identity.get("stamped_at", 0) < cutoff_time:
                # Remove identity and corresponding seal
                identity_file = IDENTITY_DIR / f"{identity_slug}.json"
                seal_file = SEALS_DIR / f"{identity_slug}.json"
                
                if identity_file.exists():
                    identity_file.unlink()
                if seal_file.exists():
                    seal_file.unlink()
                
                cleaned_count += 1
        
        return cleaned_count
    except Exception as e:
        print(f"Error cleaning up identities: {e}")
        return 0

def get_identity_stats() -> Dict:
    """Get statistics about identities and seals"""
    try:
        identities = list_identities()
        seals = list_seals()
        
        # Calculate storage usage
        identity_size = sum(f.stat().st_size for f in IDENTITY_DIR.glob("*.json"))
        seals_size = sum(f.stat().st_size for f in SEALS_DIR.glob("*.json"))
        
        return {
            "total_identities": len(identities),
            "total_seals": len(seals),
            "identity_storage_bytes": identity_size,
            "seals_storage_bytes": seals_size,
            "total_storage_bytes": identity_size + seals_size,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error getting identity stats: {e}")
        return {}

if __name__ == "__main__":
    # Test the identity system
    print("🔮 Testing Core Identity System")
    print("=" * 40)
    
    # Test identity creation
    test_slug = generate_identity_slug("Test User")
    test_identity = {
        "name": "Test User",
        "roles": ["tester", "admin"],
        "slug": test_slug,
        "stamped_at": int(time.time())
    }
    test_seal = {
        "slug": test_slug,
        "seal": f"SIGIL-{test_slug}",
        "status": "crowned"
    }
    
    # Save and load test
    print(f"✅ Generated slug: {test_slug}")
    print(f"✅ Saving identity: {save_identity(test_slug, test_identity)}")
    print(f"✅ Saving seal: {save_seal(test_slug, test_seal)}")
    
    loaded_identity = load_identity(test_slug)
    loaded_seal = load_seal(test_slug)
    
    print(f"✅ Loaded identity: {loaded_identity is not None}")
    print(f"✅ Loaded seal: {loaded_seal is not None}")
    
    # Validation test
    print(f"✅ Identity valid: {validate_identity(test_identity)}")
    print(f"✅ Seal valid: {validate_seal(test_seal)}")
    
    # Stats test
    stats = get_identity_stats()
    print(f"✅ Identity stats: {stats}")
    
    print("\n🎉 Core Identity System Test Complete!")