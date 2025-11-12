#!/bin/bash
# SSL Setup Script for Axiom-Flame API

set -e

echo "🔐 Setting up SSL for codexdominion.app..."

# Install Certbot
echo "📦 Installing Certbot..."
sudo apt update
sudo apt install certbot python3-certbot-nginx -y

# Verify nginx configuration before SSL
echo "🔍 Testing nginx configuration..."
sudo nginx -t

# Get SSL certificates
echo "🌐 Obtaining SSL certificates..."
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app

# Test automatic renewal
echo "🔄 Testing certificate renewal..."
sudo certbot renew --dry-run

# Setup automatic renewal cron job
echo "⏰ Setting up automatic renewal..."
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# Update nginx configuration to use SSL
echo "⚙️  Updating nginx configuration for SSL..."
sudo cp /opt/axiom-flame/nginx/codexdominion_ssl.conf /etc/nginx/sites-available/codexdominion.conf
sudo systemctl reload nginx

# Verify SSL setup
echo "✅ Verifying SSL setup..."
curl -I https://codexdominion.app/health

echo "🎉 SSL setup complete!"
echo "📋 Certificate details:"
sudo certbot certificates

echo ""
echo "🔗 Your API is now available at:"
echo "   https://codexdominion.app"
echo "   https://www.codexdominion.app"
echo ""
echo "📝 To check certificate status:"
echo "   sudo certbot certificates"
echo ""
echo "🔄 To renew certificates manually:"
echo "   sudo certbot renew"