# Axiom-Flame System Startup Script
Write-Host "🔥 Starting Axiom-Flame System..." -ForegroundColor Yellow

Set-Location $PSScriptRoot

# Start Flask API
Write-Host "Starting Flask API..." -ForegroundColor Green
python axiom-flame\packages\api\start_api.py start --daemon 8089

# Wait a moment for API to start
Start-Sleep 2

# Test API health
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8089/health" -Method Get -TimeoutSec 5
    Write-Host "✅ API Health Check: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ API Health Check failed: $_" -ForegroundColor Yellow
}

Write-Host "✅ Axiom-Flame System started successfully!" -ForegroundColor Green
Write-Host "🌐 API Access: http://localhost:8089" -ForegroundColor Cyan
Write-Host "📊 Health: http://localhost:8089/health" -ForegroundColor Cyan

# Show available commands
Write-Host "`n🔧 Available Commands:" -ForegroundColor White
Write-Host "  - python system_health_check.py     # System diagnostics"
Write-Host "  - python system_validation.py       # Full validation"
Write-Host "  - python axiom-flame\axiom_flame.py health # CLI health check"

Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")