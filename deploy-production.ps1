# Production Deployment Script for CodexDominion.app (Windows)
# Usage: .\deploy-production.ps1

Write-Host "🚀 Starting CodexDominion.app Production Deployment" -ForegroundColor Green

# Check if .env exists
if (!(Test-Path ".env")) {
    Write-Host "⚠️  Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "📝 Please edit .env with your production secrets before continuing!" -ForegroundColor Yellow
    Write-Host "🔑 Don't forget to update:" -ForegroundColor Cyan
    Write-Host "   - JWT_SECRET" -ForegroundColor White
    Write-Host "   - CLI_API_KEY" -ForegroundColor White
    Write-Host "   - POSTGRES_PASSWORD" -ForegroundColor White
    Write-Host "   - ACME_EMAIL" -ForegroundColor White
    exit 1
}

# Create frontend build directory if it doesn't exist
if (!(Test-Path "frontend\build")) {
    Write-Host "📁 Creating frontend build directory..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path "frontend\build" | Out-Null
    Set-Content -Path "frontend\build\index.html" -Value @"
<html>
<head><title>CodexDominion.app</title></head>
<body style="font-family:Arial;text-align:center;margin:50px">
<h1>🏰 CodexDominion.app</h1>
<p>Production Environment Ready</p>
<p>Deploy your React build to <code>frontend/build/</code></p>
</body>
</html>
"@
}

# Pull latest images
Write-Host "📦 Pulling latest Docker images..." -ForegroundColor Blue
docker-compose pull

# Build services
Write-Host "🔨 Building services..." -ForegroundColor Blue
docker-compose build --no-cache

# Start services
Write-Host "🆙 Starting services..." -ForegroundColor Blue
docker-compose up -d

# Wait for services to be ready
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service health
Write-Host "🩺 Checking service health..." -ForegroundColor Blue

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ Backend is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend health check failed" -ForegroundColor Red
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5
    Write-Host "✅ Axiom-flame is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Axiom-flame health check failed (may be normal if not implemented)" -ForegroundColor Yellow
}

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -TimeoutSec 5
    Write-Host "✅ Frontend is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend health check failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your application should be available at:" -ForegroundColor Cyan
Write-Host "   - Local: http://localhost (via Caddy)" -ForegroundColor White
Write-Host "   - Production: https://CodexDominion.app (once DNS is configured)" -ForegroundColor White
Write-Host ""
Write-Host "📊 Service URLs:" -ForegroundColor Cyan
Write-Host "   - Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "   - Axiom-flame: http://localhost:5000" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   - Caddy Admin: http://localhost:2019" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Point CodexDominion.app DNS A record to your server IP" -ForegroundColor White
Write-Host "   2. Update .env with your email for SSL certificates" -ForegroundColor White
Write-Host "   3. Deploy your React frontend to frontend/build/" -ForegroundColor White
Write-Host "   4. Monitor logs with: docker-compose logs -f" -ForegroundColor White