"""
Codex Configuration Management
Centralized configuration for the Super-Codex-AI system with environment variable support
and validation for all components.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


@dataclass
class CodexConfig:
    """Configuration management for Codex Engine"""
    
    # Core paths
    data_path: Path = field(default_factory=lambda: Path("codex/data"))
    corpus_path: Path = field(default_factory=lambda: Path("codex/data/corpus"))
    vectors_path: Path = field(default_factory=lambda: Path("codex/data/vectors"))
    templates_path: Path = field(default_factory=lambda: Path("codex/scrolls/templates"))
    
    # RAG configuration
    vector_dimension: int = 1536
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunks_per_query: int = 5
    similarity_threshold: float = 0.7
    
    # Model configuration
    embedding_model: str = "text-embedding-ada-002"
    completion_model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Scroll configuration
    scroll_templates: Dict[str, str] = field(default_factory=dict)
    default_scroll_type: str = "general"
    
    # Audit configuration
    audit_enabled: bool = True
    audit_retention_days: int = 90
    audit_detail_level: str = "standard"  # minimal, standard, verbose
    
    # Replay configuration
    replay_enabled: bool = True
    max_replay_queries: int = 100
    replay_timeout_minutes: int = 30
    
    # Performance configuration
    batch_size: int = 10
    max_concurrent_queries: int = 5
    cache_enabled: bool = True
    cache_ttl_minutes: int = 60
    
    # Security configuration
    api_key_required: bool = False
    rate_limit_per_minute: int = 60
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])
    
    # Integration configuration
    ledger_integration: bool = True
    artifact_dispatch: bool = True
    honor_system_integration: bool = True
    
    # Environment overrides
    environment: str = "development"
    debug_mode: bool = False
    log_level: str = "INFO"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration with optional config file override"""
        # Set defaults
        self._set_defaults()
        
        # Load from config file if provided
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
        
        # Override with environment variables
        self._load_from_environment()
        
        # Validate configuration
        self._validate()
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Load scroll templates
        self._load_scroll_templates()
        
        logger.info(f"Codex configuration initialized for {self.environment} environment")
    
    def _set_defaults(self):
        """Set default values based on current context"""
        base_path = Path(__file__).parent.parent
        self.data_path = base_path / "data"
        self.corpus_path = self.data_path / "corpus"
        self.vectors_path = self.data_path / "vectors"
        self.templates_path = base_path / "scrolls" / "templates"
        
        # Default scroll templates mapping
        self.scroll_templates = {
            "resume": "resume_scroll.jinja",
            "finance": "finance_scroll.jinja", 
            "governance": "governance101_scroll.jinja",
            "general": "general_scroll.jinja"
        }
    
    def _load_from_file(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            # Update configuration with file data
            for key, value in config_data.items():
                if hasattr(self, key):
                    # Convert path strings to Path objects
                    if key.endswith('_path'):
                        setattr(self, key, Path(value))
                    else:
                        setattr(self, key, value)
            
            logger.info(f"Configuration loaded from {config_path}")
            
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        # Core paths
        if os.getenv("CODEX_DATA_PATH"):
            self.data_path = Path(os.getenv("CODEX_DATA_PATH"))
        
        if os.getenv("CODEX_CORPUS_PATH"):
            self.corpus_path = Path(os.getenv("CODEX_CORPUS_PATH"))
        
        if os.getenv("CODEX_VECTORS_PATH"):
            self.vectors_path = Path(os.getenv("CODEX_VECTORS_PATH"))
        
        # RAG configuration
        if os.getenv("CODEX_VECTOR_DIMENSION"):
            self.vector_dimension = int(os.getenv("CODEX_VECTOR_DIMENSION"))
        
        if os.getenv("CODEX_CHUNK_SIZE"):
            self.chunk_size = int(os.getenv("CODEX_CHUNK_SIZE"))
        
        if os.getenv("CODEX_CHUNK_OVERLAP"):
            self.chunk_overlap = int(os.getenv("CODEX_CHUNK_OVERLAP"))
        
        # Model configuration
        if os.getenv("CODEX_EMBEDDING_MODEL"):
            self.embedding_model = os.getenv("CODEX_EMBEDDING_MODEL")
        
        if os.getenv("CODEX_COMPLETION_MODEL"):
            self.completion_model = os.getenv("CODEX_COMPLETION_MODEL")
        
        if os.getenv("CODEX_TEMPERATURE"):
            self.temperature = float(os.getenv("CODEX_TEMPERATURE"))
        
        if os.getenv("CODEX_MAX_TOKENS"):
            self.max_tokens = int(os.getenv("CODEX_MAX_TOKENS"))
        
        # Environment settings
        if os.getenv("CODEX_ENVIRONMENT"):
            self.environment = os.getenv("CODEX_ENVIRONMENT")
        
        if os.getenv("CODEX_DEBUG"):
            self.debug_mode = os.getenv("CODEX_DEBUG").lower() == "true"
        
        if os.getenv("CODEX_LOG_LEVEL"):
            self.log_level = os.getenv("CODEX_LOG_LEVEL")
        
        # Feature flags
        if os.getenv("CODEX_AUDIT_ENABLED"):
            self.audit_enabled = os.getenv("CODEX_AUDIT_ENABLED").lower() == "true"
        
        if os.getenv("CODEX_REPLAY_ENABLED"):
            self.replay_enabled = os.getenv("CODEX_REPLAY_ENABLED").lower() == "true"
        
        if os.getenv("CODEX_CACHE_ENABLED"):
            self.cache_enabled = os.getenv("CODEX_CACHE_ENABLED").lower() == "true"
        
        # Integration flags
        if os.getenv("CODEX_LEDGER_INTEGRATION"):
            self.ledger_integration = os.getenv("CODEX_LEDGER_INTEGRATION").lower() == "true"
        
        if os.getenv("CODEX_ARTIFACT_DISPATCH"):
            self.artifact_dispatch = os.getenv("CODEX_ARTIFACT_DISPATCH").lower() == "true"
    
    def _validate(self):
        """Validate configuration values"""
        errors = []
        
        # Validate vector dimension
        if self.vector_dimension <= 0:
            errors.append("vector_dimension must be positive")
        
        # Validate chunk sizes
        if self.chunk_size <= 0:
            errors.append("chunk_size must be positive")
        
        if self.chunk_overlap >= self.chunk_size:
            errors.append("chunk_overlap must be less than chunk_size")
        
        # Validate temperature
        if not (0.0 <= self.temperature <= 2.0):
            errors.append("temperature must be between 0.0 and 2.0")
        
        # Validate similarity threshold
        if not (0.0 <= self.similarity_threshold <= 1.0):
            errors.append("similarity_threshold must be between 0.0 and 1.0")
        
        # Validate environment
        if self.environment not in ["development", "staging", "production"]:
            logger.warning(f"Unknown environment: {self.environment}")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
        
        logger.info("Configuration validation passed")
    
    def _ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.data_path,
            self.corpus_path,
            self.vectors_path,
            self.templates_path
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
    
    def _load_scroll_templates(self):
        """Load and validate scroll templates"""
        template_files = {}
        
        if self.templates_path.exists():
            for template_name, template_file in self.scroll_templates.items():
                template_path = self.templates_path / template_file
                if template_path.exists():
                    template_files[template_name] = str(template_path)
                    logger.debug(f"Found scroll template: {template_name} -> {template_file}")
                else:
                    logger.warning(f"Scroll template not found: {template_path}")
        
        # Update with actual file paths
        self.scroll_templates = template_files
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model-specific configuration"""
        return {
            "embedding_model": self.embedding_model,
            "completion_model": self.completion_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_rag_config(self) -> Dict[str, Any]:
        """Get RAG-specific configuration"""
        return {
            "vector_dimension": self.vector_dimension,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "max_chunks_per_query": self.max_chunks_per_query,
            "similarity_threshold": self.similarity_threshold,
            "corpus_path": str(self.corpus_path),
            "vectors_path": str(self.vectors_path)
        }
    
    def get_audit_config(self) -> Dict[str, Any]:
        """Get audit-specific configuration"""
        return {
            "enabled": self.audit_enabled,
            "retention_days": self.audit_retention_days,
            "detail_level": self.audit_detail_level,
            "ledger_integration": self.ledger_integration
        }
    
    def get_scroll_config(self) -> Dict[str, Any]:
        """Get scroll-specific configuration"""
        return {
            "templates": self.scroll_templates,
            "default_type": self.default_scroll_type,
            "templates_path": str(self.templates_path)
        }
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance-specific configuration"""
        return {
            "batch_size": self.batch_size,
            "max_concurrent_queries": self.max_concurrent_queries,
            "cache_enabled": self.cache_enabled,
            "cache_ttl_minutes": self.cache_ttl_minutes
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security-specific configuration"""
        return {
            "api_key_required": self.api_key_required,
            "rate_limit_per_minute": self.rate_limit_per_minute,
            "allowed_origins": self.allowed_origins
        }
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        for key, value in updates.items():
            if hasattr(self, key):
                # Convert path strings to Path objects
                if key.endswith('_path') and isinstance(value, str):
                    setattr(self, key, Path(value))
                else:
                    setattr(self, key, value)
                logger.info(f"Configuration updated: {key} = {value}")
            else:
                logger.warning(f"Unknown configuration key: {key}")
        
        # Re-validate after updates
        self._validate()
    
    def save_config(self, config_path: str):
        """Save current configuration to file"""
        try:
            config_data = {}
            
            # Convert configuration to serializable format
            for key, value in self.__dict__.items():
                if not key.startswith('_'):
                    if isinstance(value, Path):
                        config_data[key] = str(value)
                    else:
                        config_data[key] = value
            
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save config to {config_path}: {e}")
            raise
    
    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary for display/logging"""
        return {
            "environment": self.environment,
            "debug_mode": self.debug_mode,
            "data_path": str(self.data_path),
            "vector_dimension": self.vector_dimension,
            "chunk_size": self.chunk_size,
            "embedding_model": self.embedding_model,
            "completion_model": self.completion_model,
            "features": {
                "audit_enabled": self.audit_enabled,
                "replay_enabled": self.replay_enabled,
                "cache_enabled": self.cache_enabled,
                "ledger_integration": self.ledger_integration,
                "artifact_dispatch": self.artifact_dispatch
            },
            "scroll_templates": list(self.scroll_templates.keys()),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Convenience function for creating config
def create_config(config_path: Optional[str] = None, **overrides) -> CodexConfig:
    """Create a CodexConfig instance with optional overrides"""
    config = CodexConfig(config_path)
    
    if overrides:
        config.update_config(overrides)
    
    return config