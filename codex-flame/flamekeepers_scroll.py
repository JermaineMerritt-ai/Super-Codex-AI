"""
Flamekeepers Scroll Module - Sacred Flame Custodian System
============================================================

This module implements the Flamekeepers Scroll system for managing sacred flame custodians,
their duties, ceremonial responsibilities, and the preservation of eternal flame knowledge.

The Flamekeepers Scroll serves as the authoritative record of flame custodian assignments,
flame monitoring protocols, and the sacred procedures for flame preservation within 
the ceremonial architecture.
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Flamekeepers storage paths
FLAMEKEEPERS_RECORDS_PATH = "codex-flame/storage/flamekeepers/records"
FLAME_MONITORING_PATH = "codex-flame/storage/flamekeepers/monitoring"
DUTY_ASSIGNMENTS_PATH = "codex-flame/storage/flamekeepers/duty-assignments"
SACRED_PROTOCOLS_PATH = "codex-flame/storage/flamekeepers/sacred-protocols"

class FlameKeeperRank(Enum):
    """Ranks within the flamekeeper hierarchy"""
    INITIATE_KEEPER = "initiate_keeper"
    APPRENTICE_KEEPER = "apprentice_keeper"
    GUARDIAN_KEEPER = "guardian_keeper"
    MASTER_KEEPER = "master_keeper"
    ELDER_KEEPER = "elder_keeper"
    ETERNAL_KEEPER = "eternal_keeper"

class FlameType(Enum):
    """Types of sacred flames under custodial care"""
    ETERNAL_FLAME = "eternal_flame"
    CEREMONIAL_FLAME = "ceremonial_flame"
    WISDOM_FLAME = "wisdom_flame"
    PROTECTION_FLAME = "protection_flame"
    DOMINION_FLAME = "dominion_flame"
    SACRED_HEARTH = "sacred_hearth"

class DutyType(Enum):
    """Types of flamekeeper duties"""
    FLAME_TENDING = "flame_tending"
    CEREMONIAL_LIGHTING = "ceremonial_lighting"
    SACRED_MONITORING = "sacred_monitoring"
    RITUAL_PREPARATION = "ritual_preparation"
    KNOWLEDGE_PRESERVATION = "knowledge_preservation"
    APPRENTICE_TRAINING = "apprentice_training"
    EMERGENCY_RESPONSE = "emergency_response"

class FlameStatus(Enum):
    """Status of sacred flames"""
    BURNING_BRIGHT = "burning_bright"
    STEADY_GLOW = "steady_glow"
    FLICKERING = "flickering"
    DIMMING = "dimming"
    CRITICAL = "critical"
    EXTINGUISHED = "extinguished"
    REKINDLED = "rekindled"

@dataclass
class FlameKeeper:
    """Represents a sacred flame custodian"""
    keeper_id: str
    keeper_name: str
    rank: FlameKeeperRank
    ordination_date: str
    assigned_flames: List[str]
    specializations: List[str]
    mentor: Optional[str]
    apprentices: List[str]
    ceremonial_authorities: List[str]
    sacred_oath: str
    keeper_seal: str
    status: str
    metadata: Dict[str, Any]

@dataclass
class FlameRecord:
    """Represents a sacred flame under custodial care"""
    flame_id: str
    flame_name: str
    flame_type: FlameType
    location: str
    primary_keeper: str
    secondary_keepers: List[str]
    ignition_date: str
    last_tending: str
    current_status: FlameStatus
    sacred_properties: Dict[str, Any]
    monitoring_schedule: Dict[str, Any]
    ceremonial_significance: str

@dataclass
class DutyAssignment:
    """Represents a duty assignment for flamekeepers"""
    assignment_id: str
    timestamp: str
    keeper_name: str
    duty_type: DutyType
    flame_reference: str
    scheduled_time: str
    duration_hours: float
    assignment_authority: str
    special_instructions: str
    completion_status: str
    completion_notes: Optional[str]

@dataclass
class FlameMonitoringReport:
    """Represents a flame monitoring report"""
    report_id: str
    timestamp: str
    flame_id: str
    reporting_keeper: str
    flame_status: FlameStatus
    flame_intensity: float
    fuel_level: float
    environmental_conditions: Dict[str, Any]
    observations: str
    maintenance_actions: List[str]
    next_check_scheduled: str
    ceremonial_notes: str

class FlameKeepersScroll:
    """Main class for managing flamekeepers and sacred flame custodial duties"""
    
    def __init__(self, storage_root: str = "."):
        """Initialize the flamekeepers scroll system"""
        self.storage_root = Path(storage_root)
        self.records_path = self.storage_root / FLAMEKEEPERS_RECORDS_PATH
        self.monitoring_path = self.storage_root / FLAME_MONITORING_PATH
        self.assignments_path = self.storage_root / DUTY_ASSIGNMENTS_PATH
        self.protocols_path = self.storage_root / SACRED_PROTOCOLS_PATH
        
        # Ensure storage directories exist
        self._ensure_storage_directories()
        
    def _ensure_storage_directories(self):
        """Create necessary storage directories for flamekeepers"""
        for path in [self.records_path, self.monitoring_path, self.assignments_path, self.protocols_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _generate_keeper_seal(self, keeper_data: Dict[str, Any]) -> str:
        """Generate a sacred seal for a flamekeeper"""
        import hashlib
        content = json.dumps(keeper_data, sort_keys=True)
        return f"FK-{hashlib.sha256(content.encode()).hexdigest()[:16].upper()}"
    
    def _generate_flame_id(self, flame_name: str, flame_type: FlameType) -> str:
        """Generate a unique identifier for a sacred flame"""
        import hashlib
        content = f"{flame_name}:{flame_type.value}:{datetime.now().isoformat()}"
        return f"SF-{hashlib.sha256(content.encode()).hexdigest()[:12].upper()}"
    
    def ordain_flame_keeper(self,
                          keeper_name: str,
                          rank: FlameKeeperRank,
                          specializations: List[str],
                          mentor: Optional[str] = None,
                          ceremonial_authorities: Optional[List[str]] = None) -> FlameKeeper:
        """Ordain a new flame keeper with sacred duties"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        keeper_id = f"FKP-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Generate sacred oath based on rank
        sacred_oath = self._generate_sacred_oath(rank)
        
        # Generate keeper seal
        seal_data = {
            "keeper_id": keeper_id,
            "name": keeper_name,
            "rank": rank.value,
            "ordination_date": timestamp
        }
        keeper_seal = self._generate_keeper_seal(seal_data)
        
        # Create flame keeper record
        keeper = FlameKeeper(
            keeper_id=keeper_id,
            keeper_name=keeper_name,
            rank=rank,
            ordination_date=timestamp,
            assigned_flames=[],
            specializations=specializations,
            mentor=mentor,
            apprentices=[],
            ceremonial_authorities=ceremonial_authorities or [],
            sacred_oath=sacred_oath,
            keeper_seal=keeper_seal,
            status="active",
            metadata={
                "ordination_ceremony": "sacred_flame_custodial_rite",
                "ceremonial_witness": "Elder Council",
                "flame_keeper_covenant": "eternal_flame_preservation"
            }
        )
        
        # Store flame keeper record
        self._store_flame_keeper(keeper)
        
        return keeper
    
    def register_sacred_flame(self,
                            flame_name: str,
                            flame_type: FlameType,
                            location: str,
                            primary_keeper: str,
                            ceremonial_significance: str,
                            sacred_properties: Optional[Dict[str, Any]] = None) -> FlameRecord:
        """Register a new sacred flame under custodial care"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        flame_id = self._generate_flame_id(flame_name, flame_type)
        
        # Create flame record
        flame = FlameRecord(
            flame_id=flame_id,
            flame_name=flame_name,
            flame_type=flame_type,
            location=location,
            primary_keeper=primary_keeper,
            secondary_keepers=[],
            ignition_date=timestamp,
            last_tending=timestamp,
            current_status=FlameStatus.BURNING_BRIGHT,
            sacred_properties=sacred_properties or {},
            monitoring_schedule={
                "daily_checks": 3,
                "deep_inspection_frequency": "weekly",
                "ceremonial_renewal": "monthly"
            },
            ceremonial_significance=ceremonial_significance
        )
        
        # Store flame record
        self._store_flame_record(flame)
        
        # Assign flame to primary keeper
        self._assign_flame_to_keeper(primary_keeper, flame_id)
        
        return flame
    
    def assign_keeper_duty(self,
                         keeper_name: str,
                         duty_type: DutyType,
                         flame_reference: str,
                         scheduled_time: str,
                         duration_hours: float,
                         assignment_authority: str,
                         special_instructions: str = "") -> DutyAssignment:
        """Assign a duty to a flame keeper"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        assignment_id = f"DA-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Create duty assignment
        assignment = DutyAssignment(
            assignment_id=assignment_id,
            timestamp=timestamp,
            keeper_name=keeper_name,
            duty_type=duty_type,
            flame_reference=flame_reference,
            scheduled_time=scheduled_time,
            duration_hours=duration_hours,
            assignment_authority=assignment_authority,
            special_instructions=special_instructions,
            completion_status="assigned",
            completion_notes=None
        )
        
        # Store duty assignment
        self._store_duty_assignment(assignment)
        
        return assignment
    
    def submit_flame_monitoring_report(self,
                                     flame_id: str,
                                     reporting_keeper: str,
                                     flame_status: FlameStatus,
                                     flame_intensity: float,
                                     fuel_level: float,
                                     environmental_conditions: Dict[str, Any],
                                     observations: str,
                                     maintenance_actions: List[str]) -> FlameMonitoringReport:
        """Submit a flame monitoring report"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        report_id = f"FMR-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Calculate next check time based on flame status
        next_check = self._calculate_next_check_time(flame_status)
        
        # Create monitoring report
        report = FlameMonitoringReport(
            report_id=report_id,
            timestamp=timestamp,
            flame_id=flame_id,
            reporting_keeper=reporting_keeper,
            flame_status=flame_status,
            flame_intensity=flame_intensity,
            fuel_level=fuel_level,
            environmental_conditions=environmental_conditions,
            observations=observations,
            maintenance_actions=maintenance_actions,
            next_check_scheduled=next_check,
            ceremonial_notes=""
        )
        
        # Store monitoring report
        self._store_monitoring_report(report)
        
        # Update flame status
        self._update_flame_status(flame_id, flame_status, timestamp)
        
        return report
    
    def _generate_sacred_oath(self, rank: FlameKeeperRank) -> str:
        """Generate a sacred oath appropriate to the keeper's rank"""
        oaths = {
            FlameKeeperRank.INITIATE_KEEPER: "I solemnly pledge to tend the sacred flame with reverence and learn the ancient ways of custodial care.",
            FlameKeeperRank.APPRENTICE_KEEPER: "I vow to guard the sacred flames and uphold the traditions passed down through generations of keepers.",
            FlameKeeperRank.GUARDIAN_KEEPER: "I swear to protect the sacred flames from all threats and to guide those who would learn the keeper's path.",
            FlameKeeperRank.MASTER_KEEPER: "I covenant to preserve the eternal flames and to teach the sacred mysteries to worthy apprentices.",
            FlameKeeperRank.ELDER_KEEPER: "I bind myself to the eternal flame and pledge to safeguard the ancient knowledge for future generations.",
            FlameKeeperRank.ETERNAL_KEEPER: "I am one with the eternal flame, bound in sacred covenant to preserve its light for all eternity."
        }
        return oaths.get(rank, "I pledge to serve the sacred flames with honor and dedication.")
    
    def _calculate_next_check_time(self, flame_status: FlameStatus) -> str:
        """Calculate the next scheduled check time based on flame status"""
        now = datetime.now(timezone.utc)
        
        if flame_status == FlameStatus.CRITICAL:
            next_check = now + timedelta(hours=1)
        elif flame_status == FlameStatus.FLICKERING:
            next_check = now + timedelta(hours=4)
        elif flame_status == FlameStatus.DIMMING:
            next_check = now + timedelta(hours=8)
        elif flame_status == FlameStatus.STEADY_GLOW:
            next_check = now + timedelta(hours=12)
        else:  # BURNING_BRIGHT
            next_check = now + timedelta(hours=24)
        
        return next_check.isoformat()
    
    def _assign_flame_to_keeper(self, keeper_name: str, flame_id: str):
        """Assign a flame to a keeper's responsibility"""
        # Find and update the keeper's record
        for keeper_file in self.records_path.glob("FKP-*.json"):
            with open(keeper_file, 'r') as f:
                keeper_data = json.load(f)
            
            if keeper_data.get('keeper_name') == keeper_name:
                if flame_id not in keeper_data.get('assigned_flames', []):
                    keeper_data['assigned_flames'].append(flame_id)
                    
                    with open(keeper_file, 'w') as f:
                        json.dump(keeper_data, f, indent=2)
                break
    
    def _update_flame_status(self, flame_id: str, new_status: FlameStatus, timestamp: str):
        """Update the status of a sacred flame"""
        flame_file = None
        for file in self.records_path.glob(f"*{flame_id}*.json"):
            if flame_id in file.name:
                flame_file = file
                break
        
        if flame_file and flame_file.exists():
            with open(flame_file, 'r') as f:
                flame_data = json.load(f)
            
            flame_data['current_status'] = new_status.value
            flame_data['last_tending'] = timestamp
            
            with open(flame_file, 'w') as f:
                json.dump(flame_data, f, indent=2)
    
    def _store_flame_keeper(self, keeper: FlameKeeper):
        """Store a flame keeper record to persistent storage"""
        keeper_dict = asdict(keeper)
        keeper_dict['rank'] = keeper.rank.value
        
        keeper_file = self.records_path / f"{keeper.keeper_id}.json"
        with open(keeper_file, 'w') as f:
            json.dump(keeper_dict, f, indent=2)
    
    def _store_flame_record(self, flame: FlameRecord):
        """Store a flame record to persistent storage"""
        flame_dict = asdict(flame)
        flame_dict['flame_type'] = flame.flame_type.value
        flame_dict['current_status'] = flame.current_status.value
        
        flame_file = self.records_path / f"{flame.flame_id}.json"
        with open(flame_file, 'w') as f:
            json.dump(flame_dict, f, indent=2)
    
    def _store_duty_assignment(self, assignment: DutyAssignment):
        """Store a duty assignment to persistent storage"""
        assignment_dict = asdict(assignment)
        assignment_dict['duty_type'] = assignment.duty_type.value
        
        assignment_file = self.assignments_path / f"{assignment.assignment_id}.json"
        with open(assignment_file, 'w') as f:
            json.dump(assignment_dict, f, indent=2)
    
    def _store_monitoring_report(self, report: FlameMonitoringReport):
        """Store a monitoring report to persistent storage"""
        report_dict = asdict(report)
        report_dict['flame_status'] = report.flame_status.value
        
        report_file = self.monitoring_path / f"{report.report_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report_dict, f, indent=2)
    
    def get_keeper_duties(self, keeper_name: str, include_completed: bool = False) -> List[Dict[str, Any]]:
        """Get current duties assigned to a specific keeper"""
        duties = []
        
        for assignment_file in self.assignments_path.glob("*.json"):
            with open(assignment_file, 'r') as f:
                assignment_data = json.load(f)
            
            if assignment_data.get('keeper_name') == keeper_name:
                if include_completed or assignment_data.get('completion_status') != 'completed':
                    duties.append(assignment_data)
        
        return duties
    
    def get_flame_status_report(self, flame_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status report for flames (specific flame or all flames)"""
        flame_statuses = {}
        
        # Get flame records
        for flame_file in self.records_path.glob("SF-*.json"):
            with open(flame_file, 'r') as f:
                flame_data = json.load(f)
            
            current_flame_id = flame_data.get('flame_id')
            
            if flame_id is None or current_flame_id == flame_id:
                flame_statuses[current_flame_id] = {
                    "flame_name": flame_data.get('flame_name'),
                    "flame_type": flame_data.get('flame_type'),
                    "current_status": flame_data.get('current_status'),
                    "location": flame_data.get('location'),
                    "primary_keeper": flame_data.get('primary_keeper'),
                    "last_tending": flame_data.get('last_tending')
                }
        
        return flame_statuses

# Factory function for easy flamekeepers scroll creation
def create_flamekeepers_scroll(storage_root: str = ".") -> FlameKeepersScroll:
    """Factory function to create a configured flamekeepers scroll system"""
    return FlameKeepersScroll(storage_root=storage_root)

# Example usage and ceremonial demonstration
if __name__ == "__main__":
    # Create flamekeepers scroll system
    flamekeepers = create_flamekeepers_scroll()
    
    # Example: Ordain a new flame keeper
    new_keeper = flamekeepers.ordain_flame_keeper(
        keeper_name="Keeper Lyra",
        rank=FlameKeeperRank.GUARDIAN_KEEPER,
        specializations=["eternal_flame_tending", "ceremonial_lighting", "apprentice_training"],
        mentor="Master Aurelius",
        ceremonial_authorities=["ceremonial_flame_duties", "sacred_monitoring"]
    )
    
    print(f"Flame Keeper Ordained: {new_keeper.keeper_name}")
    print(f"Keeper ID: {new_keeper.keeper_id}")
    print(f"Sacred Seal: {new_keeper.keeper_seal}")
    print(f"Sacred Oath: {new_keeper.sacred_oath}")
    
    # Example: Register a sacred flame
    sacred_flame = flamekeepers.register_sacred_flame(
        flame_name="Eternal Wisdom Flame",
        flame_type=FlameType.WISDOM_FLAME,
        location="Sacred Chamber of Knowledge",
        primary_keeper="Keeper Lyra",
        ceremonial_significance="Sacred flame that illuminates the path to eternal wisdom and knowledge preservation.",
        sacred_properties={
            "flame_color": "golden_blue",
            "sacred_fuel": "wisdom_essence",
            "ceremonial_power": "knowledge_enhancement"
        }
    )
    
    print(f"Sacred Flame Registered: {sacred_flame.flame_name}")
    print(f"Flame ID: {sacred_flame.flame_id}")
    print(f"Ceremonial Significance: {sacred_flame.ceremonial_significance}")
    
    # Example: Assign keeper duty
    duty = flamekeepers.assign_keeper_duty(
        keeper_name="Keeper Lyra",
        duty_type=DutyType.FLAME_TENDING,
        flame_reference=sacred_flame.flame_id,
        scheduled_time=datetime.now(timezone.utc).isoformat(),
        duration_hours=4.0,
        assignment_authority="Master Aurelius",
        special_instructions="Monitor flame intensity and ensure sacred fuel levels remain adequate."
    )
    
    print(f"Duty Assigned: {duty.assignment_id}")
    print(f"Duty Type: {duty.duty_type.value}")
    print(f"Duration: {duty.duration_hours} hours")
    
    # Example: Submit monitoring report
    report = flamekeepers.submit_flame_monitoring_report(
        flame_id=sacred_flame.flame_id,
        reporting_keeper="Keeper Lyra",
        flame_status=FlameStatus.BURNING_BRIGHT,
        flame_intensity=0.85,
        fuel_level=0.92,
        environmental_conditions={
            "temperature": 22.5,
            "humidity": 0.35,
            "air_pressure": 1013.2
        },
        observations="Flame burns steadily with golden-blue radiance. Sacred fuel consumption within normal parameters.",
        maintenance_actions=["Sacred fuel replenishment", "Chamber ventilation check"]
    )
    
    print(f"Monitoring Report Submitted: {report.report_id}")
    print(f"Flame Status: {report.flame_status.value}")
    print(f"Next Check: {report.next_check_scheduled}")