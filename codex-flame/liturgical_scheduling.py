"""
Liturgical Scheduling Module - Sacred Ceremony Management System
==================================================================

This module implements the liturgical scheduling system for managing sacred ceremonies,
ritual timings, ceremonial calendars, and the coordination of sacred observances within
the ceremonial flame architecture.

The liturgical scheduling system ensures that:
1. Sacred ceremonies are properly scheduled and coordinated
2. Ceremonial participants are notified and prepared
3. Sacred timings align with astronomical and traditional observances
4. Ritual resources and sacred spaces are allocated appropriately
"""

import json
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

# Liturgical scheduling storage paths
CEREMONIES_SCHEDULE_PATH = "codex-flame/storage/liturgy/ceremonies"
RITUAL_CALENDAR_PATH = "codex-flame/storage/liturgy/calendar"
SACRED_OBSERVANCES_PATH = "codex-flame/storage/liturgy/observances"
CEREMONIAL_RESOURCES_PATH = "codex-flame/storage/liturgy/resources"

class CeremonyType(Enum):
    """Types of sacred ceremonies"""
    DAILY_FLAME_TENDING = "daily_flame_tending"
    WEEKLY_CONCORD = "weekly_concord"
    MONTHLY_RENEWAL = "monthly_renewal"
    SEASONAL_CELEBRATION = "seasonal_celebration"
    ANNUAL_GATHERING = "annual_gathering"
    HONOR_BESTOWMENT = "honor_bestowment"
    FLAME_BLESSING = "flame_blessing"
    SACRED_INITIATION = "sacred_initiation"
    WISDOM_SHARING = "wisdom_sharing"
    ETERNAL_COMMEMORATION = "eternal_commemoration"

class CeremonyPriority(Enum):
    """Priority levels for ceremonies"""
    ROUTINE = "routine"
    IMPORTANT = "important"
    SACRED = "sacred"
    CRITICAL = "critical"
    ETERNAL = "eternal"

class ParticipantRole(Enum):
    """Roles for ceremony participants"""
    PRESIDER = "presider"
    CELEBRANT = "celebrant"
    FLAME_KEEPER = "flame_keeper"
    WITNESS = "witness"
    PARTICIPANT = "participant"
    GUARDIAN = "guardian"
    SCRIBE = "scribe"

class CeremonyStatus(Enum):
    """Status of scheduled ceremonies"""
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    PREPARED = "prepared"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"

@dataclass
class CeremonySchedule:
    """Represents a scheduled ceremony"""
    ceremony_id: str
    ceremony_name: str
    ceremony_type: CeremonyType
    scheduled_datetime: str
    duration_minutes: int
    location: str
    presider: str
    participants: List[Dict[str, str]]  # [{"name": str, "role": ParticipantRole.value}]
    required_resources: List[str]
    sacred_preparations: List[str]
    ceremony_purpose: str
    priority: CeremonyPriority
    status: CeremonyStatus
    ceremonial_notes: str
    notification_schedule: Dict[str, str]
    metadata: Dict[str, Any]

@dataclass
class SacredObservance:
    """Represents a recurring sacred observance"""
    observance_id: str
    observance_name: str
    observance_type: str
    recurrence_pattern: str  # daily, weekly, monthly, annual, astronomical
    base_datetime: str
    duration_minutes: int
    ceremonial_authority: str
    traditional_preparations: List[str]
    sacred_significance: str
    participants_criteria: Dict[str, Any]
    resource_requirements: List[str]
    observance_metadata: Dict[str, Any]

@dataclass
class CeremonialResource:
    """Represents a ceremonial resource for liturgical use"""
    resource_id: str
    resource_name: str
    resource_type: str
    location: str
    availability_schedule: Dict[str, Any]
    required_preparations: List[str]
    ceremonial_restrictions: List[str]
    custodian: str
    resource_status: str
    metadata: Dict[str, Any]

