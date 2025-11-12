# SSL Certificate Management

## Initial Setup

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates for your domain
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app
```

## Automatic Renewal

Certbot automatically installs a renewal timer. Check with:

```bash
# Check renewal timer status
sudo systemctl status certbot.timer

# Test renewal process
sudo certbot renew --dry-run

# Force renewal (if needed)
sudo certbot renew --force-renewal
```

## Certificate Information

```bash
# List all certificates
sudo certbot certificates

# Check certificate expiration
sudo certbot certificates | grep -E "(Certificate Name|Expiry Date)"

# Check specific domain certificate
openssl x509 -in /etc/letsencrypt/live/codexdominion.app/fullchain.pem -text -noout | grep -A 2 "Validity"
```

## Manual Renewal Process

If automatic renewal fails:

```bash
# Stop nginx temporarily
sudo systemctl stop nginx

# Get new certificate (standalone mode)
sudo certbot certonly --standalone -d codexdominion.app -d www.codexdominion.app

# Start nginx
sudo systemctl start nginx

# Or use webroot mode (with nginx running)
sudo certbot certonly --webroot -w /var/www/html -d codexdominion.app -d www.codexdominion.app
```

## Troubleshooting

### Certificate Not Loading
```bash
# Check nginx SSL configuration
sudo nginx -t

# Verify certificate files exist
ls -la /etc/letsencrypt/live/codexdominion.app/

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Renewal Failures
```bash
# Check certbot logs
sudo journalctl -u certbot.timer

# Check renewal log
sudo cat /var/log/letsencrypt/letsencrypt.log

# Manual renewal with verbose output
sudo certbot renew --verbose
```

### Domain Validation Issues
```bash
# Ensure domain points to your server
nslookup codexdominion.app

# Test HTTP access (port 80 must be open)
curl -I http://codexdominion.app/.well-known/acme-challenge/test

# Check firewall
sudo ufw status
```

## SSL Security Best Practices

### Nginx SSL Configuration
Already included in `codexdominion_ssl.conf`:
- TLS 1.2 and 1.3 only
- Strong cipher suites
- HSTS headers
- Security headers

### Monitor Certificate Health
```bash
#!/bin/bash
# Add to cron: 0 6 * * * /path/to/ssl-check.sh

DOMAIN="codexdominion.app"
EXPIRY_DATE=$(openssl x509 -in /etc/letsencrypt/live/$DOMAIN/fullchain.pem -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_EPOCH=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "⚠️ SSL certificate for $DOMAIN expires in $DAYS_UNTIL_EXPIRY days!"
    # Send alert (email, webhook, etc.)
fi
```

## Certificate Backup

```bash
# Backup certificates
sudo tar -czf /backup/letsencrypt-$(date +%Y%m%d).tar.gz /etc/letsencrypt/

# Restore certificates (if needed)
sudo tar -xzf /backup/letsencrypt-YYYYMMDD.tar.gz -C /
sudo systemctl reload nginx
```

## Environment-Specific Notes

### Development
- Use self-signed certificates for local development
- Skip SSL verification in CLI: `NODE_TLS_REJECT_UNAUTHORIZED=0`

### Staging
- Use Let's Encrypt staging environment for testing
- Add `--test-cert` flag to certbot commands

### Production
- Monitor certificate expiry
- Set up alerting for renewal failures
- Keep backups of certificate files

## Quick Reference

| Command | Purpose |
|---------|---------|
| `sudo certbot certificates` | List all certificates |
| `sudo certbot renew --dry-run` | Test renewal process |
| `sudo certbot renew` | Renew all certificates |
| `sudo certbot delete --cert-name codexdominion.app` | Delete certificate |
| `sudo systemctl status certbot.timer` | Check auto-renewal timer |