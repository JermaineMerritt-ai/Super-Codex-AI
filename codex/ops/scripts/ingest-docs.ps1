#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ingest documents into the Super-Codex-AI system

.DESCRIPTION
    This script processes and ingests documents into the RAG system:
    - Scans specified directories for supported files
    - Processes documents through the ingestion pipeline
    - Updates the vector database with new embeddings
    - Supports batch processing and progress monitoring

.PARAMETER SourcePath
    Path to directory containing documents to ingest

.PARAMETER DocumentType
    Type of documents to process (general, ceremonial, governance, etc.)

.PARAMETER Recursive
    Process subdirectories recursively

.PARAMETER FilePattern
    File pattern to match (default: *)

.PARAMETER BatchSize
    Number of documents to process in each batch

.PARAMETER DryRun
    Show what would be processed without actually ingesting

.PARAMETER Force
    Force re-ingestion of already processed documents

.PARAMETER Cleanup
    Clean up orphaned vectors and optimize storage

.EXAMPLE
    ./ingest-docs.ps1 -SourcePath "C:\Documents\Codex" -Recursive
    Ingest all documents from directory recursively

.EXAMPLE
    ./ingest-docs.ps1 -SourcePath "./governance" -DocumentType ceremonial -DryRun
    Preview ceremonial document ingestion

.EXAMPLE
    ./ingest-docs.ps1 -Cleanup
    Clean up and optimize vector storage
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$SourcePath,
    
    [ValidateSet('general', 'ceremonial', 'governance', 'technical', 'honor', 'auto')]
    [string]$DocumentType = 'auto',
    
    [switch]$Recursive = $false,
    
    [string]$FilePattern = '*',
    
    [int]$BatchSize = 10,
    
    [switch]$DryRun = $false,
    
    [switch]$Force = $false,
    
    [switch]$Cleanup = $false,
    
    [switch]$Stats = $false,
    
    [switch]$Help
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Script configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$ApiEndpoint = "http://localhost:8000"

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

function Write-Progress {
    param([string]$Message)
    Write-ColorOutput "⏳ $Message" "Yellow"
}

