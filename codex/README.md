# Super-Codex-AI

A ceremonial AI system with honor-based governance, designed for knowledge management, guidance, and ceremonial document generation.

## 🏛️ Architecture Overview

Super-Codex-AI is built around the concept of ceremonial AI governance with modular architecture:

### Core Components

- **Core Services** (`codex/core/`): Foundation services for configuration, event handling, auditing, replay, identity management, and utilities
- **AI Engines** (`codex/engines/`): Specialized processing engines for different ceremonial functions
- **Scrolls System** (`codex/scrolls/`): Template-based document generation with ceremonial capsules
- **Data Management** (`codex/data/`): Structured storage for corpus, vectors, replay logs, identities, and seals

### Key Features

- **Honor System**: Merit-based recognition and governance framework
- **Ceremonial Protocols**: Structured processes for decision-making and documentation
- **Capsule System**: Configurable AI personalities for different use cases
- **RAG Pipeline**: Retrieval-Augmented Generation for knowledge-based responses
- **Event-Driven Architecture**: Comprehensive event bus and audit logging
- **Modular Design**: Extensible engine system for specialized AI capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment tool (venv, conda, etc.)

### Installation

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd Super-Codex-AI/codex
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**:
   ```bash
   # Copy environment template
   cp .env.template .env
   # Edit .env with your settings
   ```

3. **Initialize Data Directories**:
   ```bash
   # Data directories are auto-created, but you can pre-populate:
   mkdir -p data/corpus data/vectors data/replay data/identities data/seals
   ```

4. **Start the Server**:
   ```bash
   python server.py --host 0.0.0.0 --port 8000 --reload
   ```

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Server Status**: `http://localhost:8000/api/status`

### Core Endpoints

#### Query Processing
```bash
POST /api/query
{
  "query": "What is the governance system?",
  "capsule_id": "sovereign_crown",
  "user_context": {"authority_level": "council"},
  "ceremonial_context": {
    "actor": "Council Member",
    "realm": "PL-001",
    "significance": "standard"
  }
}
```

#### Capsule Management
```bash
GET /api/capsules?realm_id=PL-001&access_level=public
```

#### Content Analysis
```bash
POST /api/analyze
{
  "content": "Text to analyze",
  "analysis_type": "sigil",
  "context": {}
}
```

#### Content Transformation
```bash
POST /api/transform
{
  "content": "Content to transform",
  "flame_type": "purification",
  "intensity": 0.7
}
```

## 🎯 AI Engines

### Axiom Engine
**Purpose**: Ceremonial reasoning and governance logic
- Constitutional interpretation
- Ceremonial protocol validation
- Governance decision support

### RAG Engine  
**Purpose**: Knowledge retrieval and response generation
- Document corpus search
- Vector similarity matching
- Context-aware response generation

### Sigil Engine
**Purpose**: Pattern recognition and symbolic analysis
- Document pattern detection
- Symbolic meaning interpretation
- Ceremonial significance analysis

### Oracle Engine
**Purpose**: Wisdom provision and insight generation
- Deep context analysis
- Strategic guidance
- Wisdom synthesis

### Lantern Engine
**Purpose**: Guidance and navigation assistance
- Learning path recommendation
- Process navigation
- Educational guidance

### Flame Engine
**Purpose**: Content transformation and purification
- Text refinement and improvement
- Style transformation
- Content purification and enhancement

## 📜 Capsule System

### Available Capsules

#### Sovereign Crown (`sovereign_crown`)
- **Purpose**: Supreme governance and constitutional matters
- **Access**: Sovereign level
- **Template**: `governance101_scroll.jinja`
- **Use Cases**: Constitutional decisions, high-level governance

#### Guardian Protocols (`guardian_protocols`)
- **Purpose**: Operational guidance and maintenance
- **Access**: Custodian level
- **Template**: `general_scroll.jinja`
- **Use Cases**: System operations, technical guidance

#### Scholar Archives (`scholar_archives`)
- **Purpose**: Research and knowledge preservation
- **Access**: Member level
- **Template**: `general_scroll.jinja`
- **Use Cases**: Academic research, documentation

#### Career Advancement (`career_advancement`)
- **Purpose**: Professional development guidance
- **Access**: Public
- **Template**: `resume_scroll.jinja`
- **Use Cases**: Resume building, career planning

#### Financial Wisdom (`financial_wisdom`)
- **Purpose**: Financial education and planning
- **Access**: Public
- **Template**: `finance_scroll.jinja`
- **Use Cases**: Financial literacy, planning guidance

### Creating Custom Capsules

