#!/usr/bin/env python3
"""
SIGIL Seal System for the Codex Dominion
Sacred ceremonial authentication and binding system for content preservation.

This system provides cryptographic seals that bind content to custodians,
avatar roles, and ceremonial cycles with flame glyphs for visual identification.
"""

import uuid
import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class CycleType(Enum):
    """Sacred ceremonial cycle types."""
    MILLENNIAL = "millennial"
    CENTENNIAL = "centennial"
    DECENNIAL = "decennial"
    ANNUAL = "annual"
    SEASONAL = "seasonal"
    LUNAR = "lunar"
    ETERNAL = "eternal"

class SealAuthority(Enum):
    """Authority levels for seal generation."""
    SUPREME = "supreme"  # Ultimate custodian authority
    HIGH = "high"        # Council member authority  
    SACRED = "sacred"    # Flame keeper authority
    NOBLE = "noble"      # Wisdom bearer authority
    GUARDIAN = "guardian" # Guardian authority
    CEREMONIAL = "ceremonial" # Ceremonial guide authority
    HERALD = "herald"    # Herald authority
    INITIATE = "initiate" # Initiate authority

@dataclass
class SealMetadata:
    """Metadata for SIGIL seals."""
    content_hash: str
    binding_strength: int
    ceremonial_weight: float
    authority_level: str
    verification_count: int = 0
    linked_seals: List[str] = None
    
    def __post_init__(self):
        if self.linked_seals is None:
            self.linked_seals = []