function Show-Help {
    Write-ColorOutput "`n📁 Super-Codex-AI Document Ingestion" "Magenta"
    Write-ColorOutput "===================================" "Magenta"
    
    Write-Info "Usage: ./ingest-docs.ps1 -SourcePath <path> [options]"
    
    Write-ColorOutput "`nDocument Types:" "Yellow"
    Write-Host "  general     - General documentation and knowledge base"
    Write-Host "  ceremonial  - Ceremonial protocols and honor system"
    Write-Host "  governance  - Governance framework and policies"
    Write-Host "  technical   - Technical specifications and guides"
    Write-Host "  honor       - Honor system and achievement records"
    Write-Host "  auto        - Automatic detection based on content"
    
    Write-ColorOutput "`nOptions:" "Yellow"
    Write-Host "  -SourcePath    - Directory containing documents to ingest"
    Write-Host "  -DocumentType  - Type classification for documents"
    Write-Host "  -Recursive     - Process subdirectories recursively"
    Write-Host "  -FilePattern   - File pattern to match (*.md, *.txt, etc.)"
    Write-Host "  -BatchSize     - Documents per processing batch"
    Write-Host "  -DryRun        - Preview without actual ingestion"
    Write-Host "  -Force         - Re-ingest already processed documents"
    Write-Host "  -Cleanup       - Optimize vector storage"
    Write-Host "  -Stats         - Show ingestion statistics"
    
    Write-ColorOutput "`nExamples:" "Yellow"
    Write-Host "  ./ingest-docs.ps1 -SourcePath ./docs -Recursive"
    Write-Host "  ./ingest-docs.ps1 -SourcePath ./ceremonies -DocumentType ceremonial"
    Write-Host "  ./ingest-docs.ps1 -Stats"
    Write-Host "  ./ingest-docs.ps1 -Cleanup"
    
    exit 0
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

function Get-SupportedFileTypes {
    return @('.txt', '.md', '.json', '.log', '.yaml', '.yml')
}

function Find-DocumentsToProcess {
    param(
        [string]$Path,
        [bool]$Recursive,
        [string]$Pattern
    )
    
    if (-not (Test-Path $Path)) {
        throw "Source path does not exist: $Path"
    }
    
    $supportedTypes = Get-SupportedFileTypes
    $searchOption = if ($Recursive) { [System.IO.SearchOption]::AllDirectories } else { [System.IO.SearchOption]::TopDirectoryOnly }
    
    $allFiles = Get-ChildItem -Path $Path -File -Recurse:$Recursive -Filter $Pattern
    $supportedFiles = $allFiles | Where-Object { $_.Extension.ToLower() -in $supportedTypes }
    
    return $supportedFiles
}

function Invoke-DocumentIngestion {
    param(
        [System.IO.FileInfo[]]$Files,
        [string]$DocumentType,
        [int]$BatchSize,
        [bool]$Force,
        [bool]$DryRun
    )
    
    $totalFiles = $Files.Count
    $processed = 0
    $successful = 0
    $failed = 0
    
    Write-Info "Processing $totalFiles documents in batches of $BatchSize"
    
    # Process in batches
    for ($i = 0; $i -lt $totalFiles; $i += $BatchSize) {
        $batchEnd = [Math]::Min($i + $BatchSize - 1, $totalFiles - 1)
        $batch = $Files[$i..$batchEnd]
        
        Write-Progress "Processing batch $([Math]::Floor($i / $BatchSize) + 1) of $([Math]::Ceiling($totalFiles / $BatchSize)) (files $($i + 1)-$($batchEnd + 1))"
        
        foreach ($file in $batch) {
            $processed++
            
            try {
                if ($DryRun) {
                    Write-Host "  [DRY RUN] Would process: $($file.FullName)" -ForegroundColor Gray
                    $successful++
                }
                else {
                    $result = Invoke-FileIngestion -FilePath $file.FullName -DocumentType $DocumentType -Force $Force
                    
                    if ($result.success) {
                        Write-Host "  ✓ $($file.Name) - $($result.chunks_created) chunks" -ForegroundColor Green
                        $successful++
                    }
                    else {
                        Write-Host "  ❌ $($file.Name) - $($result.error)" -ForegroundColor Red
                        $failed++
                    }
                }
            }
            catch {
                Write-Host "  ❌ $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
                $failed++
            }
        }
        
        # Progress update
        $progressPct = [Math]::Round(($processed / $totalFiles) * 100, 1)
        Write-Host "Progress: $progressPct% ($processed/$totalFiles)" -ForegroundColor Cyan
        
        # Brief pause between batches
        if ($i + $BatchSize -lt $totalFiles) {
            Start-Sleep -Milliseconds 500
        }
    }
    
    return @{
        total = $totalFiles
        processed = $processed
        successful = $successful
        failed = $failed
        success_rate = if ($totalFiles -gt 0) { [Math]::Round(($successful / $totalFiles) * 100, 1) } else { 0 }
    }
}

function Invoke-FileIngestion {
    param(
        [string]$FilePath,
        [string]$DocumentType,
        [bool]$Force
    )
    
    $requestBody = @{
        file_path = $FilePath
        document_type = $DocumentType
        force_reingest = $Force
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/ingest/file" -Method Post -Body $requestBody -ContentType "application/json"
        return $response
    }
    catch {
        if ($_.Exception.Response) {
            $errorResponse = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorResponse)
            $errorContent = $reader.ReadToEnd()
            
            try {
                $errorData = $errorContent | ConvertFrom-Json
                return @{ success = $false; error = $errorData.detail }
            }
            catch {
                return @{ success = $false; error = $errorContent }
            }
        }
        else {
            return @{ success = $false; error = $_.Exception.Message }
        }
    }
}