```python
from scrolls.capsule import CapsuleDefinition, CapsuleType, AccessLevel, ScrollType

custom_capsule = CapsuleDefinition(
    capsule_id="custom_guidance",
    name="Custom Guidance Capsule",
    capsule_type=CapsuleType.MENTOR,
    scroll_type=ScrollType.GENERAL,
    access_level=AccessLevel.MEMBER,
    template_path="custom_template.jinja",
    description="Specialized guidance capsule",
    configuration={
        "tone": "supportive",
        "detail_level": "comprehensive"
    }
)

registry.register_capsule(custom_capsule)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the codex directory:

```env
# Core Configuration
CODEX_ENV=development
LOG_LEVEL=INFO

# Data Paths
CODEX_DATA_DIR=./data
CORPUS_PATH=./data/corpus
VECTORS_PATH=./data/vectors
REPLAY_PATH=./data/replay

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# AI Configuration  
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Vector Database
CHROMA_PERSIST_DIRECTORY=./data/vectors
FAISS_INDEX_PATH=./data/faiss_index

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
RELOAD=true
```

### Configuration Classes

The system uses type-safe configuration classes:

```python
from core.config import CodexConfig

config = CodexConfig()
print(config.server_host)  # Reads from env with defaults
print(config.corpus_path)  # Path configuration
```

## 🎭 Development

### Project Structure

```
codex/
├── core/                 # Foundation services
│   ├── config.py        # Configuration management
│   ├── bus.py           # Event handling
│   ├── audit.py         # Audit logging
│   ├── replay.py        # Replay management
│   ├── identity.py      # Identity and access
│   └── utils.py         # Common utilities
├── engines/             # AI processing engines
│   ├── axiom.py         # Ceremonial reasoning
│   ├── rag.py           # Knowledge retrieval
│   ├── sigil.py         # Pattern recognition
│   ├── oracle.py        # Wisdom provision
│   ├── lantern.py       # Guidance system
│   └── flame.py         # Content transformation
├── scrolls/             # Document generation
│   ├── capsule.py       # Capsule management
│   ├── realtime.py      # Real-time processing
│   └── templates/       # Jinja2 templates
├── data/                # Data storage
│   ├── corpus/          # Document corpus
│   ├── vectors/         # Vector embeddings
│   ├── replay/          # Event replay logs
│   ├── identities/      # User identities
│   └── seals/           # Authority seals
├── server.py           # FastAPI application
└── requirements.txt    # Dependencies
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=codex

# Run specific test file
pytest tests/test_engines.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black codex/
isort codex/

# Lint code
flake8 codex/

# Type checking
mypy codex/
```

## 🔒 Security Considerations

- **Authentication**: Implement proper authentication for production
- **Authorization**: Use the built-in authority levels and access controls
- **Data Protection**: Ensure sensitive data is properly encrypted
- **API Security**: Use HTTPS in production, validate all inputs
- **Audit Logging**: Comprehensive audit trails are maintained

## 📈 Monitoring and Observability

### Health Checks

The system provides multiple health check endpoints:

```bash
# Basic health
GET /health

# Detailed status
GET /api/status

# Component-specific health
GET /health/engines
```

### Audit Logs

All significant actions are logged with structured audit trails:

```python
# Automatic logging in engines
await audit_logger.log_event(
    event_type="query_processed",
    actor="user_id",
    details={"query_length": 100, "success": True}
)
```

### Event Monitoring

Subscribe to system events:

```python
async def handle_query_event(event_data):
    print(f"Query processed: {event_data['query']}")

event_bus.subscribe("query_processed", handle_query_event)
```

## 🌟 Advanced Usage

### Custom Engines

Create specialized engines by extending the base patterns:

```python
from engines.base import BaseEngine

class CustomEngine(BaseEngine):
    async def process(self, input_data, context=None):
        # Custom processing logic
        return {"result": "processed"}
    
    async def health_check(self):
        return {"status": "healthy"}
```

### Custom Templates

Create new scroll templates in `scrolls/templates/`:

```jinja2
{# custom_scroll.jinja #}
# {{ title }}

**Generated**: {{ timestamp }}
**Context**: {{ context_type }}

## Response

{{ main_response }}

## Custom Section

{{ custom_data }}
```

### Event-Driven Processing

Leverage the event system for custom workflows:

```python
async def custom_processor(event_data):
    if event_data.get("type") == "custom_trigger":
        # Process custom events
        pass

event_bus.subscribe("custom_event", custom_processor)
```

## 🤝 Contributing

1. Follow the ceremonial development principles
2. Maintain test coverage above 80%
3. Use type hints throughout
4. Update documentation for new features
5. Follow the honor system protocols

## 📄 License

This project is part of the Super-Codex-AI ceremonial governance system. See the main project LICENSE for details.

## 🎖️ Honor System

Contributions to Super-Codex-AI are recognized through the honor system. Excellence in code, documentation, and community support are formally acknowledged through ceremonial protocols.

---

*"Knowledge shared in honor, wisdom preserved in ceremony, progress achieved through understanding."*

**Codex Seal**: 🔱 *Super-Codex-AI v1.0.0*