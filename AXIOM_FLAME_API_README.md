# AXIOM-FLAME API

A comprehensive FastAPI application for the AXIOM-FLAME ceremonial system with artifacts management, governance, identity management, and recall functionality.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment activated (`.venv`)
- Required dependencies installed (`pip install -r requirements.txt`)

### Starting the API

#### Option 1: Using the startup script
```bash
python start_axiom_api.py
```

#### Option 2: Using uvicorn directly
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

#### Option 3: Running the app module directly
```bash
python -m app.main
```

### Testing the API
```bash
python test_axiom_api.py
```

## 📖 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc  
- **OpenAPI Schema**: http://localhost:8080/openapi.json
- **Health Check**: http://localhost:8080/health

## 🔧 API Endpoints

### Core Endpoints

- `GET /health` - Health check endpoint

### Artifacts (`/v1/artifacts`)
- `GET /` - List all artifacts
- `GET /{artifact_id}` - Get specific artifact
- `POST /` - Create new artifact
- `PUT /{artifact_id}` - Update artifact
- `DELETE /{artifact_id}` - Delete artifact

### Ceremonies (`/v1/ceremonies`)
- `GET /` - List all ceremonies
- `GET /{ceremony_id}` - Get specific ceremony
- `POST /` - Create new ceremony
- `POST /reason` - Perform ceremonial reasoning
- `POST /replay` - Replay ceremony by dispatch ID
- `POST /audit` - Audit ceremony by dispatch ID

### Governance (`/v1/governance`)
- `GET /rules` - List governance rules
- `GET /rules/{rule_id}` - Get specific rule
- `POST /rules` - Create governance rule
- `GET /councils` - List councils
- `GET /councils/{council_id}` - Get specific council
- `POST /councils` - Create council
- `GET /seals` - List seal types
- `GET /status` - Get governance status

### Identity (`/v1/identity`)
- `GET /` - List all identities
- `GET /{identity_id}` - Get specific identity
- `POST /` - Create new identity
- `POST /authenticate` - Authenticate and get token
- `GET /me/profile` - Get current user profile (requires auth)
- `POST /verify` - Verify access to realm/capsule (requires auth)
- `GET /realms` - List available realms
- `GET /capsules` - List available capsules

### Recall (`/v1/recall`)
- `GET /` - List recall entries (with filtering)
- `GET /{recall_id}` - Get specific recall entry
- `POST /` - Create new recall entry
- `POST /search` - Advanced search for recall entries
- `GET /dispatch/{dispatch_id}` - Get recalls by dispatch ID
- `PUT /{recall_id}/archive` - Archive recall entry
- `PUT /{recall_id}/restore` - Restore archived entry
- `DELETE /{recall_id}` - Delete recall entry
- `GET /stats/summary` - Get recall statistics

## 🔐 Authentication

The Identity endpoints support JWT token authentication:

1. Create an identity via `POST /v1/identity/`
2. Authenticate via `POST /v1/identity/authenticate`
3. Use the returned access token in the `Authorization: Bearer <token>` header

## 📝 Example Usage

### Create a Ceremony
```bash
curl -X POST "http://localhost:8080/v1/ceremonies/reason" \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "Custodian",
    "realm": "PL-001",
    "capsule": "Sovereign Crown",
    "intent": "Crown.Invocation",
    "seal": "Sacred"
  }'
```

### Create an Artifact
```bash
curl -X POST "http://localhost:8080/v1/artifacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sacred Document",
    "type": "document",
    "content": "This is the content of the sacred document",
    "metadata": {"classification": "sacred"}
  }'
```

### Search Recall Entries
```bash
curl -X POST "http://localhost:8080/v1/recall/search" \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "Custodian",
    "realm": "PL-001",
    "tags": ["sacred"]
  }'
```

## 🏗️ Architecture

```
app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application setup
└── routes/              # API route modules
    ├── __init__.py      # Routes package init
    ├── artifacts.py     # Artifacts management
    ├── ceremonies.py    # Ceremonial operations
    ├── governance.py    # Governance and rules
    ├── identity.py      # Identity and authentication
    └── recall.py        # Memory and recall system
```

## 🎯 Features

### Artifacts Management
- CRUD operations for artifacts
- Metadata support
- Type classification

### Ceremonies
- Ceremonial reasoning with dispatch IDs
- Replay and audit functionality
- Actor/realm/capsule tracking

### Governance
- Rule management system
- Council administration
- Seal type definitions
- Authority levels

### Identity & Authentication
- JWT token-based authentication
- Role-based access control
- Realm and capsule permissions
- Authority level validation

### Recall System
- Advanced search capabilities
- Archiving and restoration
- Statistics and analytics
- Tag-based organization

## 🔧 Configuration

The API uses in-memory storage for demonstration purposes. In production, you would integrate with:

- PostgreSQL for persistent data storage
- Redis for caching and sessions
- External authentication providers
- File storage systems for artifacts

## 📊 Monitoring

The API includes built-in health checks and is compatible with:

- Prometheus metrics (via existing setup)
- Grafana dashboards
- Application performance monitoring
- Structured logging

## 🚀 Production Deployment

For production deployment, the API integrates with the existing infrastructure:

- Docker containers (via `docker-compose.yml`)
- Nginx reverse proxy
- SSL/TLS termination
- Monitoring and alerting

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_axiom_api.py
```

This tests all endpoints and verifies the API functionality.

---

**🔥 AXIOM-FLAME API is now ready for integration with the Super-Codex-AI system!**