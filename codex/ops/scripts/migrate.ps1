#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Database migration and schema management for Super-Codex-AI

.DESCRIPTION
    This script manages database schema migrations, data migrations,
    and system configuration for the Super-Codex-AI system:
    - Run database schema migrations
    - Initialize system with default data
    - Backup and restore database state
    - Validate system configuration

.PARAMETER Action
    Migration action to perform (migrate, init, reset, backup, restore, status)

.PARAMETER Target
    Target migration version (latest, specific version, or rollback target)

.PARAMETER BackupPath
    Path for backup/restore operations

.PARAMETER Force
    Force migration without confirmation prompts

.PARAMETER DryRun
    Show what would be done without executing

.PARAMETER Verbose
    Show detailed migration information

.EXAMPLE
    ./migrate.ps1 -Action migrate
    Run all pending migrations

.EXAMPLE
    ./migrate.ps1 -Action init -Force
    Initialize system with default data

.EXAMPLE
    ./migrate.ps1 -Action backup -BackupPath "./backups/"
    Create database backup

.EXAMPLE
    ./migrate.ps1 -Action status
    Show migration status
#>

param(
    [ValidateSet('migrate', 'init', 'reset', 'backup', 'restore', 'status', 'validate')]
    [string]$Action = 'status',
    
    [string]$Target = 'latest',
    
    [string]$BackupPath,
    
    [switch]$Force = $false,
    
    [switch]$DryRun = $false,
    
    [switch]$Verbose = $false,
    
    [switch]$Help
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Script configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$ApiEndpoint = "http://localhost:8000"
$MigrationsDir = Join-Path $ProjectRoot "migrations"

# Database configuration (from environment or defaults)
$DbConfig = @{
    Host = $env:DB_HOST ?? "localhost"
    Port = $env:DB_PORT ?? 5432
    Database = $env:DB_NAME ?? "codex_db"
    User = $env:DB_USER ?? "codex_user"
    Password = $env:DB_PASSWORD ?? "codex_password"
}

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" "Red"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ️  $Message" "Cyan"
}

function Write-Step {
    param([string]$Message)
    Write-ColorOutput "🔄 $Message" "Yellow"
}

function Show-Help {
    Write-ColorOutput "`n🗃️  Super-Codex-AI Migration Manager" "Magenta"
    Write-ColorOutput "==================================" "Magenta"
    
    Write-Info "Usage: ./migrate.ps1 -Action <action> [options]"
    
    Write-ColorOutput "`nActions:" "Yellow"
    Write-Host "  migrate   - Run database schema migrations"
    Write-Host "  init      - Initialize system with default data"
    Write-Host "  reset     - Reset database to clean state"
    Write-Host "  backup    - Create database backup"
    Write-Host "  restore   - Restore from database backup"
    Write-Host "  status    - Show migration status and system health"
    Write-Host "  validate  - Validate system configuration"
    
    Write-ColorOutput "`nOptions:" "Yellow"
    Write-Host "  -Target     - Migration target (latest, version number, or rollback target)"
    Write-Host "  -BackupPath - Path for backup/restore operations"
    Write-Host "  -Force      - Skip confirmation prompts"
    Write-Host "  -DryRun     - Show actions without executing"
    Write-Host "  -Verbose    - Show detailed information"
    
    Write-ColorOutput "`nExamples:" "Yellow"
    Write-Host "  ./migrate.ps1 -Action status"
    Write-Host "  ./migrate.ps1 -Action migrate -Target latest"
    Write-Host "  ./migrate.ps1 -Action init -Force"
    Write-Host "  ./migrate.ps1 -Action backup -BackupPath ./backups"
    
    exit 0
}

