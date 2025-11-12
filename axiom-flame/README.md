# Axiom Flame

A ceremonial governance system with reasoning, replay, and audit capabilities.

## Architecture

- **API Package** (Flask): Handles reasoning, replay, ledger operations, and registry management
- **CLI Package** (Node.js): Ceremony dispatch, honors management, and broadcast functionality
- **Artifacts**: Living scrolls stored as JSON/YAML for ceremonies, honors, registry, and blueprints
- **Storage**: File-based vaults for ledger entries, annals, and replay data
- **Ops**: Configuration and deployment scripts

## Quick Start

### API (Flask)
```bash
cd packages/api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask run
```

### CLI (Node.js)
```bash
cd packages/cli
npm install
npm run ceremony:dispatch
```

## Data Structures

### Ledger Entry Format
Each ceremonial action creates a structured ledger entry with:
- Unique dispatch ID
- Actor and realm identification
- Capsule and intent classification
- Input/output tracking
- Governance seals and audit requirements
- Links to replay and annal references

See `artifacts/ceremonies/` for examples.

## Storage Layout

- `storage/ledger/` - Timestamped ledger entries
- `storage/annals/` - Monthly aggregated records
- `storage/replays/` - Detailed replay data for audit trails

## Operations

- Health checks via `ops/healthcheck.sh`
- NGINX reverse proxy configuration
- systemd service management