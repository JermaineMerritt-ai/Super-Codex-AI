# Axiom Engine - Core reasoning and ceremonial operations
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from ..core.config import CodexConfig
from ..core.audit import AuditLogger
from ..core.replay import ReplayManager
from ..core.identity import IdentityManager
from ..core.utils import CodexUtils

class AxiomEngine:
    """Core reasoning engine for ceremonial operations and governance"""
    
    def __init__(self, config: CodexConfig):
        self.config = config
        self.audit = AuditLogger(config.audit_log_path)
        self.replay = ReplayManager(config.replay_dir)
        self.identity = IdentityManager(config.identity_dir, config.seal_dir)
        
    def process_ceremony(self, actor: str, realm: str, capsule: str, 
                        intent: str, ceremony_type: str = "reasoning") -> Dict[str, Any]:
        """Process a ceremonial reasoning operation"""
        
        # Validate actor identity
        identity = self.identity.find_identity_by_name(actor)
        if not identity:
            return {
                "success": False,
                "error": "Unknown actor",
                "ceremony_id": None
            }
        
        # Verify realm access
        if not self.identity.verify_realm_access(identity.id, realm):
            return {
                "success": False,
                "error": "Insufficient realm access",
                "ceremony_id": None
            }
        
        # Verify capsule permissions
        if not self.identity.verify_capsule_permission(identity.id, capsule):
            return {
                "success": False,
                "error": "Insufficient capsule permissions",
                "ceremony_id": None
            }
        
        # Generate ceremony ID
        ceremony_id = CodexUtils.generate_ceremony_id(realm)
        
        # Create governance seal
        governance_seal = self._create_governance_seal(identity, realm, capsule)
        
        # Process the reasoning
        reasoning_result = self._execute_reasoning(intent, capsule, identity)
        
        # Record for replay
        replay_entry = self.replay.record(
            ceremony_type=ceremony_type,
            actor=actor,
            realm=realm,
            capsule=capsule,
            intent=intent,
            governance_seal=governance_seal,
            result=reasoning_result
        )
        
        # Audit log
        self.audit.log_user_action(
            user_id=actor,
            action="ceremony.execute",
            resource=f"{realm}/{capsule}",
            details={
                "ceremony_id": ceremony_id,
                "ceremony_type": ceremony_type,
                "intent": intent,
                "replay_id": replay_entry.id
            }
        )
        
        return {
            "success": True,
            "ceremony_id": ceremony_id,
            "replay_id": replay_entry.id,
            "governance_seal": governance_seal,
            "result": reasoning_result
        }
    
    def _create_governance_seal(self, identity, realm: str, capsule: str) -> Dict[str, Any]:
        """Create governance seal for the ceremony"""
        return {
            "seal_id": CodexUtils.generate_id(),
            "authority": identity.authority_level,
            "classification": identity.seal_classification,
            "realm": realm,
            "capsule": capsule,
            "timestamp": CodexUtils.generate_timestamp(),
            "actor_type": identity.type
        }
    
    def _execute_reasoning(self, intent: str, capsule: str, identity) -> Dict[str, Any]:
        """Execute the core reasoning process"""
        
        # Basic reasoning framework
        reasoning_steps = [
            self._analyze_intent(intent),
            self._evaluate_context(capsule, identity),
            self._generate_insights(intent, capsule),
            self._formulate_response(intent, capsule, identity)
        ]
        
        return {
            "intent_analysis": reasoning_steps[0],
            "context_evaluation": reasoning_steps[1],
            "insights": reasoning_steps[2],
            "response": reasoning_steps[3],
            "reasoning_chain": [step["summary"] for step in reasoning_steps],
            "confidence": self._calculate_confidence(reasoning_steps)
        }
    
    def _analyze_intent(self, intent: str) -> Dict[str, Any]:
        """Analyze the intent of the reasoning request"""
        # Simple intent classification
        intent_lower = intent.lower()
        
        if "invoke" in intent_lower or "summon" in intent_lower:
            category = "invocation"
        elif "analyze" in intent_lower or "examine" in intent_lower:
            category = "analysis"
        elif "create" in intent_lower or "generate" in intent_lower:
            category = "creation"
        elif "decide" in intent_lower or "choose" in intent_lower:
            category = "decision"
        else:
            category = "general"
        
        return {
            "category": category,
            "complexity": len(intent.split()),
            "keywords": intent.split(),
            "summary": f"Intent classified as {category} with {len(intent.split())} elements"
        }
    
    def _evaluate_context(self, capsule: str, identity) -> Dict[str, Any]:
        """Evaluate the contextual factors"""
        return {
            "capsule": capsule,
            "actor_authority": identity.authority_level,
            "actor_type": identity.type,
            "permissions": len(identity.capsule_permissions),
            "realm_access": len(identity.realm_access),
            "summary": f"Context evaluated for {identity.type} with authority {identity.authority_level}"
        }
    
    def _generate_insights(self, intent: str, capsule: str) -> List[str]:
        """Generate insights based on intent and capsule"""
        insights = []
        
        # Basic insight generation
        if "sovereign" in capsule.lower():
            insights.append("Sovereign capsule detected - high ceremonial significance")
        
        if len(intent) > 50:
            insights.append("Complex intent requires multi-step reasoning")
        
        if "crown" in intent.lower() or "throne" in intent.lower():
            insights.append("Royal symbolism present - elevated ceremonial context")
        
        if not insights:
            insights.append("Standard ceremonial processing applies")
        
        return insights
    
    def _formulate_response(self, intent: str, capsule: str, identity) -> Dict[str, Any]:
        """Formulate the ceremonial response"""
        return {
            "acknowledgment": f"Ceremonial reasoning completed for {capsule}",
            "processing_note": f"Intent '{intent}' processed under {identity.type} authority",
            "recommendations": [
                "Ceremony recorded in replay archive",
                "Governance seal applied",
                "Audit trail established"
            ],
            "next_steps": [
                "Review ceremonial outcome",
                "Consider follow-up ceremonies if needed",
                "Update realm status if applicable"
            ]
        }
    
    def _calculate_confidence(self, reasoning_steps: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for the reasoning process"""
        # Simple confidence calculation based on completeness
        base_confidence = 0.7
        
        # Boost confidence if all steps completed successfully
        if len(reasoning_steps) == 4:
            base_confidence += 0.2
        
        # Cap at 0.95 to maintain uncertainty
        return min(base_confidence, 0.95)
    
    def get_ceremony_history(self, actor: str = None, realm: str = None,
                           limit: int = 10) -> List[Dict[str, Any]]:
        """Get ceremony history with optional filters"""
        replays = self.replay.get_replays(
            actor=actor,
            realm=realm,
            limit=limit
        )
        
        return [
            {
                "ceremony_id": replay.id,
                "timestamp": replay.timestamp,
                "actor": replay.actor,
                "realm": replay.realm,
                "capsule": replay.capsule,
                "intent": replay.intent,
                "ceremony_type": replay.ceremony_type
            }
            for replay in replays
        ]
    
    def validate_ceremony_request(self, actor: str, realm: str, 
                                 capsule: str) -> Dict[str, Any]:
        """Validate a ceremony request without executing"""
        identity = self.identity.find_identity_by_name(actor)
        
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not identity:
            validation["valid"] = False
            validation["errors"].append("Unknown actor")
        else:
            if not self.identity.verify_realm_access(identity.id, realm):
                validation["valid"] = False
                validation["errors"].append("Insufficient realm access")
            
            if not self.identity.verify_capsule_permission(identity.id, capsule):
                validation["valid"] = False
                validation["errors"].append("Insufficient capsule permissions")
            
            if identity.authority_level < 2 and "sovereign" in capsule.lower():
                validation["warnings"].append("Low authority for sovereign capsule")
        
        return validation