# Axiom-Flame Quick Start Guide

## Installation

### Install Dependencies
```bash
# API dependencies
cd packages/api
pip install Flask==3.0.0 jsonschema

# CLI dependencies
cd ../cli
npm install
```

### Global CLI Installation (Optional)
```bash
cd packages/cli
npm install -g .
```

## Quick Test

### 1. Start the API
```bash
cd packages/api
python app.py
```
The API will start on `http://localhost:8080`

### 2. Test Health Check
```bash
# Using global command
axiom health

# Or using local CLI
cd packages/cli
node index.js health
```

### 3. Perform Basic Reasoning
```bash
# Using global command
axiom reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown"

# Or using local CLI
node index.js reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown"
```

### 4. View Generated Files
```bash
# Check ceremony files
ls artifacts/ceremonies/

# Check storage
ls storage/ledger/
ls storage/replays/
```

## Common Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `axiom health` | API health check | `axiom health` |
| `axiom reason` | Create ceremony | `axiom reason --actor "Custodian" --realm "PL-001"` |
| `axiom replay` | Generate replay | `axiom replay AXF-2025-11-10-12345678` |
| `axiom audit` | Audit ceremony | `axiom audit AXF-2025-11-10-12345678` |

## File Structure Overview

```
axiom-flame/
├── packages/
│   ├── api/          # Flask API (Python)
│   └── cli/          # Node.js CLI (ES modules)
├── artifacts/        # Ceremonial data
├── storage/          # File-based storage
├── schemas/          # JSON validation schemas
└── docs/            # Documentation
```

## Troubleshooting

### CLI Issues
- Ensure Node.js 16+ for ES module support
- Check package.json has `"type": "module"`
- Verify dependencies are installed: `npm install`

### API Issues
- Ensure Python 3.8+ and Flask 3.0.0
- Check that storage directories exist
- Verify API is running on port 8080

### Permission Issues
- Check file permissions in artifacts/ and storage/
- Ensure write access to ceremony and replay directories