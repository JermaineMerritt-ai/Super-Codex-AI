"""
Codex Prompts Management
Systematic prompt management for different scroll types with templating,
variables, and A/B testing capabilities.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timezone
import logging
import json
from dataclasses import dataclass, field
from enum import Enum
import re
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ScrollType(Enum):
    """Supported scroll types"""
    GENERAL = "general"
    RESUME = "resume"
    FINANCE = "finance" 
    GOVERNANCE = "governance"
    TECHNICAL = "technical"
    CEREMONIAL = "ceremonial"
    HONOR = "honor"
    CUSTOM = "custom"


class PromptVersion(Enum):
    """Prompt versioning for A/B testing"""
    STABLE = "stable"
    EXPERIMENTAL = "experimental"
    CANARY = "canary"


@dataclass
class PromptTemplate:
    """Template for prompts with variables and metadata"""
    template_id: str
    scroll_type: ScrollType
    version: PromptVersion
    template_text: str
    variables: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Extract variables from template text"""
        if not self.variables:
            self.variables = self._extract_variables()
    
    def _extract_variables(self) -> List[str]:
        """Extract {variable} placeholders from template"""
        pattern = r'\{([^}]+)\}'
        variables = re.findall(pattern, self.template_text)
        return list(set(variables))  # Remove duplicates
    
    def render(self, context: Dict[str, Any]) -> str:
        """Render template with context variables"""
        try:
            return self.template_text.format(**context)
        except KeyError as e:
            missing_var = str(e).strip("'")
            logger.warning(f"Missing variable '{missing_var}' for template {self.template_id}")
            # Return template with placeholder for missing variables
            safe_context = {var: context.get(var, f"[{var}]") for var in self.variables}
            return self.template_text.format(**safe_context)
    
    def validate(self, context: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate that all required variables are present"""
        missing = [var for var in self.variables if var not in context]
        return len(missing) == 0, missing
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "template_id": self.template_id,
            "scroll_type": self.scroll_type.value,
            "version": self.version.value,
            "template_text": self.template_text,
            "variables": self.variables,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "performance_metrics": self.performance_metrics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptTemplate":
        """Create from dictionary"""
        data["scroll_type"] = ScrollType(data["scroll_type"])
        data["version"] = PromptVersion(data["version"])
        return cls(**data)


class PromptBuilder(ABC):
    """Abstract base for prompt builders"""
    
    @abstractmethod
    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt"""
        pass
    
    @abstractmethod
    def build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build user prompt"""
        pass
    
    @abstractmethod
    def build_context_prompt(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Build context prompt from retrieved sources"""
        pass


class GeneralPromptBuilder(PromptBuilder):
    """Builder for general queries"""
    
    def __init__(self, templates: Dict[str, PromptTemplate]):
        self.templates = templates
    
    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt for general queries"""
        template = self.templates.get("general_system")
        if not template:
            return self._get_default_system_prompt()
        
        return template.render(context)
    
    def build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build user prompt for general queries"""
        template = self.templates.get("general_user")
        if not template:
            return self._get_default_user_prompt(query)
        
        prompt_context = {**context, "query": query}
        return template.render(prompt_context)
    
    def build_context_prompt(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Build context from sources"""
        template = self.templates.get("general_context")
        
        # Format sources
        formatted_sources = []
        for i, source in enumerate(sources, 1):
            source_text = f"Source {i}:\nContent: {source.get('content', 'N/A')}\nType: {source.get('document_type', 'unknown')}"
            if source.get('metadata', {}).get('file_name'):
                source_text += f"\nFile: {source['metadata']['file_name']}"
            formatted_sources.append(source_text)
        
        context_data = {
            **context,
            "sources": "\n\n".join(formatted_sources),
            "source_count": len(sources)
        }
        
        if template:
            return template.render(context_data)
        else:
            return self._get_default_context_prompt(formatted_sources)
    
    def _get_default_system_prompt(self) -> str:
        """Default system prompt"""
        return """You are the Super-Codex-AI assistant, an expert in ceremonial governance, honor systems, and the operational framework of the Codex project. 

Provide comprehensive, accurate responses based on the available documentation. When uncertain, clearly indicate limitations in your knowledge.

Always maintain the ceremonial tone and respect for the honor-based governance system."""
    
    def _get_default_user_prompt(self, query: str) -> str:
        """Default user prompt"""
        return f"""Based on the provided context from the Super-Codex-AI documentation, please answer the following question:

{query}

Provide a comprehensive answer that:
1. Directly addresses the question
2. References relevant documentation when applicable
3. Maintains appropriate ceremonial tone
4. Indicates if additional context would be helpful"""
    
    def _get_default_context_prompt(self, sources: List[str]) -> str:
        """Default context prompt"""
        return f"""Context from Super-Codex-AI documentation:

{chr(10).join(sources)}

---

Please use this context to answer the user's question."""


class ResumePromptBuilder(PromptBuilder):
    """Builder for resume-related queries"""
    
    def __init__(self, templates: Dict[str, PromptTemplate]):
        self.templates = templates
    
    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt for resume queries"""
        template = self.templates.get("resume_system")
        if not template:
            return self._get_default_system_prompt()
        
        return template.render(context)
    
    def build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build user prompt for resume queries"""
        template = self.templates.get("resume_user")
        if not template:
            return self._get_default_user_prompt(query)
        
        prompt_context = {**context, "query": query}
        return template.render(prompt_context)
    
    def build_context_prompt(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Build context for resume queries"""
        template = self.templates.get("resume_context")
        
        # Extract career and achievement related content
        career_sources = []
        achievement_sources = []
        
        for source in sources:
            content = source.get('content', '').lower()
            if any(keyword in content for keyword in ['career', 'job', 'position', 'role', 'employment']):
                career_sources.append(source)
            elif any(keyword in content for keyword in ['achievement', 'honor', 'award', 'recognition']):
                achievement_sources.append(source)
            else:
                career_sources.append(source)  # Default to career
        
        context_data = {
            **context,
            "career_info": self._format_career_sources(career_sources),
            "achievements": self._format_achievement_sources(achievement_sources),
            "total_sources": len(sources)
        }
        
        if template:
            return template.render(context_data)
        else:
            return self._get_default_context_prompt(career_sources + achievement_sources)
    
    def _format_career_sources(self, sources: List[Dict[str, Any]]) -> str:
        """Format career-related sources"""
        if not sources:
            return "No specific career information available."
        
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"Career Info {i}: {source.get('content', 'N/A')}")
        
        return "\n\n".join(formatted)
    
    def _format_achievement_sources(self, sources: List[Dict[str, Any]]) -> str:
        """Format achievement-related sources"""
        if not sources:
            return "No specific achievements documented."
        
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"Achievement {i}: {source.get('content', 'N/A')}")
        
        return "\n\n".join(formatted)
    
    def _get_default_system_prompt(self) -> str:
        """Default system prompt for resume"""
        return """You are a professional career advisor with expertise in resume writing and career development. 

Your task is to help create compelling resume content based on the available information about the person's career, achievements, and professional background.

Provide structured, professional responses that highlight strengths and accomplishments."""
    
    def _get_default_user_prompt(self, query: str) -> str:
        """Default user prompt for resume"""
        return f"""Based on the available career and achievement information, please help with the following resume request:

{query}

Please provide:
1. Specific, actionable advice
2. Professional language suggestions
3. Quantifiable accomplishments where possible
4. Industry-appropriate formatting recommendations"""
    
    def _get_default_context_prompt(self, sources: List[Dict[str, Any]]) -> str:
        """Default context prompt for resume"""
        return "Available professional background information:\n\n" + "\n\n".join(
            f"- {source.get('content', 'N/A')}" for source in sources
        )


class FinancePromptBuilder(PromptBuilder):
    """Builder for finance-related queries"""
    
    def __init__(self, templates: Dict[str, PromptTemplate]):
        self.templates = templates
    
    def build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt for finance queries"""
        template = self.templates.get("finance_system")
        if not template:
            return self._get_default_system_prompt()
        
        return template.render(context)
    
    def build_user_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build user prompt for finance queries"""
        template = self.templates.get("finance_user")
        if not template:
            return self._get_default_user_prompt(query)
        
        prompt_context = {**context, "query": query}
        return template.render(prompt_context)
    
    def build_context_prompt(self, sources: List[Dict[str, Any]], context: Dict[str, Any]) -> str:
        """Build context for finance queries"""
        template = self.templates.get("finance_context")
        
        # Categorize financial information
        budget_sources = []
        investment_sources = []
        general_sources = []
        
        for source in sources:
            content = source.get('content', '').lower()
            if any(keyword in content for keyword in ['budget', 'expense', 'cost', 'spending']):
                budget_sources.append(source)
            elif any(keyword in content for keyword in ['investment', 'roi', 'return', 'portfolio']):
                investment_sources.append(source)
            else:
                general_sources.append(source)
        
        context_data = {
            **context,
            "budget_info": self._format_financial_sources(budget_sources, "Budget"),
            "investment_info": self._format_financial_sources(investment_sources, "Investment"),
            "general_finance": self._format_financial_sources(general_sources, "General"),
            "total_sources": len(sources)
        }
        
        if template:
            return template.render(context_data)
        else:
            return self._get_default_context_prompt(sources)
    
    def _format_financial_sources(self, sources: List[Dict[str, Any]], category: str) -> str:
        """Format financial sources by category"""
        if not sources:
            return f"No {category.lower()} information available."
        
        formatted = []
        for i, source in enumerate(sources, 1):
            formatted.append(f"{category} {i}: {source.get('content', 'N/A')}")
        
        return "\n\n".join(formatted)
    
    def _get_default_system_prompt(self) -> str:
        """Default system prompt for finance"""
        return """You are a financial advisor with expertise in budgeting, investments, and financial planning.

Provide accurate, helpful financial guidance based on the available information. Always:
1. Emphasize the importance of professional financial advice for major decisions
2. Focus on general principles and educational content
3. Avoid giving specific investment recommendations
4. Maintain a responsible and conservative approach"""
    
    def _get_default_user_prompt(self, query: str) -> str:
        """Default user prompt for finance"""
        return f"""Based on the available financial information, please help with this financial question:

{query}

Please provide:
1. Educational information and general principles
2. Relevant considerations and factors to evaluate
3. Suggestions for further research or professional consultation
4. Clear disclaimers about the limitations of the advice"""
    
    def _get_default_context_prompt(self, sources: List[Dict[str, Any]]) -> str:
        """Default context prompt for finance"""
        return "Available financial information:\n\n" + "\n\n".join(
            f"- {source.get('content', 'N/A')}" for source in sources
        )


class PromptManager:
    """Central manager for prompt templates and builders"""
    
    def __init__(self, config):
        self.config = config
        self.templates: Dict[str, PromptTemplate] = {}
        self.builders: Dict[ScrollType, PromptBuilder] = {}
        
        # Performance tracking
        self.performance_tracker = {}
        
        # Initialize
        self._initialize_default_templates()
        self._initialize_builders()
    
    def _initialize_default_templates(self):
        """Initialize default prompt templates"""
        # General templates
        self.templates["general_system"] = PromptTemplate(
            template_id="general_system_v1",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="""You are the Super-Codex-AI assistant, expert in {domain} with access to comprehensive documentation.

Your role: {role}
Context: {context_type}

Provide accurate, helpful responses while maintaining the appropriate tone for the {domain} domain.""",
            metadata={"domain": "general", "optimized_for": "broad_queries"}
        )
        
        self.templates["general_user"] = PromptTemplate(
            template_id="general_user_v1",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="""Question: {query}

Please provide a comprehensive answer that:
1. Directly addresses the question
2. Uses relevant context from the documentation
3. Maintains appropriate {tone} tone
4. Indicates any limitations or areas needing clarification

Context type: {context_type}"""
        )
        
        self.templates["general_context"] = PromptTemplate(
            template_id="general_context_v1",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="""Available Documentation Context ({source_count} sources):

{sources}

---

Use this context to provide accurate, well-sourced responses."""
        )
        
        # Resume templates
        self.templates["resume_system"] = PromptTemplate(
            template_id="resume_system_v1",
            scroll_type=ScrollType.RESUME,
            version=PromptVersion.STABLE,
            template_text="""You are a professional career counselor and resume writing expert.

Specialization: {specialization}
Target role level: {target_level}
Industry focus: {industry}

Help create compelling, professional resume content that highlights achievements and aligns with modern hiring practices.""",
            metadata={"optimized_for": "professional_development"}
        )
        
        # Finance templates
        self.templates["finance_system"] = PromptTemplate(
            template_id="finance_system_v1",
            scroll_type=ScrollType.FINANCE,
            version=PromptVersion.STABLE,
            template_text="""You are a knowledgeable financial educator and advisor.

Specialty areas: {specialty_areas}
Risk tolerance context: {risk_context}
Educational focus: {education_level}

Provide educational financial guidance while emphasizing the importance of professional consultation for major decisions.""",
            metadata={"compliance": "educational_only"}
        )
    
    def _initialize_builders(self):
        """Initialize prompt builders for each scroll type"""
        self.builders[ScrollType.GENERAL] = GeneralPromptBuilder(self.templates)
        self.builders[ScrollType.RESUME] = ResumePromptBuilder(self.templates)
        self.builders[ScrollType.FINANCE] = FinancePromptBuilder(self.templates)
    
    def get_builder(self, scroll_type: ScrollType) -> PromptBuilder:
        """Get prompt builder for scroll type"""
        return self.builders.get(scroll_type, self.builders[ScrollType.GENERAL])
    
    def add_template(self, template: PromptTemplate):
        """Add or update a prompt template"""
        template.updated_at = datetime.now(timezone.utc).isoformat()
        self.templates[template.template_id] = template
        
        # Reinitialize builders if needed
        if template.scroll_type in self.builders:
            self._reinitialize_builder(template.scroll_type)
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self, scroll_type: Optional[ScrollType] = None, 
                      version: Optional[PromptVersion] = None) -> List[PromptTemplate]:
        """List templates with optional filters"""
        templates = list(self.templates.values())
        
        if scroll_type:
            templates = [t for t in templates if t.scroll_type == scroll_type]
        
        if version:
            templates = [t for t in templates if t.version == version]
        
        return sorted(templates, key=lambda t: t.updated_at, reverse=True)
    
    def build_full_prompt(self, scroll_type: ScrollType, query: str, 
                         sources: List[Dict[str, Any]], 
                         context: Dict[str, Any]) -> Dict[str, str]:
        """Build complete prompt set for a query"""
        builder = self.get_builder(scroll_type)
        
        # Set default context values
        default_context = {
            "domain": scroll_type.value,
            "role": "helpful assistant",
            "context_type": "documentation",
            "tone": "professional",
            "specialization": "general",
            "target_level": "professional",
            "industry": "technology",
            "specialty_areas": "general financial planning",
            "risk_context": "moderate",
            "education_level": "intermediate"
        }
        
        full_context = {**default_context, **context}
        
        return {
            "system": builder.build_system_prompt(full_context),
            "user": builder.build_user_prompt(query, full_context),
            "context": builder.build_context_prompt(sources, full_context)
        }
    
    def track_prompt_performance(self, template_id: str, 
                               performance_data: Dict[str, Any]):
        """Track performance metrics for a template"""
        if template_id in self.templates:
            template = self.templates[template_id]
            
            # Update performance metrics
            if "performance_metrics" not in template.performance_metrics:
                template.performance_metrics = {
                    "usage_count": 0,
                    "average_response_time": 0,
                    "satisfaction_score": 0,
                    "samples": []
                }
            
            metrics = template.performance_metrics
            metrics["usage_count"] += 1
            
            # Update averages
            if "response_time" in performance_data:
                current_avg = metrics["average_response_time"]
                new_time = performance_data["response_time"]
                metrics["average_response_time"] = (
                    (current_avg * (metrics["usage_count"] - 1) + new_time) / metrics["usage_count"]
                )
            
            # Store recent samples (keep last 100)
            metrics["samples"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **performance_data
            })
            
            if len(metrics["samples"]) > 100:
                metrics["samples"] = metrics["samples"][-100:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for all templates"""
        report = {
            "total_templates": len(self.templates),
            "by_scroll_type": {},
            "by_version": {},
            "top_performers": [],
            "needs_optimization": []
        }
        
        # Analyze by scroll type
        for scroll_type in ScrollType:
            type_templates = [t for t in self.templates.values() if t.scroll_type == scroll_type]
            if type_templates:
                report["by_scroll_type"][scroll_type.value] = {
                    "count": len(type_templates),
                    "total_usage": sum(t.performance_metrics.get("usage_count", 0) for t in type_templates)
                }
        
        # Analyze by version
        for version in PromptVersion:
            version_templates = [t for t in self.templates.values() if t.version == version]
            if version_templates:
                report["by_version"][version.value] = len(version_templates)
        
        # Find top performers and templates needing optimization
        templates_with_metrics = [
            t for t in self.templates.values() 
            if t.performance_metrics.get("usage_count", 0) > 0
        ]
        
        # Sort by usage and performance
        templates_with_metrics.sort(
            key=lambda t: (
                t.performance_metrics.get("usage_count", 0),
                -t.performance_metrics.get("average_response_time", float('inf'))
            ),
            reverse=True
        )
        
        report["top_performers"] = [
            {
                "template_id": t.template_id,
                "scroll_type": t.scroll_type.value,
                "usage_count": t.performance_metrics.get("usage_count", 0),
                "avg_response_time": t.performance_metrics.get("average_response_time", 0)
            }
            for t in templates_with_metrics[:5]
        ]
        
        # Templates with poor performance
        poor_performers = [
            t for t in templates_with_metrics
            if t.performance_metrics.get("average_response_time", 0) > 5.0  # > 5 seconds
        ]
        
        report["needs_optimization"] = [
            {
                "template_id": t.template_id,
                "scroll_type": t.scroll_type.value,
                "avg_response_time": t.performance_metrics.get("average_response_time", 0)
            }
            for t in poor_performers[:5]
        ]
        
        return report
    
    def _reinitialize_builder(self, scroll_type: ScrollType):
        """Reinitialize builder after template changes"""
        if scroll_type == ScrollType.GENERAL:
            self.builders[scroll_type] = GeneralPromptBuilder(self.templates)
        elif scroll_type == ScrollType.RESUME:
            self.builders[scroll_type] = ResumePromptBuilder(self.templates)
        elif scroll_type == ScrollType.FINANCE:
            self.builders[scroll_type] = FinancePromptBuilder(self.templates)
        # Add other builders as needed


# Example usage
if __name__ == "__main__":
    def test_prompts():
        from dataclasses import dataclass
        
        @dataclass
        class MockConfig:
            pass
        
        config = MockConfig()
        manager = PromptManager(config)
        
        # Test general prompt building
        sources = [
            {"content": "The honor system is fundamental to governance...", "document_type": "governance"},
            {"content": "Ceremonial procedures require specific protocols...", "document_type": "ceremony"}
        ]
        
        context = {"scroll_type": "general"}
        
        prompts = manager.build_full_prompt(
            ScrollType.GENERAL,
            "What is the honor system?",
            sources,
            context
        )
        
        print("System Prompt:", prompts["system"])
        print("\nUser Prompt:", prompts["user"])
        print("\nContext Prompt:", prompts["context"])
        
        # Test performance tracking
        manager.track_prompt_performance("general_system_v1", {
            "response_time": 1.2,
            "user_satisfaction": 4.5
        })
        
        report = manager.get_performance_report()
        print("\nPerformance Report:", report)
    
    test_prompts()