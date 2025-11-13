"""
Treasury Binding Module - Ceremonial Flame Architecture
========================================================

This module implements the sacred treasury binding system for the ceremonial flame architecture,
managing abundance flows, resource allocation, and ceremonial value preservation.

The treasury binding operates as the financial heart of the ceremonial system, ensuring that:
1. Sacred resources are properly allocated and tracked
2. Ceremonial transactions maintain integrity and auditability  
3. Abundance flows align with governance and honor structures
4. Treasury operations support Twilio dominion flame communications
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Treasury binding constants
TREASURY_STORAGE_PATH = "codex-flame/storage/treasury"
ABUNDANCE_FLOW_PATH = "codex-flame/storage/abundance-flows"
BINDING_REGISTRY_PATH = "codex-flame/storage/binding-registry"

class ResourceType(Enum):
    """Sacred resource types in the treasury binding system"""
    FLAME_ESSENCE = "flame_essence"
    CEREMONIAL_TOKENS = "ceremonial_tokens"
    DOMINION_CREDITS = "dominion_credits"
    HONOR_POINTS = "honor_points"
    WISDOM_SHARES = "wisdom_shares"
    SACRED_BONDS = "sacred_bonds"

class TreasuryOperation(Enum):
    """Types of treasury operations"""
    ALLOCATION = "allocation"
    TRANSFER = "transfer"
    BINDING = "binding"
    RELEASE = "release"
    AUDIT = "audit"
    CEREMONIAL_GRANT = "ceremonial_grant"

@dataclass
class TreasuryEntry:
    """Represents a single treasury entry with ceremonial binding"""
    entry_id: str
    timestamp: str
    resource_type: ResourceType
    amount: float
    operation: TreasuryOperation
    actor: str
    realm: str
    capsule: Optional[str]
    governance_seal: str
    binding_hash: str
    metadata: Dict[str, Any]

@dataclass
class AbundanceFlow:
    """Represents an abundance flow between ceremonial entities"""
    flow_id: str
    timestamp: str
    source_entity: str
    target_entity: str
    resource_type: ResourceType
    flow_amount: float
    flow_purpose: str
    ceremonial_authority: str
    binding_signature: str

class TreasuryBinding:
    """Main treasury binding class for ceremonial resource management"""
    
    def __init__(self, storage_root: str = "."):
        """Initialize treasury binding with storage paths"""
        self.storage_root = Path(storage_root)
        self.treasury_path = self.storage_root / TREASURY_STORAGE_PATH
        self.abundance_path = self.storage_root / ABUNDANCE_FLOW_PATH
        self.binding_path = self.storage_root / BINDING_REGISTRY_PATH
        
        # Ensure storage directories exist
        self._ensure_storage_directories()
        
    def _ensure_storage_directories(self):
        """Create necessary storage directories"""
        for path in [self.treasury_path, self.abundance_path, self.binding_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _generate_binding_hash(self, data: Dict[str, Any]) -> str:
        """Generate a ceremonial binding hash for treasury operations"""
        import hashlib
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16].upper()
    
    def allocate_resources(self, 
                         resource_type: ResourceType,
                         amount: float,
                         actor: str,
                         realm: str,
                         capsule: Optional[str] = None,
                         purpose: str = "ceremonial_allocation") -> TreasuryEntry:
        """Allocate sacred resources with ceremonial binding"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        entry_id = f"TRE-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Create binding data for hash generation
        binding_data = {
            "entry_id": entry_id,
            "resource_type": resource_type.value,
            "amount": amount,
            "actor": actor,
            "realm": realm,
            "timestamp": timestamp
        }
        
        binding_hash = self._generate_binding_hash(binding_data)
        governance_seal = f"GS-{binding_hash[:8]}"
        
        # Create treasury entry
        entry = TreasuryEntry(
            entry_id=entry_id,
            timestamp=timestamp,
            resource_type=resource_type,
            amount=amount,
            operation=TreasuryOperation.ALLOCATION,
            actor=actor,
            realm=realm,
            capsule=capsule,
            governance_seal=governance_seal,
            binding_hash=binding_hash,
            metadata={
                "purpose": purpose,
                "allocation_authority": actor,
                "binding_ceremony": "sacred_resource_allocation"
            }
        )
        
        # Store treasury entry
        self._store_treasury_entry(entry)
        
        return entry
    
    def create_abundance_flow(self,
                            source_entity: str,
                            target_entity: str,
                            resource_type: ResourceType,
                            flow_amount: float,
                            flow_purpose: str,
                            ceremonial_authority: str) -> AbundanceFlow:
        """Create an abundance flow between ceremonial entities"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        flow_id = f"ABF-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Generate binding signature for flow integrity
        flow_data = {
            "flow_id": flow_id,
            "source": source_entity,
            "target": target_entity,
            "amount": flow_amount,
            "timestamp": timestamp
        }
        
        binding_signature = self._generate_binding_hash(flow_data)
        
        # Create abundance flow
        flow = AbundanceFlow(
            flow_id=flow_id,
            timestamp=timestamp,
            source_entity=source_entity,
            target_entity=target_entity,
            resource_type=resource_type,
            flow_amount=flow_amount,
            flow_purpose=flow_purpose,
            ceremonial_authority=ceremonial_authority,
            binding_signature=binding_signature
        )
        
        # Store abundance flow
        self._store_abundance_flow(flow)
        
        return flow
    
    def bind_ceremonial_treasury(self,
                               treasury_name: str,
                               initial_resources: Dict[ResourceType, float],
                               binding_authority: str,
                               realm: str) -> Dict[str, Any]:
        """Bind a new ceremonial treasury with initial resource allocation"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        binding_id = f"CTB-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Create individual allocations for each resource type
        allocations = []
        for resource_type, amount in initial_resources.items():
            entry = self.allocate_resources(
                resource_type=resource_type,
                amount=amount,
                actor=binding_authority,
                realm=realm,
                purpose=f"ceremonial_treasury_binding_{treasury_name}"
            )
            allocations.append(entry.entry_id)
        
        # Create treasury binding registry
        binding_registry = {
            "binding_id": binding_id,
            "treasury_name": treasury_name,
            "timestamp": timestamp,
            "binding_authority": binding_authority,
            "realm": realm,
            "initial_allocations": allocations,
            "resource_summary": {rt.value: amount for rt, amount in initial_resources.items()},
            "binding_status": "active",
            "ceremonial_seal": f"CS-{binding_id[-8:]}"
        }
        
        # Store binding registry
        registry_path = self.binding_path / f"{binding_id}.json"
        with open(registry_path, 'w') as f:
            json.dump(binding_registry, f, indent=2)
        
        return binding_registry
    
    def _store_treasury_entry(self, entry: TreasuryEntry):
        """Store a treasury entry to persistent storage"""
        entry_dict = asdict(entry)
        # Convert enum to string for JSON serialization
        entry_dict['resource_type'] = entry.resource_type.value
        entry_dict['operation'] = entry.operation.value
        
        entry_path = self.treasury_path / f"{entry.entry_id}.json"
        with open(entry_path, 'w') as f:
            json.dump(entry_dict, f, indent=2)
    
    def _store_abundance_flow(self, flow: AbundanceFlow):
        """Store an abundance flow to persistent storage"""
        flow_dict = asdict(flow)
        # Convert enum to string for JSON serialization
        flow_dict['resource_type'] = flow.resource_type.value
        
        flow_path = self.abundance_path / f"{flow.flow_id}.json"
        with open(flow_path, 'w') as f:
            json.dump(flow_dict, f, indent=2)
    
    def get_treasury_balance(self, 
                           entity_name: str, 
                           resource_type: Optional[ResourceType] = None) -> Dict[str, float]:
        """Calculate current treasury balance for an entity"""
        balances = {}
        
        # Scan all treasury entries for this entity
        for entry_file in self.treasury_path.glob("*.json"):
            with open(entry_file, 'r') as f:
                entry_data = json.load(f)
                
            # Check if entry involves this entity
            if entry_data.get('actor') == entity_name or entry_data.get('capsule') == entity_name:
                rt = entry_data['resource_type']
                amount = entry_data['amount']
                operation = entry_data['operation']
                
                # Filter by resource type if specified
                if resource_type and rt != resource_type.value:
                    continue
                
                # Initialize balance if not exists
                if rt not in balances:
                    balances[rt] = 0.0
                
                # Add or subtract based on operation
                if operation in ['allocation', 'ceremonial_grant']:
                    balances[rt] += amount
                elif operation in ['transfer', 'release']:
                    balances[rt] -= amount
        
        return balances
    
    def audit_treasury_operations(self, 
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                actor: Optional[str] = None) -> List[Dict[str, Any]]:
        """Perform treasury audit with optional filters"""
        audit_results = []
        
        # Scan all treasury entries
        for entry_file in self.treasury_path.glob("*.json"):
            with open(entry_file, 'r') as f:
                entry_data = json.load(f)
            
            # Apply filters
            if start_date and entry_data['timestamp'] < start_date:
                continue
            if end_date and entry_data['timestamp'] > end_date:
                continue
            if actor and entry_data['actor'] != actor:
                continue
            
            audit_results.append(entry_data)
        
        # Sort by timestamp
        audit_results.sort(key=lambda x: x['timestamp'])
        
        return audit_results

