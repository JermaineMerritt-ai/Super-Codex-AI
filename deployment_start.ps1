# deployment_start.ps1
# PowerShell script to start all services for deployment

param(
    [string]$Domain = "your-domain.com",
    [int]$BackendPort = 8010,
    [int]$FrontendPort = 3001,
    [switch]$Production = $false,
    [switch]$UseCaddy = $true
)

Write-Host "🚀 Starting Super-Codex-AI Deployment" -ForegroundColor Green
Write-Host "Domain: $Domain" -ForegroundColor Cyan
Write-Host "Backend Port: $BackendPort" -ForegroundColor Cyan  
Write-Host "Frontend Port: $FrontendPort" -ForegroundColor Cyan
Write-Host "Production Mode: $Production" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# Function to start service in new window
function Start-ServiceWindow {
    param(
        [string]$Title,
        [string]$Command,
        [string]$WorkingDirectory = $PWD
    )
    
    Write-Host "Starting $Title..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$WorkingDirectory'; $Command" -WindowStyle Normal
    Start-Sleep 2
}

# Check prerequisites
Write-Host "🔍 Checking Prerequisites..." -ForegroundColor Blue

# Check if virtual environment exists
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating..." -ForegroundColor Red
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Check if frontend dependencies are installed
if (-not (Test-Path ".\frontend\node_modules")) {
    Write-Host "❌ Frontend dependencies not found. Installing..." -ForegroundColor Red
    cd frontend
    npm install
    cd ..
}

# Check if ports are available
Write-Host "Checking ports..." -ForegroundColor Blue
if (Test-Port $BackendPort) {
    Write-Host "⚠️  Port $BackendPort is already in use!" -ForegroundColor Yellow
}
if (Test-Port $FrontendPort) {
    Write-Host "⚠️  Port $FrontendPort is already in use!" -ForegroundColor Yellow
}

# Set environment variables
if ($Production) {
    $env:NODE_ENV = "production"
    $env:FASTAPI_ENV = "production"
} else {
    $env:NODE_ENV = "development"
    $env:FASTAPI_ENV = "development"
}

Write-Host ""
Write-Host "🎯 Starting Services..." -ForegroundColor Green

# Start Backend API
$backendCommand = ".\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort --reload"
Start-ServiceWindow "Backend API (Port $BackendPort)" $backendCommand

# Wait for backend to start
Write-Host "Waiting for backend to start..." -ForegroundColor Blue
$backendReady = $false
$attempts = 0
while (-not $backendReady -and $attempts -lt 30) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/health" -Method GET -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "✅ Backend is ready!" -ForegroundColor Green
        }
    } catch {
        $attempts++
        Start-Sleep 2
    }
}

if (-not $backendReady) {
    Write-Host "❌ Backend failed to start after 60 seconds" -ForegroundColor Red
    exit 1
}

# Start Frontend
Write-Host "Starting frontend..." -ForegroundColor Blue
$frontendCommand = if ($Production) {
    "npm run build; npx serve -s build -l $FrontendPort"
} else {
    "`$env:PORT=$FrontendPort; npm start"
}

Start-ServiceWindow "Frontend (Port $FrontendPort)" $frontendCommand ".\frontend"

# Wait for frontend to start
Write-Host "Waiting for frontend to start..." -ForegroundColor Blue
$frontendReady = $false
$attempts = 0
while (-not $frontendReady -and $attempts -lt 30) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$FrontendPort" -Method GET -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            $frontendReady = $true
            Write-Host "✅ Frontend is ready!" -ForegroundColor Green
        }
    } catch {
        $attempts++
        Start-Sleep 2
    }
}

if (-not $frontendReady) {
    Write-Host "❌ Frontend failed to start after 60 seconds" -ForegroundColor Red
}

# Update Caddyfile with actual domain
if ($Domain -ne "your-domain.com") {
    Write-Host "Updating Caddyfile with domain: $Domain" -ForegroundColor Blue
    $caddyContent = Get-Content "Caddyfile" -Raw
    $caddyContent = $caddyContent -replace "your-domain.com", $Domain
    $caddyContent = $caddyContent -replace "127.0.0.1:8010", "127.0.0.1:$BackendPort"
    $caddyContent = $caddyContent -replace "127.0.0.1:3001", "127.0.0.1:$FrontendPort"
    Set-Content "Caddyfile.temp" $caddyContent
}

# Start Caddy if requested
if ($UseCaddy) {
    Write-Host "Starting Caddy reverse proxy..." -ForegroundColor Blue
    
    # Check if Caddy is installed
    try {
        caddy version
        $caddyFile = if ($Domain -ne "your-domain.com") { "Caddyfile.temp" } else { "Caddyfile" }
        Start-ServiceWindow "Caddy Reverse Proxy" "caddy run --config $caddyFile"
        
        Write-Host "✅ Caddy started with configuration!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Caddy not found. Install with: choco install caddy" -ForegroundColor Red
        Write-Host "   Or download from: https://caddyserver.com/download" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Deployment Started Successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service URLs:" -ForegroundColor Cyan
Write-Host "  Backend API:    http://127.0.0.1:$BackendPort" -ForegroundColor White
Write-Host "  Frontend:       http://127.0.0.1:$FrontendPort" -ForegroundColor White
if ($UseCaddy) {
    Write-Host "  Public Domain:  https://$Domain" -ForegroundColor White
}
Write-Host ""
Write-Host "🔍 Health Checks:" -ForegroundColor Cyan
Write-Host "  Backend Health: http://127.0.0.1:$BackendPort/health" -ForegroundColor White
Write-Host "  AXIOM Health:   http://127.0.0.1:$BackendPort/axiom/health" -ForegroundColor White
Write-Host ""
Write-Host "📝 Logs:" -ForegroundColor Cyan
Write-Host "  Check the opened PowerShell windows for service logs" -ForegroundColor White
Write-Host ""
Write-Host "⏹️  To Stop Services:" -ForegroundColor Yellow
Write-Host "  1. Close the PowerShell windows" -ForegroundColor White
Write-Host "  2. Run: caddy stop (if using Caddy)" -ForegroundColor White
Write-Host ""

# Test deployment
Write-Host "🧪 Testing Deployment..." -ForegroundColor Blue
Start-Sleep 5

try {
    $healthResponse = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/health" -Method GET
    Write-Host "✅ Backend health check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend health check failed" -ForegroundColor Red
}

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://127.0.0.1:$FrontendPort" -Method GET  
    Write-Host "✅ Frontend accessibility check passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend accessibility check failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "✨ Super-Codex-AI is now running!" -ForegroundColor Green