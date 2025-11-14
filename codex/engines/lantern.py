# Lantern Engine - Guidance and navigation system
from typing import Dict, Any, List, Optional, Tuple
import math
from datetime import datetime, timedelta
from enum import Enum

from ..core.config import CodexConfig
from ..core.utils import CodexUtils

class PathType(Enum):
    """Types of guidance paths"""
    LEARNING = "learning"
    GOVERNANCE = "governance"
    CEREMONIAL = "ceremonial"
    PERSONAL = "personal"
    STRATEGIC = "strategic"
    SPIRITUAL = "spiritual"

class Waypoint:
    """Navigation waypoint structure"""
    
    def __init__(self, waypoint_id: str, title: str, description: str,
                 path_type: PathType, difficulty: int, prerequisites: List[str] = None):
        self.waypoint_id = waypoint_id
        self.title = title
        self.description = description
        self.path_type = path_type
        self.difficulty = difficulty  # 1-10 scale
        self.prerequisites = prerequisites or []
        self.completion_time = None
        self.created_at = CodexUtils.generate_timestamp()

class Journey:
    """Complete journey/path structure"""
    
    def __init__(self, journey_id: str, traveler: str, destination: str,
                 path_type: PathType, waypoints: List[Waypoint]):
        self.journey_id = journey_id
        self.traveler = traveler
        self.destination = destination
        self.path_type = path_type
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.started_at = CodexUtils.generate_timestamp()
        self.completed_at = None
        self.progress = 0.0