# Twilio integration for dominion flame treasury notifications
class TwilioTreasuryNotifier:
    """Handle Twilio notifications for treasury operations"""
    
    def __init__(self, account_sid: str, auth_token: str, from_whatsapp: str):
        """Initialize Twilio client for treasury notifications"""
        try:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
            self.from_whatsapp = from_whatsapp
        except ImportError:
            print("Warning: Twilio not available. Treasury notifications disabled.")
            self.client = None
    
    def notify_treasury_operation(self, 
                                entry: TreasuryEntry, 
                                recipient_whatsapp: str,
                                ceremonial_greeting: str = "🔥 Sacred Treasury Update") -> bool:
        """Send Twilio WhatsApp notification for treasury operations"""
        if not self.client:
            return False
        
        try:
            message_body = f"""
{ceremonial_greeting}

Treasury Operation: {entry.operation.value.title()}
Resource Type: {entry.resource_type.value.title()}
Amount: {entry.amount}
Actor: {entry.actor}
Realm: {entry.realm}
Governance Seal: {entry.governance_seal}

May the flames of abundance burn eternal! 🌟
"""
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_whatsapp,
                to=recipient_whatsapp
            )
            
            return True
            
        except Exception as e:
            print(f"Failed to send treasury notification: {e}")
            return False

