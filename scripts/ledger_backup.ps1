# Ceremonial Ledger Backup Script for Super-Codex-AI (PowerShell Version)
# Performs secure backup of ledger data with ceremonial validation

param(
    [string]$SourcePath = $(if ($env:LEDGER_PATH) { $env:LEDGER_PATH } else { "./storage/ledger" }),
    [string]$DestinationPath = $(if ($env:BACKUP_PATH) { $env:BACKUP_PATH } else { "/mnt/cold-storage/ledger" }),
    [string]$BackupLogPath = $(if ($env:BACKUP_LOG_PATH) { $env:BACKUP_LOG_PATH } else { "./logs/ledger_backup.log" })
)

# Generate ceremonial seal
$UnixTime = [System.DateTimeOffset]::UtcNow.ToUnixTimeSeconds().ToString()
$CeremonialSeal = "SS-" + ([System.Security.Cryptography.SHA256]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($UnixTime)) | ForEach-Object { $_.ToString("X2") } | Join-String).Substring(0,10)

# Ensure directories exist
$LogDir = Split-Path $BackupLogPath -Parent
if (!(Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

if (!(Test-Path $DestinationPath)) {
    New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
}

# Logging function with ceremonial formatting
function Write-CeremonialLog {
    param([string]$Level, [string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] [SEAL:$CeremonialSeal] $Message"
    Write-Host $LogEntry
    Add-Content -Path $BackupLogPath -Value $LogEntry
}

# Ceremonial header
Write-CeremonialLog "INFO" "🔥 CEREMONIAL LEDGER BACKUP INITIATED"
Write-CeremonialLog "INFO" "Source: $SourcePath"
Write-CeremonialLog "INFO" "Destination: $DestinationPath"
Write-CeremonialLog "INFO" "Governance Seal: $CeremonialSeal"

# Pre-backup validation
if (!(Test-Path $SourcePath)) {
    Write-CeremonialLog "ERROR" "Source ledger directory not found: $SourcePath"
    exit 1
}

# Count ledger files
$LedgerFiles = Get-ChildItem -Path $SourcePath -Recurse -File | Where-Object { $_.Extension -in @('.json', '.ledger') }
$FileCount = $LedgerFiles.Count
Write-CeremonialLog "INFO" "Found $FileCount ledger files to backup"

# Pre-backup checksums for integrity verification
$PreChecksumFile = "$BackupLogPath.pre-checksum"
$PreChecksums = @{}
foreach ($File in $LedgerFiles) {
    $Hash = Get-FileHash -Path $File.FullName -Algorithm SHA256
    $PreChecksums[$File.FullName] = $Hash.Hash
    "$($Hash.Hash) $($File.FullName)" | Add-Content -Path $PreChecksumFile
}
Write-CeremonialLog "INFO" "Pre-backup checksums calculated"

# Perform the ceremonial backup
Write-CeremonialLog "INFO" "Commencing sacred data transfer..."
try {
    # Use robocopy for Windows (equivalent to rsync)
    $RobocopyLogPath = $BackupLogPath + '.robocopy'
    $RobocopyArgs = @(
        $SourcePath,
        $DestinationPath,
        '/MIR',  # Mirror directory tree
        '/R:3',  # Retry 3 times on failed copies
        '/W:5',  # Wait 5 seconds between retries
        "/LOG+:$RobocopyLogPath"
    )
    
    $Result = Start-Process -FilePath "robocopy" -ArgumentList $RobocopyArgs -Wait -PassThru -NoNewWindow
    
    # Robocopy exit codes 0-7 are considered successful
    if ($Result.ExitCode -le 7) {
        $BackupStatus = "SUCCESS"
        Write-CeremonialLog "INFO" "✅ Ledger backup completed successfully"
    } else {
        $BackupStatus = "FAILED"
        Write-CeremonialLog "ERROR" "❌ Ledger backup failed with exit code $($Result.ExitCode)"
        exit 1
    }
} catch {
    $BackupStatus = "FAILED"
    Write-CeremonialLog "ERROR" "❌ Ledger backup failed: $($_.Exception.Message)"
    exit 1
}

# Post-backup verification
$PostChecksumFile = "$BackupLogPath.post-checksum"
$PostChecksums = @{}
$BackupFiles = Get-ChildItem -Path $DestinationPath -Recurse -File | Where-Object { $_.Extension -in @('.json', '.ledger') }

# Normalize paths for comparison
$NormalizedSourcePath = (Resolve-Path $SourcePath).Path
$NormalizedDestPath = (Resolve-Path $DestinationPath).Path

Write-CeremonialLog "INFO" "Verifying integrity of $($BackupFiles.Count) backup files..."

foreach ($File in $BackupFiles) {
    $Hash = Get-FileHash -Path $File.FullName -Algorithm SHA256
    # Calculate the relative path from destination root
    $RelativePath = $File.FullName.Substring($NormalizedDestPath.Length).TrimStart('\')
    # Map to original source path
    $OriginalPath = Join-Path $NormalizedSourcePath $RelativePath
    $PostChecksums[$OriginalPath] = $Hash.Hash
    "$($Hash.Hash) $OriginalPath" | Add-Content -Path $PostChecksumFile
    # Write-CeremonialLog "DEBUG" "Backup file: $($File.FullName) -> Original: $OriginalPath"
}

# Compare checksums
$IntegrityPassed = $true
$CheckedFiles = 0
foreach ($OriginalPath in $PreChecksums.Keys) {
    $CheckedFiles++
    if (-not $PostChecksums.ContainsKey($OriginalPath)) {
        Write-CeremonialLog "WARN" "Missing backup file: $OriginalPath"
        $IntegrityPassed = $false
        break
    }
    
    if ($PreChecksums[$OriginalPath] -ne $PostChecksums[$OriginalPath]) {
        Write-CeremonialLog "WARN" "Checksum mismatch for: $OriginalPath"
        Write-CeremonialLog "DEBUG" "Original: $($PreChecksums[$OriginalPath]) vs Backup: $($PostChecksums[$OriginalPath])"
        $IntegrityPassed = $false
        break
    }
}

if ($IntegrityPassed) {
    Write-CeremonialLog "INFO" "🔒 Integrity verification PASSED - checksums match"
} else {
    Write-CeremonialLog "ERROR" "🚨 Integrity verification FAILED - checksums do not match"
    exit 1
}

# Generate backup manifest
$ManifestFile = Join-Path $DestinationPath "backup_manifest_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$Manifest = @{
    backup_timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    ceremonial_seal = $CeremonialSeal
    source_path = $SourcePath
    destination_path = $DestinationPath
    files_backed_up = $FileCount
    backup_status = $BackupStatus
    integrity_verified = $true
    backup_type = "CEREMONIAL_LEDGER"
    governance_authority = "SUPER_CODEX_AI"
} | ConvertTo-Json -Depth 3

$Manifest | Set-Content -Path $ManifestFile
Write-CeremonialLog "INFO" "📜 Backup manifest created: $ManifestFile"

# Final ceremonial proclamation
Write-CeremonialLog "INFO" "🎉 CEREMONIAL LEDGER BACKUP COMPLETED WITH HONOR"
Write-CeremonialLog "INFO" "Sacred data preserved under seal: $CeremonialSeal"
Write-CeremonialLog "INFO" "Eternal flame of data integrity maintained"

# Set read-only permissions for cold storage (Windows equivalent)
Get-ChildItem -Path $DestinationPath -Recurse | ForEach-Object {
    $_.Attributes = $_.Attributes -bor [System.IO.FileAttributes]::ReadOnly
}
Write-CeremonialLog "INFO" "🔐 Cold storage permissions secured (read-only)"

Write-Host "Backup completed successfully. Check $BackupLogPath for details." -ForegroundColor Green