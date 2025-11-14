# Flame Engine - Transformation and purification system
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import random

from ..core.config import CodexConfig
from ..core.utils import CodexUtils

class FlameType(Enum):
    """Types of transformative flames"""
    PURIFICATION = "purification"
    ILLUMINATION = "illumination"
    TRANSFORMATION = "transformation"
    CREATION = "creation"
    DESTRUCTION = "destruction"
    RENEWAL = "renewal"

class TransformationStage(Enum):
    """Stages of transformation process"""
    PREPARATION = "preparation"
    IGNITION = "ignition"
    BURNING = "burning"
    TRANSMUTATION = "transmutation"
    COMPLETION = "completion"

class FlameRitual:
    """Flame ritual structure"""
    
    def __init__(self, ritual_id: str, flame_type: FlameType, 
                 intention: str, catalyst: str, participant: str):
        self.ritual_id = ritual_id
        self.flame_type = flame_type
        self.intention = intention
        self.catalyst = catalyst  # What's being transformed
        self.participant = participant
        self.stage = TransformationStage.PREPARATION
        self.intensity = 1.0  # 0.0 to 10.0
        self.purity = 0.5  # 0.0 to 1.0
        self.started_at = CodexUtils.generate_timestamp()
        self.completed_at = None
        self.transformations: List[Dict[str, Any]] = []