class LanternEngine:
    """Engine for guidance, navigation, and pathfinding"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.journeys: Dict[str, Journey] = {}
        self.waypoint_library: Dict[str, Waypoint] = {}
        self.guidance_templates = self._initialize_guidance_templates()
        self._populate_waypoint_library()
    
    def _initialize_guidance_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize guidance templates for different scenarios"""
        return {
            "learning": {
                "phases": ["Foundation", "Exploration", "Mastery", "Teaching"],
                "milestones": [
                    "Basic understanding acquired",
                    "Practical application demonstrated", 
                    "Complex concepts grasped",
                    "Knowledge shared with others"
                ],
                "guidance": [
                    "Begin with fundamental concepts",
                    "Practice regularly to build understanding",
                    "Seek mentorship when facing challenges",
                    "Document your learning journey"
                ]
            },
            "governance": {
                "phases": ["Observation", "Participation", "Leadership", "Stewardship"],
                "milestones": [
                    "Council proceedings observed",
                    "Decisions participated in",
                    "Leadership responsibility accepted",
                    "Realm welfare prioritized"
                ],
                "guidance": [
                    "Study existing governance structures",
                    "Seek counsel from experienced leaders",
                    "Balance authority with responsibility",
                    "Remember that power serves the realm"
                ]
            },
            "ceremonial": {
                "phases": ["Preparation", "Invocation", "Manifestation", "Integration"],
                "milestones": [
                    "Sacred space prepared",
                    "Ceremonial intent declared",
                    "Desired outcome achieved",
                    "Results integrated into being"
                ],
                "guidance": [
                    "Purify intent before beginning",
                    "Respect the sacred nature of ceremony",
                    "Maintain focus throughout the process",
                    "Honor the gifts received"
                ]
            }
        }
    
    def _populate_waypoint_library(self) -> None:
        """Populate the waypoint library with common navigation points"""
        
        # Learning waypoints
        learning_waypoints = [
            ("Foundational Concepts", "Master basic principles and terminology", 2, []),
            ("Practical Application", "Apply concepts in real scenarios", 4, ["Foundational Concepts"]),
            ("Advanced Integration", "Synthesize complex interconnections", 6, ["Practical Application"]),
            ("Mentorship Role", "Guide others on their learning path", 8, ["Advanced Integration"])
        ]
        
        for title, desc, diff, prereq in learning_waypoints:
            waypoint = Waypoint(
                waypoint_id=CodexUtils.generate_id(),
                title=title,
                description=desc,
                path_type=PathType.LEARNING,
                difficulty=diff,
                prerequisites=prereq
            )
            self.waypoint_library[waypoint.waypoint_id] = waypoint
        
        # Governance waypoints
        governance_waypoints = [
            ("Observer Status", "Attend council sessions as observer", 3, []),
            ("Council Participation", "Contribute to council discussions", 5, ["Observer Status"]),
            ("Committee Leadership", "Lead specialized council committee", 7, ["Council Participation"]),
            ("Realm Stewardship", "Take responsibility for realm welfare", 9, ["Committee Leadership"])
        ]
        
        for title, desc, diff, prereq in governance_waypoints:
            waypoint = Waypoint(
                waypoint_id=CodexUtils.generate_id(),
                title=title,
                description=desc,
                path_type=PathType.GOVERNANCE,
                difficulty=diff,
                prerequisites=prereq
            )
            self.waypoint_library[waypoint.waypoint_id] = waypoint
        
        # Ceremonial waypoints
        ceremonial_waypoints = [
            ("Sacred Space Preparation", "Learn to prepare ceremonial spaces", 3, []),
            ("Intent Clarification", "Master the art of clear intention", 4, ["Sacred Space Preparation"]),
            ("Invocation Techniques", "Practice various invocation methods", 6, ["Intent Clarification"]),
            ("Ceremonial Mastery", "Conduct complete ceremonies independently", 8, ["Invocation Techniques"])
        ]
        
        for title, desc, diff, prereq in ceremonial_waypoints:
            waypoint = Waypoint(
                waypoint_id=CodexUtils.generate_id(),
                title=title,
                description=desc,
                path_type=PathType.CEREMONIAL,
                difficulty=diff,
                prerequisites=prereq
            )
            self.waypoint_library[waypoint.waypoint_id] = waypoint
    
    def create_journey(self, traveler: str, destination: str, 
                      path_type: PathType, custom_waypoints: List[Dict[str, Any]] = None) -> str:
        """Create a new guidance journey"""
        
        journey_id = CodexUtils.generate_id()
        
        # Get waypoints for the journey
        if custom_waypoints:
            waypoints = self._create_custom_waypoints(custom_waypoints, path_type)
        else:
            waypoints = self._get_default_waypoints(path_type)
        
        journey = Journey(
            journey_id=journey_id,
            traveler=traveler,
            destination=destination,
            path_type=path_type,
            waypoints=waypoints
        )
        
        self.journeys[journey_id] = journey
        
        return journey_id
    
    def _create_custom_waypoints(self, waypoint_specs: List[Dict[str, Any]], 
                                path_type: PathType) -> List[Waypoint]:
        """Create custom waypoints from specifications"""
        waypoints = []
        
        for spec in waypoint_specs:
            waypoint = Waypoint(
                waypoint_id=CodexUtils.generate_id(),
                title=spec.get("title", "Untitled Waypoint"),
                description=spec.get("description", "No description provided"),
                path_type=path_type,
                difficulty=spec.get("difficulty", 5),
                prerequisites=spec.get("prerequisites", [])
            )
            waypoints.append(waypoint)
        
        return waypoints
    
    def _get_default_waypoints(self, path_type: PathType) -> List[Waypoint]:
        """Get default waypoints for a path type"""
        matching_waypoints = [
            wp for wp in self.waypoint_library.values() 
            if wp.path_type == path_type
        ]
        
        # Sort by difficulty
        matching_waypoints.sort(key=lambda x: x.difficulty)
        
        return matching_waypoints
    
    def get_guidance(self, journey_id: str) -> Dict[str, Any]:
        """Get guidance for a specific journey"""
        
        if journey_id not in self.journeys:
            return {"error": "Journey not found"}
        
        journey = self.journeys[journey_id]
        current_waypoint = None
        next_waypoint = None
        
        if journey.current_waypoint < len(journey.waypoints):
            current_waypoint = journey.waypoints[journey.current_waypoint]
        
        if journey.current_waypoint + 1 < len(journey.waypoints):
            next_waypoint = journey.waypoints[journey.current_waypoint + 1]
        
        # Get contextual guidance
        template = self.guidance_templates.get(journey.path_type.value, {})
        
        guidance = {
            "journey_id": journey_id,
            "traveler": journey.traveler,
            "destination": journey.destination,
            "path_type": journey.path_type.value,
            "progress": self._calculate_progress(journey),
            "current_waypoint": self._waypoint_to_dict(current_waypoint) if current_waypoint else None,
            "next_waypoint": self._waypoint_to_dict(next_waypoint) if next_waypoint else None,
            "recommendations": self._get_recommendations(journey),
            "phase_guidance": template.get("guidance", []),
            "estimated_completion": self._estimate_completion_time(journey)
        }
        
        return guidance
    
    def _calculate_progress(self, journey: Journey) -> float:
        """Calculate journey progress as percentage"""
        if not journey.waypoints:
            return 0.0
        
        completed_waypoints = sum(1 for wp in journey.waypoints[:journey.current_waypoint] 
                                if wp.completion_time is not None)
        
        return completed_waypoints / len(journey.waypoints) * 100
    
    def _waypoint_to_dict(self, waypoint: Waypoint) -> Dict[str, Any]:
        """Convert waypoint to dictionary representation"""
        if not waypoint:
            return None
        
        return {
            "waypoint_id": waypoint.waypoint_id,
            "title": waypoint.title,
            "description": waypoint.description,
            "difficulty": waypoint.difficulty,
            "prerequisites": waypoint.prerequisites,
            "completed": waypoint.completion_time is not None
        }
    
    def _get_recommendations(self, journey: Journey) -> List[str]:
        """Get personalized recommendations for the journey"""
        recommendations = []
        
        if journey.current_waypoint < len(journey.waypoints):
            current_wp = journey.waypoints[journey.current_waypoint]
            
            # Difficulty-based recommendations
            if current_wp.difficulty >= 7:
                recommendations.append("Consider seeking mentorship for this challenging waypoint")
            
            if current_wp.difficulty <= 3:
                recommendations.append("This waypoint provides good foundation - take time to master it")
            
            # Prerequisites check
            if current_wp.prerequisites:
                recommendations.append(f"Ensure you've completed: {', '.join(current_wp.prerequisites)}")
            
            # Path-specific recommendations
            if journey.path_type == PathType.LEARNING:
                recommendations.append("Document your insights and questions as you progress")
            elif journey.path_type == PathType.GOVERNANCE:
                recommendations.append("Seek feedback from experienced council members")
            elif journey.path_type == PathType.CEREMONIAL:
                recommendations.append("Practice in a safe, sacred space before formal ceremonies")
        
        if not recommendations:
            recommendations.append("Continue with steady progress and mindful attention")
        
        return recommendations
    
    def _estimate_completion_time(self, journey: Journey) -> str:
        """Estimate time to complete the journey"""
        remaining_waypoints = len(journey.waypoints) - journey.current_waypoint
        
        if remaining_waypoints == 0:
            return "Journey complete"
        
        # Base time estimates by difficulty (in days)
        difficulty_times = {
            1: 3, 2: 5, 3: 7, 4: 10, 5: 14,
            6: 21, 7: 30, 8: 45, 9: 60, 10: 90
        }
        
        total_days = 0
        for i in range(journey.current_waypoint, len(journey.waypoints)):
            waypoint = journey.waypoints[i]
            total_days += difficulty_times.get(waypoint.difficulty, 14)
        
        if total_days <= 7:
            return "Within 1 week"
        elif total_days <= 30:
            return "Within 1 month"
        elif total_days <= 90:
            return "Within 3 months"
        else:
            return "3+ months"
    
    def advance_waypoint(self, journey_id: str, completion_notes: str = "") -> Dict[str, Any]:
        """Advance to the next waypoint in the journey"""
        
        if journey_id not in self.journeys:
            return {"success": False, "error": "Journey not found"}
        
        journey = self.journeys[journey_id]
        
        if journey.current_waypoint >= len(journey.waypoints):
            return {"success": False, "error": "Journey already complete"}
        
        # Mark current waypoint as complete
        current_waypoint = journey.waypoints[journey.current_waypoint]
        current_waypoint.completion_time = CodexUtils.generate_timestamp()
        
        # Advance to next waypoint
        journey.current_waypoint += 1
        journey.progress = self._calculate_progress(journey)
        
        # Check if journey is complete
        if journey.current_waypoint >= len(journey.waypoints):
            journey.completed_at = CodexUtils.generate_timestamp()
            return {
                "success": True,
                "journey_complete": True,
                "message": f"Congratulations! Journey to {journey.destination} completed."
            }
        
        return {
            "success": True,
            "journey_complete": False,
            "current_waypoint": self._waypoint_to_dict(journey.waypoints[journey.current_waypoint]),
            "progress": journey.progress,
            "message": f"Advanced to waypoint: {journey.waypoints[journey.current_waypoint].title}"
        }
    
    def get_journey_map(self, journey_id: str) -> Dict[str, Any]:
        """Get a visual representation of the journey"""
        
        if journey_id not in self.journeys:
            return {"error": "Journey not found"}
        
        journey = self.journeys[journey_id]
        
        waypoint_map = []
        for i, waypoint in enumerate(journey.waypoints):
            status = "completed" if waypoint.completion_time else ("current" if i == journey.current_waypoint else "upcoming")
            
            waypoint_map.append({
                "position": i + 1,
                "title": waypoint.title,
                "difficulty": waypoint.difficulty,
                "status": status,
                "completion_time": waypoint.completion_time
            })
        
        return {
            "journey_id": journey_id,
            "traveler": journey.traveler,
            "destination": journey.destination,
            "path_type": journey.path_type.value,
            "started_at": journey.started_at,
            "completed_at": journey.completed_at,
            "progress": journey.progress,
            "waypoint_map": waypoint_map,
            "total_waypoints": len(journey.waypoints)
        }
    
    def search_waypoints(self, query: str, path_type: PathType = None,
                        max_difficulty: int = None) -> List[Dict[str, Any]]:
        """Search for waypoints matching criteria"""
        
        results = []
        
        for waypoint in self.waypoint_library.values():
            # Filter by path type
            if path_type and waypoint.path_type != path_type:
                continue
            
            # Filter by difficulty
            if max_difficulty and waypoint.difficulty > max_difficulty:
                continue
            
            # Text search
            if query.lower() in waypoint.title.lower() or query.lower() in waypoint.description.lower():
                results.append(self._waypoint_to_dict(waypoint))
        
        return results
    
    def get_lantern_statistics(self) -> Dict[str, Any]:
        """Get statistics about guidance usage"""
        
        total_journeys = len(self.journeys)
        completed_journeys = sum(1 for j in self.journeys.values() if j.completed_at is not None)
        
        # Path type distribution
        path_counts = {}
        for journey in self.journeys.values():
            path_type = journey.path_type.value
            path_counts[path_type] = path_counts.get(path_type, 0) + 1
        
        # Average progress
        avg_progress = 0.0
        if self.journeys:
            avg_progress = sum(j.progress for j in self.journeys.values()) / len(self.journeys)
        
        return {
            "total_journeys": total_journeys,
            "completed_journeys": completed_journeys,
            "completion_rate": completed_journeys / total_journeys if total_journeys > 0 else 0,
            "path_distribution": path_counts,
            "average_progress": avg_progress,
            "total_waypoints": len(self.waypoint_library),
            "available_path_types": [path.value for path in PathType]
        }