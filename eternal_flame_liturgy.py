"""
Eternal Flame Liturgy - Ceremonial timing and flame management system
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib

class FlamePhase(Enum):
    IGNITION = "ignition"
    SUSTENANCE = "sustenance"
    RENEWAL = "renewal"
    ETERNAL = "eternal"

class TemporalRhythm(Enum):
    DAWN = "dawn"
    MIDDAY = "midday"
    DUSK = "dusk"
    MIDNIGHT = "midnight"

class FlameState(Enum):
    DORMANT = "dormant"
    KINDLING = "kindling"
    BURNING = "burning"
    BLAZING = "blazing"
    ETERNAL = "eternal"

@dataclass
class FlameCycle:
    cycle_id: str
    phase: FlamePhase
    rhythm: TemporalRhythm
    state: FlameState
    ignited_at: datetime
    duration: timedelta
    keeper: str
    ceremonial_data: Dict[str, Any]

class EternalFlameLiturgyManager:
    def __init__(self):
        self.active_cycles: Dict[str, FlameCycle] = {}
        self.flame_history: List[FlameCycle] = []
        self.keepers: Dict[str, List[str]] = {}
        
    def ignite_flame(self, keeper: str, phase: FlamePhase, 
                    rhythm: TemporalRhythm, duration: timedelta,
                    ceremonial_data: Optional[Dict[str, Any]] = None) -> str:
        cycle_id = f"FL-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.active_cycles)+1:03d}"
        
        cycle = FlameCycle(
            cycle_id=cycle_id,
            phase=phase,
            rhythm=rhythm,
            state=FlameState.KINDLING,
            ignited_at=datetime.now(),
            duration=duration,
            keeper=keeper,
            ceremonial_data=ceremonial_data or {}
        )
        
        self.active_cycles[cycle_id] = cycle
        
        # Add to keeper's flame list
        if keeper not in self.keepers:
            self.keepers[keeper] = []
        self.keepers[keeper].append(cycle_id)
        
        return cycle_id
        
    def sustain_flame(self, cycle_id: str, additional_duration: timedelta) -> bool:
        if cycle_id not in self.active_cycles:
            return False
            
        cycle = self.active_cycles[cycle_id]
        cycle.duration += additional_duration
        cycle.state = FlameState.BURNING
        
        return True
        
    def extinguish_flame(self, cycle_id: str, extinguisher: str) -> bool:
        if cycle_id not in self.active_cycles:
            return False
            
        cycle = self.active_cycles[cycle_id]
        cycle.state = FlameState.DORMANT
        cycle.ceremonial_data['extinguished_by'] = extinguisher
        cycle.ceremonial_data['extinguished_at'] = datetime.now().isoformat()
        
        # Move to history
        self.flame_history.append(cycle)
        del self.active_cycles[cycle_id]
        
        return True
        
    def get_active_flames(self, keeper: Optional[str] = None) -> List[FlameCycle]:
        cycles = list(self.active_cycles.values())
        if keeper:
            cycles = [c for c in cycles if c.keeper == keeper]
        return cycles
        
    def get_flame_status(self, cycle_id: str) -> Optional[Dict[str, Any]]:
        if cycle_id in self.active_cycles:
            cycle = self.active_cycles[cycle_id]
            elapsed = datetime.now() - cycle.ignited_at
            remaining = cycle.duration - elapsed
            
            return {
                "cycle_id": cycle_id,
                "phase": cycle.phase.value,
                "rhythm": cycle.rhythm.value,
                "state": cycle.state.value,
                "keeper": cycle.keeper,
                "ignited_at": cycle.ignited_at.isoformat(),
                "elapsed": str(elapsed),
                "remaining": str(remaining),
                "active": remaining.total_seconds() > 0
            }
        return None
        
    def advance_flame_state(self, cycle_id: str) -> bool:
        if cycle_id not in self.active_cycles:
            return False
            
        cycle = self.active_cycles[cycle_id]
        
        state_progression = {
            FlameState.DORMANT: FlameState.KINDLING,
            FlameState.KINDLING: FlameState.BURNING,
            FlameState.BURNING: FlameState.BLAZING,
            FlameState.BLAZING: FlameState.ETERNAL,
            FlameState.ETERNAL: FlameState.ETERNAL
        }
        
        if cycle.state in state_progression:
            cycle.state = state_progression[cycle.state]
            return True
            
        return False