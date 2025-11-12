# AXIOM FLAME Service Quick Reference

## Service Management Commands

### Essential Commands
```bash
# Enable service (start on boot)
sudo systemctl enable axiom-flame

# Start the service
sudo systemctl start axiom-flame

# Check service status
sudo systemctl status axiom-flame

# Stop the service
sudo systemctl stop axiom-flame

# Restart the service
sudo systemctl restart axiom-flame

# Disable service (prevent auto-start)
sudo systemctl disable axiom-flame
```

### Service Information
```bash
# View recent logs
sudo journalctl -u axiom-flame -n 50

# Follow live logs
sudo journalctl -u axiom-flame -f

# Check if service is enabled
sudo systemctl is-enabled axiom-flame

# Check if service is active
sudo systemctl is-active axiom-flame
```

### API Testing
```bash
# Test API health
curl http://localhost:8080/health

# Test ceremonial reasoning
curl -X POST http://localhost:8080/reason \
  -H "Content-Type: application/json" \
  -d '{"actor":"Custodian","realm":"PL-001","capsule":"Test"}'

# Test via nginx proxy (if configured)
curl -H "Host: codexdominion.app" http://localhost/health
```

## Service File Locations

- **Service Definition**: `/etc/systemd/system/axiom-flame.service`
- **Application Directory**: `/srv/axiom-flame/`
- **Python Virtual Environment**: `/srv/axiom-flame/.venv/`
- **API Code**: `/srv/axiom-flame/packages/api/`
- **Storage**: `/srv/axiom-flame/storage/`
- **Artifacts**: `/srv/axiom-flame/artifacts/`

## Troubleshooting

### Service Won't Start
```bash
# Check service status for errors
sudo systemctl status axiom-flame

# View detailed logs
sudo journalctl -u axiom-flame --no-pager

# Check Python virtual environment
ls -la /srv/axiom-flame/.venv/bin/python

# Test Python app manually
cd /srv/axiom-flame/packages/api
/srv/axiom-flame/.venv/bin/python app.py
```

### Port Already in Use
```bash
# Check what's using port 8080
sudo netstat -tlnp | grep :8080
sudo lsof -i :8080

# Kill conflicting process
sudo kill -9 <PID>
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R axiom-flame:axiom-flame /srv/axiom-flame

# Fix permissions
sudo chmod -R 755 /srv/axiom-flame
sudo chmod -R 750 /srv/axiom-flame/storage
```

### Configuration Reload
```bash
# After changing service file
sudo systemctl daemon-reload
sudo systemctl restart axiom-flame
```

## Monitoring

### Health Check Script
```bash
#!/bin/bash
# Save as /usr/local/bin/axiom-health-check
if curl -f -s http://localhost:8080/health > /dev/null; then
    echo "✅ AXIOM FLAME API is healthy"
    exit 0
else
    echo "❌ AXIOM FLAME API health check failed"
    sudo systemctl status axiom-flame --no-pager
    exit 1
fi
```

### Cron Job for Monitoring
```bash
# Add to crontab: crontab -e
*/5 * * * * /usr/local/bin/axiom-health-check >> /var/log/axiom-health.log 2>&1
```

## Performance Tuning

### Memory Usage
```bash
# Check memory usage
sudo systemctl show axiom-flame --property=MemoryCurrent

# Set memory limit (edit service file)
MemoryMax=1G
```

### File Limits
```bash
# Check file descriptor usage
sudo systemctl show axiom-flame --property=FileDescriptorStore

# Increase limits (edit service file)
LimitNOFILE=65536
```