<#
.SYNOPSIS
    Launches the FastAPI server with stable development or production-grade options

.DESCRIPTION
    This script provides two launch modes:
    1. Stable Development - Uses uvicorn directly for development and testing
    2. Production Grade - Uses gunicorn with uvicorn workers for high performance

.PARAMETER Production
    Use gunicorn with uvicorn workers for production deployment

.PARAMETER BindHost
    The host to bind the server to. Default is "0.0.0.0" (all interfaces)

.PARAMETER Port
    The port to bind the server to. Default is 8010

.PARAMETER Workers
    Number of gunicorn workers (production mode only). Default is 4

.PARAMETER LogLevel
    The logging level for the server. Default is "info"

.EXAMPLE
    .\launch_server.ps1
    # Stable development launch with uvicorn

.EXAMPLE
    .\launch_server.ps1 -Production
    # Production-grade launch with gunicorn

.EXAMPLE
    .\launch_server.ps1 -Production -Workers 8 -Port 8080
    # Production launch with 8 workers on port 8080

.EXAMPLE
    .\launch_server.ps1 -BindHost "127.0.0.1" -Port 8080 -LogLevel "debug"
    # Development launch with custom settings
#>

param (
    [switch]$Production,
    [string]$BindHost = "0.0.0.0",
    [int]$Port = 8010,
    [int]$Workers = 4,
    [string]$LogLevel = "info"
)

# Set working directory and activate virtual environment
$workDir = Get-Location
$venvPath = Join-Path $workDir ".venv\Scripts\Activate.ps1"

# Determine launch mode
$launchMode = if ($Production) { "Production-Grade (Gunicorn)" } else { "Stable Development (Uvicorn)" }

Write-Host "🚀 Starting FastAPI Application - $launchMode" -ForegroundColor Green
Write-Host "📂 Working Directory: $workDir" -ForegroundColor Cyan
Write-Host "🌐 Server Address: http://$BindHost`:$Port" -ForegroundColor Yellow
Write-Host "📊 Log Level: $LogLevel" -ForegroundColor Cyan

if ($Production) {
    Write-Host "👥 Workers: $Workers" -ForegroundColor Cyan
}

Write-Host "=" * 80

# Activate virtual environment if it exists
if (Test-Path $venvPath) {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "⚠️ Virtual environment not found, using system Python" -ForegroundColor Yellow
}

# Kill any existing processes on the target port
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
    if ($Production) {
        Write-Host "🎯 Starting production server with gunicorn..." -ForegroundColor Green
        
        # Check if gunicorn is installed
        $gunicornCheck = python -m pip show gunicorn 2>$null
        if (-not $gunicornCheck) {
            Write-Host "⚠️ Gunicorn not installed. Installing..." -ForegroundColor Yellow
            python -m pip install gunicorn
        }
        
        # Production-grade launch
        Start-Process -NoNewWindow -FilePath "gunicorn" -ArgumentList "app.main:app -k uvicorn.workers.UvicornWorker --bind ${BindHost}:${Port} --workers $Workers --log-level $LogLevel"
        
        Write-Host "✅ Production server started successfully!" -ForegroundColor Green
        Write-Host "🏭 Running with $Workers gunicorn workers" -ForegroundColor Green
        
    } else {
        Write-Host "🎯 Starting development server with uvicorn..." -ForegroundColor Green
        
        # Stable launch
        Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host $BindHost --port $Port --log-level $LogLevel"
        
        Write-Host "✅ Development server started successfully!" -ForegroundColor Green
    }
    
    Write-Host "🌐 Server running at: http://${BindHost}:${Port}" -ForegroundColor Yellow
    Write-Host "📚 API Documentation: http://${BindHost}:${Port}/docs" -ForegroundColor Cyan
    Write-Host "🔍 Health Check: http://${BindHost}:${Port}/api/health" -ForegroundColor Cyan
    
    if ($Production) {
        Write-Host ""
        Write-Host "🏭 Production Features Active:" -ForegroundColor Green
        Write-Host "  • Multiple worker processes for high availability" -ForegroundColor White
        Write-Host "  • Automatic worker restarts on failure" -ForegroundColor White
        Write-Host "  • Load balancing across workers" -ForegroundColor White
        Write-Host "  • Production-optimized performance" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "🛠️ Development Features Active:" -ForegroundColor Blue
        Write-Host "  • Single process for easy debugging" -ForegroundColor White
        Write-Host "  • Hot reload on code changes (with --reload)" -ForegroundColor White
        Write-Host "  • Detailed error messages" -ForegroundColor White
    }
    
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  • Check if port $Port is available" -ForegroundColor White
    Write-Host "  • Verify app.main:app imports correctly" -ForegroundColor White
    Write-Host "  • Try running with different port: -Port 8080" -ForegroundColor White
    Write-Host "  • Switch modes: $(if ($Production) { 'Remove -Production flag' } else { 'Add -Production flag' })" -ForegroundColor White
}

Write-Host "`n🏁 Launch script completed. Press Ctrl+C to stop the server." -ForegroundColor Cyan