# Oracle Engine - Divination and wisdom processing
from typing import Dict, Any, List, Optional, Tuple
import random
from datetime import datetime, timedelta
from enum import Enum

from ..core.config import CodexConfig
from ..core.utils import CodexUtils

class OracleMethod(Enum):
    """Methods of oracular consultation"""
    RUNES = "runes"
    CARDS = "cards"
    SCRYING = "scrying"
    NUMEROLOGY = "numerology"
    ELEMENTAL = "elemental"
    CELESTIAL = "celestial"

class Prophecy:
    """Prophecy structure"""
    
    def __init__(self, prophecy_id: str, method: OracleMethod, 
                 question: str, interpretation: str, 
                 confidence: float, symbols: List[str]):
        self.prophecy_id = prophecy_id
        self.method = method
        self.question = question
        self.interpretation = interpretation
        self.confidence = confidence
        self.symbols = symbols
        self.cast_at = CodexUtils.generate_timestamp()
        self.fulfillment_date: Optional[str] = None

class OracleEngine:
    """Engine for divination, prophecy, and wisdom consultation"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.prophecies: Dict[str, Prophecy] = {}
        self.wisdom_base = self._initialize_wisdom_base()
        self.rune_meanings = self._initialize_runes()
        self.elemental_aspects = self._initialize_elements()
    
    def _initialize_wisdom_base(self) -> Dict[str, List[str]]:
        """Initialize base wisdom sayings and insights"""
        return {
            "governance": [
                "True authority flows from wisdom, not force",
                "The crown that bears lightly rules longest",
                "In council lies strength, in isolation lies folly",
                "Justice delayed is justice denied, yet haste breeds injustice"
            ],
            "knowledge": [
                "Knowledge hoarded becomes stagnant; knowledge shared becomes power",
                "The wise admit ignorance; the foolish claim omniscience", 
                "In questions lie the seeds of understanding",
                "Truth has many faces but one essence"
            ],
            "power": [
                "Power without responsibility is tyranny",
                "The mightiest fortress falls from within",
                "True power empowers others",
                "The throne serves the realm, not the reverse"
            ],
            "change": [
                "The river that resists its banks breaks them",
                "In ending lies beginning",
                "Change is the only constant; adaptation the only wisdom",
                "The oak that bends survives the storm"
            ]
        }
    
    def _initialize_runes(self) -> Dict[str, Dict[str, str]]:
        """Initialize runic meanings"""
        return {
            "ᚠ": {"name": "Fehu", "meaning": "Wealth, abundance, material success", "aspect": "prosperity"},
            "ᚢ": {"name": "Uruz", "meaning": "Strength, health, courage", "aspect": "power"},
            "ᚦ": {"name": "Thurisaz", "meaning": "Protection, conflict, breakthrough", "aspect": "challenge"},
            "ᚨ": {"name": "Ansuz", "meaning": "Wisdom, communication, divine insight", "aspect": "knowledge"},
            "ᚱ": {"name": "Raidho", "meaning": "Journey, travel, personal quest", "aspect": "movement"},
            "ᚲ": {"name": "Kenaz", "meaning": "Knowledge, creativity, inspiration", "aspect": "illumination"},
            "ᚷ": {"name": "Gebo", "meaning": "Gift, partnership, generosity", "aspect": "exchange"},
            "ᚹ": {"name": "Wunjo", "meaning": "Joy, happiness, fulfillment", "aspect": "harmony"},
            "ᚺ": {"name": "Hagalaz", "meaning": "Disruption, crisis, transformation", "aspect": "upheaval"},
            "ᚾ": {"name": "Nauthiz", "meaning": "Need, resistance, survival", "aspect": "necessity"},
            "ᛁ": {"name": "Isa", "meaning": "Ice, stillness, patience", "aspect": "stasis"},
            "ᛃ": {"name": "Jera", "meaning": "Harvest, reward, cycles", "aspect": "completion"}
        }
    
    def _initialize_elements(self) -> Dict[str, Dict[str, Any]]:
        """Initialize elemental aspects"""
        return {
            "fire": {
                "symbol": "🔥",
                "qualities": ["passion", "transformation", "energy", "destruction", "creation"],
                "season": "summer",
                "direction": "south"
            },
            "water": {
                "symbol": "🌊",
                "qualities": ["emotion", "intuition", "healing", "flow", "depth"],
                "season": "winter", 
                "direction": "west"
            },
            "earth": {
                "symbol": "🌍",
                "qualities": ["stability", "growth", "abundance", "grounding", "endurance"],
                "season": "autumn",
                "direction": "north"
            },
            "air": {
                "symbol": "🌪️",
                "qualities": ["intellect", "communication", "change", "freedom", "clarity"],
                "season": "spring",
                "direction": "east"
            }
        }
    
    def consult_oracle(self, question: str, method: OracleMethod = OracleMethod.RUNES,
                      seeker: str = "unknown") -> Dict[str, Any]:
        """Consult the oracle with a specific question"""
        
        prophecy_id = CodexUtils.generate_id()
        
        if method == OracleMethod.RUNES:
            result = self._cast_runes(question)
        elif method == OracleMethod.CARDS:
            result = self._draw_cards(question)
        elif method == OracleMethod.SCRYING:
            result = self._scry_vision(question)
        elif method == OracleMethod.NUMEROLOGY:
            result = self._calculate_numerology(question)
        elif method == OracleMethod.ELEMENTAL:
            result = self._consult_elements(question)
        elif method == OracleMethod.CELESTIAL:
            result = self._read_stars(question)
        else:
            result = self._cast_runes(question)  # Default fallback
        
        # Create prophecy record
        prophecy = Prophecy(
            prophecy_id=prophecy_id,
            method=method,
            question=question,
            interpretation=result["interpretation"],
            confidence=result["confidence"],
            symbols=result["symbols"]
        )
        
        self.prophecies[prophecy_id] = prophecy
        
        return {
            "prophecy_id": prophecy_id,
            "method": method.value,
            "question": question,
            "seeker": seeker,
            "cast_at": prophecy.cast_at,
            "symbols": result["symbols"],
            "interpretation": result["interpretation"],
            "confidence": result["confidence"],
            "guidance": result.get("guidance", []),
            "timeframe": result.get("timeframe", "unknown")
        }
    
    def _cast_runes(self, question: str) -> Dict[str, Any]:
        """Cast runes for divination"""
        
        # Select 3 runes for past, present, future
        selected_runes = random.sample(list(self.rune_meanings.keys()), 3)
        
        interpretations = []
        symbols = []
        
        positions = ["past", "present", "future"]
        
        for i, rune in enumerate(selected_runes):
            rune_data = self.rune_meanings[rune]
            symbols.append(rune)
            
            interpretations.append({
                "position": positions[i],
                "rune": rune,
                "name": rune_data["name"],
                "meaning": rune_data["meaning"],
                "aspect": rune_data["aspect"]
            })
        
        # Generate overall interpretation
        past_aspect = interpretations[0]["aspect"]
        present_aspect = interpretations[1]["aspect"]
        future_aspect = interpretations[2]["aspect"]
        
        interpretation = f"The runes speak of a journey from {past_aspect} through {present_aspect} toward {future_aspect}. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.6, 0.9),
            "details": interpretations,
            "timeframe": "within one lunar cycle"
        }
    
    def _draw_cards(self, question: str) -> Dict[str, Any]:
        """Draw oracle cards"""
        
        # Simplified card meanings
        cards = [
            {"name": "The Crown", "meaning": "Authority and responsibility"},
            {"name": "The Flame", "meaning": "Passion and transformation"},
            {"name": "The Well", "meaning": "Deep wisdom and intuition"},
            {"name": "The Path", "meaning": "Journey and choice"},
            {"name": "The Tower", "meaning": "Strength and foundation"},
            {"name": "The Star", "meaning": "Hope and guidance"},
            {"name": "The Mirror", "meaning": "Truth and reflection"},
            {"name": "The Bridge", "meaning": "Connection and transition"}
        ]
        
        drawn_cards = random.sample(cards, 2)
        symbols = ["🃏", "✨"]
        
        interpretation = f"The cards reveal {drawn_cards[0]['name']} and {drawn_cards[1]['name']}. "
        interpretation += f"This suggests {drawn_cards[0]['meaning'].lower()} working with {drawn_cards[1]['meaning'].lower()}. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.5, 0.8),
            "cards": drawn_cards,
            "timeframe": "in the coming season"
        }
    
    def _scry_vision(self, question: str) -> Dict[str, Any]:
        """Scrying vision interpretation"""
        
        # Vision elements
        vision_elements = [
            "flowing water", "flickering flames", "soaring birds", "ancient trees",
            "shifting clouds", "crystalline formations", "swirling mists", "starlight"
        ]
        
        selected_elements = random.sample(vision_elements, 3)
        symbols = ["🔮", "👁️", "✨"]
        
        interpretation = f"In the scrying pool, I see {', '.join(selected_elements)}. "
        interpretation += "These visions suggest patterns of change and revelation. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.4, 0.7),
            "vision_elements": selected_elements,
            "timeframe": "timeframe unclear, look for signs"
        }
    
    def _calculate_numerology(self, question: str) -> Dict[str, Any]:
        """Numerological analysis"""
        
        # Convert question to numbers
        question_value = sum(ord(char.lower()) - ord('a') + 1 
                           for char in question if char.isalpha())
        
        # Reduce to single digit
        while question_value >= 10:
            question_value = sum(int(digit) for digit in str(question_value))
        
        number_meanings = {
            1: "New beginnings and leadership",
            2: "Partnership and cooperation", 
            3: "Creativity and communication",
            4: "Stability and hard work",
            5: "Change and freedom",
            6: "Harmony and responsibility",
            7: "Wisdom and introspection",
            8: "Material success and power",
            9: "Completion and universal love"
        }
        
        symbols = [str(question_value), "🔢"]
        meaning = number_meanings[question_value]
        
        interpretation = f"The numerical essence of your question resonates with {question_value}, "
        interpretation += f"which signifies {meaning.lower()}. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.6, 0.8),
            "number": question_value,
            "meaning": meaning,
            "timeframe": f"{question_value} days or weeks"
        }
    
    def _consult_elements(self, question: str) -> Dict[str, Any]:
        """Elemental consultation"""
        
        # Select dominant element
        element_name = random.choice(list(self.elemental_aspects.keys()))
        element = self.elemental_aspects[element_name]
        
        # Select secondary influence
        secondary_element = random.choice([e for e in self.elemental_aspects.keys() 
                                         if e != element_name])
        
        symbols = [element["symbol"], self.elemental_aspects[secondary_element]["symbol"]]
        
        primary_quality = random.choice(element["qualities"])
        
        interpretation = f"The elements speak through {element_name}, emphasizing {primary_quality}. "
        interpretation += f"Secondary influence from {secondary_element} brings additional nuance. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.5, 0.8),
            "primary_element": element_name,
            "secondary_element": secondary_element,
            "dominant_quality": primary_quality,
            "timeframe": f"during {element['season']}"
        }
    
    def _read_stars(self, question: str) -> Dict[str, Any]:
        """Celestial consultation"""
        
        celestial_bodies = [
            {"name": "Luna", "influence": "intuition and cycles"},
            {"name": "Sol", "influence": "clarity and power"},
            {"name": "Mars", "influence": "action and courage"},
            {"name": "Venus", "influence": "harmony and love"},
            {"name": "Mercury", "influence": "communication and travel"},
            {"name": "Jupiter", "influence": "expansion and wisdom"},
            {"name": "Saturn", "influence": "structure and discipline"}
        ]
        
        primary_body = random.choice(celestial_bodies)
        symbols = ["⭐", "🌙", "☀️"]
        
        interpretation = f"The stars align with {primary_body['name']} in prominence, "
        interpretation += f"bringing influence of {primary_body['influence']}. "
        interpretation += self._get_wisdom_for_question(question)
        
        return {
            "symbols": symbols,
            "interpretation": interpretation,
            "confidence": random.uniform(0.6, 0.9),
            "celestial_body": primary_body,
            "timeframe": "when the stars next align"
        }
    
    def _get_wisdom_for_question(self, question: str) -> str:
        """Get relevant wisdom saying based on question content"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["rule", "govern", "lead", "authority"]):
            wisdom_type = "governance"
        elif any(word in question_lower for word in ["know", "learn", "understand", "wisdom"]):
            wisdom_type = "knowledge"
        elif any(word in question_lower for word in ["power", "strength", "control"]):
            wisdom_type = "power"
        elif any(word in question_lower for word in ["change", "future", "transform"]):
            wisdom_type = "change"
        else:
            wisdom_type = random.choice(list(self.wisdom_base.keys()))
        
        return random.choice(self.wisdom_base[wisdom_type])
    
    def get_prophecy(self, prophecy_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific prophecy"""
        
        if prophecy_id not in self.prophecies:
            return None
        
        prophecy = self.prophecies[prophecy_id]
        
        return {
            "prophecy_id": prophecy.prophecy_id,
            "method": prophecy.method.value,
            "question": prophecy.question,
            "interpretation": prophecy.interpretation,
            "confidence": prophecy.confidence,
            "symbols": prophecy.symbols,
            "cast_at": prophecy.cast_at,
            "fulfillment_date": prophecy.fulfillment_date
        }
    
    def mark_prophecy_fulfilled(self, prophecy_id: str) -> bool:
        """Mark a prophecy as fulfilled"""
        
        if prophecy_id not in self.prophecies:
            return False
        
        self.prophecies[prophecy_id].fulfillment_date = CodexUtils.generate_timestamp()
        return True
    
    def get_oracle_statistics(self) -> Dict[str, Any]:
        """Get oracle consultation statistics"""
        
        total_prophecies = len(self.prophecies)
        fulfilled_prophecies = sum(1 for p in self.prophecies.values() 
                                 if p.fulfillment_date is not None)
        
        # Method distribution
        method_counts = {}
        for prophecy in self.prophecies.values():
            method = prophecy.method.value
            method_counts[method] = method_counts.get(method, 0) + 1
        
        # Average confidence
        avg_confidence = 0.0
        if self.prophecies:
            avg_confidence = sum(p.confidence for p in self.prophecies.values()) / len(self.prophecies)
        
        return {
            "total_prophecies": total_prophecies,
            "fulfilled_prophecies": fulfilled_prophecies,
            "fulfillment_rate": fulfilled_prophecies / total_prophecies if total_prophecies > 0 else 0,
            "method_distribution": method_counts,
            "average_confidence": avg_confidence,
            "available_methods": [method.value for method in OracleMethod]
        }