# Axiom-Flame Deployment Guide

## Prerequisites

- Ubuntu/Debian server with sudo access
- Domain name pointing to your server IP (codexdominion.app)
- Python 3.8+ installed
- Node.js 16+ installed

## Installation Steps

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install nginx
sudo apt install nginx -y

# Install Python dependencies
pip install Flask==3.0.0 jsonschema

# Install Node.js dependencies (if using CLI)
npm install -g yargs chalk node-fetch
```

### 2. Deploy API

```bash
# Create application directory
sudo mkdir -p /opt/axiom-flame
sudo chown $USER:$USER /opt/axiom-flame
cd /opt/axiom-flame

# Copy API files
cp -r packages/api/* /opt/axiom-flame/

# Create systemd service
sudo tee /etc/systemd/system/axiom-flame.service << EOF
[Unit]
Description=Axiom-Flame Ceremonial API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/axiom-flame
Environment=PORT=8080
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable axiom-flame
sudo systemctl start axiom-flame
```

### 3. Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx/codexdominion.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/codexdominion.conf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 4. SSL Setup (Optional but Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app

# Use SSL configuration
sudo cp nginx/codexdominion_ssl.conf /etc/nginx/sites-available/codexdominion.conf
sudo systemctl reload nginx
```

### 5. Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## Verification

### Check API Status
```bash
sudo systemctl status axiom-flame
curl http://localhost:8080/health
```

### Check Nginx Status
```bash
sudo systemctl status nginx
curl -H "Host: codexdominion.app" http://localhost/health
```

### Test External Access
```bash
curl https://codexdominion.app/health
```

## CLI Usage

After deployment, test the CLI:

```bash
# Install CLI globally (on development machine)
npm install -g ./packages/cli

# Set API endpoint
export AXIOM_API="https://codexdominion.app"

# Test commands
axiom health
axiom invoke "PL-001" "Sovereign Crown"
```

## Monitoring

### Check Logs
```bash
# API logs
sudo journalctl -u axiom-flame -f

# Nginx logs
sudo tail -f /var/log/nginx/codexdominion_access.log
sudo tail -f /var/log/nginx/codexdominion_error.log
```

### Health Monitoring
Set up a monitoring service to check `/health` endpoint regularly.

## Maintenance

### Update API
```bash
cd /opt/axiom-flame
sudo systemctl stop axiom-flame
# Update files
sudo systemctl start axiom-flame
```

### Renew SSL Certificate
```bash
sudo certbot renew --dry-run
```

## Security Notes

- API runs on localhost:8080 (not directly accessible)
- All external traffic goes through nginx proxy
- SSL termination at nginx level
- Security headers configured
- Regular updates recommended

## Troubleshooting

### API Not Starting
- Check Python dependencies: `pip list`
- Check port availability: `netstat -tlnp | grep 8080`
- Check permissions: `ls -la /opt/axiom-flame`

### Nginx Issues
- Test config: `sudo nginx -t`
- Check error logs: `sudo tail /var/log/nginx/error.log`
- Verify DNS: `nslookup codexdominion.app`