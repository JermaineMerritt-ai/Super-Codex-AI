# CodexDominion.app Startup Script
# Run this to start all services for the React frontend demo

Write-Host "🚀 Starting CodexDominion.app Services..." -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Gray

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Activating Python virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

Write-Host "🐍 Python environment: $env:VIRTUAL_ENV" -ForegroundColor Cyan

# Start services in separate PowerShell windows
Write-Host "🔧 Starting Backend API on port 8010..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010 --reload"

Start-Sleep -Seconds 2

Write-Host "⚡ Starting Axiom-flame API on port 5010..." -ForegroundColor Magenta  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\axiom-flame\packages\api'; python app.py"

Start-Sleep -Seconds 2

Write-Host "📡 React Frontend already running on port 3001!" -ForegroundColor Green

Write-Host "=" * 50 -ForegroundColor Gray
Write-Host "✅ Services Status:" -ForegroundColor Green
Write-Host "   🔗 Frontend: http://localhost:3001" -ForegroundColor White
Write-Host "   🔗 Backend:  http://localhost:8010" -ForegroundColor White  
Write-Host "   🔗 Axiom:    http://localhost:5010" -ForegroundColor White
Write-Host "=" * 50 -ForegroundColor Gray

Write-Host "🎯 Testing API endpoints..." -ForegroundColor Yellow

# Wait for services to start
Start-Sleep -Seconds 5

# Test health endpoints
try {
    Write-Host "Testing Backend Health..." -ForegroundColor Cyan
    $backendHealth = Invoke-RestMethod -Uri "http://127.0.0.1:8010/health/live" -Method GET -TimeoutSec 5
    Write-Host "✅ Backend: $($backendHealth.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend: Not responding" -ForegroundColor Red
}

try {
    Write-Host "Testing Axiom Health..." -ForegroundColor Cyan
    $axiomHealth = Invoke-RestMethod -Uri "http://127.0.0.1:5010/health" -Method GET -TimeoutSec 5
    Write-Host "✅ Axiom: $($axiomHealth.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Axiom: Not responding" -ForegroundColor Red
}

Write-Host "=" * 50 -ForegroundColor Gray
Write-Host "🎉 Ready! Open http://localhost:3001 to test your API client!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Gray