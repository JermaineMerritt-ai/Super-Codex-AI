"""
Test suite for the Super-Codex-AI Scroll system
Comprehensive tests for scroll generation, capsule management, and templating.
"""

import pytest
import asyncio
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, List, Any
from datetime import datetime, timezone

# Import the modules to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrolls.capsule import (
    CapsuleType, AccessLevel, CeremonialContext, CapsuleDefinition,
    CapsuleRegistry, ScrollGenerator
)
from scrolls.realtime import (
    EventType, ConnectionState, RealtimeEvent, UserConnection,
    ScrollSession, RealtimeScrollManager
)
from engine.models.prompts import (
    ScrollType, PromptVersion, PromptTemplate, PromptManager
)


class TestCeremonialContext:
    """Test ceremonial context functionality"""
    
    def test_initialization(self):
        """Test basic initialization"""
        context = CeremonialContext(
            actor="Test Custodian",
            realm="PL-001",
            authority_level="council",
            significance="high"
        )
        
        assert context.actor == "Test Custodian"
        assert context.realm == "PL-001"
        assert context.authority_level == "council"
        assert context.significance == "high"
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        context = CeremonialContext(
            actor="Test Actor",
            realm="ST-007",
            ceremony_type="recognition"
        )
        
        data = context.to_dict()
        
        assert isinstance(data, dict)
        assert data["actor"] == "Test Actor"
        assert data["realm"] == "ST-007"
        assert data["ceremony_type"] == "recognition"
        assert "authority_level" in data
    
    def test_default_values(self):
        """Test default values"""
        context = CeremonialContext()
        
        assert context.actor is None
        assert context.authority_level == "standard"
        assert context.significance == "routine"


class TestCapsuleDefinition:
    """Test capsule definition functionality"""
    
    def test_initialization(self):
        """Test capsule definition initialization"""
        capsule = CapsuleDefinition(
            capsule_id="test_capsule",
            name="Test Capsule",
            capsule_type=CapsuleType.SCHOLAR,
            scroll_type=ScrollType.GENERAL,
            access_level=AccessLevel.PUBLIC,
            template_path="general_scroll.jinja",
            description="Test capsule for unit tests"
        )
        
        assert capsule.capsule_id == "test_capsule"
        assert capsule.name == "Test Capsule"
        assert capsule.capsule_type == CapsuleType.SCHOLAR
        assert capsule.scroll_type == ScrollType.GENERAL
        assert capsule.access_level == AccessLevel.PUBLIC
        assert capsule.active is True
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        capsule = CapsuleDefinition(
            capsule_id="test",
            name="Test",
            capsule_type=CapsuleType.GUARDIAN,
            scroll_type=ScrollType.TECHNICAL,
            access_level=AccessLevel.CUSTODIAN,
            template_path="test.jinja"
        )
        
        data = capsule.to_dict()
        
        assert isinstance(data, dict)
        assert data["capsule_id"] == "test"
        assert data["capsule_type"] == "guardian"
        assert data["scroll_type"] == "technical"
        assert data["access_level"] == "custodian"
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "capsule_id": "test",
            "name": "Test",
            "capsule_type": "scholar",
            "scroll_type": "general",
            "access_level": "public",
            "template_path": "test.jinja",
            "description": "Test capsule",
            "active": True,
            "ceremonial_requirements": {},
            "configuration": {},
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "realm_id": None
        }
        
        capsule = CapsuleDefinition.from_dict(data)
        
        assert capsule.capsule_id == "test"
        assert capsule.capsule_type == CapsuleType.SCHOLAR
        assert capsule.scroll_type == ScrollType.GENERAL
        assert capsule.access_level == AccessLevel.PUBLIC