# Factory function for easy treasury binding creation
def create_treasury_binding(storage_root: str = ".") -> TreasuryBinding:
    """Factory function to create a configured treasury binding"""
    return TreasuryBinding(storage_root=storage_root)

# Example usage and ceremonial initialization
if __name__ == "__main__":
    # Create treasury binding instance
    treasury = create_treasury_binding()
    
    # Example: Allocate initial ceremonial resources
    flame_allocation = treasury.allocate_resources(
        resource_type=ResourceType.FLAME_ESSENCE,
        amount=1000.0,
        actor="Custodian",
        realm="PL-001",
        capsule="Sovereign Crown",
        purpose="ceremonial_flame_initialization"
    )
    
    print(f"Sacred Treasury Allocation Complete: {flame_allocation.entry_id}")
    print(f"Governance Seal: {flame_allocation.governance_seal}")
    print(f"Binding Hash: {flame_allocation.binding_hash}")
    
    # Example: Create abundance flow
    abundance_flow = treasury.create_abundance_flow(
        source_entity="Sacred Treasury",
        target_entity="Ceremonial Council",
        resource_type=ResourceType.CEREMONIAL_TOKENS,
        flow_amount=500.0,
        flow_purpose="council_operations_funding",
        ceremonial_authority="Custodian"
    )
    
    print(f"Abundance Flow Established: {abundance_flow.flow_id}")
    print(f"Binding Signature: {abundance_flow.binding_signature}")