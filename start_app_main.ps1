<#
.SYNOPSIS
    Starts the FastAPI application using uvicorn (default) or gunicorn

.DESCRIPTION
    This script provides a flexible way to start the FastAPI application with either
    uvicorn or gunicorn ASGI servers, with proper process isolation to avoid
    PowerShell interaction issues.

.PARAMETER UseGunicorn
    Use gunicorn with uvicorn workers instead of uvicorn directly.
    Gunicorn provides better production performance with multiple workers.

.PARAMETER Host
    The host to bind the server to. Default is "0.0.0.0" (all interfaces)

.PARAMETER Port
    The port to bind the server to. Default is 8010

.PARAMETER LogLevel
    The logging level for the server. Default is "info"
    Options: critical, error, warning, info, debug, trace

.EXAMPLE
    .\start_app_main.ps1
    # Starts with uvicorn on default settings (0.0.0.0:8010)

.EXAMPLE
    .\start_app_main.ps1 -UseGunicorn
    # Starts with gunicorn using 4 uvicorn workers

.EXAMPLE
    .\start_app_main.ps1 -Host "127.0.0.1" -Port 8080 -LogLevel "debug"
    # Starts with custom host, port, and debug logging

.EXAMPLE
    .\start_app_main.ps1 -UseGunicorn -Port 8080
    # Starts with gunicorn on port 8080
#>

param (
    [switch]$UseGunicorn,
    [string]$Host = "0.0.0.0",
    [int]$Port = 8010,
    [string]$LogLevel = "info"
)

# PowerShell script to run uvicorn or gunicorn with proper process isolation
# This bypasses the PowerShell/ASGI server interaction issue

# Set working directory and activate virtual environment
$workDir = Get-Location
$venvPath = Join-Path $workDir ".venv\Scripts\Activate.ps1"

# Determine which server to use
$serverName = if ($UseGunicorn) { "gunicorn" } else { "uvicorn" }
$serverModule = if ($UseGunicorn) { "gunicorn" } else { "uvicorn" }

Write-Host "🚀 Starting FastAPI Application with $serverName" -ForegroundColor Green
Write-Host "📂 Working Directory: $workDir" -ForegroundColor Cyan

if ($UseGunicorn) {
    $command = "python -m gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind ${Host}:${Port} --log-level $LogLevel"
} else {
    $command = "python -m uvicorn app.main:app --host $Host --port $Port --log-level $LogLevel"
}

Write-Host "🔌 Command: $command" -ForegroundColor Cyan
Write-Host "🌐 Access URL: http://localhost:$Port" -ForegroundColor Yellow
Write-Host "=" * 80

# Activate virtual environment if it exists
if (Test-Path $venvPath) {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "⚠️ Virtual environment not found, using system Python" -ForegroundColor Yellow
}

# Kill any existing Python processes on the target port
$processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($processes) {
    Write-Host "🔄 Stopping existing processes on port $Port..." -ForegroundColor Yellow
    $processes | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 2
}

# Set environment variables
$env:PYTHONPATH = $workDir
$env:PYTHONUNBUFFERED = "1"

try {
    Write-Host "🎯 Starting $serverName server..." -ForegroundColor Green
    
    # Use simplified Start-Process approach
    if ($UseGunicorn) {
        # Check if gunicorn is installed
        $gunicornCheck = python -m pip show gunicorn 2>$null
        if (-not $gunicornCheck) {
            Write-Host "⚠️ Gunicorn not installed. Installing..." -ForegroundColor Yellow
            python -m pip install gunicorn
        }
        
        Start-Process -NoNewWindow -FilePath "gunicorn" -ArgumentList "app.main:app -k uvicorn.workers.UvicornWorker --bind ${Host}:${Port} --log-level $LogLevel"
    } else {
        Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host $Host --port $Port --log-level $LogLevel"
    }
    
    Write-Host "✅ Server started successfully!" -ForegroundColor Green
    Write-Host "🌐 Server running at: http://${Host}:${Port}" -ForegroundColor Yellow
    Write-Host "📚 API Documentation: http://${Host}:${Port}/docs" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host "💡 Try running in Command Prompt instead: start_app_main.cmd" -ForegroundColor Yellow
    Write-Host "💡 Or try the alternative server: .\start_app_main.ps1 $(if ($UseGunicorn) { '' } else { '-UseGunicorn' })" -ForegroundColor Yellow
}

Write-Host "`n🏁 Server stopped. Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")