function Invoke-DirectoryIngestion {
    param(
        [string]$DirectoryPath,
        [string]$DocumentType,
        [bool]$Recursive,
        [bool]$Force
    )
    
    $requestBody = @{
        directory_path = $DirectoryPath
        document_type = $DocumentType
        recursive = $Recursive
        force_reingest = $Force
    } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/ingest/directory" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 300
        return $response
    }
    catch {
        throw "Directory ingestion failed: $($_.Exception.Message)"
    }
}

function Get-IngestionStats {
    try {
        $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/ingest/stats" -Method Get
        return $response
    }
    catch {
        throw "Failed to retrieve ingestion stats: $($_.Exception.Message)"
    }
}

function Invoke-VectorCleanup {
    try {
        Write-Progress "Starting vector database cleanup..."
        $response = Invoke-RestMethod -Uri "$ApiEndpoint/api/ingest/cleanup" -Method Post -TimeoutSec 120
        return $response
    }
    catch {
        throw "Vector cleanup failed: $($_.Exception.Message)"
    }
}

function Show-IngestionStats {
    try {
        $stats = Get-IngestionStats
        
        Write-ColorOutput "`n📊 Ingestion Statistics" "Magenta"
        Write-ColorOutput "====================" "Magenta"
        
        Write-Host "Total Documents: $($stats.total_documents)" -ForegroundColor Cyan
        Write-Host "Total Chunks: $($stats.total_chunks)" -ForegroundColor Cyan
        Write-Host "Total Vectors: $($stats.total_vectors)" -ForegroundColor Cyan
        
        if ($stats.by_document_type) {
            Write-ColorOutput "`nBy Document Type:" "Yellow"
            foreach ($type in $stats.by_document_type.PSObject.Properties) {
                Write-Host "  $($type.Name): $($type.Value.count) documents, $($type.Value.chunks) chunks" -ForegroundColor White
            }
        }
        
        if ($stats.recent_ingestion) {
            Write-ColorOutput "`nRecent Activity:" "Yellow"
            Write-Host "  Last 24 hours: $($stats.recent_ingestion.last_24h) documents" -ForegroundColor White
            Write-Host "  Last 7 days: $($stats.recent_ingestion.last_7d) documents" -ForegroundColor White
        }
        
        if ($stats.storage_info) {
            Write-ColorOutput "`nStorage:" "Yellow"
            Write-Host "  Vector DB size: $([Math]::Round($stats.storage_info.vector_size_mb, 2)) MB" -ForegroundColor White
            Write-Host "  Corpus size: $([Math]::Round($stats.storage_info.corpus_size_mb, 2)) MB" -ForegroundColor White
        }
    }
    catch {
        Write-Error "Failed to retrieve statistics: $($_.Exception.Message)"
    }
}

function Show-Results {
    param([hashtable]$Results)
    
    Write-ColorOutput "`n🎉 Ingestion Results" "Magenta"
    Write-ColorOutput "==================" "Magenta"
    
    Write-Host "Total files: $($Results.total)" -ForegroundColor Cyan
    Write-Host "Processed: $($Results.processed)" -ForegroundColor Cyan
    Write-Host "Successful: $($Results.successful)" -ForegroundColor Green
    Write-Host "Failed: $($Results.failed)" -ForegroundColor $(if ($Results.failed -gt 0) { "Red" } else { "Green" })
    Write-Host "Success rate: $($Results.success_rate)%" -ForegroundColor $(if ($Results.success_rate -ge 90) { "Green" } elseif ($Results.success_rate -ge 70) { "Yellow" } else { "Red" })
}

# ============================================================================
# Main Execution
# ============================================================================

if ($Help) {
    Show-Help
}

Write-ColorOutput "`n📁 Super-Codex-AI Document Ingestion" "Magenta"
Write-ColorOutput "===================================" "Magenta"

