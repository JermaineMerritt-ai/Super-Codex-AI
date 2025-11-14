"""
Eternal Recognition Scrolls - Honor and recognition system
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime
import json

class RecognitionType(Enum):
    FLAME_KEEPER = "flame_keeper"
    COUNCIL_MEMBER = "council_member"
    CUSTODIAN = "custodian"
    SOVEREIGN = "sovereign"
    CONTRIBUTOR = "contributor"

class ScrollStatus(Enum):
    DRAFT = "draft"
    SEALED = "sealed"
    ETERNAL = "eternal"
    ARCHIVED = "archived"

@dataclass
class RecognitionScroll:
    scroll_id: str
    recipient_name: str
    recognition_type: RecognitionType
    granting_authority: str
    scroll_date: datetime
    status: ScrollStatus
    sacred_deeds: List[str]
    ceremonial_data: Dict[str, Any]
    lineage_chain: List[str]

class EternalRecognitionScrolls:
    def __init__(self):
        self.scrolls: Dict[str, RecognitionScroll] = {}
        self.recipient_index: Dict[str, List[str]] = {}
        
    def inscribe_scroll(self, recipient_name: str, recognition_type: RecognitionType,
                       granting_authority: str, sacred_deeds: List[str],
                       ceremonial_data: Optional[Dict[str, Any]] = None,
                       lineage_chain: Optional[List[str]] = None) -> str:
        scroll_id = f"ERS-{datetime.now().strftime('%Y%m%d')}-{len(self.scrolls)+1:04d}"
        
        scroll = RecognitionScroll(
            scroll_id=scroll_id,
            recipient_name=recipient_name,
            recognition_type=recognition_type,
            granting_authority=granting_authority,
            scroll_date=datetime.now(),
            status=ScrollStatus.DRAFT,
            sacred_deeds=sacred_deeds,
            ceremonial_data=ceremonial_data or {},
            lineage_chain=lineage_chain or []
        )
        
        self.scrolls[scroll_id] = scroll
        
        # Add to recipient index
        if recipient_name not in self.recipient_index:
            self.recipient_index[recipient_name] = []
        self.recipient_index[recipient_name].append(scroll_id)
        
        return scroll_id
        
    def seal_scroll(self, scroll_id: str, sealing_authority: str) -> bool:
        if scroll_id not in self.scrolls:
            return False
            
        scroll = self.scrolls[scroll_id]
        scroll.status = ScrollStatus.SEALED
        scroll.ceremonial_data['sealed_by'] = sealing_authority
        scroll.ceremonial_data['sealed_at'] = datetime.now().isoformat()
        
        return True
        
    def eternalize_scroll(self, scroll_id: str, eternal_authority: str) -> bool:
        if scroll_id not in self.scrolls:
            return False
            
        scroll = self.scrolls[scroll_id]
        if scroll.status != ScrollStatus.SEALED:
            return False
            
        scroll.status = ScrollStatus.ETERNAL
        scroll.ceremonial_data['eternalized_by'] = eternal_authority
        scroll.ceremonial_data['eternalized_at'] = datetime.now().isoformat()
        
        return True
        
    def get_scroll(self, scroll_id: str) -> Optional[RecognitionScroll]:
        return self.scrolls.get(scroll_id)
        
    def get_recipient_scrolls(self, recipient_name: str) -> List[RecognitionScroll]:
        if recipient_name not in self.recipient_index:
            return []
            
        return [self.scrolls[sid] for sid in self.recipient_index[recipient_name]
                if sid in self.scrolls]
        
    def list_scrolls_by_type(self, recognition_type: RecognitionType) -> List[RecognitionScroll]:
        return [s for s in self.scrolls.values() if s.recognition_type == recognition_type]
        
    def export_scroll_data(self, scroll_id: str) -> Optional[Dict[str, Any]]:
        if scroll_id not in self.scrolls:
            return None
            
        scroll = self.scrolls[scroll_id]
        data = asdict(scroll)
        data['scroll_date'] = scroll.scroll_date.isoformat()
        data['recognition_type'] = scroll.recognition_type.value
        data['status'] = scroll.status.value
        
        return data