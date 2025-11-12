#!/bin/bash
# Complete deployment script for Axiom-Flame

set -e

echo "🚀 Deploying Axiom-Flame Ceremonial API..."

# Variables
DOMAIN="codexdominion.app"
APP_DIR="/srv/axiom-flame"
NGINX_CONFIG="codexdominion.conf"

# Create system user for the service
echo "👤 Creating axiom-flame system user..."
sudo useradd --system --home-dir $APP_DIR --shell /bin/false axiom-flame || echo "User already exists"

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p $APP_DIR
sudo chown axiom-flame:axiom-flame $APP_DIR

# Copy application files
echo "📋 Copying application files..."
cp -r packages/ $APP_DIR/
cp -r artifacts/ $APP_DIR/
cp -r storage/ $APP_DIR/ 2>/dev/null || mkdir -p $APP_DIR/storage
cp -r schemas/ $APP_DIR/ 2>/dev/null || echo "No schemas directory found"

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
cd $APP_DIR
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install Flask==3.0.0 jsonschema

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo cp systemd/axiom-flame-production.service /etc/systemd/system/axiom-flame.service

# Set permissions
echo "🔒 Setting permissions..."
sudo chown -R axiom-flame:axiom-flame $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 750 $APP_DIR/storage $APP_DIR/artifacts

# Enable and start service
echo "🔄 Starting Axiom-Flame service..."
sudo systemctl daemon-reload
sudo systemctl enable axiom-flame
sudo systemctl start axiom-flame

# Wait for service to start
sleep 3

# Check service status
if sudo systemctl is-active --quiet axiom-flame; then
    echo "✅ Axiom-Flame service is running"
else
    echo "❌ Axiom-Flame service failed to start"
    sudo systemctl status axiom-flame
    exit 1
fi

# Install nginx if not present
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing nginx..."
    sudo apt update
    sudo apt install nginx -y
fi

# Configure nginx
echo "🌐 Configuring nginx..."
sudo cp nginx/$NGINX_CONFIG /etc/nginx/sites-available/
sudo ln -sf /etc/nginx/sites-available/$NGINX_CONFIG /etc/nginx/sites-enabled/

# Remove default nginx site
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "🔍 Testing nginx configuration..."
sudo nginx -t

# Start nginx
sudo systemctl enable nginx
sudo systemctl restart nginx

# Configure firewall
echo "🛡️ Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# Test API
echo "🧪 Testing API..."
sleep 5

# Test direct API connection
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ API health check passed"
else
    echo "❌ API health check failed"
    echo "📋 Checking service logs..."
    sudo journalctl -u axiom-flame --no-pager -n 10
    exit 1
fi

if curl -f -H "Host: $DOMAIN" http://localhost/health > /dev/null 2>&1; then
    echo "✅ Nginx proxy test passed"
else
    echo "❌ Nginx proxy test failed"
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Enable and start the service:"
echo "   sudo systemctl enable axiom-flame"
echo "   sudo systemctl start axiom-flame"
echo ""
echo "2. Point your domain DNS to this server's IP"
echo "3. Run SSL setup: ./scripts/setup-ssl.sh"
echo "4. Test your API: curl https://$DOMAIN/health"
echo ""
echo "📊 Service status:"
sudo systemctl status axiom-flame --no-pager
echo ""
echo "🌐 Nginx status:"
sudo systemctl status nginx --no-pager