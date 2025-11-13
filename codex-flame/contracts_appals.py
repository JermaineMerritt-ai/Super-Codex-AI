"""
Contracts Appeals Module - Sacred Contract and Appeal Management System
========================================================================

This module implements the contracts and appeals system for managing sacred agreements,
ceremonial disputes, and the resolution of conflicts within the ceremonial flame architecture.

The contracts and appeals system provides:
1. Sacred contract creation and management
2. Dispute resolution mechanisms
3. Appeal processes and arbitration
4. Ceremonial mediation protocols
5. Binding agreement enforcement
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Contracts and Appeals storage paths
CONTRACTS_PATH = "codex-flame/storage/contracts/agreements"
APPEALS_PATH = "codex-flame/storage/contracts/appeals"
ARBITRATIONS_PATH = "codex-flame/storage/contracts/arbitrations"
RESOLUTIONS_PATH = "codex-flame/storage/contracts/resolutions"

class ContractType(Enum):
    """Types of sacred contracts"""
    CEREMONIAL_SERVICE = "ceremonial_service"
    FLAME_CUSTODY = "flame_custody"
    WISDOM_PRESERVATION = "wisdom_preservation"
    SACRED_ALLIANCE = "sacred_alliance"
    HONOR_COVENANT = "honor_covenant"
    SUCCESSION_AGREEMENT = "succession_agreement"
    RESOURCE_ALLOCATION = "resource_allocation"
    CEREMONIAL_PARTNERSHIP = "ceremonial_partnership"

class ContractStatus(Enum):
    """Status of sacred contracts"""
    DRAFT = "draft"
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    BREACHED = "breached"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    UNDER_REVIEW = "under_review"

class AppealType(Enum):
    """Types of ceremonial appeals"""
    CONTRACT_BREACH = "contract_breach"
    CEREMONIAL_DISPUTE = "ceremonial_dispute"
    HONOR_VIOLATION = "honor_violation"
    AUTHORITY_CHALLENGE = "authority_challenge"
    SUCCESSION_DISPUTE = "succession_dispute"
    RESOURCE_CONFLICT = "resource_conflict"
    PROCEDURAL_OBJECTION = "procedural_objection"

class AppealStatus(Enum):
    """Status of appeals"""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    MEDIATION = "mediation"
    ARBITRATION = "arbitration"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"
    ESCALATED = "escalated"

class ArbitrationLevel(Enum):
    """Levels of arbitration authority"""
    KEEPER_COUNCIL = "keeper_council"
    ELDER_TRIBUNAL = "elder_tribunal"
    TRIUMVIRATE_DECISION = "triumvirate_decision"
    SUPREME_ARBITRATION = "supreme_arbitration"

@dataclass
class SacredContract:
    """Represents a sacred contract or agreement"""
    contract_id: str
    contract_name: str
    contract_type: ContractType
    parties: List[Dict[str, str]]  # [{"name": str, "role": str}]
    contract_terms: List[str]
    obligations: Dict[str, List[str]]  # party_name: [obligations]
    ceremonial_conditions: List[str]
    effective_date: str
    expiration_date: Optional[str]
    renewal_terms: Optional[Dict[str, Any]]
    contract_status: ContractStatus
    witness_seals: List[str]
    sacred_binding: str
    enforcement_authority: str
    metadata: Dict[str, Any]

@dataclass
class CeremonialAppeal:
    """Represents a ceremonial appeal or dispute"""
    appeal_id: str
    appeal_type: AppealType
    appellant_name: str
    respondent_name: str
    appeal_subject: str
    appeal_description: str
    supporting_evidence: List[str]
    ceremonial_basis: List[str]
    submitted_date: str
    appeal_status: AppealStatus
    assigned_mediator: Optional[str]
    arbitration_level: Optional[ArbitrationLevel]
    witness_statements: List[Dict[str, str]]
    appeal_metadata: Dict[str, Any]

@dataclass
class ArbitrationProceeding:
    """Represents an arbitration proceeding"""
    arbitration_id: str
    appeal_reference: str
    arbitration_level: ArbitrationLevel
    arbitration_panel: List[str]
    proceeding_date: str
    testimonies: List[Dict[str, str]]
    evidence_review: List[str]
    deliberation_notes: str
    arbitration_decision: str
    decision_rationale: str
    binding_authority: str
    enforcement_measures: List[str]
    metadata: Dict[str, Any]

@dataclass
class DisputeResolution:
    """Represents the final resolution of a dispute"""
    resolution_id: str
    dispute_reference: str
    resolution_type: str
    resolution_date: str
    resolution_authority: str
    resolution_terms: List[str]
    enforcement_actions: List[str]
    ceremonial_reconciliation: str
    sacred_healing: List[str]
    future_prevention: List[str]
    resolution_seal: str
    metadata: Dict[str, Any]

class ContractsAppealsSystem:
    """Main class for managing contracts and appeals system"""
    
    def __init__(self, storage_root: str = "."):
        """Initialize the contracts and appeals system"""
        self.storage_root = Path(storage_root)
        self.contracts_path = self.storage_root / CONTRACTS_PATH
        self.appeals_path = self.storage_root / APPEALS_PATH
        self.arbitrations_path = self.storage_root / ARBITRATIONS_PATH
        self.resolutions_path = self.storage_root / RESOLUTIONS_PATH
        
        # Ensure storage directories exist
        self._ensure_storage_directories()
        
    def _ensure_storage_directories(self):
        """Create necessary storage directories for contracts and appeals"""
        for path in [self.contracts_path, self.appeals_path, self.arbitrations_path, self.resolutions_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _generate_sacred_binding(self, data: Dict[str, Any]) -> str:
        """Generate a sacred binding seal for contract integrity"""
        import hashlib
        content = json.dumps(data, sort_keys=True)
        return f"SB-{hashlib.sha256(content.encode()).hexdigest()[:16].upper()}"
    
    def _generate_witness_seal(self, witness_name: str, contract_id: str) -> str:
        """Generate a witness seal for contract validation"""
        import hashlib
        content = f"{witness_name}:{contract_id}:{datetime.now().isoformat()}"
        return f"WS-{hashlib.sha256(content.encode()).hexdigest()[:12].upper()}"
    
    def create_sacred_contract(self,
                             contract_name: str,
                             contract_type: ContractType,
                             parties: List[Dict[str, str]],
                             contract_terms: List[str],
                             obligations: Dict[str, List[str]],
                             ceremonial_conditions: List[str],
                             effective_date: str,
                             expiration_date: Optional[str] = None,
                             renewal_terms: Optional[Dict[str, Any]] = None,
                             witness_names: List[str] = None) -> SacredContract:
        """Create a new sacred contract"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        contract_id = f"SC-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Generate sacred binding
        binding_data = {
            "contract_id": contract_id,
            "contract_type": contract_type.value,
            "parties": parties,
            "terms": contract_terms,
            "effective_date": effective_date
        }
        sacred_binding = self._generate_sacred_binding(binding_data)
        
        # Generate witness seals
        witness_seals = []
        for witness in (witness_names or []):
            witness_seal = self._generate_witness_seal(witness, contract_id)
            witness_seals.append(f"{witness}:{witness_seal}")
        
        # Determine enforcement authority based on contract type
        enforcement_authority = self._determine_enforcement_authority(contract_type)
        
        # Create sacred contract
        contract = SacredContract(
            contract_id=contract_id,
            contract_name=contract_name,
            contract_type=contract_type,
            parties=parties,
            contract_terms=contract_terms,
            obligations=obligations,
            ceremonial_conditions=ceremonial_conditions,
            effective_date=effective_date,
            expiration_date=expiration_date,
            renewal_terms=renewal_terms,
            contract_status=ContractStatus.ACTIVE,
            witness_seals=witness_seals,
            sacred_binding=sacred_binding,
            enforcement_authority=enforcement_authority,
            metadata={
                "creation_date": timestamp,
                "contract_authority": "sacred_covenant_system",
                "ceremonial_weight": "binding"
            }
        )
        
        # Store sacred contract
        self._store_sacred_contract(contract)
        
        return contract
    
    def submit_ceremonial_appeal(self,
                               appeal_type: AppealType,
                               appellant_name: str,
                               respondent_name: str,
                               appeal_subject: str,
                               appeal_description: str,
                               supporting_evidence: List[str],
                               ceremonial_basis: List[str],
                               witness_statements: List[Dict[str, str]]) -> CeremonialAppeal:
        """Submit a ceremonial appeal or dispute"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        appeal_id = f"CA-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Determine appropriate arbitration level
        arbitration_level = self._determine_arbitration_level(appeal_type)
        
        # Assign mediator based on appeal type
        assigned_mediator = self._assign_mediator(appeal_type, appellant_name, respondent_name)
        
        # Create ceremonial appeal
        appeal = CeremonialAppeal(
            appeal_id=appeal_id,
            appeal_type=appeal_type,
            appellant_name=appellant_name,
            respondent_name=respondent_name,
            appeal_subject=appeal_subject,
            appeal_description=appeal_description,
            supporting_evidence=supporting_evidence,
            ceremonial_basis=ceremonial_basis,
            submitted_date=timestamp,
            appeal_status=AppealStatus.SUBMITTED,
            assigned_mediator=assigned_mediator,
            arbitration_level=arbitration_level,
            witness_statements=witness_statements,
            appeal_metadata={
                "submission_authority": "ceremonial_justice_system",
                "appeal_covenant": "fair_resolution_seeking",
                "sacred_right": "ceremonial_appeal_granted"
            }
        )
        
        # Store ceremonial appeal
        self._store_ceremonial_appeal(appeal)
        
        return appeal
    
    def conduct_arbitration(self,
                          appeal_reference: str,
                          arbitration_level: ArbitrationLevel,
                          arbitration_panel: List[str],
                          testimonies: List[Dict[str, str]],
                          evidence_review: List[str],
                          deliberation_notes: str,
                          arbitration_decision: str,
                          decision_rationale: str,
                          enforcement_measures: List[str]) -> ArbitrationProceeding:
        """Conduct an arbitration proceeding"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        arbitration_id = f"AP-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Determine binding authority based on arbitration level
        binding_authority = self._determine_binding_authority(arbitration_level)
        
        # Create arbitration proceeding
        arbitration = ArbitrationProceeding(
            arbitration_id=arbitration_id,
            appeal_reference=appeal_reference,
            arbitration_level=arbitration_level,
            arbitration_panel=arbitration_panel,
            proceeding_date=timestamp,
            testimonies=testimonies,
            evidence_review=evidence_review,
            deliberation_notes=deliberation_notes,
            arbitration_decision=arbitration_decision,
            decision_rationale=decision_rationale,
            binding_authority=binding_authority,
            enforcement_measures=enforcement_measures,
            metadata={
                "arbitration_authority": "ceremonial_tribunal_system",
                "decision_weight": "binding",
                "arbitration_covenant": "justice_and_wisdom"
            }
        )
        
        # Store arbitration proceeding
        self._store_arbitration_proceeding(arbitration)
        
        # Update appeal status
        self._update_appeal_status(appeal_reference, AppealStatus.RESOLVED)
        
        return arbitration
    
    def finalize_dispute_resolution(self,
                                  dispute_reference: str,
                                  resolution_type: str,
                                  resolution_authority: str,
                                  resolution_terms: List[str],
                                  enforcement_actions: List[str],
                                  ceremonial_reconciliation: str,
                                  sacred_healing: List[str],
                                  future_prevention: List[str]) -> DisputeResolution:
        """Finalize the resolution of a dispute"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        resolution_id = f"DR-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Generate resolution seal
        seal_data = {
            "resolution_id": resolution_id,
            "dispute_reference": dispute_reference,
            "resolution_date": timestamp,
            "authority": resolution_authority
        }
        resolution_seal = self._generate_sacred_binding(seal_data)
        
        # Create dispute resolution
        resolution = DisputeResolution(
            resolution_id=resolution_id,
            dispute_reference=dispute_reference,
            resolution_type=resolution_type,
            resolution_date=timestamp,
            resolution_authority=resolution_authority,
            resolution_terms=resolution_terms,
            enforcement_actions=enforcement_actions,
            ceremonial_reconciliation=ceremonial_reconciliation,
            sacred_healing=sacred_healing,
            future_prevention=future_prevention,
            resolution_seal=resolution_seal,
            metadata={
                "resolution_authority": "supreme_ceremonial_justice",
                "resolution_finality": "binding",
                "healing_covenant": "community_restoration"
            }
        )
        
        # Store dispute resolution
        self._store_dispute_resolution(resolution)
        
        return resolution
    
    def _determine_enforcement_authority(self, contract_type: ContractType) -> str:
        """Determine appropriate enforcement authority for contract type"""
        authorities = {
            ContractType.CEREMONIAL_SERVICE: "Ceremonial Council",
            ContractType.FLAME_CUSTODY: "Flame Keepers Council",
            ContractType.WISDOM_PRESERVATION: "Wisdom Guardians",
            ContractType.SACRED_ALLIANCE: "Elder Tribunal",
            ContractType.HONOR_COVENANT: "Honor Council",
            ContractType.SUCCESSION_AGREEMENT: "Triumvirate Authority",
            ContractType.RESOURCE_ALLOCATION: "Resource Council",
            ContractType.CEREMONIAL_PARTNERSHIP: "Partnership Council"
        }
        return authorities.get(contract_type, "General Council")
    
    def _determine_arbitration_level(self, appeal_type: AppealType) -> ArbitrationLevel:
        """Determine appropriate arbitration level for appeal type"""
        levels = {
            AppealType.CONTRACT_BREACH: ArbitrationLevel.KEEPER_COUNCIL,
            AppealType.CEREMONIAL_DISPUTE: ArbitrationLevel.ELDER_TRIBUNAL,
            AppealType.HONOR_VIOLATION: ArbitrationLevel.ELDER_TRIBUNAL,
            AppealType.AUTHORITY_CHALLENGE: ArbitrationLevel.TRIUMVIRATE_DECISION,
            AppealType.SUCCESSION_DISPUTE: ArbitrationLevel.SUPREME_ARBITRATION,
            AppealType.RESOURCE_CONFLICT: ArbitrationLevel.KEEPER_COUNCIL,
            AppealType.PROCEDURAL_OBJECTION: ArbitrationLevel.ELDER_TRIBUNAL
        }
        return levels.get(appeal_type, ArbitrationLevel.KEEPER_COUNCIL)
    
    def _assign_mediator(self, appeal_type: AppealType, appellant: str, respondent: str) -> str:
        """Assign appropriate mediator for the appeal"""
        # Simplified mediator assignment - in practice, this would be more sophisticated
        mediators = {
            AppealType.CONTRACT_BREACH: "Senior Keeper Magnus",
            AppealType.CEREMONIAL_DISPUTE: "Elder Theodora",
            AppealType.HONOR_VIOLATION: "Honor Guardian Lyra",
            AppealType.AUTHORITY_CHALLENGE: "Triumvirate Representative",
            AppealType.SUCCESSION_DISPUTE: "Succession Arbiter",
            AppealType.RESOURCE_CONFLICT: "Resource Mediator",
            AppealType.PROCEDURAL_OBJECTION: "Procedure Guardian"
        }
        return mediators.get(appeal_type, "General Mediator")
    
    def _determine_binding_authority(self, arbitration_level: ArbitrationLevel) -> str:
        """Determine binding authority for arbitration level"""
        authorities = {
            ArbitrationLevel.KEEPER_COUNCIL: "Keeper Council Binding Authority",
            ArbitrationLevel.ELDER_TRIBUNAL: "Elder Tribunal Supreme Authority",
            ArbitrationLevel.TRIUMVIRATE_DECISION: "Triumvirate Absolute Authority",
            ArbitrationLevel.SUPREME_ARBITRATION: "Supreme Ceremonial Authority"
        }
        return authorities.get(arbitration_level, "General Arbitration Authority")
    
    def _update_appeal_status(self, appeal_reference: str, new_status: AppealStatus):
        """Update the status of an appeal"""
        for appeal_file in self.appeals_path.glob("*.json"):
            with open(appeal_file, 'r') as f:
                appeal_data = json.load(f)
            
            if appeal_data.get('appeal_id') == appeal_reference:
                appeal_data['appeal_status'] = new_status.value
                appeal_data['status_update_date'] = datetime.now(timezone.utc).isoformat()
                
                with open(appeal_file, 'w') as f:
                    json.dump(appeal_data, f, indent=2)
                break
    
    def _store_sacred_contract(self, contract: SacredContract):
        """Store a sacred contract to persistent storage"""
        contract_dict = asdict(contract)
        
        # Convert enums to strings for JSON serialization
        contract_dict['contract_type'] = contract.contract_type.value
        contract_dict['contract_status'] = contract.contract_status.value
        
        contract_file = self.contracts_path / f"{contract.contract_id}.json"
        with open(contract_file, 'w') as f:
            json.dump(contract_dict, f, indent=2)
    
    def _store_ceremonial_appeal(self, appeal: CeremonialAppeal):
        """Store a ceremonial appeal to persistent storage"""
        appeal_dict = asdict(appeal)
        
        # Convert enums to strings for JSON serialization
        appeal_dict['appeal_type'] = appeal.appeal_type.value
        appeal_dict['appeal_status'] = appeal.appeal_status.value
        if appeal.arbitration_level:
            appeal_dict['arbitration_level'] = appeal.arbitration_level.value
        
        appeal_file = self.appeals_path / f"{appeal.appeal_id}.json"
        with open(appeal_file, 'w') as f:
            json.dump(appeal_dict, f, indent=2)
    
    def _store_arbitration_proceeding(self, arbitration: ArbitrationProceeding):
        """Store an arbitration proceeding to persistent storage"""
        arbitration_dict = asdict(arbitration)
        arbitration_dict['arbitration_level'] = arbitration.arbitration_level.value
        
        arbitration_file = self.arbitrations_path / f"{arbitration.arbitration_id}.json"
        with open(arbitration_file, 'w') as f:
            json.dump(arbitration_dict, f, indent=2)
    
    def _store_dispute_resolution(self, resolution: DisputeResolution):
        """Store a dispute resolution to persistent storage"""
        resolution_dict = asdict(resolution)
        
        resolution_file = self.resolutions_path / f"{resolution.resolution_id}.json"
        with open(resolution_file, 'w') as f:
            json.dump(resolution_dict, f, indent=2)
    
    def get_active_contracts(self, party_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active contracts, optionally filtered by party"""
        active_contracts = []
        
        for contract_file in self.contracts_path.glob("*.json"):
            with open(contract_file, 'r') as f:
                contract_data = json.load(f)
            
            if contract_data.get('contract_status') == 'active':
                if party_name is None:
                    active_contracts.append(contract_data)
                else:
                    # Check if party is involved in contract
                    parties = contract_data.get('parties', [])
                    if any(party.get('name') == party_name for party in parties):
                        active_contracts.append(contract_data)
        
        return active_contracts
    
    def get_pending_appeals(self, mediator: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get pending appeals, optionally filtered by assigned mediator"""
        pending_appeals = []
        
        for appeal_file in self.appeals_path.glob("*.json"):
            with open(appeal_file, 'r') as f:
                appeal_data = json.load(f)
            
            if appeal_data.get('appeal_status') in ['submitted', 'under_review', 'mediation']:
                if mediator is None or appeal_data.get('assigned_mediator') == mediator:
                    pending_appeals.append(appeal_data)
        
        return pending_appeals

# Factory function for easy contracts and appeals system creation
def create_contracts_appeals_system(storage_root: str = ".") -> ContractsAppealsSystem:
    """Factory function to create a configured contracts and appeals system"""
    return ContractsAppealsSystem(storage_root=storage_root)

# Example usage and ceremonial demonstration
if __name__ == "__main__":
    # Create contracts and appeals system
    system = create_contracts_appeals_system()
    
    # Example: Create sacred contract
    contract = system.create_sacred_contract(
        contract_name="Sacred Flame Custody Agreement",
        contract_type=ContractType.FLAME_CUSTODY,
        parties=[
            {"name": "Guardian Aurelius", "role": "Primary Custodian"},
            {"name": "Keeper Lyra", "role": "Secondary Custodian"},
            {"name": "Elder Council", "role": "Oversight Authority"}
        ],
        contract_terms=[
            "Daily flame tending and maintenance",
            "Emergency response protocols",
            "Sacred fuel management",
            "Ceremonial flame lighting duties"
        ],
        obligations={
            "Guardian Aurelius": ["Primary daily tending", "Training supervision", "Emergency response"],
            "Keeper Lyra": ["Secondary tending", "Backup coverage", "Ceremonial assistance"],
            "Elder Council": ["Oversight supervision", "Resource provision", "Ceremonial validation"]
        },
        ceremonial_conditions=[
            "Sacred oath of flame protection",
            "Ceremonial blessing required",
            "Monthly flame blessing ceremony"
        ],
        effective_date=datetime.now(timezone.utc).isoformat(),
        expiration_date=(datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
        witness_names=["Elder Maximus", "Master Theron"]
    )
    
    print(f"Sacred Contract Created: {contract.contract_name}")
    print(f"Contract ID: {contract.contract_id}")
    print(f"Sacred Binding: {contract.sacred_binding}")
    print(f"Enforcement Authority: {contract.enforcement_authority}")
    
    # Example: Submit ceremonial appeal
    appeal = system.submit_ceremonial_appeal(
        appeal_type=AppealType.CONTRACT_BREACH,
        appellant_name="Keeper Lyra",
        respondent_name="Guardian Aurelius",
        appeal_subject="Alleged breach of daily flame tending obligations",
        appeal_description="The appellant alleges that the respondent has failed to maintain consistent daily flame tending as required by the custody agreement.",
        supporting_evidence=[
            "Flame monitoring logs showing irregular tending",
            "Witness testimony from chamber visitors",
            "Photographic evidence of dimmed flames"
        ],
        ceremonial_basis=[
            "Sacred flame custody agreement violation",
            "Breach of ceremonial duty",
            "Endangerment of sacred flame continuity"
        ],
        witness_statements=[
            {"witness": "Scribe Theodora", "statement": "Observed irregular flame brightness on multiple occasions"},
            {"witness": "Initiate Marcus", "statement": "Witnessed delayed morning flame tending procedures"}
        ]
    )
    
    print(f"Ceremonial Appeal Submitted: {appeal.appeal_subject}")
    print(f"Appeal ID: {appeal.appeal_id}")
    print(f"Assigned Mediator: {appeal.assigned_mediator}")
    print(f"Arbitration Level: {appeal.arbitration_level.value if appeal.arbitration_level else 'None'}")
    
    # Example: Conduct arbitration
    arbitration = system.conduct_arbitration(
        appeal_reference=appeal.appeal_id,
        arbitration_level=ArbitrationLevel.KEEPER_COUNCIL,
        arbitration_panel=["Senior Keeper Magnus", "Elder Theodora", "Master Theron"],
        testimonies=[
            {"party": "Keeper Lyra", "testimony": "Detailed account of observed violations"},
            {"party": "Guardian Aurelius", "testimony": "Explanation of circumstances and remedial actions"}
        ],
        evidence_review=[
            "Flame monitoring logs analysis",
            "Witness testimony evaluation",
            "Contractual obligations review"
        ],
        deliberation_notes="Panel found evidence of minor procedural lapses but no intentional negligence",
        arbitration_decision="Minor contract modification with additional oversight",
        decision_rationale="Respondent showed good faith efforts with room for improvement",
        enforcement_measures=[
            "Additional training requirement",
            "Weekly oversight meetings",
            "Probationary period of 90 days"
        ]
    )
    
    print(f"Arbitration Conducted: {arbitration.arbitration_id}")
    print(f"Decision: {arbitration.arbitration_decision}")
    print(f"Binding Authority: {arbitration.binding_authority}")
    
    # Example: Get active contracts
    active_contracts = system.get_active_contracts("Guardian Aurelius")
    print(f"Active Contracts for Guardian Aurelius: {len(active_contracts)}")
    
    # Example: Get pending appeals
    pending_appeals = system.get_pending_appeals("Senior Keeper Magnus")
    print(f"Pending Appeals for Senior Keeper Magnus: {len(pending_appeals)}")