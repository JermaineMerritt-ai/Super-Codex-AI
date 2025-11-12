# AXIOM FLAME API - Production Verification

## Quick Health Check

Your primary verification command:
```bash
curl https://codexdominion.app/health
```

Expected response:
```json
{
  "status": "ok",
  "time": "2025-11-10T12:00:00Z"
}
```

## Complete API Testing

Run the comprehensive test suite:
```bash
chmod +x scripts/test-api.sh
./scripts/test-api.sh
```

## Manual Testing Commands

### Health Endpoints
```bash
# HTTPS health check
curl https://codexdominion.app/health

# HTTP redirect test
curl -I http://codexdominion.app/health

# Local direct test
curl http://localhost:8080/health
```

### Ceremonial API Testing
```bash
# Test ceremonial reasoning
curl -X POST https://codexdominion.app/reason \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "Custodian",
    "realm": "PL-001", 
    "capsule": "Sovereign Crown",
    "intent": "Crown.Invocation",
    "seal": "Eternal"
  }'

# Test replay (use dispatch_id from above response)
curl -X POST https://codexdominion.app/replay \
  -H "Content-Type: application/json" \
  -d '{"dispatch_id": "AXF-2025-11-10-12345678"}'

# Test audit
curl -X POST https://codexdominion.app/audit \
  -H "Content-Type: application/json" \
  -d '{"dispatch_id": "AXF-2025-11-10-12345678"}'
```

### CLI Testing
```bash
# Set API endpoint
export AXIOM_API="https://codexdominion.app"

# Test CLI commands
axiom health
axiom invoke "PL-001" "Sovereign Crown"
axiom replay AXF-2025-11-10-12345678
axiom audit AXF-2025-11-10-12345678
```

## SSL Certificate Verification

```bash
# Check certificate details
openssl s_client -connect codexdominion.app:443 -servername codexdominion.app </dev/null | openssl x509 -noout -text

# Check certificate expiration
openssl s_client -connect codexdominion.app:443 -servername codexdominion.app </dev/null | openssl x509 -noout -dates

# Test SSL labs (online)
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=codexdominion.app
```

## Security Headers Check

```bash
# Check security headers
curl -I https://codexdominion.app/health

# Look for these headers:
# - Strict-Transport-Security
# - X-Frame-Options
# - X-Content-Type-Options
# - Content-Security-Policy
```

## Performance Testing

```bash
# Response time test
curl -w "Response time: %{time_total}s\n" -o /dev/null -s https://codexdominion.app/health

# Compression test
curl -H "Accept-Encoding: gzip" -I https://codexdominion.app/health | grep -i content-encoding

# Load testing (install apache2-utils first)
ab -n 100 -c 10 https://codexdominion.app/health
```

## Monitoring Setup

### Health Check Script
```bash
#!/bin/bash
# Save as /usr/local/bin/axiom-domain-health
HEALTH_URL="https://codexdominion.app/health"

if curl -f -s "$HEALTH_URL" > /dev/null; then
    echo "✅ AXIOM FLAME API (codexdominion.app) is healthy"
    exit 0
else
    echo "❌ AXIOM FLAME API (codexdominion.app) health check failed"
    # Optional: send alert via webhook, email, etc.
    exit 1
fi
```

### Cron Job for Monitoring
```bash
# Add to crontab: crontab -e
*/5 * * * * /usr/local/bin/axiom-domain-health >> /var/log/axiom-domain-health.log 2>&1
```

## Troubleshooting

### API Not Responding
```bash
# Check service status
sudo systemctl status axiom-flame

# Check nginx status  
sudo systemctl status nginx

# Check service logs
sudo journalctl -u axiom-flame -f

# Check nginx logs
sudo tail -f /var/log/nginx/codexdominion_access.log
sudo tail -f /var/log/nginx/codexdominion_error.log
```

### SSL Issues
```bash
# Check certificate files
sudo ls -la /etc/letsencrypt/live/codexdominion.app/

# Test certificate renewal
sudo certbot renew --dry-run

# Check nginx SSL configuration
sudo nginx -t
```

### DNS Issues
```bash
# Check DNS resolution
nslookup codexdominion.app
dig codexdominion.app

# Check from different locations
# Use online tools like whatsmydns.net
```

## Expected Results

When everything is working correctly:

1. ✅ `curl https://codexdominion.app/health` returns JSON with status "ok"
2. ✅ HTTP requests redirect to HTTPS
3. ✅ SSL certificate is valid and trusted
4. ✅ Security headers are present
5. ✅ API endpoints respond correctly
6. ✅ CLI commands work with domain endpoint

Your AXIOM FLAME API is production-ready when all tests pass! 🎉