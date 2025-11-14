#!/usr/bin/env bash
set -euo pipefail

# Ceremonial Ledger Backup Script for Super-Codex-AI
# Performs secure backup of ledger data with ceremonial validation

# Configuration
SRC="${LEDGER_PATH:-./storage/ledger}"
DST="${BACKUP_PATH:-/mnt/cold-storage/ledger}"
BACKUP_LOG="${BACKUP_LOG_PATH:-./logs/ledger_backup.log}"
CEREMONIAL_SEAL="${CEREMONIAL_SEAL:-SS-$(date +%s | sha256sum | cut -c1-10 | tr '[:lower:]' '[:upper:]')}"

# Ensure log directory exists
mkdir -p "$(dirname "$BACKUP_LOG")"
mkdir -p "$DST"

# Logging function with ceremonial formatting
log_ceremonial() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] [SEAL:$CEREMONIAL_SEAL] $message" | tee -a "$BACKUP_LOG"
}

# Ceremonial header
log_ceremonial "INFO" "🔥 CEREMONIAL LEDGER BACKUP INITIATED"
log_ceremonial "INFO" "Source: $SRC"
log_ceremonial "INFO" "Destination: $DST"
log_ceremonial "INFO" "Governance Seal: $CEREMONIAL_SEAL"

# Pre-backup validation
if [[ ! -d "$SRC" ]]; then
    log_ceremonial "ERROR" "Source ledger directory not found: $SRC"
    exit 1
fi

# Count ledger files
LEDGER_FILES=$(find "$SRC" -type f \( -name "*.json" -o -name "*.ledger" \) | wc -l)
log_ceremonial "INFO" "Found $LEDGER_FILES ledger files to backup"

# Pre-backup checksum for integrity verification
if command -v sha256sum >/dev/null 2>&1; then
    CHECKSUM_CMD="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
    CHECKSUM_CMD="shasum -a 256"
else
    log_ceremonial "WARN" "No checksum utility found, proceeding without integrity verification"
    CHECKSUM_CMD=""
fi

if [[ -n "$CHECKSUM_CMD" ]]; then
    PRE_CHECKSUM_FILE="$BACKUP_LOG.pre-checksum"
    find "$SRC" -type f \( -name "*.json" -o -name "*.ledger" \) -exec $CHECKSUM_CMD {} \; > "$PRE_CHECKSUM_FILE"
    log_ceremonial "INFO" "Pre-backup checksums calculated"
fi

# Perform the ceremonial backup with rsync
log_ceremonial "INFO" "Commencing sacred data transfer..."
if rsync -av --checksum --progress "$SRC/" "$DST/" 2>&1 | tee -a "$BACKUP_LOG"; then
    BACKUP_STATUS="SUCCESS"
    log_ceremonial "INFO" "✅ Ledger backup completed successfully"
else
    BACKUP_STATUS="FAILED"
    log_ceremonial "ERROR" "❌ Ledger backup failed"
    exit 1
fi

# Post-backup verification
if [[ -n "$CHECKSUM_CMD" ]]; then
    POST_CHECKSUM_FILE="$BACKUP_LOG.post-checksum"
    find "$DST" -type f \( -name "*.json" -o -name "*.ledger" \) -exec $CHECKSUM_CMD {} \; | sed "s|$DST|$SRC|g" > "$POST_CHECKSUM_FILE"
    
    if diff "$PRE_CHECKSUM_FILE" "$POST_CHECKSUM_FILE" >/dev/null; then
        log_ceremonial "INFO" "🔒 Integrity verification PASSED - checksums match"
    else
        log_ceremonial "ERROR" "🚨 Integrity verification FAILED - checksums do not match"
        exit 1
    fi
fi

# Generate backup manifest
MANIFEST_FILE="$DST/backup_manifest_$(date +%Y%m%d_%H%M%S).json"
cat > "$MANIFEST_FILE" << EOF
{
  "backup_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "ceremonial_seal": "$CEREMONIAL_SEAL",
  "source_path": "$SRC",
  "destination_path": "$DST",
  "files_backed_up": $LEDGER_FILES,
  "backup_status": "$BACKUP_STATUS",
  "integrity_verified": $([ -n "$CHECKSUM_CMD" ] && echo "true" || echo "false"),
  "backup_type": "CEREMONIAL_LEDGER",
  "governance_authority": "SUPER_CODEX_AI"
}
EOF

log_ceremonial "INFO" "📜 Backup manifest created: $MANIFEST_FILE"

# Final ceremonial proclamation
log_ceremonial "INFO" "🎉 CEREMONIAL LEDGER BACKUP COMPLETED WITH HONOR"
log_ceremonial "INFO" "Sacred data preserved under seal: $CEREMONIAL_SEAL"
log_ceremonial "INFO" "Eternal flame of data integrity maintained"

# Set appropriate permissions for cold storage
chmod -R 440 "$DST"
log_ceremonial "INFO" "🔐 Cold storage permissions secured (read-only)"

echo "Backup completed successfully. Check $BACKUP_LOG for details."