#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start the Super-Codex-AI development environment

.DESCRIPTION
    This script starts the complete development environment including:
    - Codex API server
    - PostgreSQL database
    - Redis cache
    - MinIO storage
    - Monitoring stack (Prometheus, Grafana)
    - Supporting services

.PARAMETER Mode
    Development mode: 'full' (all services), 'api' (API only), 'minimal' (core services only)

.PARAMETER Build
    Force rebuild of Docker images

.PARAMETER Logs
    Show logs after startup

.PARAMETER Background
    Run services in background (detached mode)

.EXAMPLE
    ./run-dev.ps1
    Start full development environment

.EXAMPLE
    ./run-dev.ps1 -Mode minimal -Build
    Start minimal services with forced rebuild

.EXAMPLE
    ./run-dev.ps1 -Logs
    Start and follow logs
#>

param(
    [ValidateSet('full', 'api', 'minimal', 'testing')]
    [string]$Mode = 'full',
    
    [switch]$Build,
    
    [switch]$Logs,
    
    [switch]$Background = $false,
    
    [switch]$Clean,
    
    [switch]$Help
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

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

function Show-Help {
    Write-ColorOutput "`n🚀 Super-Codex-AI Development Environment" "Magenta"
    Write-ColorOutput "=========================================" "Magenta"
    
    Write-Info "Usage: ./run-dev.ps1 [-Mode <mode>] [-Build] [-Logs] [-Background] [-Clean]"
    
    Write-ColorOutput "`nModes:" "Yellow"
    Write-Host "  full     - All services (API, DB, Cache, Storage, Monitoring)"
    Write-Host "  api      - API server only (requires external dependencies)"
    Write-Host "  minimal  - Core services only (API, DB, Redis)"
    Write-Host "  testing  - Testing environment with test data"
    
    Write-ColorOutput "`nOptions:" "Yellow"
    Write-Host "  -Build     - Force rebuild of Docker images"
    Write-Host "  -Logs      - Show logs after startup"
    Write-Host "  -Background - Run in detached mode (background)"
    Write-Host "  -Clean     - Clean up volumes and containers before starting"
    Write-Host "  -Help      - Show this help message"
    
    Write-ColorOutput "`nExamples:" "Yellow"
    Write-Host "  ./run-dev.ps1                    # Start full environment"
    Write-Host "  ./run-dev.ps1 -Mode minimal      # Start core services only"
    Write-Host "  ./run-dev.ps1 -Build -Logs       # Rebuild and show logs"
    Write-Host "  ./run-dev.ps1 -Clean             # Clean start"
    
    exit 0
}

function Test-DockerAvailable {
    try {
        docker --version | Out-Null
        docker-compose --version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Set-EnvironmentVariables {
    Write-Info "Setting up environment variables..."
    
    # Get git information
    try {
        $gitCommit = git rev-parse --short HEAD 2>$null
        $buildDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        $buildVersion = if (git describe --tags --exact-match 2>$null) { 
            git describe --tags --exact-match 
        } else { 
            "dev-$gitCommit" 
        }
    }
    catch {
        $gitCommit = "unknown"
        $buildDate = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        $buildVersion = "dev"
    }
    
    $env:GIT_COMMIT = $gitCommit
    $env:BUILD_DATE = $buildDate
    $env:BUILD_VERSION = $buildVersion
    
    Write-Success "Environment variables set (Version: $buildVersion, Commit: $gitCommit)"
}

function Invoke-CleanUp {
    Write-Warning "Cleaning up existing containers and volumes..."
    
    try {
        # Stop and remove containers
        docker-compose -f "$ProjectRoot/ops/docker/docker-compose.yml" down -v --remove-orphans
        
        # Remove dangling images
        $danglingImages = docker images -f "dangling=true" -q
        if ($danglingImages) {
            docker rmi $danglingImages
        }
        
        # Prune system (but keep volumes with data)
        docker system prune -f
        
        Write-Success "Cleanup completed"
    }
    catch {
        Write-Warning "Some cleanup operations failed, continuing..."
    }
}

function Get-ServiceProfiles {
    param([string]$Mode)
    
    switch ($Mode) {
        'api' { 
            return @('codex-api')
        }
        'minimal' { 
            return @('codex-api', 'postgres', 'redis')
        }
        'testing' {
            return @('codex-api', 'postgres', 'redis', 'minio')
        }
        'full' { 
            return @()  # All services
        }
        default {
            return @()  # All services
        }
    }
}

function Start-Services {
    param(
        [string]$Mode,
        [bool]$BuildImages,
        [bool]$RunInBackground
    )
    
    Write-Info "Starting services in $Mode mode..."
    
    $composeFile = "$ProjectRoot/ops/docker/docker-compose.yml"
    
    # Build arguments
    $buildArgs = if ($BuildImages) { @('--build') } else { @() }
    $detachArgs = if ($RunInBackground) { @('--detach') } else { @()
    
    # Service selection
    $services = Get-ServiceProfiles -Mode $Mode
    
    try {
        if ($services.Count -gt 0) {
            # Start specific services
            $cmd = @('docker-compose', '-f', $composeFile, 'up') + $buildArgs + $detachArgs + $services
        } else {
            # Start all services
            $cmd = @('docker-compose', '-f', $composeFile, 'up') + $buildArgs + $detachArgs
        }
        
        Write-Info "Executing: $($cmd -join ' ')"
        & $cmd[0] $cmd[1..($cmd.Length-1)]
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Services started successfully"
        } else {
            throw "Docker compose failed with exit code $LASTEXITCODE"
        }
    }
    catch {
        Write-Error "Failed to start services: $($_.Exception.Message)"
        exit 1
    }
}

function Show-ServiceStatus {
    Write-Info "Service status:"
    
    try {
        docker-compose -f "$ProjectRoot/ops/docker/docker-compose.yml" ps
    }
    catch {
        Write-Warning "Could not retrieve service status"
    }
}

function Show-ServiceUrls {
    param([string]$Mode)
    
    Write-ColorOutput "`n🌐 Service URLs:" "Magenta"
    Write-ColorOutput "===============" "Magenta"
    
    Write-Host "📊 Codex API:        http://localhost:8000"
    Write-Host "📈 API Documentation: http://localhost:8000/docs"
    Write-Host "❤️  Health Check:     http://localhost:8000/health"
    
    if ($Mode -eq 'full') {
        Write-Host "📦 MinIO Console:     http://localhost:9001 (admin/admin)"
        Write-Host "📊 Grafana:          http://localhost:3000 (admin/admin)"
        Write-Host "🔍 Prometheus:       http://localhost:9090"
        Write-Host "🔎 Jaeger:           http://localhost:16686"
        Write-Host "📧 MailHog:          http://localhost:8025"
    }
    
    if ($Mode -in @('full', 'minimal', 'testing')) {
        Write-Host "🗄️  PostgreSQL:       localhost:5432 (codex_user/codex_password)"
        Write-Host "🔴 Redis:            localhost:6379"
    }
    
    if ($Mode -in @('full', 'testing')) {
        Write-Host "📦 MinIO:            http://localhost:9000"
    }
}

function Show-Logs {
    Write-Info "Following service logs (Ctrl+C to stop)..."
    
    try {
        docker-compose -f "$ProjectRoot/ops/docker/docker-compose.yml" logs -f
    }
    catch {
        Write-Info "Log following stopped"
    }
}

function Wait-ForServices {
    Write-Info "Waiting for services to be ready..."
    
    $maxWait = 60  # seconds
    $waited = 0
    $interval = 2
    
    while ($waited -lt $maxWait) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Success "Services are ready!"
                return
            }
        }
        catch {
            # Service not ready yet
        }
        
        Start-Sleep -Seconds $interval
        $waited += $interval
        Write-Host "." -NoNewline
    }
    
    Write-Warning "Services may not be fully ready yet. Check logs if issues persist."
}

