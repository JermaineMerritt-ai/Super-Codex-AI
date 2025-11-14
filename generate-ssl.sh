#!/bin/bash
# generate-ssl.sh - Generate self-signed SSL certificate for development

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Generate self-signed certificate for development
openssl req -x509 -newkey rsa:4096 -keyout ssl/codexdominion.app.key -out ssl/codexdominion.app.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=codexdominion.app"

echo "✅ Self-signed SSL certificate generated for development"
echo "📁 Files created:"
echo "   - ssl/codexdominion.app.key"
echo "   - ssl/codexdominion.app.crt"
echo ""
echo "⚠️  For production, replace with valid SSL certificates from a CA"
echo "💡 Consider using Let's Encrypt for free SSL certificates"