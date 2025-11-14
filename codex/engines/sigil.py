# Sigil Engine - Pattern recognition and symbolic processing
from typing import Dict, Any, List, Optional, Set, Tuple
import re
import json
from collections import Counter
from datetime import datetime

from ..core.config import CodexConfig
from ..core.utils import CodexUtils

class SigilPattern:
    """Sigil pattern structure"""
    
    def __init__(self, pattern_id: str, pattern_type: str, 
                 signature: str, meaning: str, frequency: int = 0):
        self.pattern_id = pattern_id
        self.pattern_type = pattern_type
        self.signature = signature
        self.meaning = meaning
        self.frequency = frequency
        self.discovered_at = CodexUtils.generate_timestamp()

class SigilEngine:
    """Engine for pattern recognition and sigil processing"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.patterns: Dict[str, SigilPattern] = {}
        self.symbol_registry: Dict[str, Dict[str, Any]] = {}
        self._load_base_patterns()
    
    def _load_base_patterns(self) -> None:
        """Load base sigil patterns and symbols"""
        
        # Royal/Sovereignty patterns
        royal_patterns = {
            "crown": {"type": "royal", "meaning": "supreme authority", "symbols": ["👑", "♛", "♕"]},
            "throne": {"type": "royal", "meaning": "seat of power", "symbols": ["🪑", "⊰", "⊱"]},
            "scepter": {"type": "royal", "meaning": "ruling instrument", "symbols": ["🪄", "│", "┃"]},
            "orb": {"type": "royal", "meaning": "worldly dominion", "symbols": ["🌍", "⚪", "◯"]}
        }
        
        # Ceremonial patterns
        ceremonial_patterns = {
            "seal": {"type": "ceremonial", "meaning": "authority binding", "symbols": ["⚡", "✦", "❋"]},
            "flame": {"type": "ceremonial", "meaning": "eternal knowledge", "symbols": ["🔥", "🕯️", "✨"]},
            "lantern": {"type": "ceremonial", "meaning": "guidance light", "symbols": ["🏮", "💡", "🔆"]},
            "scroll": {"type": "ceremonial", "meaning": "preserved wisdom", "symbols": ["📜", "📋", "📰"]}
        }
        
        # Realm patterns
        realm_patterns = {
            "realm_id": {"type": "realm", "meaning": "domain identifier", "pattern": r"[A-Z]{2}-\d{3}"},
            "capsule_ref": {"type": "capsule", "meaning": "ceremonial vessel", "pattern": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"},
            "intent_marker": {"type": "intent", "meaning": "purpose declaration", "pattern": r"\b(invoke|summon|create|analyze|decide)\b"}
        }
        
        # Register all patterns
        all_patterns = {**royal_patterns, **ceremonial_patterns, **realm_patterns}
        
        for pattern_name, pattern_data in all_patterns.items():
            pattern_id = CodexUtils.generate_id()
            
            if "symbols" in pattern_data:
                # Symbol-based pattern
                signature = "|".join(pattern_data["symbols"])
            elif "pattern" in pattern_data:
                # Regex pattern
                signature = pattern_data["pattern"]
            else:
                # Keyword pattern
                signature = pattern_name
            
            sigil_pattern = SigilPattern(
                pattern_id=pattern_id,
                pattern_type=pattern_data["type"],
                signature=signature,
                meaning=pattern_data["meaning"]
            )
            
            self.patterns[pattern_name] = sigil_pattern
            
        # Initialize symbol registry
        self.symbol_registry = {
            "royal": ["👑", "♛", "♕", "🪑", "⊰", "⊱", "🪄"],
            "ceremonial": ["⚡", "✦", "❋", "🔥", "🕯️", "✨", "🏮", "💡"],
            "elemental": ["🌍", "🌊", "🔥", "🌪️", "⚡", "🌙", "☀️"],
            "protective": ["🛡️", "⚔️", "🗡️", "🔐", "🔒", "🗝️"]
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text for sigil patterns and symbolic content"""
        
        analysis = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "patterns_found": [],
            "symbol_analysis": {},
            "significance_score": 0.0,
            "ceremonial_markers": [],
            "realm_indicators": []
        }
        
        # Pattern matching
        for pattern_name, pattern in self.patterns.items():
            matches = self._find_pattern_matches(text, pattern)
            
            if matches:
                analysis["patterns_found"].append({
                    "pattern": pattern_name,
                    "type": pattern.pattern_type,
                    "meaning": pattern.meaning,
                    "matches": matches,
                    "count": len(matches)
                })
                
                # Update pattern frequency
                pattern.frequency += len(matches)
        
        # Symbol analysis
        analysis["symbol_analysis"] = self._analyze_symbols(text)
        
        # Detect ceremonial markers
        analysis["ceremonial_markers"] = self._detect_ceremonial_markers(text)
        
        # Detect realm indicators
        analysis["realm_indicators"] = self._detect_realm_indicators(text)
        
        # Calculate significance score
        analysis["significance_score"] = self._calculate_significance(analysis)
        
        return analysis
    
    def _find_pattern_matches(self, text: str, pattern: SigilPattern) -> List[str]:
        """Find matches for a specific pattern"""
        matches = []
        
        if pattern.pattern_type in ["royal", "ceremonial"]:
            # Symbol-based matching
            symbols = pattern.signature.split("|")
            for symbol in symbols:
                if symbol in text:
                    matches.append(symbol)
        else:
            # Regex-based matching
            try:
                regex_matches = re.findall(pattern.signature, text, re.IGNORECASE)
                matches.extend(regex_matches)
            except re.error:
                # Fallback to simple string matching
                if pattern.signature.lower() in text.lower():
                    matches.append(pattern.signature)
        
        return matches
    
    def _analyze_symbols(self, text: str) -> Dict[str, Any]:
        """Analyze symbolic content in text"""
        symbol_analysis = {
            "categories": {},
            "unique_symbols": set(),
            "symbol_density": 0.0
        }
        
        total_symbols = 0
        
        for category, symbols in self.symbol_registry.items():
            category_count = 0
            found_symbols = []
            
            for symbol in symbols:
                count = text.count(symbol)
                if count > 0:
                    category_count += count
                    total_symbols += count
                    found_symbols.append({"symbol": symbol, "count": count})
                    symbol_analysis["unique_symbols"].add(symbol)
            
            if category_count > 0:
                symbol_analysis["categories"][category] = {
                    "count": category_count,
                    "symbols": found_symbols
                }
        
        # Calculate symbol density
        if len(text) > 0:
            symbol_analysis["symbol_density"] = total_symbols / len(text)
        
        # Convert set to list for JSON serialization
        symbol_analysis["unique_symbols"] = list(symbol_analysis["unique_symbols"])
        
        return symbol_analysis
    
    def _detect_ceremonial_markers(self, text: str) -> List[Dict[str, Any]]:
        """Detect ceremonial language markers"""
        ceremonial_words = [
            "invoke", "summon", "decree", "proclaim", "seal", "witness",
            "ceremony", "ritual", "sacred", "blessed", "consecrated",
            "ordained", "sanctified", "hallowed"
        ]
        
        markers = []
        text_lower = text.lower()
        
        for word in ceremonial_words:
            if word in text_lower:
                # Find all occurrences
                positions = []
                start = 0
                while True:
                    pos = text_lower.find(word, start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                
                if positions:
                    markers.append({
                        "marker": word,
                        "occurrences": len(positions),
                        "positions": positions
                    })
        
        return markers
    
    def _detect_realm_indicators(self, text: str) -> List[Dict[str, Any]]:
        """Detect realm and domain indicators"""
        
        # Realm ID pattern (e.g., PL-001, ST-007)
        realm_ids = re.findall(r'\b[A-Z]{2}-\d{3}\b', text)
        
        # Capsule patterns (Title Case combinations)
        capsule_patterns = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Authority terms
        authority_terms = [
            "custodian", "council", "sovereign", "oracle", "guardian",
            "keeper", "warden", "steward", "regent", "chancellor"
        ]
        
        found_authorities = []
        text_lower = text.lower()
        for term in authority_terms:
            if term in text_lower:
                found_authorities.append(term)
        
        indicators = []
        
        if realm_ids:
            indicators.append({
                "type": "realm_ids",
                "values": list(set(realm_ids)),
                "count": len(realm_ids)
            })
        
        if capsule_patterns:
            indicators.append({
                "type": "capsule_references",
                "values": list(set(capsule_patterns)),
                "count": len(capsule_patterns)
            })
        
        if found_authorities:
            indicators.append({
                "type": "authority_terms",
                "values": list(set(found_authorities)),
                "count": len(found_authorities)
            })
        
        return indicators
    
    def _calculate_significance(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall significance score"""
        score = 0.0
        
        # Base score from pattern matches
        pattern_score = min(len(analysis["patterns_found"]) * 0.1, 0.3)
        
        # Symbol density contribution
        symbol_density = analysis["symbol_analysis"].get("symbol_density", 0)
        symbol_score = min(symbol_density * 100, 0.2)
        
        # Ceremonial markers boost
        ceremonial_score = min(len(analysis["ceremonial_markers"]) * 0.05, 0.2)
        
        # Realm indicators boost
        realm_score = min(len(analysis["realm_indicators"]) * 0.1, 0.3)
        
        score = pattern_score + symbol_score + ceremonial_score + realm_score
        
        return min(score, 1.0)  # Cap at 1.0
    
    def create_sigil(self, intent: str, symbols: List[str] = None) -> Dict[str, Any]:
        """Create a sigil based on intent and optional symbols"""
        
        sigil_id = CodexUtils.generate_id()
        
        # Generate sigil pattern from intent
        intent_words = intent.lower().split()
        
        # Select relevant symbols
        selected_symbols = symbols or self._select_symbols_for_intent(intent)
        
        # Create sigil structure
        sigil = {
            "sigil_id": sigil_id,
            "intent": intent,
            "symbols": selected_symbols,
            "pattern": self._generate_pattern(intent_words, selected_symbols),
            "created_at": CodexUtils.generate_timestamp(),
            "power_level": self._calculate_power_level(intent, selected_symbols),
            "activation_phrase": self._generate_activation_phrase(intent)
        }
        
        return sigil
    
    def _select_symbols_for_intent(self, intent: str) -> List[str]:
        """Select appropriate symbols based on intent"""
        intent_lower = intent.lower()
        selected = []
        
        # Royal intentions
        if any(word in intent_lower for word in ["crown", "throne", "rule", "sovereign"]):
            selected.extend(["👑", "⊰"])
        
        # Protection intentions
        if any(word in intent_lower for word in ["protect", "guard", "shield", "defend"]):
            selected.extend(["🛡️", "⚔️"])
        
        # Knowledge intentions
        if any(word in intent_lower for word in ["know", "learn", "wisdom", "understand"]):
            selected.extend(["📜", "💡"])
        
        # Power intentions
        if any(word in intent_lower for word in ["power", "strength", "force", "might"]):
            selected.extend(["⚡", "🔥"])
        
        # Default ceremonial symbols if none selected
        if not selected:
            selected = ["✦", "❋"]
        
        return selected[:3]  # Limit to 3 symbols
    
    def _generate_pattern(self, words: List[str], symbols: List[str]) -> str:
        """Generate a sigil pattern"""
        # Simple pattern: alternate symbols and key letters
        pattern_parts = []
        
        for i, symbol in enumerate(symbols):
            pattern_parts.append(symbol)
            if i < len(words):
                pattern_parts.append(words[i][0].upper())
        
        return "".join(pattern_parts)
    
    def _calculate_power_level(self, intent: str, symbols: List[str]) -> int:
        """Calculate sigil power level (1-10)"""
        base_power = 3
        
        # Intent complexity
        word_count = len(intent.split())
        complexity_bonus = min(word_count // 3, 2)
        
        # Symbol power
        symbol_bonus = len(symbols)
        
        # Special keywords
        power_words = ["sovereign", "supreme", "ultimate", "eternal", "infinite"]
        keyword_bonus = sum(1 for word in power_words if word in intent.lower())
        
        total_power = base_power + complexity_bonus + symbol_bonus + keyword_bonus
        return min(total_power, 10)
    
    def _generate_activation_phrase(self, intent: str) -> str:
        """Generate activation phrase for the sigil"""
        intent_words = intent.split()
        
        if len(intent_words) <= 3:
            return f"By this sigil, let {intent.lower()}"
        else:
            key_words = intent_words[:3]
            return f"By this sigil of {' '.join(key_words).lower()}, manifest"
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about discovered patterns"""
        total_patterns = len(self.patterns)
        active_patterns = sum(1 for p in self.patterns.values() if p.frequency > 0)
        
        # Top patterns by frequency
        top_patterns = sorted(
            self.patterns.items(), 
            key=lambda x: x[1].frequency, 
            reverse=True
        )[:5]
        
        # Pattern type distribution
        type_counts = Counter(p.pattern_type for p in self.patterns.values())
        
        return {
            "total_patterns": total_patterns,
            "active_patterns": active_patterns,
            "top_patterns": [
                {
                    "name": name,
                    "type": pattern.pattern_type,
                    "frequency": pattern.frequency,
                    "meaning": pattern.meaning
                }
                for name, pattern in top_patterns
            ],
            "pattern_types": dict(type_counts),
            "symbol_categories": list(self.symbol_registry.keys())
        }