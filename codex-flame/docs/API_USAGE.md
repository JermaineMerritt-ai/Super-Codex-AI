# Axiom Flame API Usage Examples

## Streamlined Core API

The core API provides simple, direct endpoints for essential ceremonial operations:

### Health Check
```bash
curl http://localhost:8080/health
```

### Submit Reasoning
```bash
curl -X POST http://localhost:8080/reason \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "Custodian",
    "realm": "PL-001", 
    "capsule": "Sovereign Crown",
    "intent": "Crown.Invocation",
    "seal": "Sacred",
    "input": {"prompt": "Crown ceremony authorization"}
  }'
```

### Generate Replay
```bash
curl -X POST http://localhost:8080/replay \
  -H "Content-Type: application/json" \
  -d '{"dispatch_id": "AXF-2025-11-10-12345678"}'
```

### Audit Ceremony
```bash
curl -X POST http://localhost:8080/audit \
  -H "Content-Type: application/json" \
  -d '{"dispatch_id": "AXF-2025-11-10-12345678"}'
```

## CLI Usage

### Streamlined Commands (Global CLI)
```bash
# Install globally (optional)
npm install -g ./packages/cli

# Basic reasoning
axiom reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown"

# With custom intent and prompt  
axiom reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown" \
  --intent "Crown.Invocation" --seal "Sacred" --prompt "Eternal governance authorization"

# Generate replay
axiom replay AXF-2025-11-10-12345678

# Audit ceremony
axiom audit AXF-2025-11-10-12345678

# Health check
axiom health
```

### Local CLI Commands
```bash
# From packages/cli directory
node index.js reason --actor "Custodian" --realm "PL-001"
node index.js replay AXF-2025-11-10-12345678
node index.js audit AXF-2025-11-10-12345678  
node index.js health
```

### Enhanced Commands (Full Validation)
```bash
# Full ceremony with validation
npm run ceremony:dispatch -- --actor "Jermaine Merritt" --realm "PL-001" --capsule "Sovereign Crown"

# Honors management
npm run honors:add -- --name "Jermaine Merritt" --deed "Eternal Governance Stack" --insignia "Omega Crown"
npm run honors:list
npm run honors:show -- "HK-0001"

# Realm management
npm run realms:list -- --status "Active"
npm run realms:show -- "PL-001"
```

## Response Formats

### Reasoning Response
```json
{
  "ok": true,
  "dispatch_id": "AXF-2025-11-10-12345678",
  "summary": "Crown.Invocation sealed for realm PL-001."
}
```

### Replay Response
```json
{
  "ok": true,
  "replay": {
    "replay_version": "1.0",
    "replay_id": "RP-87654321",
    "timestamp": "2025-11-10T12:34:56Z",
    "source_dispatch_id": "AXF-2025-11-10-12345678",
    "realm": "PL-001",
    "capsule": "Sovereign Crown",
    "audit": {
      "status": "Verified",
      "notes": "Replay authorization matched Eternal Seal"
    }
  }
}
```

### Audit Response
```json
{
  "ok": true,
  "dispatch_id": "AXF-2025-11-10-12345678",
  "audit": "Present in ledger"
}
```

## File Structure

The streamlined API maintains the same file organization:

```
storage/
├── ledger/              # Ceremony ledger entries
│   └── AXF-2025-11-10-12345678.json
├── replays/             # Replay audit files
│   └── RP-87654321.json
└── annals/              # Monthly summaries

artifacts/
├── ceremonies/          # Enhanced ceremony records
├── honors/             # Honor awards and ledger
├── registry/           # Realm and actor registry
└── schemas/            # JSON validation schemas
```

## Deployment

### Environment Variables
```bash
PORT=8080                    # API port (default: 8080)
AXIOM_API_BASE=http://localhost:8080  # CLI API base URL
```

### Local Development

#### PowerShell (Windows)
```powershell
# Start the API
cd packages/api
python app.py

# Health check (in another terminal)
curl http://localhost:8080/health
```

#### Bash (Linux/macOS)
```bash
# Start the API
cd packages/api && python app.py

# Health check
curl http://localhost:8080/health
```

### Production Run
```bash
# API
cd packages/api && python app.py

# CLI
cd packages/cli && npm start
```

## API Compatibility

The system provides both approaches:

- **Streamlined**: `/reason`, `/replay`, `/audit` - Fast, simple operations
- **Enhanced**: `/api/reasoning`, `/api/honors`, `/api/realms` - Full validation and registry management

Choose based on your needs:
- Use **streamlined** for core ceremonial operations
- Use **enhanced** for complete governance workflows with validation