class FlameEngine:
    """Engine for transformation, purification, and renewal processes"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.active_rituals: Dict[str, FlameRitual] = {}
        self.completed_rituals: Dict[str, FlameRitual] = {}
        self.flame_properties = self._initialize_flame_properties()
        self.transformation_patterns = self._initialize_transformation_patterns()
    
    def _initialize_flame_properties(self) -> Dict[FlameType, Dict[str, Any]]:
        """Initialize properties for different flame types"""
        return {
            FlameType.PURIFICATION: {
                "color": "white",
                "symbol": "🕯️",
                "element": "spirit",
                "purpose": "Remove impurities and negative influences",
                "base_intensity": 3.0,
                "duration_multiplier": 1.0
            },
            FlameType.ILLUMINATION: {
                "color": "golden",
                "symbol": "💡",
                "element": "air",
                "purpose": "Bring clarity and understanding",
                "base_intensity": 4.0,
                "duration_multiplier": 0.8
            },
            FlameType.TRANSFORMATION: {
                "color": "blue",
                "symbol": "🔵",
                "element": "water",
                "purpose": "Fundamental change and evolution",
                "base_intensity": 6.0,
                "duration_multiplier": 1.5
            },
            FlameType.CREATION: {
                "color": "green",
                "symbol": "🌱",
                "element": "earth",
                "purpose": "Manifest new realities and forms",
                "base_intensity": 5.0,
                "duration_multiplier": 1.2
            },
            FlameType.DESTRUCTION: {
                "color": "red",
                "symbol": "🔥",
                "element": "fire",
                "purpose": "Eliminate obstacles and outdated patterns",
                "base_intensity": 8.0,
                "duration_multiplier": 0.7
            },
            FlameType.RENEWAL: {
                "color": "violet",
                "symbol": "🟣",
                "element": "ether",
                "purpose": "Regenerate and restore vital essence",
                "base_intensity": 4.5,
                "duration_multiplier": 1.3
            }
        }
    
    def _initialize_transformation_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize common transformation patterns"""
        return {
            "ego_dissolution": {
                "stages": ["Recognition", "Resistance", "Release", "Rebirth"],
                "challenges": ["Self-attachment", "Fear of change", "Identity confusion"],
                "outcomes": ["Humility", "Expanded awareness", "Authentic self"]
            },
            "shadow_integration": {
                "stages": ["Acknowledgment", "Examination", "Acceptance", "Integration"],
                "challenges": ["Denial", "Self-judgment", "Projection"],
                "outcomes": ["Wholeness", "Increased power", "Authentic expression"]
            },
            "wisdom_crystallization": {
                "stages": ["Experience", "Reflection", "Understanding", "Embodiment"],
                "challenges": ["Intellectual pride", "Attachment to concepts", "Integration difficulties"],
                "outcomes": ["Living wisdom", "Practical insight", "Natural teaching ability"]
            },
            "power_purification": {
                "stages": ["Recognition", "Examination", "Purification", "Sacred use"],
                "challenges": ["Corruption temptation", "Misuse patterns", "Responsibility fear"],
                "outcomes": ["Sacred authority", "Service orientation", "Wise leadership"]
            }
        }
    
    def kindle_flame(self, flame_type: FlameType, intention: str, 
                    catalyst: str, participant: str) -> str:
        """Kindle a new transformative flame"""
        
        ritual_id = CodexUtils.generate_id()
        
        ritual = FlameRitual(
            ritual_id=ritual_id,
            flame_type=flame_type,
            intention=intention,
            catalyst=catalyst,
            participant=participant
        )
        
        # Set initial properties based on flame type
        properties = self.flame_properties[flame_type]
        ritual.intensity = properties["base_intensity"]
        
        self.active_rituals[ritual_id] = ritual
        
        return ritual_id
    
    def tend_flame(self, ritual_id: str, focus_level: float = 1.0,
                  additional_catalyst: str = None) -> Dict[str, Any]:
        """Tend to an active flame ritual"""
        
        if ritual_id not in self.active_rituals:
            return {"success": False, "error": "Ritual not found or already completed"}
        
        ritual = self.active_rituals[ritual_id]
        properties = self.flame_properties[ritual.flame_type]
        
        # Advance the transformation stage
        stage_result = self._advance_stage(ritual, focus_level)
        
        # Update flame intensity based on tending
        intensity_change = (focus_level - 0.5) * 0.3
        ritual.intensity = max(0.1, min(10.0, ritual.intensity + intensity_change))
        
        # Update purity based on stage and focus
        if ritual.stage in [TransformationStage.BURNING, TransformationStage.TRANSMUTATION]:
            purity_gain = focus_level * 0.1
            ritual.purity = min(1.0, ritual.purity + purity_gain)
        
        # Add transformation record
        transformation = {
            "timestamp": CodexUtils.generate_timestamp(),
            "stage": ritual.stage.value,
            "intensity": ritual.intensity,
            "purity": ritual.purity,
            "focus_level": focus_level,
            "change": stage_result.get("change", "Steady progress")
        }
        
        if additional_catalyst:
            transformation["additional_catalyst"] = additional_catalyst
        
        ritual.transformations.append(transformation)
        
        # Check if ritual is complete
        if ritual.stage == TransformationStage.COMPLETION:
            self._complete_ritual(ritual)
        
        return {
            "success": True,
            "ritual_id": ritual_id,
            "current_stage": ritual.stage.value,
            "intensity": ritual.intensity,
            "purity": ritual.purity,
            "flame_color": properties["color"],
            "flame_symbol": properties["symbol"],
            "stage_description": stage_result.get("description", ""),
            "guidance": self._get_stage_guidance(ritual),
            "completed": ritual.stage == TransformationStage.COMPLETION
        }
    
    def _advance_stage(self, ritual: FlameRitual, focus_level: float) -> Dict[str, Any]:
        """Advance the ritual to the next stage"""
        
        current_stage = ritual.stage
        
        # Stage progression logic
        if current_stage == TransformationStage.PREPARATION and focus_level >= 0.7:
            ritual.stage = TransformationStage.IGNITION
            return {
                "change": "Flame ignited",
                "description": "The transformative process has begun"
            }
        
        elif current_stage == TransformationStage.IGNITION and ritual.intensity >= 3.0:
            ritual.stage = TransformationStage.BURNING
            return {
                "change": "Full burning achieved", 
                "description": "Transformation is actively occurring"
            }
        
        elif current_stage == TransformationStage.BURNING and ritual.purity >= 0.8:
            ritual.stage = TransformationStage.TRANSMUTATION
            return {
                "change": "Transmutation phase entered",
                "description": "Deep transformation is taking place"
            }
        
        elif current_stage == TransformationStage.TRANSMUTATION and ritual.purity >= 0.95:
            ritual.stage = TransformationStage.COMPLETION
            return {
                "change": "Transformation complete",
                "description": "The ritual has reached completion"
            }
        
        return {
            "change": "Continued progress",
            "description": f"Maintaining {current_stage.value} stage"
        }
    
    def _complete_ritual(self, ritual: FlameRitual) -> None:
        """Complete a ritual and move it to completed rituals"""
        
        ritual.completed_at = CodexUtils.generate_timestamp()
        
        # Generate completion insights
        completion_insight = self._generate_completion_insight(ritual)
        ritual.transformations.append({
            "timestamp": ritual.completed_at,
            "stage": "completion_insight",
            "insight": completion_insight,
            "final_intensity": ritual.intensity,
            "final_purity": ritual.purity
        })
        
        # Move to completed rituals
        self.completed_rituals[ritual.ritual_id] = ritual
        del self.active_rituals[ritual.ritual_id]
    
    def _generate_completion_insight(self, ritual: FlameRitual) -> str:
        """Generate insight for completed ritual"""
        
        flame_purpose = self.flame_properties[ritual.flame_type]["purpose"]
        
        insights = [
            f"Through {ritual.flame_type.value}, {ritual.catalyst} has been transformed",
            f"The flame has achieved its purpose: {flame_purpose.lower()}",
            f"Purity level of {ritual.purity:.1%} indicates successful transformation",
            f"The transformative essence can now be integrated into daily practice"
        ]
        
        # Add specific insights based on flame type
        if ritual.flame_type == FlameType.PURIFICATION:
            insights.append("Negative patterns and influences have been cleared")
        elif ritual.flame_type == FlameType.ILLUMINATION:
            insights.append("New understanding and clarity have been achieved")
        elif ritual.flame_type == FlameType.TRANSFORMATION:
            insights.append("Fundamental change has occurred at the core level")
        elif ritual.flame_type == FlameType.CREATION:
            insights.append("New potential and possibilities have been birthed")
        elif ritual.flame_type == FlameType.DESTRUCTION:
            insights.append("Obstacles and limitations have been dissolved")
        elif ritual.flame_type == FlameType.RENEWAL:
            insights.append("Vital energy and essence have been restored")
        
        return ". ".join(insights[:3])
    
    def _get_stage_guidance(self, ritual: FlameRitual) -> List[str]:
        """Get guidance for the current stage"""
        
        stage = ritual.stage
        flame_type = ritual.flame_type
        
        base_guidance = {
            TransformationStage.PREPARATION: [
                "Clarify your intention and commitment",
                "Prepare the sacred space mindfully",
                "Release attachment to specific outcomes"
            ],
            TransformationStage.IGNITION: [
                "Focus intently on the flame and intention",
                "Allow initial resistance to arise and pass",
                "Maintain steady breathing and presence"
            ],
            TransformationStage.BURNING: [
                "Surrender to the transformative process",
                "Observe without judgment or interference",
                "Trust in the wisdom of the flame"
            ],
            TransformationStage.TRANSMUTATION: [
                "Remain centered as deep changes occur",
                "Allow old patterns to dissolve completely",
                "Welcome the emergence of new understanding"
            ],
            TransformationStage.COMPLETION: [
                "Honor the completion of the process",
                "Integrate the transformation mindfully",
                "Express gratitude for the gifts received"
            ]
        }
        
        guidance = base_guidance.get(stage, ["Continue with presence and intention"])
        
        # Add flame-specific guidance
        if flame_type == FlameType.PURIFICATION and stage == TransformationStage.BURNING:
            guidance.append("Visualize impurities being consumed by white light")
        elif flame_type == FlameType.TRANSFORMATION and stage == TransformationStage.TRANSMUTATION:
            guidance.append("Allow your essence to be remolded by divine wisdom")
        
        return guidance
    
    def extinguish_flame(self, ritual_id: str, reason: str = "voluntary") -> Dict[str, Any]:
        """Extinguish an active flame ritual"""
        
        if ritual_id not in self.active_rituals:
            return {"success": False, "error": "Ritual not found or already completed"}
        
        ritual = self.active_rituals[ritual_id]
        
        # Record extinguishing
        extinguish_record = {
            "timestamp": CodexUtils.generate_timestamp(),
            "stage": "extinguished",
            "reason": reason,
            "final_intensity": ritual.intensity,
            "final_purity": ritual.purity,
            "completion_percentage": self._calculate_completion_percentage(ritual)
        }
        
        ritual.transformations.append(extinguish_record)
        
        # Move to completed (even if not fully finished)
        ritual.completed_at = CodexUtils.generate_timestamp()
        self.completed_rituals[ritual_id] = ritual
        del self.active_rituals[ritual_id]
        
        return {
            "success": True,
            "message": f"Flame extinguished - {reason}",
            "completion_percentage": extinguish_record["completion_percentage"],
            "final_purity": ritual.purity
        }
    
    def _calculate_completion_percentage(self, ritual: FlameRitual) -> float:
        """Calculate how complete a ritual is"""
        
        stage_percentages = {
            TransformationStage.PREPARATION: 10,
            TransformationStage.IGNITION: 25,
            TransformationStage.BURNING: 50,
            TransformationStage.TRANSMUTATION: 80,
            TransformationStage.COMPLETION: 100
        }
        
        base_percentage = stage_percentages.get(ritual.stage, 0)
        
        # Add bonus for high purity
        purity_bonus = ritual.purity * 10
        
        return min(100, base_percentage + purity_bonus)
    
    def get_flame_status(self, ritual_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a flame ritual"""
        
        ritual = self.active_rituals.get(ritual_id) or self.completed_rituals.get(ritual_id)
        
        if not ritual:
            return None
        
        properties = self.flame_properties[ritual.flame_type]
        
        return {
            "ritual_id": ritual.ritual_id,
            "flame_type": ritual.flame_type.value,
            "flame_color": properties["color"],
            "flame_symbol": properties["symbol"],
            "participant": ritual.participant,
            "intention": ritual.intention,
            "catalyst": ritual.catalyst,
            "current_stage": ritual.stage.value,
            "intensity": ritual.intensity,
            "purity": ritual.purity,
            "started_at": ritual.started_at,
            "completed_at": ritual.completed_at,
            "is_active": ritual_id in self.active_rituals,
            "transformation_count": len(ritual.transformations),
            "completion_percentage": self._calculate_completion_percentage(ritual)
        }
    
    def list_active_flames(self, participant: str = None) -> List[Dict[str, Any]]:
        """List all active flame rituals"""
        
        active_flames = []
        
        for ritual in self.active_rituals.values():
            if participant and ritual.participant != participant:
                continue
            
            status = self.get_flame_status(ritual.ritual_id)
            if status:
                active_flames.append(status)
        
        return sorted(active_flames, key=lambda x: x["started_at"], reverse=True)
    
    def get_flame_statistics(self) -> Dict[str, Any]:
        """Get statistics about flame rituals"""
        
        total_rituals = len(self.active_rituals) + len(self.completed_rituals)
        active_count = len(self.active_rituals)
        completed_count = len(self.completed_rituals)
        
        # Flame type distribution
        flame_type_counts = {}
        all_rituals = list(self.active_rituals.values()) + list(self.completed_rituals.values())
        
        for ritual in all_rituals:
            flame_type = ritual.flame_type.value
            flame_type_counts[flame_type] = flame_type_counts.get(flame_type, 0) + 1
        
        # Completion rate
        fully_completed = sum(1 for r in self.completed_rituals.values() 
                             if r.stage == TransformationStage.COMPLETION)
        
        completion_rate = fully_completed / completed_count if completed_count > 0 else 0
        
        return {
            "total_rituals": total_rituals,
            "active_rituals": active_count,
            "completed_rituals": completed_count,
            "fully_completed": fully_completed,
            "completion_rate": completion_rate,
            "flame_type_distribution": flame_type_counts,
            "available_flame_types": [ft.value for ft in FlameType],
            "transformation_stages": [stage.value for stage in TransformationStage]
        }