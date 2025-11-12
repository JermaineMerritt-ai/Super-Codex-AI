# AXIOM CLI - Command Line Interface for AXIOM FLAME Intelligence Suite

A powerful command-line interface for interacting with the AXIOM FLAME ceremonial operations system.

## Features

- **Health Monitoring**: Check API server status and health
- **Ceremonial Operations**: Execute reasoning, replay, and audit operations
- **Cross-Platform**: Works on Windows (PowerShell/CMD) and Unix-like systems
- **Easy Integration**: Multiple wrapper scripts for different environments

## Installation

The CLI is automatically available when the AXIOM FLAME system is set up. Ensure you have:

1. Python 3.8+ with virtual environment activated
2. AXIOM FLAME API server running (default: http://127.0.0.1:8087)
3. Required Python packages (requests, json)

## Usage

### Direct Python Usage

```bash
python cli/axiom_cli.py <command> [arguments...]
```

### Platform-Specific Wrappers

**Windows Batch:**
```cmd
axiom.bat health
axiom.bat reason "Custodian" "PL-001" "Sovereign Crown" "Crown.Invocation"
```

**PowerShell:**
```powershell
.\axiom.ps1 health
.\axiom.ps1 reason "Council" "ST-007" "Sacred Protocols" "Protocol.Enhancement"
```

**Unix/Linux:**
```bash
./axiom.sh health
./axiom.sh reason "Guardian" "PL-002" "Digital Sovereignty" "Sovereignty.Declaration"
```

## Available Commands

### Health & Status
- `health` - Check API server health
- `status` - Get detailed system status and configuration

### Ceremonial Operations
- `reason <actor> <realm> <capsule> <intent>` - Execute ceremonial reasoning
- `replay <dispatch_id>` - Replay a ceremonial dispatch
- `audit <dispatch_id>` - Audit a ceremonial dispatch for integrity

### Registry & Ledger
- `registry` - List all registry entries (when available)

### Legacy Support
- `execute <command> [json_payload]` - Generic API execution for compatibility

## Examples

### Basic Health Check
```bash
python cli/axiom_cli.py health
```

Output:
```json
{
  "service": "axiom-flame-api",
  "status": "healthy", 
  "timestamp": "2025-11-12T01:21:22.009815+00:00",
  "version": "1.0.0"
}
```

### Ceremonial Reasoning
```bash
python cli/axiom_cli.py reason "Custodian" "PL-001" "Sovereign Crown" "Crown.Invocation"
```

Output:
```json
{
  "dispatch_id": "AXF-2025-11-11-e2dfa702",
  "reasoning_entry": {
    "actor": "Custodian",
    "capsule": "Sovereign Crown", 
    "dispatch_id": "AXF-2025-11-11-e2dfa702",
    "governance_seal": {
      "authority": "ceremonial",
      "classification": "reasoning",
      "seal_hash": "73d33b880cd75a1f3a9ec3b142cfa24066a39d40b956dee2a2c26c2a1602b83f"
    },
    "intent": "Crown.Invocation",
    "realm": "PL-001",
    "reasoning": "",
    "timestamp": "2025-11-12T01:20:38.168302+00:00"
  },
  "status": "reasoning_complete"
}
```

### Audit Verification
```bash
python cli/axiom_cli.py audit AXF-2025-11-11-e2dfa702
```

Output:
```json
{
  "audit_results": {
    "audit_status": "passed",
    "audit_timestamp": "2025-11-12T01:20:49.314299+00:00",
    "dispatch_id": "AXF-2025-11-11-e2dfa702",
    "integrity_checks": {
      "file_exists": true,
      "json_valid": true,
      "required_fields": {
        "actor": true,
        "dispatch_id": true,
        "governance_seal": true,
        "timestamp": true
      }
    },
    "seal_verification": {
      "seal_hash_valid": true,
      "seal_present": true
    }
  },
  "status": "audit_complete"
}
```

## Configuration

### Environment Variables

- `AXIOM_API_BASE` - Override the default API base URL
  - Default: `http://127.0.0.1:8087`
  - Example: `export AXIOM_API_BASE=https://axiom.yourdomain.com`

### Custom API Endpoints

To use a different AXIOM FLAME API server:

```bash
export AXIOM_API_BASE=https://your-axiom-server.com
python cli/axiom_cli.py health
```

## Error Handling

The CLI provides detailed error messages and appropriate exit codes:

- **Exit Code 0**: Success
- **Exit Code 1**: Invalid usage/arguments
- **Exit Code 2**: HTTP error from API
- **Exit Code 3**: JSON parsing error
- **Exit Code 4**: General application error

## Integration Examples

### Bash Script Integration
```bash
#!/bin/bash
DISPATCH_ID=$(python cli/axiom_cli.py reason "AutomatedAgent" "PL-003" "System Check" "Check.Routine" | jq -r '.dispatch_id')
echo "Created dispatch: $DISPATCH_ID"

# Audit the dispatch
python cli/axiom_cli.py audit "$DISPATCH_ID"
```

### PowerShell Integration
```powershell
$result = python cli/axiom_cli.py reason "PowerShellAgent" "PL-004" "Maintenance" "System.Update" | ConvertFrom-Json
$dispatchId = $result.dispatch_id
Write-Host "Dispatch ID: $dispatchId"

# Verify with audit
python cli/axiom_cli.py audit $dispatchId
```

## Troubleshooting

### Connection Issues
1. Verify AXIOM FLAME API is running: `python cli/axiom_cli.py health`
2. Check the API base URL: `echo $AXIOM_API_BASE`
3. Ensure firewall/network allows connection to port 8087

### Authentication Issues
The current CLI version uses the local API without authentication. For production deployments, authentication headers can be added to the requests.

### JSON Parsing Errors
Ensure all command arguments are properly quoted, especially when containing spaces or special characters.

## Development

To extend the CLI with new commands:

1. Add the command function to `cli/axiom_cli.py`
2. Add the command handler in the `main()` function
3. Update this README with usage examples
4. Test with the platform-specific wrappers

## Support

For issues or feature requests related to AXIOM CLI, please refer to the main AXIOM FLAME documentation or create an issue in the project repository.