"""
Codex Scroll Capsule System
Manages ceremonial capsules and their associated scroll generation capabilities.
Integrates with the honor system and governance framework.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timezone
import logging
import json
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Import engine components
sys.path.insert(0, str(Path(__file__).parent.parent))
from engine.models.prompts import ScrollType, PromptManager

logger = logging.getLogger(__name__)


class CapsuleType(Enum):
    """Types of ceremonial capsules"""
    SOVEREIGN = "sovereign"
    GUARDIAN = "guardian"
    SCHOLAR = "scholar"
    ARTIFICER = "artificer"
    HERALD = "herald"
    STEWARD = "steward"
    MENTOR = "mentor"
    CUSTOM = "custom"


class AccessLevel(Enum):
    """Access levels for capsules"""
    PUBLIC = "public"
    MEMBER = "member"
    CUSTODIAN = "custodian"
    COUNCIL = "council"
    SOVEREIGN = "sovereign"
    RESTRICTED = "restricted"


@dataclass
class CeremonialContext:
    """Context for ceremonial capsule usage"""
    actor: Optional[str] = None
    realm: Optional[str] = None
    authority_level: str = "standard"
    ceremony_type: Optional[str] = None
    significance: str = "routine"
    honor_implications: Optional[str] = None
    governance_level: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "actor": self.actor,
            "realm": self.realm,
            "authority_level": self.authority_level,
            "ceremony_type": self.ceremony_type,
            "significance": self.significance,
            "honor_implications": self.honor_implications,
            "governance_level": self.governance_level
        }


@dataclass 
class CapsuleDefinition:
    """Definition of a ceremonial capsule"""
    capsule_id: str
    name: str
    capsule_type: CapsuleType
    scroll_type: ScrollType
    access_level: AccessLevel
    template_path: str
    description: str = ""
    realm_id: Optional[str] = None
    ceremonial_requirements: Dict[str, Any] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            "capsule_id": self.capsule_id,
            "name": self.name,
            "capsule_type": self.capsule_type.value,
            "scroll_type": self.scroll_type.value,
            "access_level": self.access_level.value,
            "template_path": self.template_path,
            "description": self.description,
            "realm_id": self.realm_id,
            "ceremonial_requirements": self.ceremonial_requirements,
            "configuration": self.configuration,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "active": self.active
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CapsuleDefinition":
        """Create from dictionary"""
        data["capsule_type"] = CapsuleType(data["capsule_type"])
        data["scroll_type"] = ScrollType(data["scroll_type"])
        data["access_level"] = AccessLevel(data["access_level"])
        return cls(**data)


class CapsuleRegistry:
    """Registry for managing ceremonial capsules"""
    
    def __init__(self, config):
        self.config = config
        self.capsules: Dict[str, CapsuleDefinition] = {}
        self.realm_capsules: Dict[str, List[str]] = {}
        self.registry_path = config.capsule_registry_path
        
        # Ensure registry directory exists
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing capsules
        self._load_registry()
        
        # Initialize default capsules if registry is empty
        if not self.capsules:
            self._initialize_default_capsules()
    
    def _load_registry(self):
        """Load capsule registry from disk"""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    registry_data = json.load(f)
                
                for capsule_data in registry_data.get("capsules", []):
                    capsule = CapsuleDefinition.from_dict(capsule_data)
                    self.capsules[capsule.capsule_id] = capsule
                    
                    # Update realm index
                    if capsule.realm_id:
                        if capsule.realm_id not in self.realm_capsules:
                            self.realm_capsules[capsule.realm_id] = []
                        self.realm_capsules[capsule.realm_id].append(capsule.capsule_id)
                
                logger.info(f"Loaded {len(self.capsules)} capsules from registry")
                
            except Exception as e:
                logger.error(f"Failed to load capsule registry: {e}")
    
    def _save_registry(self):
        """Save capsule registry to disk"""
        try:
            registry_data = {
                "version": "1.0",
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "capsules": [capsule.to_dict() for capsule in self.capsules.values()]
            }
            
            with open(self.registry_path, 'w') as f:
                json.dump(registry_data, f, indent=2)
            
            logger.debug(f"Saved {len(self.capsules)} capsules to registry")
            
        except Exception as e:
            logger.error(f"Failed to save capsule registry: {e}")
    
    def _initialize_default_capsules(self):
        """Initialize default ceremonial capsules"""
        default_capsules = [
            CapsuleDefinition(
                capsule_id="sovereign_crown",
                name="Sovereign Crown",
                capsule_type=CapsuleType.SOVEREIGN,
                scroll_type=ScrollType.GOVERNANCE,
                access_level=AccessLevel.SOVEREIGN,
                template_path="governance101_scroll.jinja",
                description="Supreme governance capsule for constitutional matters",
                realm_id="PL-001",
                ceremonial_requirements={
                    "minimum_authority": "council",
                    "consensus_required": True,
                    "audit_trail": True
                },
                configuration={
                    "formal_tone": True,
                    "ceremonial_language": "high",
                    "validation_required": True
                }
            ),
            CapsuleDefinition(
                capsule_id="guardian_protocols",
                name="Guardian Protocols", 
                capsule_type=CapsuleType.GUARDIAN,
                scroll_type=ScrollType.GENERAL,
                access_level=AccessLevel.CUSTODIAN,
                template_path="general_scroll.jinja",
                description="Guardian-level operational and maintenance guidance",
                realm_id="ST-007",
                ceremonial_requirements={
                    "minimum_authority": "custodian",
                    "specialization_check": True
                },
                configuration={
                    "practical_focus": True,
                    "technical_detail": "high"
                }
            ),
            CapsuleDefinition(
                capsule_id="scholar_archives",
                name="Scholar Archives",
                capsule_type=CapsuleType.SCHOLAR,
                scroll_type=ScrollType.GENERAL,
                access_level=AccessLevel.MEMBER,
                template_path="general_scroll.jinja",
                description="Scholarly research and knowledge preservation",
                realm_id="ED-003",
                ceremonial_requirements={
                    "documentation_standards": True,
                    "peer_review": "encouraged"
                },
                configuration={
                    "academic_tone": True,
                    "comprehensive_sources": True
                }
            ),
            CapsuleDefinition(
                capsule_id="career_advancement",
                name="Career Advancement Capsule",
                capsule_type=CapsuleType.MENTOR,
                scroll_type=ScrollType.RESUME,
                access_level=AccessLevel.PUBLIC,
                template_path="resume_scroll.jinja",
                description="Professional development and career guidance",
                configuration={
                    "professional_focus": True,
                    "practical_advice": True,
                    "industry_adaptation": True
                }
            ),
            CapsuleDefinition(
                capsule_id="financial_wisdom",
                name="Financial Wisdom Capsule",
                capsule_type=CapsuleType.STEWARD,
                scroll_type=ScrollType.FINANCE,
                access_level=AccessLevel.PUBLIC,
                template_path="finance_scroll.jinja",
                description="Financial education and planning guidance",
                configuration={
                    "educational_focus": True,
                    "risk_awareness": True,
                    "disclaimer_emphasis": True
                }
            )
        ]
        
        for capsule in default_capsules:
            self.register_capsule(capsule)
        
        logger.info(f"Initialized {len(default_capsules)} default capsules")
    
    def register_capsule(self, capsule: CapsuleDefinition):
        """Register a new capsule"""
        self.capsules[capsule.capsule_id] = capsule
        
        # Update realm index
        if capsule.realm_id:
            if capsule.realm_id not in self.realm_capsules:
                self.realm_capsules[capsule.realm_id] = []
            if capsule.capsule_id not in self.realm_capsules[capsule.realm_id]:
                self.realm_capsules[capsule.realm_id].append(capsule.capsule_id)
        
        self._save_registry()
        logger.info(f"Registered capsule: {capsule.name} ({capsule.capsule_id})")
    
    def get_capsule(self, capsule_id: str) -> Optional[CapsuleDefinition]:
        """Get capsule by ID"""
        return self.capsules.get(capsule_id)
    
    def list_capsules(self, realm_id: Optional[str] = None,
                     capsule_type: Optional[CapsuleType] = None,
                     access_level: Optional[AccessLevel] = None,
                     active_only: bool = True) -> List[CapsuleDefinition]:
        """List capsules with optional filters"""
        capsules = list(self.capsules.values())
        
        if active_only:
            capsules = [c for c in capsules if c.active]
        
        if realm_id:
            capsules = [c for c in capsules if c.realm_id == realm_id]
        
        if capsule_type:
            capsules = [c for c in capsules if c.capsule_type == capsule_type]
        
        if access_level:
            capsules = [c for c in capsules if c.access_level == access_level]
        
        return sorted(capsules, key=lambda c: c.name)
    
    def get_realm_capsules(self, realm_id: str) -> List[CapsuleDefinition]:
        """Get all capsules for a realm"""
        capsule_ids = self.realm_capsules.get(realm_id, [])
        return [self.capsules[cid] for cid in capsule_ids if cid in self.capsules]
    
    def check_access(self, capsule_id: str, user_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Check if user has access to capsule"""
        capsule = self.get_capsule(capsule_id)
        if not capsule:
            return False, "Capsule not found"
        
        if not capsule.active:
            return False, "Capsule is not active"
        
        # Basic access level check (in production, integrate with auth system)
        user_level = user_context.get("authority_level", "public")
        
        access_hierarchy = {
            "public": 0,
            "member": 1,
            "custodian": 2,
            "council": 3,
            "sovereign": 4,
            "restricted": 5
        }
        
        required_level = access_hierarchy.get(capsule.access_level.value, 5)
        user_access = access_hierarchy.get(user_level, 0)
        
        if user_access < required_level:
            return False, f"Requires {capsule.access_level.value} level access"
        
        # Check ceremonial requirements
        if capsule.ceremonial_requirements:
            min_auth = capsule.ceremonial_requirements.get("minimum_authority")
            if min_auth and access_hierarchy.get(user_level, 0) < access_hierarchy.get(min_auth, 5):
                return False, f"Requires minimum authority: {min_auth}"
        
        return True, "Access granted"


