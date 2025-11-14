# axiom_parser.py - Python AXIOM Intent Parser for Sovereign Commerce Platform
# Part of the AXIOM-FLAME multi-engine architecture

from typing import Dict, List
from dataclasses import dataclass
import re

@dataclass
class ParsedIntent:
    """Structured intent data extracted from natural language invocations"""
    app_type: str
    audience: List[str]
    modules: List[str]
    style: List[str]

class AxiomIntentParser:
    """AXIOM engine for parsing natural language invocations into structured intents"""
    
    def __init__(self):
        self.module_patterns = {
            "product_catalog": r"catalog|products?|inventory",
            "checkout": r"checkout|payment|purchase|buy",
            "funder_dashboard": r"dashboard|analytics|insights|metrics",
            "contributor_recognition": r"recognition|honor|achievement|contributor"
        }
        
        self.style_patterns = {
            "mythic": r"sovereign|royal|divine|sacred",
            "ceremonial": r"scroll|ceremony|ritual|formal"
        }
        
        self.audience_patterns = {
            "diaspora funders": r"diaspora\s+funders?|diaspora\s+investors?",
            "general": r"general|public|all|everyone"
        }

    def parse_invocation(self, phrase: str) -> ParsedIntent:
        """Parse a natural language phrase into structured intent"""
        lower_phrase = phrase.lower()
        
        # Determine app type
        app_type = "e-commerce" if "commerce" in lower_phrase else "generic-app"
        
        # Extract audience
        audience = []
        for aud, pattern in self.audience_patterns.items():
            if re.search(pattern, lower_phrase):
                audience.append(aud)
        if not audience:
            audience = ["general"]
        
        # Extract modules
        modules = []
        for module, pattern in self.module_patterns.items():
            if re.search(pattern, lower_phrase):
                modules.append(module)
        
        # Extract style
        style = []
        for style_name, pattern in self.style_patterns.items():
            if re.search(pattern, lower_phrase):
                style.append(style_name)
        
        return ParsedIntent(
            app_type=app_type,
            audience=audience,
            modules=modules,
            style=style
        )

    def to_dict(self, intent: ParsedIntent) -> Dict:
        """Convert ParsedIntent to dictionary for JSON serialization"""
        return {
            "appType": intent.app_type,
            "audience": intent.audience,
            "modules": intent.modules,
            "style": intent.style
        }

    def analyze_phrase(self, phrase: str) -> Dict:
        """Complete analysis of a phrase returning structured data"""
        intent = self.parse_invocation(phrase)
        return {
            "original_phrase": phrase,
            "parsed_intent": self.to_dict(intent),
            "confidence": self._calculate_confidence(intent),
            "recommendations": self._get_recommendations(intent)
        }

    def _calculate_confidence(self, intent: ParsedIntent) -> float:
        """Calculate confidence score based on detected patterns"""
        score = 0.5  # Base score
        if intent.modules:
            score += 0.3 * len(intent.modules) / 4  # Up to 0.3 for all modules
        if intent.style:
            score += 0.1 * len(intent.style) / 2   # Up to 0.1 for all styles
        if "diaspora funders" in intent.audience:
            score += 0.1  # Specific audience bonus
        return min(score, 1.0)

    def _get_recommendations(self, intent: ParsedIntent) -> List[str]:
        """Generate recommendations based on parsed intent"""
        recommendations = []
        
        if intent.app_type == "e-commerce" and not intent.modules:
            recommendations.append("Consider adding specific modules like catalog or checkout")
        
        if "diaspora funders" in intent.audience and "funder_dashboard" not in intent.modules:
            recommendations.append("Diaspora funders would benefit from a specialized dashboard")
        
        if intent.style and "contributor_recognition" not in intent.modules:
            recommendations.append("Ceremonial/mythic styles pair well with recognition systems")
        
        return recommendations

# Global parser instance
axiom_parser = AxiomIntentParser()

def parse_invocation(phrase: str) -> Dict:
    """Convenience function for quick parsing"""
    return axiom_parser.analyze_phrase(phrase)

# Test function
def test_axiom_parser():
    """Test the AXIOM parser with various phrases"""
    test_phrases = [
        "sovereign commerce scroll for diaspora funders",
        "create catalog and checkout system",
        "dashboard with recognition features", 
        "ceremonial sovereign platform",
        "simple product catalog",
        "diaspora funder analytics dashboard"
    ]
    
    print("🧪 AXIOM Intent Parser Tests")
    print("=" * 50)
    
    for phrase in test_phrases:
        print(f"\n🔍 Testing: '{phrase}'")
        result = parse_invocation(phrase)
        print(f"📊 Intent: {result['parsed_intent']}")
        print(f"🎯 Confidence: {result['confidence']:.2f}")
        if result['recommendations']:
            print(f"💡 Recommendations: {result['recommendations']}")

if __name__ == "__main__":
    test_axiom_parser()