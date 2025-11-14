# Generate SSL Certificate for Development
# PowerShell version of generate-ssl.sh

# Create SSL directory if it doesn't exist
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Name "ssl"
}

# Generate self-signed certificate for development using OpenSSL
# Note: OpenSSL must be installed on Windows
try {
    openssl req -x509 -newkey rsa:4096 -keyout ssl/codexdominion.app.key -out ssl/codexdominion.app.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=codexdominion.app"
    
    Write-Host "✅ Self-signed SSL certificate generated for development" -ForegroundColor Green
    Write-Host "📁 Files created:" -ForegroundColor Yellow
    Write-Host "   - ssl/codexdominion.app.key" -ForegroundColor Cyan
    Write-Host "   - ssl/codexdominion.app.crt" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  For production, replace with valid SSL certificates from a CA" -ForegroundColor Yellow
    Write-Host "💡 Consider using Let's Encrypt for free SSL certificates" -ForegroundColor Blue
}
catch {
    Write-Host "❌ OpenSSL not found. Please install OpenSSL or use alternative:" -ForegroundColor Red
    Write-Host "   - Install OpenSSL: https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor Yellow
    Write-Host "   - Or use Windows Certificate Store for development" -ForegroundColor Yellow
}