class ScrollGenerator:
    """Generates scrolls using capsules and templates"""
    
    def __init__(self, config, capsule_registry: CapsuleRegistry, 
                 prompt_manager: PromptManager):
        self.config = config
        self.capsule_registry = capsule_registry
        self.prompt_manager = prompt_manager
        
        # Initialize Jinja2 environment
        self.template_env = Environment(
            loader=FileSystemLoader(config.scroll_templates_path),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._add_custom_filters()
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters"""
        self.template_env.filters['timestamp'] = lambda x: x.strftime('%Y-%m-%d %H:%M:%S UTC') if x else 'N/A'
        self.template_env.filters['excerpt'] = lambda text, length=100: text[:length] + '...' if len(text) > length else text
        self.template_env.filters['title_case'] = lambda text: text.replace('_', ' ').title() if text else ''
    
    async def generate_scroll(self, capsule_id: str, query: str,
                             sources: List[Dict[str, Any]],
                             rag_result: Dict[str, Any],
                             user_context: Dict[str, Any] = None,
                             ceremonial_context: CeremonialContext = None) -> Dict[str, Any]:
        """Generate scroll using specified capsule"""
        try:
            # Get capsule definition
            capsule = self.capsule_registry.get_capsule(capsule_id)
            if not capsule:
                raise ValueError(f"Capsule not found: {capsule_id}")
            
            # Check access
            access_granted, access_msg = self.capsule_registry.check_access(
                capsule_id, user_context or {}
            )
            if not access_granted:
                raise PermissionError(f"Access denied: {access_msg}")
            
            # Load template
            try:
                template = self.template_env.get_template(capsule.template_path)
            except Exception as e:
                logger.error(f"Failed to load template {capsule.template_path}: {e}")
                # Fallback to general template
                template = self.template_env.get_template("general_scroll.jinja")
            
            # Prepare template context
            template_context = await self._build_template_context(
                capsule, query, sources, rag_result, user_context, ceremonial_context
            )
            
            # Render scroll
            start_time = datetime.now(timezone.utc)
            scroll_content = template.render(**template_context)
            generation_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            # Generate scroll metadata
            scroll_metadata = {
                "scroll_id": self._generate_scroll_id(capsule_id),
                "capsule_id": capsule_id,
                "capsule_name": capsule.name,
                "scroll_type": capsule.scroll_type.value,
                "query": query,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generation_time": generation_time,
                "template_path": capsule.template_path,
                "sources_count": len(sources),
                "user_context": user_context,
                "ceremonial_context": ceremonial_context.to_dict() if ceremonial_context else None,
                "rag_metadata": {
                    "confidence_score": rag_result.get("confidence_score"),
                    "processing_time": rag_result.get("processing_time"),
                    "vector_results": rag_result.get("vector_results_count")
                }
            }
            
            logger.info(f"Generated scroll {scroll_metadata['scroll_id']} using capsule {capsule.name}")
            
            return {
                "success": True,
                "scroll_content": scroll_content,
                "scroll_metadata": scroll_metadata,
                "capsule_info": {
                    "name": capsule.name,
                    "type": capsule.capsule_type.value,
                    "access_level": capsule.access_level.value
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate scroll with capsule {capsule_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "capsule_id": capsule_id
            }
    
    async def _build_template_context(self, capsule: CapsuleDefinition,
                                    query: str, sources: List[Dict[str, Any]],
                                    rag_result: Dict[str, Any],
                                    user_context: Dict[str, Any],
                                    ceremonial_context: CeremonialContext) -> Dict[str, Any]:
        """Build context for template rendering"""
        # Base context
        context = {
            "query": query,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "main_response": rag_result.get("response", "Response not available"),
            "sources": sources,
            "confidence_score": rag_result.get("confidence_score", 0),
            "processing_time": rag_result.get("processing_time", 0),
            "vector_results_count": rag_result.get("vector_results_count", 0),
            "rag_version": "1.0"
        }
        
        # Add capsule configuration
        context.update(capsule.configuration)
        
        # Add ceremonial context
        if ceremonial_context:
            context["scroll_context"] = ceremonial_context.to_dict()
            context["ceremonial_significance"] = ceremonial_context.significance
            context["authority_level"] = ceremonial_context.authority_level
            context["governance_level"] = ceremonial_context.governance_level
        
        # Add user context
        if user_context:
            context["user_context"] = user_context
            context["guidance_level"] = user_context.get("guidance_level", "standard")
            context["industry_focus"] = user_context.get("industry", "general")
            context["risk_level"] = user_context.get("risk_tolerance", "moderate")
        
        # Scroll-specific context building
        if capsule.scroll_type == ScrollType.RESUME:
            context.update(await self._build_resume_context(sources, rag_result))
        elif capsule.scroll_type == ScrollType.FINANCE:
            context.update(await self._build_finance_context(sources, rag_result))
        elif capsule.scroll_type == ScrollType.GOVERNANCE:
            context.update(await self._build_governance_context(sources, rag_result, ceremonial_context))
        
        # Generate unique IDs
        context["generation_id"] = self._generate_scroll_id(capsule.capsule_id)
        
        return context
    
    async def _build_resume_context(self, sources: List[Dict[str, Any]], 
                                  rag_result: Dict[str, Any]) -> Dict[str, Any]:
        """Build context specific to resume scrolls"""
        career_data = []
        achievements = []
        
        # Extract career and achievement information from sources
        for source in sources:
            content = source.get('content', '').lower()
            
            # Mock career data extraction (in production, use NLP)
            if any(keyword in content for keyword in ['career', 'job', 'position', 'role']):
                career_data.append({
                    "title": "Professional Experience",
                    "organization": source.get('metadata', {}).get('file_name', 'Unknown'),
                    "description": source.get('content', '')[:200] + '...'
                })
            
            if any(keyword in content for keyword in ['achievement', 'honor', 'award']):
                achievements.append({
                    "category": "Professional Achievement",
                    "title": source.get('metadata', {}).get('file_name', 'Achievement'),
                    "description": source.get('content', '')[:150] + '...'
                })
        
        return {
            "career_data": career_data,
            "achievements": achievements,
            "resume_recommendations": {
                "summary": ["Highlight quantifiable achievements", "Use action verbs"],
                "experience": ["Focus on results and impact", "Show progression"]
            },
            "next_steps": [
                "Review and update content regularly",
                "Tailor for specific opportunities",
                "Seek professional feedback"
            ]
        }
    
    async def _build_finance_context(self, sources: List[Dict[str, Any]], 
                                   rag_result: Dict[str, Any]) -> Dict[str, Any]:
        """Build context specific to finance scrolls"""
        financial_data = []
        
        # Extract financial information from sources
        for source in sources:
            content = source.get('content', '').lower()
            if any(keyword in content for keyword in ['budget', 'finance', 'money', 'investment']):
                financial_data.append({
                    "category": "Financial Information",
                    "description": source.get('content', '')[:200] + '...'
                })
        
        return {
            "financial_data": financial_data,
            "consultation_areas": [
                "Complex investment strategy",
                "Tax optimization planning",
                "Estate planning considerations"
            ],
            "next_steps": [
                "Assess current financial position",
                "Define clear financial goals",
                "Consult qualified professionals"
            ]
        }
    
    async def _build_governance_context(self, sources: List[Dict[str, Any]], 
                                      rag_result: Dict[str, Any],
                                      ceremonial_context: CeremonialContext) -> Dict[str, Any]:
        """Build context specific to governance scrolls"""
        honor_system_data = []
        authority_structure = []
        realm_data = []
        ceremonial_protocols = []
        
        # Extract governance information from sources
        for source in sources:
            content = source.get('content', '').lower()
            
            if any(keyword in content for keyword in ['honor', 'achievement', 'recognition']):
                honor_system_data.append({
                    "title": "Honor System Component",
                    "description": source.get('content', '')[:300] + '...'
                })
            
            if any(keyword in content for keyword in ['governance', 'authority', 'council']):
                authority_structure.append({
                    "title": "Governance Role",
                    "description": source.get('content', '')[:200] + '...'
                })
            
            if any(keyword in content for keyword in ['ceremony', 'protocol', 'ritual']):
                ceremonial_protocols.append({
                    "name": "Ceremonial Protocol",
                    "description": source.get('content', '')[:200] + '...'
                })
        
        # Mock realm data based on ceremonial context
        if ceremonial_context and ceremonial_context.realm:
            realm_data = [{
                "id": ceremonial_context.realm,
                "name": f"Realm {ceremonial_context.realm}",
                "status": "Active",
                "description": "Governance realm with ceremonial protocols"
            }]
        
        return {
            "honor_system_data": honor_system_data,
            "authority_structure": authority_structure,
            "realm_data": realm_data,
            "ceremonial_protocols": ceremonial_protocols,
            "learning_paths": [{
                "title": "Governance Foundation",
                "audience": "All participants",
                "description": "Basic governance principles and honor system"
            }]
        }
    
    def _generate_scroll_id(self, capsule_id: str) -> str:
        """Generate unique scroll ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        capsule_hash = hashlib.md5(capsule_id.encode()).hexdigest()[:6]
        return f"scroll_{timestamp}_{capsule_hash}"


# Example usage
if __name__ == "__main__":
    async def test_capsule_system():
        from dataclasses import dataclass
        from engine.config import CodexConfig
        from engine.models.prompts import PromptManager
        
        config = CodexConfig()
        registry = CapsuleRegistry(config)
        prompt_manager = PromptManager(config)
        generator = ScrollGenerator(config, registry, prompt_manager)
        
        # Test capsule listing
        capsules = registry.list_capsules()
        print(f"Available capsules: {[c.name for c in capsules]}")
        
        # Test scroll generation
        sources = [{"content": "Test governance content", "metadata": {"file_name": "test.md"}}]
        rag_result = {"response": "Test response", "confidence_score": 85, "processing_time": 1.2}
        
        result = await generator.generate_scroll(
            "sovereign_crown",
            "What is the governance system?",
            sources,
            rag_result,
            {"authority_level": "council"},
            CeremonialContext(actor="Test Council", realm="PL-001")
        )
        
        if result["success"]:
            print(f"Generated scroll: {result['scroll_metadata']['scroll_id']}")
        else:
            print(f"Failed to generate scroll: {result['error']}")
    
    asyncio.run(test_capsule_system())