class TestCapsuleRegistry:
    """Test capsule registry functionality"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_config(self, temp_dir):
        """Mock configuration"""
        config = Mock()
        config.capsule_registry_path = temp_dir / "capsules.json"
        return config
    
    @pytest.fixture
    def registry(self, mock_config):
        """Create capsule registry for testing"""
        with patch.object(CapsuleRegistry, '_initialize_default_capsules'):
            return CapsuleRegistry(mock_config)
    
    def test_initialization(self, registry):
        """Test registry initialization"""
        assert isinstance(registry.capsules, dict)
        assert isinstance(registry.realm_capsules, dict)
    
    def test_register_capsule(self, registry):
        """Test capsule registration"""
        capsule = CapsuleDefinition(
            capsule_id="test_capsule",
            name="Test Capsule",
            capsule_type=CapsuleType.SCHOLAR,
            scroll_type=ScrollType.GENERAL,
            access_level=AccessLevel.PUBLIC,
            template_path="test.jinja",
            realm_id="ED-003"
        )
        
        registry.register_capsule(capsule)
        
        assert "test_capsule" in registry.capsules
        assert registry.capsules["test_capsule"] == capsule
        assert "ED-003" in registry.realm_capsules
        assert "test_capsule" in registry.realm_capsules["ED-003"]
    
    def test_get_capsule(self, registry):
        """Test getting capsule by ID"""
        capsule = CapsuleDefinition(
            capsule_id="test",
            name="Test",
            capsule_type=CapsuleType.SCHOLAR,
            scroll_type=ScrollType.GENERAL,
            access_level=AccessLevel.PUBLIC,
            template_path="test.jinja"
        )
        
        registry.register_capsule(capsule)
        
        retrieved = registry.get_capsule("test")
        assert retrieved == capsule
        
        not_found = registry.get_capsule("nonexistent")
        assert not_found is None
    
    def test_list_capsules_with_filters(self, registry):
        """Test listing capsules with filters"""
        capsules = [
            CapsuleDefinition(
                capsule_id="scholar1",
                name="Scholar 1",
                capsule_type=CapsuleType.SCHOLAR,
                scroll_type=ScrollType.GENERAL,
                access_level=AccessLevel.PUBLIC,
                template_path="test.jinja",
                realm_id="ED-003"
            ),
            CapsuleDefinition(
                capsule_id="guardian1",
                name="Guardian 1",
                capsule_type=CapsuleType.GUARDIAN,
                scroll_type=ScrollType.TECHNICAL,
                access_level=AccessLevel.CUSTODIAN,
                template_path="test.jinja",
                realm_id="ST-007"
            ),
            CapsuleDefinition(
                capsule_id="inactive",
                name="Inactive",
                capsule_type=CapsuleType.SCHOLAR,
                scroll_type=ScrollType.GENERAL,
                access_level=AccessLevel.PUBLIC,
                template_path="test.jinja",
                active=False
            )
        ]
        
        for capsule in capsules:
            registry.register_capsule(capsule)
        
        # Test filtering by type
        scholar_capsules = registry.list_capsules(capsule_type=CapsuleType.SCHOLAR)
        assert len(scholar_capsules) == 1  # Only active scholar capsule
        
        # Test filtering by realm
        ed_capsules = registry.list_capsules(realm_id="ED-003")
        assert len(ed_capsules) == 1
        
        # Test including inactive
        all_scholars = registry.list_capsules(capsule_type=CapsuleType.SCHOLAR, active_only=False)
        assert len(all_scholars) == 2
    
    def test_check_access(self, registry):
        """Test access checking"""
        # Create capsule with council access
        capsule = CapsuleDefinition(
            capsule_id="restricted",
            name="Restricted",
            capsule_type=CapsuleType.SOVEREIGN,
            scroll_type=ScrollType.GOVERNANCE,
            access_level=AccessLevel.COUNCIL,
            template_path="test.jinja",
            ceremonial_requirements={"minimum_authority": "council"}
        )
        
        registry.register_capsule(capsule)
        
        # Test public user access (should fail)
        public_context = {"authority_level": "public"}
        access, msg = registry.check_access("restricted", public_context)
        assert not access
        assert "council level access" in msg.lower()
        
        # Test council user access (should succeed)
        council_context = {"authority_level": "council"}
        access, msg = registry.check_access("restricted", council_context)
        assert access
        assert "granted" in msg.lower()
        
        # Test nonexistent capsule
        access, msg = registry.check_access("nonexistent", {})
        assert not access
        assert "not found" in msg.lower()


class TestPromptTemplate:
    """Test prompt template functionality"""
    
    def test_initialization(self):
        """Test template initialization"""
        template = PromptTemplate(
            template_id="test_template",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="Hello {name}, your query is: {query}"
        )
        
        assert template.template_id == "test_template"
        assert template.scroll_type == ScrollType.GENERAL
        assert template.version == PromptVersion.STABLE
        assert "name" in template.variables
        assert "query" in template.variables
    
    def test_render(self):
        """Test template rendering"""
        template = PromptTemplate(
            template_id="test",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="Hello {name}, your {item} is ready."
        )
        
        result = template.render({"name": "User", "item": "scroll"})
        assert result == "Hello User, your scroll is ready."
    
    def test_render_missing_variable(self):
        """Test rendering with missing variables"""
        template = PromptTemplate(
            template_id="test",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="Hello {name}, {missing} variable here."
        )
        
        result = template.render({"name": "User"})
        assert "[missing]" in result  # Should use placeholder
    
    def test_validate(self):
        """Test template validation"""
        template = PromptTemplate(
            template_id="test",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="Hello {name}, your {item} is ready."
        )
        
        # Valid context
        valid, missing = template.validate({"name": "User", "item": "scroll"})
        assert valid
        assert len(missing) == 0
        
        # Invalid context
        invalid, missing = template.validate({"name": "User"})
        assert not invalid
        assert "item" in missing
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        template = PromptTemplate(
            template_id="test",
            scroll_type=ScrollType.GENERAL,
            version=PromptVersion.STABLE,
            template_text="Test {var}"
        )
        
        data = template.to_dict()
        
        assert isinstance(data, dict)
        assert data["template_id"] == "test"
        assert data["scroll_type"] == "general"
        assert data["version"] == "stable"
    
    def test_from_dict(self):
        """Test creation from dictionary"""
        data = {
            "template_id": "test",
            "scroll_type": "general",
            "version": "stable",
            "template_text": "Test template",
            "variables": [],
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "performance_metrics": {}
        }
        
        template = PromptTemplate.from_dict(data)
        
        assert template.template_id == "test"
        assert template.scroll_type == ScrollType.GENERAL
        assert template.version == PromptVersion.STABLE


class TestPromptManager:
    """Test prompt manager functionality"""
    
    @pytest.fixture
    def config(self):
        """Mock configuration"""
        return Mock()
    
    @pytest.fixture
    def manager(self, config):
        """Create prompt manager for testing"""
        return PromptManager(config)
    
    def test_initialization(self, manager):
        """Test manager initialization"""
        assert isinstance(manager.templates, dict)
        assert isinstance(manager.builders, dict)
        assert len(manager.templates) > 0  # Should have default templates
    
    def test_add_template(self, manager):
        """Test adding a template"""
        template = PromptTemplate(
            template_id="custom_template",
            scroll_type=ScrollType.CUSTOM,
            version=PromptVersion.EXPERIMENTAL,
            template_text="Custom template: {content}"
        )
        
        manager.add_template(template)
        
        assert "custom_template" in manager.templates
        assert manager.templates["custom_template"] == template
    
    def test_get_template(self, manager):
        """Test getting template by ID"""
        # Should have default templates
        template = manager.get_template("general_system")
        assert template is not None
        
        # Non-existent template
        none_template = manager.get_template("nonexistent")
        assert none_template is None
    
    def test_list_templates(self, manager):
        """Test listing templates with filters"""
        # All templates
        all_templates = manager.list_templates()
        assert len(all_templates) > 0
        
        # Filter by scroll type
        general_templates = manager.list_templates(scroll_type=ScrollType.GENERAL)
        assert all(t.scroll_type == ScrollType.GENERAL for t in general_templates)
        
        # Filter by version
        stable_templates = manager.list_templates(version=PromptVersion.STABLE)
        assert all(t.version == PromptVersion.STABLE for t in stable_templates)
    
    def test_build_full_prompt(self, manager):
        """Test building complete prompt set"""
        sources = [
            {
                "content": "Test document content",
                "metadata": {"file_name": "test.md", "document_type": "test"}
            }
        ]
        
        prompts = manager.build_full_prompt(
            ScrollType.GENERAL,
            "What is this about?",
            sources,
            {"context_type": "documentation"}
        )
        
        assert "system" in prompts
        assert "user" in prompts
        assert "context" in prompts
        assert all(isinstance(p, str) for p in prompts.values())
    
    def test_track_prompt_performance(self, manager):
        """Test performance tracking"""
        template_id = "general_system"
        
        # Track performance
        manager.track_prompt_performance(template_id, {
            "response_time": 1.5,
            "user_satisfaction": 4.5
        })
        
        template = manager.get_template(template_id)
        assert template.performance_metrics["usage_count"] == 1
        assert template.performance_metrics["average_response_time"] == 1.5
    
    def test_get_performance_report(self, manager):
        """Test performance reporting"""
        # Add some performance data
        manager.track_prompt_performance("general_system", {"response_time": 1.0})
        manager.track_prompt_performance("resume_system", {"response_time": 2.0})
        
        report = manager.get_performance_report()
        
        assert "total_templates" in report
        assert "by_scroll_type" in report
        assert "top_performers" in report
        assert report["total_templates"] > 0


class TestRealtimeEvent:
    """Test real-time event functionality"""
    
    def test_initialization(self):
        """Test event initialization"""
        event = RealtimeEvent(
            event_type=EventType.SCROLL_REQUEST,
            event_id="test_event_123",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"query": "Test query"},
            user_id="test_user",
            session_id="test_session"
        )
        
        assert event.event_type == EventType.SCROLL_REQUEST
        assert event.event_id == "test_event_123"
        assert event.data["query"] == "Test query"
        assert event.user_id == "test_user"
        assert event.session_id == "test_session"
    
    def test_to_json(self):
        """Test JSON serialization"""
        event = RealtimeEvent(
            event_type=EventType.SCROLL_COMPLETE,
            event_id="test",
            timestamp=datetime.now(timezone.utc).isoformat(),
            data={"status": "success"}
        )
        
        json_str = event.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["event_type"] == "scroll_complete"
        assert parsed["event_id"] == "test"
        assert parsed["data"]["status"] == "success"
    
    def test_from_json(self):
        """Test JSON deserialization"""
        json_data = {
            "event_type": "scroll_progress",
            "event_id": "test",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"progress": 50},
            "user_id": None,
            "session_id": None
        }
        
        json_str = json.dumps(json_data)
        event = RealtimeEvent.from_json(json_str)
        
        assert event.event_type == EventType.SCROLL_PROGRESS
        assert event.data["progress"] == 50


class TestScrollSession:
    """Test scroll session functionality"""
    
    def test_initialization(self):
        """Test session initialization"""
        request_data = {"query": "Test query", "capsule_id": "test_capsule"}
        session = ScrollSession("session_123", request_data)
        
        assert session.session_id == "session_123"
        assert session.request_data == request_data
        assert session.status == "pending"
        assert session.progress == 0
        assert len(session.subscribers) == 0
    
    def test_start_session(self):
        """Test starting a session"""
        session = ScrollSession("test", {})
        
        session.start()
        
        assert session.status == "processing"
        assert session.started_at is not None
    
    def test_update_progress(self):
        """Test progress updates"""
        session = ScrollSession("test", {})
        
        session.update_progress(50, "processing")
        
        assert session.progress == 50
        assert session.current_stage == "processing"
    
    def test_complete_session(self):
        """Test session completion"""
        session = ScrollSession("test", {})
        result = {"scroll_content": "Generated scroll"}
        
        session.complete(result)
        
        assert session.status == "completed"
        assert session.progress == 100
        assert session.current_stage == "complete"
        assert session.result == result
        assert session.completed_at is not None
    
    def test_error_session(self):
        """Test session error handling"""
        session = ScrollSession("test", {})
        
        session.error_out("Test error")
        
        assert session.status == "error"
        assert session.current_stage == "error"
        assert session.error == "Test error"
        assert session.completed_at is not None
    
    def test_subscriber_management(self):
        """Test subscriber management"""
        session = ScrollSession("test", {})
        
        session.add_subscriber("user1")
        session.add_subscriber("user2")
        
        assert "user1" in session.subscribers
        assert "user2" in session.subscribers
        assert len(session.subscribers) == 2
        
        session.remove_subscriber("user1")
        
        assert "user1" not in session.subscribers
        assert "user2" in session.subscribers
        assert len(session.subscribers) == 1
    
    def test_get_status(self):
        """Test status retrieval"""
        session = ScrollSession("test", {})
        session.add_subscriber("user1")
        session.update_progress(25, "initializing")
        
        status = session.get_status()
        
        assert status["session_id"] == "test"
        assert status["status"] == "pending"
        assert status["progress"] == 25
        assert status["current_stage"] == "initializing"
        assert status["subscriber_count"] == 1


class TestScrollGenerator:
    """Test scroll generator functionality"""
    
    @pytest.fixture
    def mock_config(self, tmp_path):
        """Mock configuration"""
        config = Mock()
        config.scroll_templates_path = tmp_path / "templates"
        config.scroll_templates_path.mkdir(parents=True)
        return config
    
    @pytest.fixture
    def mock_registry(self):
        """Mock capsule registry"""
        registry = Mock()
        
        # Mock capsule
        capsule = CapsuleDefinition(
            capsule_id="test_capsule",
            name="Test Capsule",
            capsule_type=CapsuleType.SCHOLAR,
            scroll_type=ScrollType.GENERAL,
            access_level=AccessLevel.PUBLIC,
            template_path="test_scroll.jinja",
            configuration={"test_setting": True}
        )
        
        registry.get_capsule.return_value = capsule
        registry.check_access.return_value = (True, "Access granted")
        
        return registry
    
    @pytest.fixture
    def mock_prompt_manager(self):
        """Mock prompt manager"""
        return Mock()
    
    @pytest.fixture
    def generator(self, mock_config, mock_registry, mock_prompt_manager, tmp_path):
        """Create scroll generator for testing"""
        # Create a simple test template
        template_dir = tmp_path / "templates"
        template_dir.mkdir(exist_ok=True)
        
        template_content = """