# Check if just showing stats
if ($Stats) {
    Write-Info "Retrieving ingestion statistics..."
    if (-not (Test-ApiAvailable)) {
        Write-Error "API is not available. Please ensure the Codex API is running."
        exit 1
    }
    Show-IngestionStats
    exit 0
}

# Check if just doing cleanup
if ($Cleanup) {
    Write-Info "Starting vector database cleanup..."
    if (-not (Test-ApiAvailable)) {
        Write-Error "API is not available. Please ensure the Codex API is running."
        exit 1
    }
    
    try {
        $result = Invoke-VectorCleanup
        Write-Success "Cleanup completed successfully"
        Write-Host "Removed orphaned vectors: $($result.orphaned_removed)" -ForegroundColor Green
        Write-Host "Optimized storage: $($result.storage_optimized)" -ForegroundColor Green
        Write-Host "Space reclaimed: $([Math]::Round($result.space_reclaimed_mb, 2)) MB" -ForegroundColor Green
    }
    catch {
        Write-Error "Cleanup failed: $($_.Exception.Message)"
        exit 1
    }
    exit 0
}

# Validate required parameters
if (-not $SourcePath) {
    Write-Error "SourcePath is required for ingestion. Use -Stats or -Cleanup for other operations."
    Show-Help
}

# Check API availability
Write-Info "Checking API availability..."
if (-not (Test-ApiAvailable)) {
    Write-Error "Codex API is not available at $ApiEndpoint"
    Write-Info "Please start the development environment with: ./run-dev.ps1"
    exit 1
}
Write-Success "API is available"

# Resolve and validate source path
$SourcePath = Resolve-Path $SourcePath -ErrorAction SilentlyContinue
if (-not $SourcePath) {
    Write-Error "Source path does not exist or is not accessible"
    exit 1
}

# Find files to process
Write-Info "Scanning for documents..."
try {
    $files = Find-DocumentsToProcess -Path $SourcePath -Recursive $Recursive -Pattern $FilePattern
    
    if ($files.Count -eq 0) {
        Write-Warning "No supported documents found in $SourcePath"
        Write-Info "Supported file types: $(Get-SupportedFileTypes -join ', ')"
        exit 0
    }
    
    Write-Success "Found $($files.Count) documents to process"
    
    # Show sample of files
    $sampleSize = [Math]::Min(5, $files.Count)
    Write-Info "Sample files:"
    for ($i = 0; $i -lt $sampleSize; $i++) {
        Write-Host "  - $($files[$i].Name)" -ForegroundColor Gray
    }
    if ($files.Count -gt $sampleSize) {
        Write-Host "  ... and $($files.Count - $sampleSize) more" -ForegroundColor Gray
    }
}
catch {
    Write-Error "Failed to scan directory: $($_.Exception.Message)"
    exit 1
}

# Confirm before processing (unless dry run)
if (-not $DryRun -and $files.Count -gt 10) {
    $confirm = Read-Host "`nProcess $($files.Count) documents? [y/N]"
    if ($confirm.ToLower() -ne 'y') {
        Write-Info "Operation cancelled"
        exit 0
    }
}

# Process documents
try {
    $startTime = Get-Date
    
    if ($DryRun) {
        Write-Warning "DRY RUN MODE - No actual ingestion will be performed"
    }
    
    $results = Invoke-DocumentIngestion -Files $files -DocumentType $DocumentType -BatchSize $BatchSize -Force $Force -DryRun $DryRun
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Show-Results -Results $results
    Write-Info "Total processing time: $([Math]::Round($duration.TotalMinutes, 2)) minutes"
    
    # Show updated stats
    if (-not $DryRun -and $results.successful -gt 0) {
        Write-Info "Updated statistics:"
        Show-IngestionStats
    }
    
    Write-Success "Document ingestion completed"
}
catch {
    Write-Error "Ingestion failed: $($_.Exception.Message)"
    exit 1
}