function Test-DatabaseConnection {
    param([hashtable]$Config)
    
    try {
        # Use psql to test connection (requires PostgreSQL client tools)
        $env:PGPASSWORD = $Config.Password
        $testCmd = "psql -h $($Config.Host) -p $($Config.Port) -U $($Config.User) -d $($Config.Database) -c '\q' 2>&1"
        $result = Invoke-Expression $testCmd
        
        if ($LASTEXITCODE -eq 0) {
            return $true
        } else {
            Write-Verbose "Database connection test failed: $result"
            return $false
        }
    }
    catch {
        Write-Verbose "Database connection test failed: $($_.Exception.Message)"
        return $false
    }
    finally {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Test-ApiAvailable {
    try {
        $response = Invoke-RestMethod -Uri "$ApiEndpoint/health" -Method Get -TimeoutSec 5
        return $response.status -eq "healthy"
    }
    catch {
        return $false
    }
}

function Get-MigrationStatus {
    try {
        if (Test-ApiAvailable) {
            # Get status from API
            $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/system/migration-status" -Method Get
            return $response
        } else {
            # Direct database query
            return Get-DatabaseMigrationStatus
        }
    }
    catch {
        Write-Verbose "Failed to get migration status: $($_.Exception.Message)"
        return $null
    }
}

function Get-DatabaseMigrationStatus {
    try {
        $env:PGPASSWORD = $DbConfig.Password
        $query = @"
SELECT 
    version, 
    applied_at,
    description
FROM schema_migrations 
ORDER BY version DESC 
LIMIT 1;
"@
        
        $result = psql -h $DbConfig.Host -p $DbConfig.Port -U $DbConfig.User -d $DbConfig.Database -t -c $query 2>$null
        
        if ($LASTEXITCODE -eq 0 -and $result) {
            $parts = $result.Trim() -split '\|'
            return @{
                current_version = $parts[0].Trim()
                applied_at = $parts[1].Trim()
                description = if ($parts.Count -gt 2) { $parts[2].Trim() } else { "" }
                status = "ready"
            }
        } else {
            return @{
                current_version = "none"
                status = "not_initialized"
            }
        }
    }
    catch {
        return @{
            current_version = "unknown"
            status = "error"
            error = $_.Exception.Message
        }
    }
    finally {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Invoke-Migration {
    param(
        [string]$Target,
        [bool]$DryRun
    )
    
    Write-Step "Running database migrations..."
    
    try {
        if (Test-ApiAvailable) {
            # Use API endpoint
            $requestBody = @{
                target = $Target
                dry_run = $DryRun
            } | ConvertTo-Json
            
            $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/system/migrate" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 120
            
            return $response
        } else {
            # Direct migration execution
            return Invoke-DirectMigration -Target $Target -DryRun $DryRun
        }
    }
    catch {
        throw "Migration failed: $($_.Exception.Message)"
    }
}

function Invoke-DirectMigration {
    param(
        [string]$Target,
        [bool]$DryRun
    )
    
    # This would contain the actual migration logic
    # For now, return a mock response
    Write-Info "Direct migration not implemented - use API endpoint"
    return @{
        success = $false
        error = "Direct migration requires API endpoint"
    }
}

function Initialize-System {
    param([bool]$Force, [bool]$DryRun)
    
    Write-Step "Initializing system with default data..."
    
    if (-not $Force -and -not $DryRun) {
        $confirm = Read-Host "This will initialize the system with default data. Continue? [y/N]"
        if ($confirm.ToLower() -ne 'y') {
            Write-Info "Initialization cancelled"
            return
        }
    }
    
    try {
        if (Test-ApiAvailable) {
            $requestBody = @{
                include_sample_data = $true
                dry_run = $DryRun
            } | ConvertTo-Json
            
            $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/system/initialize" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 180
            
            if ($response.success) {
                Write-Success "System initialization completed"
                if ($response.items_created) {
                    Write-Info "Items created:"
                    foreach ($category in $response.items_created.PSObject.Properties) {
                        Write-Host "  $($category.Name): $($category.Value)" -ForegroundColor White
                    }
                }
            } else {
                throw $response.error
            }
        } else {
            throw "API not available - cannot initialize system"
        }
    }
    catch {
        throw "System initialization failed: $($_.Exception.Message)"
    }
}

function Reset-Database {
    param([bool]$Force, [bool]$DryRun)
    
    Write-Warning "This will completely reset the database and remove all data!"
    
    if (-not $Force -and -not $DryRun) {
        $confirm = Read-Host "Are you sure you want to reset the database? Type 'RESET' to confirm"
        if ($confirm -ne 'RESET') {
            Write-Info "Reset cancelled"
            return
        }
    }
    
    Write-Step "Resetting database..."
    
    try {
        if (Test-ApiAvailable) {
            $requestBody = @{
                confirm = $true
                dry_run = $DryRun
            } | ConvertTo-Json
            
            $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/system/reset" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 120
            
            if ($response.success) {
                Write-Success "Database reset completed"
            } else {
                throw $response.error
            }
        } else {
            throw "API not available - cannot reset database"
        }
    }
    catch {
        throw "Database reset failed: $($_.Exception.Message)"
    }
}

function Backup-Database {
    param([string]$BackupPath, [bool]$DryRun)
    
    if (-not $BackupPath) {
        $BackupPath = Join-Path (Get-Location) "backups"
    }
    
    # Ensure backup directory exists
    if (-not (Test-Path $BackupPath)) {
        New-Item -Path $BackupPath -ItemType Directory -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = Join-Path $BackupPath "codex_backup_$timestamp.sql"
    
    Write-Step "Creating database backup..."
    Write-Info "Backup location: $backupFile"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would create backup at: $backupFile"
        return
    }
    
    try {
        $env:PGPASSWORD = $DbConfig.Password
        $cmd = "pg_dump -h $($DbConfig.Host) -p $($DbConfig.Port) -U $($DbConfig.User) -d $($DbConfig.Database) -f `"$backupFile`""
        
        Invoke-Expression $cmd
        
        if ($LASTEXITCODE -eq 0 -and (Test-Path $backupFile)) {
            $backupSize = (Get-Item $backupFile).Length
            Write-Success "Database backup created successfully"
            Write-Info "Backup size: $([Math]::Round($backupSize / 1MB, 2)) MB"
            Write-Info "Backup file: $backupFile"
        } else {
            throw "pg_dump failed with exit code $LASTEXITCODE"
        }
    }
    catch {
        throw "Database backup failed: $($_.Exception.Message)"
    }
    finally {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Restore-Database {
    param([string]$BackupPath, [bool]$Force, [bool]$DryRun)
    
    if (-not $BackupPath -or -not (Test-Path $BackupPath)) {
        throw "Backup file not found: $BackupPath"
    }
    
    Write-Warning "This will restore the database and overwrite existing data!"
    
    if (-not $Force -and -not $DryRun) {
        $confirm = Read-Host "Are you sure you want to restore from backup? [y/N]"
        if ($confirm.ToLower() -ne 'y') {
            Write-Info "Restore cancelled"
            return
        }
    }
    
    Write-Step "Restoring database from backup..."
    Write-Info "Backup file: $BackupPath"
    
    if ($DryRun) {
        Write-Info "[DRY RUN] Would restore from: $BackupPath"
        return
    }
    
    try {
        $env:PGPASSWORD = $DbConfig.Password
        
        # Drop and recreate database
        Write-Info "Dropping and recreating database..."
        $dropCmd = "psql -h $($DbConfig.Host) -p $($DbConfig.Port) -U $($DbConfig.User) -d postgres -c `"DROP DATABASE IF EXISTS $($DbConfig.Database);`""
        Invoke-Expression $dropCmd
        
        $createCmd = "psql -h $($DbConfig.Host) -p $($DbConfig.Port) -U $($DbConfig.User) -d postgres -c `"CREATE DATABASE $($DbConfig.Database);`""
        Invoke-Expression $createCmd
        
        # Restore from backup
        Write-Info "Restoring data..."
        $restoreCmd = "psql -h $($DbConfig.Host) -p $($DbConfig.Port) -U $($DbConfig.User) -d $($DbConfig.Database) -f `"$BackupPath`""
        Invoke-Expression $restoreCmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Database restore completed successfully"
        } else {
            throw "psql restore failed with exit code $LASTEXITCODE"
        }
    }
    catch {
        throw "Database restore failed: $($_.Exception.Message)"
    }
    finally {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
    }
}

function Show-SystemStatus {
    Write-ColorOutput "`n🌐 System Status" "Magenta"
    Write-ColorOutput "=============" "Magenta"
    
    # API Status
    Write-Info "Checking API availability..."
    if (Test-ApiAvailable) {
        Write-Success "API is available at $ApiEndpoint"
    } else {
        Write-Warning "API is not available at $ApiEndpoint"
    }
    
    # Database Connection
    Write-Info "Checking database connection..."
    if (Test-DatabaseConnection -Config $DbConfig) {
        Write-Success "Database connection successful"
    } else {
        Write-Error "Database connection failed"
    }
    
    # Migration Status
    Write-Info "Checking migration status..."
    $migrationStatus = Get-MigrationStatus
    
    if ($migrationStatus) {
        Write-ColorOutput "`n🗃️  Migration Information" "Yellow"
        Write-Host "Current version: $($migrationStatus.current_version)" -ForegroundColor White
        Write-Host "Status: $($migrationStatus.status)" -ForegroundColor White
        
        if ($migrationStatus.applied_at) {
            Write-Host "Applied at: $($migrationStatus.applied_at)" -ForegroundColor White
        }
        
        if ($migrationStatus.description) {
            Write-Host "Description: $($migrationStatus.description)" -ForegroundColor White
        }
        
        if ($migrationStatus.pending_migrations) {
            Write-Warning "Pending migrations: $($migrationStatus.pending_migrations.Count)"
        }
    } else {
        Write-Warning "Could not retrieve migration status"
    }
    
    # System Health
    if (Test-ApiAvailable) {
        try {
            $health = Invoke-RestMethod -Uri "$ApiEndpoint/health" -Method Get
            
            Write-ColorOutput "`n❤️  System Health" "Yellow"
            Write-Host "Status: $($health.status)" -ForegroundColor Green
            Write-Host "Version: $($health.version)" -ForegroundColor White
            Write-Host "Uptime: $($health.uptime)" -ForegroundColor White
            
            if ($health.components) {
                Write-Info "Component status:"
                foreach ($component in $health.components.PSObject.Properties) {
                    $status = $component.Value.status
                    $color = if ($status -eq "healthy") { "Green" } else { "Red" }
                    Write-Host "  $($component.Name): $status" -ForegroundColor $color
                }
            }
        }
        catch {
            Write-Warning "Could not retrieve system health information"
        }
    }
}

function Invoke-SystemValidation {
    Write-Step "Validating system configuration..."
    
    $issues = @()
    
    # Check environment variables
    $requiredEnvVars = @('DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD')
    foreach ($var in $requiredEnvVars) {
        if (-not (Get-ChildItem Env:$var -ErrorAction SilentlyContinue)) {
            $issues += "Missing environment variable: $var"
        }
    }
    
    # Check database connection
    if (-not (Test-DatabaseConnection -Config $DbConfig)) {
        $issues += "Database connection failed"
    }
    
    # Check required directories
    $requiredDirs = @(
        (Join-Path $ProjectRoot "data"),
        (Join-Path $ProjectRoot "logs"),
        (Join-Path $ProjectRoot "config")
    )
    
    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path $dir)) {
            $issues += "Missing directory: $dir"
        }
    }
    
    # Show results
    if ($issues.Count -eq 0) {
        Write-Success "System validation passed"
    } else {
        Write-Warning "System validation found issues:"
        foreach ($issue in $issues) {
            Write-Host "  - $issue" -ForegroundColor Red
        }
    }
}

