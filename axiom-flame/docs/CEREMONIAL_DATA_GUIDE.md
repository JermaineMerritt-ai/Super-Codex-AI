# Ceremonial Data Structures Guide

## Overview

The Axiom Flame ceremonial system uses structured JSON data to represent all governance, ceremonial, and honor operations. This guide details the data structure patterns, validation rules, and usage conventions.

## Core Data Structures

### 1. Ledger Entry (Ceremony)

The fundamental unit of ceremonial action. Every ceremony creates a ledger entry with:

#### Required Fields
- `ledger_version`: Format version (currently "1.0")
- `dispatch_id`: Unique identifier (format: "AXF-YYYY-MM-DD-NNNN")
- `timestamp`: ISO 8601 with Z suffix
- `actor`: Entity performing ceremony (Custodian, Council, Sentinel, Architect, Witness)
- `realm`: Hierarchical identifier (Planetary|Stellar|Galactic|Universal:name)
- `capsule`: Ceremonial context/type
- `intent`: Dot-separated action hierarchy (e.g., "Reasoning.Replay.Audit")
- `governance`: Seal level and audit requirements

#### Optional Fields
- `input`: Ceremony parameters
- `output`: Results and outcomes
- `links`: References to replays, annals, parent ceremonies
- `metadata`: Priority, tags, expiration, category

#### Example Structure
```json
{
  "ledger_version": "1.0",
  "dispatch_id": "AXF-2025-11-10-0001",
  "timestamp": "2025-11-10T06:42:00Z",
  "actor": "Custodian",
  "realm": "Planetary:Jackson-NC", 
  "capsule": "Sovereign Crown",
  "intent": "Reasoning.Replay.Audit",
  "input": { "prompt": "Crown invocation: source→replay" },
  "output": { "summary": "Crown sealed; replay authorized." },
  "governance": { "seal": "Eternal", "audit_required": true }
}
```

### 2. Honor Awards

Recognition system for ceremonial achievements:

#### Required Fields
- `honor_id`: Unique identifier (format: "HNR-YYYY-NNN")
- `recipient`: Actor receiving the honor
- `achievement`: Description of accomplishment
- `timestamp`: Award timestamp
- `seal`: Governance level

#### Metadata Fields
- `category`: Type of achievement (Ceremony, Service, Innovation, Guardian, Wisdom)
- `tier`: Award level (Bronze, Silver, Gold, Platinum, Legendary)
- `verification`: Ceremony references and audit status

### 3. Registry Entries

System state and permissions:

- **Actors**: Permissions, realms, active status
- **Capsules**: Types, governance levels, audit requirements  
- **Realms**: Jurisdiction, governance model, active status

## Governance Patterns

### Seal Levels (ascending authority)
1. **Temporal**: Time-limited, basic operations
2. **Eternal**: Permanent record, standard ceremonies
3. **Immutable**: Cannot be altered, security operations
4. **Sacred**: Highest level, genesis/creation ceremonies

### Authority Levels
- **Low**: Basic operations, informational
- **Medium**: Standard ceremonies, routine governance
- **High**: Security operations, important decisions
- **Critical**: System changes, genesis events

### Intent Hierarchies

Common patterns:
- `Reasoning.Process` - Basic processing
- `Reasoning.Replay.Audit` - Auditable reasoning with replay
- `Security.Monitoring.Alert` - Security monitoring
- `Creation.Design.Manifest` - Creation ceremonies
- `Governance.Decision.Ratify` - Council decisions

## Actor Roles and Capabilities

### Custodian
- **Realms**: Planetary scope
- **Capabilities**: Standard ceremonies, crown invocations
- **Seal Authority**: Up to Eternal

### Sentinel  
- **Realms**: Stellar scope
- **Capabilities**: Security monitoring, threat response
- **Seal Authority**: Up to Immutable

### Architect
- **Realms**: Universal scope
- **Capabilities**: Genesis ceremonies, blueprint design
- **Seal Authority**: Up to Sacred

### Council
- **Realms**: Galactic scope
- **Capabilities**: Governance decisions, ratification
- **Seal Authority**: Up to Sacred

### Witness
- **Realms**: Any (observer role)
- **Capabilities**: Attestation, verification
- **Seal Authority**: Temporal only

## API Integration Patterns

### Ceremony Creation
```python
POST /api/reasoning
{
  "actor": "Custodian",
  "realm": "Planetary:Jackson-NC",
  "capsule": "Sovereign Crown",
  "intent": "Reasoning.Replay.Audit",
  "input": {"prompt": "ceremony_prompt"}
}
```

### Honor Awards
```python
POST /api/honors
{
  "recipient": "Custodian", 
  "achievement": "Crown Ceremony Mastery",
  "category": "Ceremony",
  "tier": "Gold"
}
```

### Validation
```python
POST /api/validate/ceremony
{
  # Complete ceremony JSON for validation
}
```

## File Organization

```
artifacts/
├── ceremonies/          # Individual ceremony records
│   ├── AXF-2025-11-10-0001.json
│   └── AXF-2025-11-10-0002.json
├── honors/             # Honor awards
│   ├── HNR-2025-001.json
│   └── HNR-2025-002.json
├── registry/           # System registry
│   └── registry.json
├── schemas/            # JSON schemas
│   ├── ledger-entry.schema.json
│   └── honor.schema.json
└── blueprints/         # Ceremony templates
    └── crown_invocation.yaml

storage/
├── ledger/             # Timestamped ledger entries
├── replays/            # Detailed audit replays  
└── annals/             # Monthly aggregated records
```

## CLI Usage Patterns

### Ceremony Dispatch
```bash
npm run ceremony:dispatch -- --actor Custodian --realm "Planetary:Jackson-NC" --capsule "Sovereign Crown"
```

### Honor Granting
```bash
npm run honors:grant -- --recipient "Sentinel" --achievement "Exemplary Threat Detection"
```

### Broadcasting
```bash
npm run broadcast -- --dispatch-id "AXF-2025-11-10-0001"
```

## Best Practices

1. **Always validate** ceremony structures against schemas
2. **Use appropriate seal levels** based on ceremony importance
3. **Include audit trails** for high-authority operations
4. **Reference parent ceremonies** for multi-step processes
5. **Tag ceremonies consistently** for searchability
6. **Set expiration dates** for temporal ceremonies
7. **Maintain replay data** for all auditable ceremonies

## Error Handling

- Missing required fields → 400 Bad Request
- Schema validation failure → 400 Bad Request with validation details
- File system errors → 500 Internal Server Error
- Invalid dispatch IDs → 404 Not Found