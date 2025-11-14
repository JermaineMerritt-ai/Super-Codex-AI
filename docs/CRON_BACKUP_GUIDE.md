# Codex Backup Cron Installation Guide

## Overview
The `codex-backup.cron` file contains automated backup and maintenance tasks for the Super-Codex-AI system. This guide covers installation, monitoring, and troubleshooting.

## Installation

### 1. Copy the cron file to system location
```bash
sudo cp ops/codex-backup.cron /etc/cron.d/codex-backup
sudo chmod 644 /etc/cron.d/codex-backup
sudo chown root:root /etc/cron.d/codex-backup
```

### 2. Verify cron service is running
```bash
sudo systemctl status cron
sudo systemctl enable cron  # if not already enabled
```

### 3. Check cron logs
```bash
sudo tail -f /var/log/cron.log
```

## Prerequisites

### Directory Structure
Ensure these directories exist with proper permissions:
```bash
sudo mkdir -p /backups
sudo mkdir -p /opt/Super-Codex-AI/storage/replays
sudo chown -R codex:codex /backups
sudo chown -R codex:codex /opt/Super-Codex-AI/storage
```

### Docker Container
The PostgreSQL backup requires a running Docker container:
```bash
docker ps | grep codex_postgres
```

### Python Environment
Ensure Python and required packages are available:
```bash
/usr/bin/python --version
/usr/bin/python -c "import sys; print(sys.path)"
```

## Scheduled Tasks

| Time  | Task | Description |
|-------|------|-------------|
| 02:00 | Database Backup | Export PostgreSQL database to timestamped SQL file |
| 02:15 | Replay Capsules | Generate ceremonial replay archives |
| 02:30 | Checksums | Create SHA256 verification hashes |

## Monitoring

### Check recent backups
```bash
ls -la /backups/codexdb_*.sql | tail -5
```

### Verify replay capsules
```bash
ls -la /opt/Super-Codex-AI/storage/replays/*.zip | tail -5
```

### Check checksums
```bash
cat /opt/Super-Codex-AI/storage/replays/checksums.txt
```

### Verify integrity
```bash
cd /opt/Super-Codex-AI/storage/replays
sha256sum -c checksums.txt
```

## Troubleshooting

### Common Issues

1. **Permission denied**
   ```bash
   sudo chown -R codex:codex /opt/Super-Codex-AI
   sudo chown -R codex:codex /backups
   ```

2. **Docker container not found**
   ```bash
   docker ps -a | grep postgres
   docker start codex_postgres
   ```

3. **Python script fails**
   ```bash
   cd /opt/Super-Codex-AI
   /usr/bin/python scripts/generate_replay_capsule.py
   ```

4. **Cron not executing**
   ```bash
   sudo systemctl restart cron
   sudo tail -f /var/log/syslog | grep CRON
   ```

### Log Locations
- Cron execution: `/var/log/cron.log`
- System messages: `/var/log/syslog`
- Database backup errors: `/backups/backup.log` (if configured)

## Manual Execution

Test individual tasks manually:

```bash
# Database backup
docker exec codex_postgres pg_dump -U codex codexdb > /backups/test_backup.sql

# Replay capsule generation
cd /opt/Super-Codex-AI
/usr/bin/python scripts/generate_replay_capsule.py

# Checksum generation
sha256sum /opt/Super-Codex-AI/storage/replays/*.zip > /opt/Super-Codex-AI/storage/replays/test_checksums.txt
```

## Security Considerations

1. **File Permissions**: Ensure backup files are not world-readable
2. **Database Credentials**: Use environment variables or secure credential storage
3. **Log Rotation**: Configure logrotate for backup and system logs
4. **Disk Space**: Monitor available space in backup directories

## Customization

### Enable Optional Cleanup Tasks
Uncomment the cleanup lines in the cron file to automatically remove old files:
- Database backups older than 30 days
- Replay archives older than 90 days

### Modify Schedule
Edit `/etc/cron.d/codex-backup` and reload:
```bash
sudo systemctl reload cron
```

## Integration with Monitoring

Consider integrating with monitoring systems:
- Add healthcheck endpoints for backup verification
- Configure alerts for failed backup tasks
- Monitor disk usage in backup directories
- Track backup file sizes and integrity