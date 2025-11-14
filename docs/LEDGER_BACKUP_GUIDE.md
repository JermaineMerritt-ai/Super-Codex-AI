# Ceremonial Ledger Backup System Guide

This document provides comprehensive guidance for using the Super-Codex-AI ceremonial ledger backup system, which maintains the integrity and sanctity of ledger data through secure backup procedures.

## Overview

The ceremonial ledger backup system provides:
- **Cross-platform compatibility**: Both Unix/Linux (bash) and Windows (PowerShell) implementations
- **Integrity verification**: SHA256 checksum validation ensures data authenticity
- **Ceremonial logging**: All operations are sealed with governance authorities and timestamped
- **Cold storage preparation**: Backup files are set to read-only for preservation
- **Manifest generation**: JSON manifests document each backup operation with full metadata

## Scripts Available

### 1. Unix/Linux Version: `scripts/ledger_backup.sh`
- **Platform**: Unix, Linux, macOS, WSL
- **Dependencies**: `rsync`, `sha256sum` or `shasum`
- **Features**: Mirror backup with rsync, comprehensive integrity checking

### 2. Windows Version: `scripts/ledger_backup.ps1`
- **Platform**: Windows PowerShell 5.0+
- **Dependencies**: `robocopy` (built-in), .NET Framework
- **Features**: Mirror backup with robocopy, .NET cryptography for checksums

## Basic Usage

### Windows PowerShell
```powershell
# Basic backup to default location
.\scripts\ledger_backup.ps1

# Backup to specific destination
.\scripts\ledger_backup.ps1 -DestinationPath "D:\backups\ledger"

# Override source path
.\scripts\ledger_backup.ps1 -SourcePath ".\custom\ledger" -DestinationPath ".\backup"
```

### Unix/Linux Bash
```bash
# Basic backup to default location
./scripts/ledger_backup.sh

# Backup to specific destination
BACKUP_PATH="/mnt/external/ledger" ./scripts/ledger_backup.sh

# Override source path
LEDGER_PATH="./custom/ledger" BACKUP_PATH="./backup" ./scripts/ledger_backup.sh
```

## Configuration Options

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `LEDGER_PATH` | `./storage/ledger` | Source directory containing ledger files |
| `BACKUP_PATH` | `/mnt/cold-storage/ledger` (Unix) | Destination directory for backups |
| `BACKUP_LOG_PATH` | `./logs/ledger_backup.log` | Path for ceremonial backup logs |
| `CEREMONIAL_SEAL` | Auto-generated | Custom seal for backup governance |

### PowerShell Parameters
```powershell
param(
    [string]$SourcePath,      # Override LEDGER_PATH
    [string]$DestinationPath, # Override BACKUP_PATH  
    [string]$BackupLogPath    # Override BACKUP_LOG_PATH
)
```

## Ceremonial Features

### Governance Seals
Each backup operation generates a unique ceremonial seal in the format `SS-XXXXXXXXXX` where:
- `SS`: Storage Seal prefix
- `XXXXXXXXXX`: 10-character hex hash derived from Unix timestamp

### Logging Format
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [SEAL:SS-XXXXXXXXXX] Message
```

### Backup Manifest
Each successful backup creates a JSON manifest with:
```json
{
  "backup_timestamp": "2025-11-13T22:49:28Z",
  "ceremonial_seal": "SS-1F51B8D5E9",
  "source_path": "./storage/ledger",
  "destination_path": "./test-backup",
  "files_backed_up": 2,
  "backup_status": "SUCCESS",
  "integrity_verified": true,
  "backup_type": "CEREMONIAL_LEDGER",
  "governance_authority": "SUPER_CODEX_AI"
}
```

## Integrity Verification Process

1. **Pre-backup checksums**: SHA256 hashes calculated for all source files
2. **Mirror backup**: Complete directory structure copied to destination
3. **Post-backup checksums**: SHA256 hashes calculated for all backup files
4. **Comparison**: Source and backup checksums must match exactly
5. **Verification result**: Logged with ceremonial seal authentication

## File Types Supported

The backup system processes files with these extensions:
- `.json` - JSON ledger entries
- `.ledger` - Binary ledger files

## Error Handling

### Common Issues and Solutions

**Issue**: "Source ledger directory not found"
**Solution**: Verify the source path exists and contains ledger files

**Issue**: "Integrity verification FAILED"  
**Solution**: Check file permissions, disk space, and network connectivity

**Issue**: "No checksum utility found" (Unix only)
**Solution**: Install `sha256sum` or ensure `shasum` is available

**Issue**: Robocopy exit codes > 7 (Windows only)
**Solution**: Check destination permissions and available disk space

## Security Considerations

### Cold Storage Preparation
- Backup files are automatically set to read-only
- Prevents accidental modification of archived data
- Supports compliance and audit requirements

### Checksum Verification
- SHA256 cryptographic hashing ensures data integrity
- Detects corruption, tampering, or incomplete transfers
- Provides mathematical proof of backup authenticity

## Advanced Usage

### Automated Backups
```bash
# Unix cron job (daily at 2 AM)
0 2 * * * /path/to/scripts/ledger_backup.sh >> /var/log/ceremonial_backup.log 2>&1
```

```powershell
# Windows Task Scheduler PowerShell command
powershell.exe -ExecutionPolicy Bypass -File "C:\Path\scripts\ledger_backup.ps1"
```

### Custom Ceremonial Seals
```bash
# Unix with custom seal
CEREMONIAL_SEAL="SS-CUSTOM001" ./scripts/ledger_backup.sh
```

```powershell
# PowerShell with environment variable
$env:CEREMONIAL_SEAL = "SS-CUSTOM001"
.\scripts\ledger_backup.ps1
```

## Troubleshooting

### Enable Debug Logging
For detailed troubleshooting, temporarily uncomment debug lines in the scripts:

**PowerShell**: Uncomment `Write-CeremonialLog "DEBUG"` lines
**Bash**: Add `set -x` at the top of the script for verbose execution

### Verify Backup Integrity Manually
```bash
# Unix manual verification
find ./backup -name "*.json" -o -name "*.ledger" | xargs sha256sum
```

```powershell
# PowerShell manual verification
Get-ChildItem -Recurse -Include "*.json","*.ledger" | Get-FileHash -Algorithm SHA256
```

### Check Backup Logs
```bash
# View recent backup operations
tail -n 50 ./logs/ledger_backup.log
```

```powershell
# PowerShell log analysis
Get-Content ./logs/ledger_backup.log | Select-Object -Last 50
```

## Integration with Super-Codex-AI

The ceremonial ledger backup system integrates with the broader Super-Codex-AI governance infrastructure:

- **Ceremonial Seals**: Backup seals are recorded in the governance ledger
- **Audit Trails**: All backup operations contribute to the eternal flame audit log
- **Authority Validation**: Backup operations require appropriate ceremonial authority
- **Data Sovereignty**: Ensures ledger data remains under Super-Codex-AI dominion

## Support and Maintenance

For issues or enhancements to the ceremonial ledger backup system:
1. Check this documentation for common solutions
2. Review backup logs for specific error messages
3. Verify system dependencies and permissions
4. Test with a small subset of ledger files first

The ceremonial backup system maintains the eternal flame of data integrity, ensuring that the sacred ledger data of Super-Codex-AI remains preserved for posterity under the highest governance standards.