# ============================================================================
# Main Execution
# ============================================================================

if ($Help) {
    Show-Help
}

Write-ColorOutput "`n🚀 Super-Codex-AI Development Environment" "Magenta"
Write-ColorOutput "=========================================" "Magenta"

# Validate Docker availability
if (-not (Test-DockerAvailable)) {
    Write-Error "Docker and docker-compose are required but not found."
    Write-Info "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
}

if (-not (Test-DockerRunning)) {
    Write-Error "Docker is installed but not running."
    Write-Info "Please start Docker Desktop and try again."
    exit 1
}

Write-Success "Docker is available and running"

# Set working directory
Set-Location $ProjectRoot

# Setup environment
Set-EnvironmentVariables

# Clean up if requested
if ($Clean) {
    Invoke-CleanUp
}

# Start services
Start-Services -Mode $Mode -BuildImages $Build -RunInBackground $Background

# Wait for services if running in background
if ($Background) {
    Wait-ForServices
}

# Show status and URLs
Show-ServiceStatus
Show-ServiceUrls -Mode $Mode

# Show logs if requested
if ($Logs -and -not $Background) {
    Write-Info "Press Ctrl+C to stop services..."
    Show-Logs
} elseif ($Logs -and $Background) {
    Show-Logs
}

Write-ColorOutput "`n🎉 Development environment is ready!" "Green"
Write-Info "Use 'docker-compose -f ops/docker/docker-compose.yml logs -f' to view logs"
Write-Info "Use 'docker-compose -f ops/docker/docker-compose.yml down' to stop services"