# Test Scroll

**Query**: {{ query }}
**Generated**: {{ timestamp }}

## Response

{{ main_response }}

## Sources

{% for source in sources %}
- {{ source.content[:100] }}
{% endfor %}
        """.strip()
        
        template_file = template_dir / "test_scroll.jinja"
        template_file.write_text(template_content)
        
        return ScrollGenerator(mock_config, mock_registry, mock_prompt_manager)
    
    @pytest.mark.asyncio
    async def test_generate_scroll_success(self, generator):
        """Test successful scroll generation"""
        sources = [
            {"content": "Test document content", "metadata": {"file_name": "test.md"}}
        ]
        rag_result = {
            "response": "This is a test response",
            "confidence_score": 85,
            "processing_time": 1.2
        }
        user_context = {"authority_level": "public"}
        ceremonial_context = CeremonialContext(actor="Test User", realm="ED-003")
        
        result = await generator.generate_scroll(
            "test_capsule",
            "What is this test about?",
            sources,
            rag_result,
            user_context,
            ceremonial_context
        )
        
        assert result["success"] is True
        assert "scroll_content" in result
        assert "scroll_metadata" in result
        assert "What is this test about?" in result["scroll_content"]
        assert "This is a test response" in result["scroll_content"]
    
    @pytest.mark.asyncio
    async def test_generate_scroll_access_denied(self, generator, mock_registry):
        """Test scroll generation with access denied"""
        # Mock access denied
        mock_registry.check_access.return_value = (False, "Access denied")
        
        result = await generator.generate_scroll(
            "test_capsule",
            "Test query",
            [],
            {},
            {"authority_level": "public"}
        )
        
        assert result["success"] is False
        assert "Access denied" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_scroll_capsule_not_found(self, generator, mock_registry):
        """Test scroll generation with nonexistent capsule"""
        mock_registry.get_capsule.return_value = None
        
        result = await generator.generate_scroll(
            "nonexistent_capsule",
            "Test query",
            [],
            {}
        )
        
        assert result["success"] is False
        assert "not found" in result["error"].lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])