class SIGILSeal:
    """
    Sacred Identification Glyph for Immutable Ledger (SIGIL) Seal.
    
    Provides ceremonial authentication and binding for content within
    the Codex Dominion archive system.
    """
    
    def __init__(self, custodian_name: str, avatar_role: str, cycle_tag: str, 
                 cycle_type: CycleType = CycleType.ETERNAL, 
                 authority: SealAuthority = SealAuthority.INITIATE,
                 content_hash: str = None):
        """
        Initialize a new SIGIL seal.
        
        Args:
            custodian_name: Name of the custodian creating the seal
            avatar_role: Role within the avatar hierarchy
            cycle_tag: Ceremonial cycle identifier
            cycle_type: Type of ceremonial cycle
            authority: Authority level of the seal creator
            content_hash: Hash of content being sealed (optional)
        """
        self.seal_id = str(uuid.uuid4())
        self.custodian_name = custodian_name
        self.avatar_role = avatar_role
        self.cycle_tag = cycle_tag
        self.cycle_type = cycle_type
        self.authority = authority
        self.issued_at = datetime.now(timezone.utc)
        self.content_hash = content_hash or self._generate_content_hash()
        
        # Calculate binding strength first
        self.binding_strength = self._calculate_binding_strength()
        
        # Generate seal metadata
        self.metadata = SealMetadata(
            content_hash=self.content_hash,
            binding_strength=self.binding_strength,
            ceremonial_weight=self._calculate_ceremonial_weight(),
            authority_level=authority.value
        )
        
        # Generate cryptographic signature
        self.signature = self._generate_signature()
    
    def _generate_content_hash(self) -> str:
        """Generate a hash for the seal content."""
        content = f"{self.custodian_name}{self.avatar_role}{self.cycle_tag}{self.issued_at.isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _calculate_binding_strength(self) -> int:
        """Calculate the binding strength based on authority level."""
        authority_weights = {
            SealAuthority.SUPREME: 100,
            SealAuthority.HIGH: 85,
            SealAuthority.SACRED: 70,
            SealAuthority.NOBLE: 60,
            SealAuthority.GUARDIAN: 50,
            SealAuthority.CEREMONIAL: 40,
            SealAuthority.HERALD: 30,
            SealAuthority.INITIATE: 20
        }
        return authority_weights.get(self.authority, 20)
    
    def _calculate_ceremonial_weight(self) -> float:
        """Calculate ceremonial weight based on cycle type."""
        cycle_weights = {
            CycleType.ETERNAL: 10.0,
            CycleType.MILLENNIAL: 8.0,
            CycleType.CENTENNIAL: 6.0,
            CycleType.DECENNIAL: 4.0,
            CycleType.ANNUAL: 3.0,
            CycleType.SEASONAL: 2.0,
            CycleType.LUNAR: 1.0
        }
        base_weight = cycle_weights.get(self.cycle_type, 1.0)
        # Multiply by authority level for final weight
        authority_multiplier = (self.binding_strength / 100)
        return round(base_weight * authority_multiplier, 2)
    
    def _generate_signature(self) -> str:
        """Generate cryptographic signature for the seal."""
        signature_data = {
            "seal_id": self.seal_id,
            "custodian": self.custodian_name,
            "role": self.avatar_role,
            "cycle": self.cycle_tag,
            "timestamp": self.issued_at.timestamp(),
            "authority": self.authority.value,
            "content_hash": self.content_hash
        }
        
        signature_string = json.dumps(signature_data, sort_keys=True)
        return hashlib.sha256(signature_string.encode()).hexdigest()
    
    def generate_flame_glyph(self) -> str:
        """Generate the sacred flame glyph for visual identification."""
        # Different flames based on authority level
        flame_symbols = {
            SealAuthority.SUPREME: "🔥🔥🔥",
            SealAuthority.HIGH: "🔥🔥",
            SealAuthority.SACRED: "🔥",
            SealAuthority.NOBLE: "🕯️",
            SealAuthority.GUARDIAN: "🏮",
            SealAuthority.CEREMONIAL: "💫", 
            SealAuthority.HERALD: "⭐",
            SealAuthority.INITIATE: "✨"
        }
        
        flame = flame_symbols.get(self.authority, "✨")
        role_abbrev = self.avatar_role[:3].upper()
        cycle_abbrev = self.cycle_tag[:3].upper()
        seal_short = self.seal_id[:8]
        
        return f"{flame}-{role_abbrev}-{cycle_abbrev}-{seal_short}"
    
    def generate_binding_sigil(self) -> str:
        """Generate a complex binding sigil for high-security seals."""
        if self.authority in [SealAuthority.SUPREME, SealAuthority.HIGH, SealAuthority.SACRED]:
            # Complex sigil for high authority
            symbols = ["⚡", "🌟", "💎", "🗝️", "🛡️", "👑", "⚖️"]
            # Use seal_id for symbol selection (guaranteed to be hex)
            symbol_index = int(self.seal_id[:2], 16) % len(symbols)
            base_symbol = symbols[symbol_index]
            
            return f"{base_symbol}{self.generate_flame_glyph()}{base_symbol}"
        else:
            return self.generate_flame_glyph()
    
    def verify_seal(self) -> bool:
        """Verify the seal's cryptographic integrity."""
        try:
            # Regenerate signature and compare
            expected_signature = self._generate_signature()
            is_valid = self.signature == expected_signature
            
            if is_valid:
                self.metadata.verification_count += 1
                
            return is_valid
        except Exception:
            return False
    
    def display_seal(self) -> Dict[str, Any]:
        """Display the complete seal information."""
        return {
            "Seal ID": self.seal_id,
            "Custodian": self.custodian_name,
            "Avatar Role": self.avatar_role,
            "Ceremonial Cycle": self.cycle_tag,
            "Cycle Type": self.cycle_type.value.title(),
            "Authority Level": self.authority.value.title(),
            "Flame Glyph": self.generate_flame_glyph(),
            "Binding Sigil": self.generate_binding_sigil(),
            "Issued": self.issued_at.isoformat(),
            "Content Hash": self.content_hash,
            "Binding Strength": self.metadata.binding_strength,
            "Ceremonial Weight": self.metadata.ceremonial_weight,
            "Verification Count": self.metadata.verification_count,
            "Signature": self.signature[:16] + "...",
            "Valid": self.verify_seal()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert seal to dictionary for storage."""
        return {
            "seal_id": self.seal_id,
            "custodian_name": self.custodian_name,
            "avatar_role": self.avatar_role,
            "cycle_tag": self.cycle_tag,
            "cycle_type": self.cycle_type.value,
            "authority": self.authority.value,
            "issued_at": self.issued_at.isoformat(),
            "content_hash": self.content_hash,
            "signature": self.signature,
            "metadata": asdict(self.metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SIGILSeal':
        """Create seal from dictionary data."""
        seal = cls.__new__(cls)
        seal.seal_id = data["seal_id"]
        seal.custodian_name = data["custodian_name"]
        seal.avatar_role = data["avatar_role"]
        seal.cycle_tag = data["cycle_tag"]
        seal.cycle_type = CycleType(data["cycle_type"])
        seal.authority = SealAuthority(data["authority"])
        seal.issued_at = datetime.fromisoformat(data["issued_at"])
        seal.content_hash = data["content_hash"]
        seal.signature = data["signature"]
        
        # Reconstruct metadata
        metadata_dict = data["metadata"]
        seal.metadata = SealMetadata(
            content_hash=metadata_dict["content_hash"],
            binding_strength=metadata_dict["binding_strength"],
            ceremonial_weight=metadata_dict["ceremonial_weight"],
            authority_level=metadata_dict["authority_level"],
            verification_count=metadata_dict.get("verification_count", 0),
            linked_seals=metadata_dict.get("linked_seals", [])
        )
        
        return seal

class SealRegistry:
    """Registry for managing and storing SIGIL seals."""
    
    def __init__(self, storage_path: str = "sigil_registry"):
        """Initialize the seal registry."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.registry_file = self.storage_path / "seal_registry.json"
        self.seals: Dict[str, SIGILSeal] = {}
        self.load_registry()
    
    def load_registry(self):
        """Load existing seals from storage."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for seal_data in data.get("seals", []):
                    seal = SIGILSeal.from_dict(seal_data)
                    self.seals[seal.seal_id] = seal
                    
        except Exception as e:
            print(f"⚠️  Warning: Could not load seal registry: {e}")
    
    def save_registry(self):
        """Save seals to storage."""
        try:
            registry_data = {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "total_seals": len(self.seals),
                "seals": [seal.to_dict() for seal in self.seals.values()]
            }
            
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry_data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving seal registry: {e}")
    
    def register_seal(self, seal: SIGILSeal) -> bool:
        """Register a new seal in the registry."""
        try:
            if seal.verify_seal():
                self.seals[seal.seal_id] = seal
                self.save_registry()
                return True
            return False
        except Exception:
            return False
    
    def get_seal(self, seal_id: str) -> Optional[SIGILSeal]:
        """Retrieve a seal by ID."""
        return self.seals.get(seal_id)
    
    def verify_seal_chain(self, seal_ids: List[str]) -> bool:
        """Verify a chain of linked seals."""
        for seal_id in seal_ids:
            seal = self.get_seal(seal_id)
            if not seal or not seal.verify_seal():
                return False
        return True
    
    def get_seals_by_custodian(self, custodian_name: str) -> List[SIGILSeal]:
        """Get all seals created by a specific custodian."""
        return [seal for seal in self.seals.values() 
                if seal.custodian_name == custodian_name]
    
    def get_seals_by_authority(self, authority: SealAuthority) -> List[SIGILSeal]:
        """Get all seals with specific authority level."""
        return [seal for seal in self.seals.values() 
                if seal.authority == authority]
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        if not self.seals:
            return {"total_seals": 0, "message": "No seals in registry"}
        
        authority_counts = {}
        cycle_counts = {}
        total_binding_strength = 0
        total_ceremonial_weight = 0.0
        
        for seal in self.seals.values():
            authority_counts[seal.authority.value] = authority_counts.get(seal.authority.value, 0) + 1
            cycle_counts[seal.cycle_type.value] = cycle_counts.get(seal.cycle_type.value, 0) + 1
            total_binding_strength += seal.metadata.binding_strength
            total_ceremonial_weight += seal.metadata.ceremonial_weight
        
        return {
            "total_seals": len(self.seals),
            "authority_distribution": authority_counts,
            "cycle_distribution": cycle_counts,
            "average_binding_strength": round(total_binding_strength / len(self.seals), 2),
            "average_ceremonial_weight": round(total_ceremonial_weight / len(self.seals), 2),
            "registry_file": str(self.registry_file)
        }

def create_supreme_seal(custodian_name: str, content_hash: str = None) -> SIGILSeal:
    """Create a supreme authority seal for ultimate custodian operations."""
    return SIGILSeal(
        custodian_name=custodian_name,
        avatar_role="Supreme Custodian",
        cycle_tag="Eternal Dominion",
        cycle_type=CycleType.ETERNAL,
        authority=SealAuthority.SUPREME,
        content_hash=content_hash
    )

def create_ceremonial_seal(custodian_name: str, avatar_role: str, ceremony_type: str) -> SIGILSeal:
    """Create a ceremonial seal for specific ritual operations."""
    return SIGILSeal(
        custodian_name=custodian_name,
        avatar_role=avatar_role,
        cycle_tag=f"Ceremony of {ceremony_type}",
        cycle_type=CycleType.SEASONAL,  # Use SEASONAL for ceremonial operations
        authority=SealAuthority.CEREMONIAL
    )

def demo_sigil_system():
    """Demonstrate the SIGIL seal system functionality."""
    print("\n" + "="*60)
    print("🔥 SIGIL SEAL SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Initialize registry
    print("\n1. Initializing SIGIL Registry...")
    registry = SealRegistry()
    print(f"   ✅ Registry initialized at: {registry.storage_path}")
    
    # Create various seals
    print("\n2. Creating Sacred Seals...")
    
    # Supreme seal
    supreme_seal = create_supreme_seal("Jermaine Merritt", "eternal_codex_hash_001")
    registry.register_seal(supreme_seal)
    print(f"   🔥🔥🔥 Supreme Seal: {supreme_seal.generate_flame_glyph()}")
    
    # High authority council seal
    council_seal = SIGILSeal(
        custodian_name="Avatar Council",
        avatar_role="Council Collective",
        cycle_tag="Millennial Governance",
        cycle_type=CycleType.MILLENNIAL,
        authority=SealAuthority.HIGH
    )
    registry.register_seal(council_seal)
    print(f"   🔥🔥 Council Seal: {council_seal.generate_flame_glyph()}")
    
    # Sacred flame keeper seal
    flame_seal = SIGILSeal(
        custodian_name="Archon Memorialis",
        avatar_role="Flame Keeper",
        cycle_tag="Sacred Preservation",
        cycle_type=CycleType.ETERNAL,
        authority=SealAuthority.SACRED
    )
    registry.register_seal(flame_seal)
    print(f"   🔥 Flame Keeper Seal: {flame_seal.generate_flame_glyph()}")
    
    # Ceremonial guide seal
    ceremonial_seal = create_ceremonial_seal("Saga the Storyteller", "Ceremonial Guide", "Memory Archive")
    registry.register_seal(ceremonial_seal)
    print(f"   💫 Ceremonial Seal: {ceremonial_seal.generate_flame_glyph()}")
    
    # Herald seal
    herald_seal = SIGILSeal(
        custodian_name="Echo the Dispatcher",
        avatar_role="Herald",
        cycle_tag="Message Distribution",
        cycle_type=CycleType.LUNAR,
        authority=SealAuthority.HERALD
    )
    registry.register_seal(herald_seal)
    print(f"   ⭐ Herald Seal: {herald_seal.generate_flame_glyph()}")
    
    # Display seal details
    print("\n3. Sacred Seal Details...")
    print("\n   🔥🔥🔥 SUPREME SEAL:")
    for key, value in supreme_seal.display_seal().items():
        print(f"      {key}: {value}")
    
    print("\n   🔥 FLAME KEEPER SEAL:")
    for key, value in flame_seal.display_seal().items():
        print(f"      {key}: {value}")
    
    # Demonstrate verification
    print("\n4. Seal Verification...")
    print(f"   ✅ Supreme Seal Valid: {supreme_seal.verify_seal()}")
    print(f"   ✅ Council Seal Valid: {council_seal.verify_seal()}")
    print(f"   ✅ Flame Seal Valid: {flame_seal.verify_seal()}")
    
    # Show registry statistics
    print("\n5. Registry Statistics...")
    stats = registry.get_registry_stats()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   📊 {key.replace('_', ' ').title()}:")
            for k, v in value.items():
                print(f"      - {k.title()}: {v}")
        else:
            print(f"   📊 {key.replace('_', ' ').title()}: {value}")
    
    # Demonstrate binding sigils for high authority
    print("\n6. Binding Sigils...")
    print(f"   🔥🔥🔥 Supreme Binding: {supreme_seal.generate_binding_sigil()}")
    print(f"   🔥🔥 Council Binding: {council_seal.generate_binding_sigil()}")
    print(f"   🔥 Sacred Binding: {flame_seal.generate_binding_sigil()}")
    print(f"   💫 Ceremonial Binding: {ceremonial_seal.generate_binding_sigil()}")
    
    print("\n" + "="*60)
    print("🎉 SIGIL SEAL SYSTEM DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nThe SIGIL system provides:")
    print("  • Cryptographic seal authentication")
    print("  • Authority-based binding strength")
    print("  • Ceremonial cycle management")
    print("  • Visual flame glyph identification")
    print("  • Persistent seal registry")
    print("  • Chain of custody verification")
    
    return registry

if __name__ == "__main__":
    # Run demonstration
    demo_sigil_system()