class LiturgicalScheduler:
    """Main class for managing liturgical scheduling and sacred ceremony coordination"""
    
    def __init__(self, storage_root: str = "."):
        """Initialize the liturgical scheduling system"""
        self.storage_root = Path(storage_root)
        self.ceremonies_path = self.storage_root / CEREMONIES_SCHEDULE_PATH
        self.calendar_path = self.storage_root / RITUAL_CALENDAR_PATH
        self.observances_path = self.storage_root / SACRED_OBSERVANCES_PATH
        self.resources_path = self.storage_root / CEREMONIAL_RESOURCES_PATH
        
        # Ensure storage directories exist
        self._ensure_storage_directories()
        
    def _ensure_storage_directories(self):
        """Create necessary storage directories for liturgical scheduling"""
        for path in [self.ceremonies_path, self.calendar_path, self.observances_path, self.resources_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def _generate_ceremony_id(self, ceremony_name: str, scheduled_datetime: str) -> str:
        """Generate a unique ceremony identifier"""
        import hashlib
        content = f"{ceremony_name}:{scheduled_datetime}"
        return f"LIT-{datetime.now().strftime('%Y-%m-%d')}-{hashlib.sha256(content.encode()).hexdigest()[:8]}"
    
    def _calculate_notification_schedule(self, scheduled_datetime: str, priority: CeremonyPriority) -> Dict[str, str]:
        """Calculate notification schedule based on ceremony priority"""
        scheduled_dt = datetime.fromisoformat(scheduled_datetime.replace('Z', '+00:00'))
        
        notification_schedules = {
            CeremonyPriority.ETERNAL: {
                "advance_notice": (scheduled_dt - timedelta(days=7)).isoformat(),
                "reminder": (scheduled_dt - timedelta(days=1)).isoformat(),
                "final_call": (scheduled_dt - timedelta(hours=2)).isoformat()
            },
            CeremonyPriority.CRITICAL: {
                "advance_notice": (scheduled_dt - timedelta(days=3)).isoformat(),
                "reminder": (scheduled_dt - timedelta(hours=12)).isoformat(),
                "final_call": (scheduled_dt - timedelta(hours=1)).isoformat()
            },
            CeremonyPriority.SACRED: {
                "advance_notice": (scheduled_dt - timedelta(days=1)).isoformat(),
                "reminder": (scheduled_dt - timedelta(hours=4)).isoformat(),
                "final_call": (scheduled_dt - timedelta(minutes=30)).isoformat()
            },
            CeremonyPriority.IMPORTANT: {
                "reminder": (scheduled_dt - timedelta(hours=2)).isoformat(),
                "final_call": (scheduled_dt - timedelta(minutes=15)).isoformat()
            },
            CeremonyPriority.ROUTINE: {
                "reminder": (scheduled_dt - timedelta(hours=1)).isoformat()
            }
        }
        
        return notification_schedules.get(priority, notification_schedules[CeremonyPriority.ROUTINE])
    
    def schedule_ceremony(self,
                        ceremony_name: str,
                        ceremony_type: CeremonyType,
                        scheduled_datetime: str,
                        duration_minutes: int,
                        location: str,
                        presider: str,
                        participants: List[Dict[str, str]],
                        ceremony_purpose: str,
                        priority: CeremonyPriority = CeremonyPriority.IMPORTANT,
                        required_resources: Optional[List[str]] = None,
                        sacred_preparations: Optional[List[str]] = None,
                        ceremonial_notes: str = "") -> CeremonySchedule:
        """Schedule a sacred ceremony"""
        
        ceremony_id = self._generate_ceremony_id(ceremony_name, scheduled_datetime)
        notification_schedule = self._calculate_notification_schedule(scheduled_datetime, priority)
        
        # Create ceremony schedule
        ceremony = CeremonySchedule(
            ceremony_id=ceremony_id,
            ceremony_name=ceremony_name,
            ceremony_type=ceremony_type,
            scheduled_datetime=scheduled_datetime,
            duration_minutes=duration_minutes,
            location=location,
            presider=presider,
            participants=participants,
            required_resources=required_resources or [],
            sacred_preparations=sacred_preparations or [],
            ceremony_purpose=ceremony_purpose,
            priority=priority,
            status=CeremonyStatus.PLANNED,
            ceremonial_notes=ceremonial_notes,
            notification_schedule=notification_schedule,
            metadata={
                "scheduling_authority": presider,
                "ceremonial_coordination": "liturgical_scheduler",
                "sacred_protocol": "traditional_ceremony_ordering"
            }
        )
        
        # Store ceremony schedule
        self._store_ceremony_schedule(ceremony)
        
        # Check for resource conflicts
        conflicts = self._check_resource_conflicts(ceremony)
        if conflicts:
            ceremony.metadata["resource_conflicts"] = conflicts
        
        return ceremony
    
    def establish_sacred_observance(self,
                                  observance_name: str,
                                  observance_type: str,
                                  recurrence_pattern: str,
                                  base_datetime: str,
                                  duration_minutes: int,
                                  ceremonial_authority: str,
                                  sacred_significance: str,
                                  traditional_preparations: Optional[List[str]] = None,
                                  resource_requirements: Optional[List[str]] = None) -> SacredObservance:
        """Establish a recurring sacred observance"""
        
        observance_id = f"SO-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Create sacred observance
        observance = SacredObservance(
            observance_id=observance_id,
            observance_name=observance_name,
            observance_type=observance_type,
            recurrence_pattern=recurrence_pattern,
            base_datetime=base_datetime,
            duration_minutes=duration_minutes,
            ceremonial_authority=ceremonial_authority,
            traditional_preparations=traditional_preparations or [],
            sacred_significance=sacred_significance,
            participants_criteria={
                "required_roles": ["presider", "flame_keeper"],
                "minimum_participants": 3,
                "sacred_qualifications": ["ceremonial_training"]
            },
            resource_requirements=resource_requirements or [],
            observance_metadata={
                "establishment_date": datetime.now(timezone.utc).isoformat(),
                "ceremonial_tradition": "eternal_flame_observance",
                "sacred_authority": ceremonial_authority
            }
        )
        
        # Store sacred observance
        self._store_sacred_observance(observance)
        
        return observance
    
    def register_ceremonial_resource(self,
                                   resource_name: str,
                                   resource_type: str,
                                   location: str,
                                   custodian: str,
                                   availability_schedule: Dict[str, Any],
                                   ceremonial_restrictions: Optional[List[str]] = None) -> CeremonialResource:
        """Register a ceremonial resource for liturgical use"""
        
        resource_id = f"CR-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}"
        
        # Create ceremonial resource
        resource = CeremonialResource(
            resource_id=resource_id,
            resource_name=resource_name,
            resource_type=resource_type,
            location=location,
            availability_schedule=availability_schedule,
            required_preparations=[],
            ceremonial_restrictions=ceremonial_restrictions or [],
            custodian=custodian,
            resource_status="available",
            metadata={
                "registration_date": datetime.now(timezone.utc).isoformat(),
                "ceremonial_authority": custodian,
                "sacred_designation": "liturgical_resource"
            }
        )
        
        # Store ceremonial resource
        self._store_ceremonial_resource(resource)
        
        return resource
    
    def generate_ceremonial_calendar(self,
                                   start_date: str,
                                   end_date: str,
                                   include_observances: bool = True) -> Dict[str, Any]:
        """Generate a ceremonial calendar for a specified date range"""
        
        calendar_data = {
            "calendar_id": f"CAL-{datetime.now().strftime('%Y-%m-%d')}-{os.urandom(4).hex().upper()}",
            "date_range": {"start": start_date, "end": end_date},
            "ceremonies": [],
            "sacred_observances": [],
            "resource_allocations": {},
            "ceremonial_conflicts": [],
            "lunar_phases": self._calculate_lunar_phases(start_date, end_date),
            "metadata": {
                "generation_timestamp": datetime.now(timezone.utc).isoformat(),
                "calendar_authority": "liturgical_scheduler",
                "sacred_coordination": "ceremonial_calendar_system"
            }
        }
        
        # Load scheduled ceremonies within date range
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        for ceremony_file in self.ceremonies_path.glob("*.json"):
            with open(ceremony_file, 'r') as f:
                ceremony_data = json.load(f)
            
            ceremony_dt = datetime.fromisoformat(ceremony_data['scheduled_datetime'].replace('Z', '+00:00'))
            if start_dt <= ceremony_dt <= end_dt:
                calendar_data["ceremonies"].append(ceremony_data)
        
        # Include recurring observances if requested
        if include_observances:
            calendar_data["sacred_observances"] = self._generate_observance_instances(start_date, end_date)
        
        # Store calendar
        calendar_file = self.calendar_path / f"{calendar_data['calendar_id']}.json"
        with open(calendar_file, 'w') as f:
            json.dump(calendar_data, f, indent=2)
        
        return calendar_data
    
    def _calculate_lunar_phases(self, start_date: str, end_date: str) -> List[Dict[str, str]]:
        """Calculate lunar phases for ceremonial calendar (simplified implementation)"""
        # This is a simplified implementation. In practice, you would use an astronomy library
        lunar_phases = []
        
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        current_date = start_dt
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        # Approximate lunar cycle (29.5 days)
        lunar_cycle_days = 29.5
        phase_names = ["New Moon", "First Quarter", "Full Moon", "Last Quarter"]
        
        while current_date <= end_dt:
            for i, phase_name in enumerate(phase_names):
                phase_date = current_date + timedelta(days=i * lunar_cycle_days / 4)
                if phase_date <= end_dt:
                    lunar_phases.append({
                        "phase": phase_name,
                        "date": phase_date.isoformat(),
                        "ceremonial_significance": self._get_phase_significance(phase_name)
                    })
            
            current_date += timedelta(days=lunar_cycle_days)
        
        return lunar_phases
    
    def _get_phase_significance(self, phase_name: str) -> str:
        """Get ceremonial significance of lunar phases"""
        significances = {
            "New Moon": "Time for new beginnings and sacred intentions",
            "First Quarter": "Time for action and manifestation of sacred purposes",
            "Full Moon": "Time for celebration and peak ceremonial energy",
            "Last Quarter": "Time for reflection and release of old patterns"
        }
        return significances.get(phase_name, "Sacred lunar observance")
    
    def _generate_observance_instances(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Generate instances of recurring observances within date range"""
        observance_instances = []
        
        for observance_file in self.observances_path.glob("*.json"):
            with open(observance_file, 'r') as f:
                observance_data = json.load(f)
            
            instances = self._calculate_recurrence_instances(
                observance_data, start_date, end_date
            )
            observance_instances.extend(instances)
        
        return observance_instances
    
    def _calculate_recurrence_instances(self, observance_data: Dict[str, Any], start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Calculate specific instances of a recurring observance"""
        instances = []
        base_dt = datetime.fromisoformat(observance_data['base_datetime'].replace('Z', '+00:00'))
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        pattern = observance_data['recurrence_pattern']
        current_dt = max(base_dt, start_dt)
        
        while current_dt <= end_dt:
            instance = {
                "observance_id": observance_data['observance_id'],
                "observance_name": observance_data['observance_name'],
                "instance_datetime": current_dt.isoformat(),
                "duration_minutes": observance_data['duration_minutes'],
                "sacred_significance": observance_data['sacred_significance']
            }
            instances.append(instance)
            
            # Calculate next occurrence based on pattern
            if pattern == "daily":
                current_dt += timedelta(days=1)
            elif pattern == "weekly":
                current_dt += timedelta(weeks=1)
            elif pattern == "monthly":
                # Simplified monthly calculation
                if current_dt.month == 12:
                    current_dt = current_dt.replace(year=current_dt.year + 1, month=1)
                else:
                    current_dt = current_dt.replace(month=current_dt.month + 1)
            elif pattern == "annual":
                current_dt = current_dt.replace(year=current_dt.year + 1)
            else:
                break  # Unknown pattern, stop
        
        return instances
    
    def _check_resource_conflicts(self, ceremony: CeremonySchedule) -> List[str]:
        """Check for resource conflicts with scheduled ceremony"""
        conflicts = []
        
        ceremony_start = datetime.fromisoformat(ceremony.scheduled_datetime.replace('Z', '+00:00'))
        ceremony_end = ceremony_start + timedelta(minutes=ceremony.duration_minutes)
        
        # Check other ceremonies for resource conflicts
        for ceremony_file in self.ceremonies_path.glob("*.json"):
            with open(ceremony_file, 'r') as f:
                other_ceremony_data = json.load(f)
            
            if other_ceremony_data['ceremony_id'] == ceremony.ceremony_id:
                continue  # Skip self
            
            other_start = datetime.fromisoformat(other_ceremony_data['scheduled_datetime'].replace('Z', '+00:00'))
            other_end = other_start + timedelta(minutes=other_ceremony_data['duration_minutes'])
            
            # Check for time overlap
            if (ceremony_start < other_end and ceremony_end > other_start):
                # Check for resource conflicts
                common_resources = set(ceremony.required_resources) & set(other_ceremony_data.get('required_resources', []))
                if common_resources:
                    conflicts.append(f"Resource conflict with ceremony {other_ceremony_data['ceremony_id']}: {list(common_resources)}")
        
        return conflicts
    
    def _store_ceremony_schedule(self, ceremony: CeremonySchedule):
        """Store a ceremony schedule to persistent storage"""
        ceremony_dict = asdict(ceremony)
        
        # Convert enums to strings for JSON serialization
        ceremony_dict['ceremony_type'] = ceremony.ceremony_type.value
        ceremony_dict['priority'] = ceremony.priority.value
        ceremony_dict['status'] = ceremony.status.value
        
        ceremony_file = self.ceremonies_path / f"{ceremony.ceremony_id}.json"
        with open(ceremony_file, 'w') as f:
            json.dump(ceremony_dict, f, indent=2)
    
    def _store_sacred_observance(self, observance: SacredObservance):
        """Store a sacred observance to persistent storage"""
        observance_dict = asdict(observance)
        
        observance_file = self.observances_path / f"{observance.observance_id}.json"
        with open(observance_file, 'w') as f:
            json.dump(observance_dict, f, indent=2)
    
    def _store_ceremonial_resource(self, resource: CeremonialResource):
        """Store a ceremonial resource to persistent storage"""
        resource_dict = asdict(resource)
        
        resource_file = self.resources_path / f"{resource.resource_id}.json"
        with open(resource_file, 'w') as f:
            json.dump(resource_dict, f, indent=2)
    
    def get_upcoming_ceremonies(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming ceremonies within specified number of days"""
        upcoming = []
        current_time = datetime.now(timezone.utc)
        cutoff_time = current_time + timedelta(days=days_ahead)
        
        for ceremony_file in self.ceremonies_path.glob("*.json"):
            with open(ceremony_file, 'r') as f:
                ceremony_data = json.load(f)
            
            ceremony_time = datetime.fromisoformat(ceremony_data['scheduled_datetime'].replace('Z', '+00:00'))
            if current_time <= ceremony_time <= cutoff_time:
                upcoming.append(ceremony_data)
        
        # Sort by scheduled time
        upcoming.sort(key=lambda x: x['scheduled_datetime'])
        
        return upcoming

# Factory function for easy liturgical scheduler creation
def create_liturgical_scheduler(storage_root: str = ".") -> LiturgicalScheduler:
    """Factory function to create a configured liturgical scheduler"""
    return LiturgicalScheduler(storage_root=storage_root)

# Example usage and ceremonial demonstration
if __name__ == "__main__":
    # Create liturgical scheduler
    scheduler = create_liturgical_scheduler()
    
    # Example: Schedule a sacred ceremony
    sacred_ceremony = scheduler.schedule_ceremony(
        ceremony_name="Weekly Sacred Concord",
        ceremony_type=CeremonyType.WEEKLY_CONCORD,
        scheduled_datetime=(datetime.now(timezone.utc) + timedelta(days=3)).isoformat(),
        duration_minutes=120,
        location="Sacred Assembly Chamber",
        presider="Elder Maximus",
        participants=[
            {"name": "Keeper Lyra", "role": ParticipantRole.FLAME_KEEPER.value},
            {"name": "Guardian Aurelius", "role": ParticipantRole.GUARDIAN.value},
            {"name": "Scribe Theodora", "role": ParticipantRole.SCRIBE.value}
        ],
        ceremony_purpose="Weekly gathering for sacred discourse and flame tending coordination",
        priority=CeremonyPriority.SACRED,
        required_resources=["Sacred Assembly Chamber", "Ceremonial Flame", "Ancient Scrolls"],
        sacred_preparations=["Chamber purification", "Flame preparation", "Sacred text arrangement"]
    )
    
    print(f"Sacred Ceremony Scheduled: {sacred_ceremony.ceremony_name}")
    print(f"Ceremony ID: {sacred_ceremony.ceremony_id}")
    print(f"Scheduled: {sacred_ceremony.scheduled_datetime}")
    print(f"Priority: {sacred_ceremony.priority.value}")
    
    # Example: Establish sacred observance
    observance = scheduler.establish_sacred_observance(
        observance_name="Daily Flame Tending",
        observance_type="maintenance_ritual",
        recurrence_pattern="daily",
        base_datetime=datetime.now(timezone.utc).isoformat(),
        duration_minutes=45,
        ceremonial_authority="Master Keeper",
        sacred_significance="Daily maintenance and blessing of the eternal sacred flame",
        traditional_preparations=["Sacred oil preparation", "Chamber cleansing", "Meditative centering"],
        resource_requirements=["Eternal Flame Chamber", "Sacred Oils", "Ceremonial Tools"]
    )
    
    print(f"Sacred Observance Established: {observance.observance_name}")
    print(f"Observance ID: {observance.observance_id}")
    print(f"Recurrence: {observance.recurrence_pattern}")
    
    # Example: Generate ceremonial calendar
    calendar = scheduler.generate_ceremonial_calendar(
        start_date=datetime.now(timezone.utc).isoformat(),
        end_date=(datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        include_observances=True
    )
    
    print(f"Ceremonial Calendar Generated: {calendar['calendar_id']}")
    print(f"Date Range: {calendar['date_range']['start']} to {calendar['date_range']['end']}")
    print(f"Scheduled Ceremonies: {len(calendar['ceremonies'])}")
    print(f"Sacred Observances: {len(calendar['sacred_observances'])}")
    print(f"Lunar Phases: {len(calendar['lunar_phases'])}")