# ============================================================================
# Main Execution
# ============================================================================

if ($Help) {
    Show-Help
}

Write-ColorOutput "`n🗃️  Super-Codex-AI Migration Manager" "Magenta"
Write-ColorOutput "==================================" "Magenta"

try {
    switch ($Action) {
        'status' {
            Show-SystemStatus
        }
        
        'validate' {
            Invoke-SystemValidation
        }
        
        'migrate' {
            Write-Info "Starting database migration to target: $Target"
            if ($DryRun) {
                Write-Warning "DRY RUN MODE - No changes will be made"
            }
            
            $result = Invoke-Migration -Target $Target -DryRun $DryRun
            
            if ($result.success) {
                Write-Success "Migration completed successfully"
                if ($result.migrations_applied) {
                    Write-Info "Migrations applied: $($result.migrations_applied.Count)"
                }
            } else {
                throw $result.error
            }
        }
        
        'init' {
            Initialize-System -Force $Force -DryRun $DryRun
        }
        
        'reset' {
            Reset-Database -Force $Force -DryRun $DryRun
        }
        
        'backup' {
            Backup-Database -BackupPath $BackupPath -DryRun $DryRun
        }
        
        'restore' {
            if (-not $BackupPath) {
                Write-Error "BackupPath is required for restore operation"
                exit 1
            }
            Restore-Database -BackupPath $BackupPath -Force $Force -DryRun $DryRun
        }
        
        default {
            Write-Error "Unknown action: $Action"
            Show-Help
        }
    }
    
    Write-Success "Operation completed successfully"
}
catch {
    Write-Error "Operation failed: $($_.Exception.Message)"
    exit 1
}
