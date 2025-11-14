"""
Flamekeeper Scroll - Sacred flame tracking and temporal management
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

class TemporalTier(Enum):
    INSTANT = "instant"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SEASONAL = "seasonal"
    YEARLY = "yearly"
    ETERNAL = "eternal"

class FlameState(Enum):
    DORMANT = "dormant"
    KINDLING = "kindling"
    BURNING = "burning"
    BLAZING = "blazing"
    ETERNAL = "eternal"

@dataclass
class FlameRecord:
    record_id: str
    keeper_name: str
    flame_name: str
    state: FlameState
    tier: TemporalTier
    ignited_at: datetime
    last_tended: datetime
    next_tending: Optional[datetime]
    sacred_words: Optional[str]
    lineage_data: Dict[str, Any]

class FlamekeeperScrollManager:
    def __init__(self, scroll_path: Optional[str] = None):
        self.scroll_path = scroll_path or "flamekeeper_scroll.json"
        self.flame_records: Dict[str, FlameRecord] = {}
        self.keeper_lineages: Dict[str, List[str]] = {}
        
    def inscribe_flame(self, keeper_name: str, flame_name: str, tier: TemporalTier,
                      sacred_words: Optional[str] = None,
                      lineage_data: Optional[Dict[str, Any]] = None) -> str:
        record_id = f"FK-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(self.flame_records)+1:03d}"
        
        record = FlameRecord(
            record_id=record_id,
            keeper_name=keeper_name,
            flame_name=flame_name,
            state=FlameState.KINDLING,
            tier=tier,
            ignited_at=datetime.now(),
            last_tended=datetime.now(),
            next_tending=self._calculate_next_tending(tier),
            sacred_words=sacred_words,
            lineage_data=lineage_data or {}
        )
        
        self.flame_records[record_id] = record
        
        # Add to keeper's lineage
        if keeper_name not in self.keeper_lineages:
            self.keeper_lineages[keeper_name] = []
        self.keeper_lineages[keeper_name].append(record_id)
        
        return record_id
        
    def tend_flame(self, record_id: str, tender_name: str, 
                  sacred_words: Optional[str] = None) -> bool:
        if record_id not in self.flame_records:
            return False
            
        record = self.flame_records[record_id]
        record.last_tended = datetime.now()
        record.next_tending = self._calculate_next_tending(record.tier)
        
        if sacred_words:
            record.sacred_words = sacred_words
            
        # Advance flame state if tended regularly
        if record.state != FlameState.ETERNAL:
            self._advance_flame_state(record)
            
        # Update lineage
        record.lineage_data.setdefault('tended_by', []).append({
            'tender': tender_name,
            'tended_at': datetime.now().isoformat(),
            'words': sacred_words
        })
        
        return True
        
    def _calculate_next_tending(self, tier: TemporalTier) -> datetime:
        base_time = datetime.now()
        
        tending_intervals = {
            TemporalTier.INSTANT: timedelta(seconds=1),
            TemporalTier.HOURLY: timedelta(hours=1),
            TemporalTier.DAILY: timedelta(days=1),
            TemporalTier.WEEKLY: timedelta(weeks=1),
            TemporalTier.MONTHLY: timedelta(days=30),
            TemporalTier.SEASONAL: timedelta(days=90),
            TemporalTier.YEARLY: timedelta(days=365),
            TemporalTier.ETERNAL: timedelta(days=365*1000)  # Effectively never
        }
        
        return base_time + tending_intervals.get(tier, timedelta(days=1))
        
    def _advance_flame_state(self, record: FlameRecord):
        state_progression = {
            FlameState.DORMANT: FlameState.KINDLING,
            FlameState.KINDLING: FlameState.BURNING,
            FlameState.BURNING: FlameState.BLAZING,
            FlameState.BLAZING: FlameState.ETERNAL
        }
        
        if record.state in state_progression:
            record.state = state_progression[record.state]
            
    def extinguish_flame(self, record_id: str, extinguisher_name: str, reason: str = "") -> bool:
        if record_id not in self.flame_records:
            return False
            
        record = self.flame_records[record_id]
        record.state = FlameState.DORMANT
        record.lineage_data['extinguished_by'] = extinguisher_name
        record.lineage_data['extinguished_at'] = datetime.now().isoformat()
        record.lineage_data['extinguishment_reason'] = reason
        
        return True
        
    def get_flames_needing_tending(self, keeper_name: Optional[str] = None) -> List[FlameRecord]:
        now = datetime.now()
        needing_tending = []
        
        for record in self.flame_records.values():
            if record.state == FlameState.DORMANT:
                continue
                
            if keeper_name and record.keeper_name != keeper_name:
                continue
                
            if record.next_tending and record.next_tending <= now:
                needing_tending.append(record)
                
        return sorted(needing_tending, key=lambda r: r.next_tending or datetime.min)
        
    def get_keeper_flames(self, keeper_name: str) -> List[FlameRecord]:
        if keeper_name not in self.keeper_lineages:
            return []
            
        return [self.flame_records[rid] for rid in self.keeper_lineages[keeper_name]
                if rid in self.flame_records]
        
    def get_flame_status(self, record_id: str) -> Optional[Dict[str, Any]]:
        if record_id not in self.flame_records:
            return None
            
        record = self.flame_records[record_id]
        
        return {
            "record_id": record_id,
            "keeper_name": record.keeper_name,
            "flame_name": record.flame_name,
            "state": record.state.value,
            "tier": record.tier.value,
            "ignited_at": record.ignited_at.isoformat(),
            "last_tended": record.last_tended.isoformat(),
            "next_tending": record.next_tending.isoformat() if record.next_tending else None,
            "sacred_words": record.sacred_words,
            "lineage_count": len(record.lineage_data.get('tended_by', []))
        }