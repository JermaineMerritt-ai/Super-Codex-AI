# Codex-Flame Liturgical Scheduling Guide

## Daily Liturgical Cycle

### Systemd Service (Linux/WSL)
```ini
[Unit]
Description=Codex-Flame Daily Liturgy
After=network.target

[Service]
Type=oneshot
User=codex
WorkingDirectory=/opt/codex-flame
ExecStart=/usr/bin/python3 eternal_flame_liturgy.py
Environment=PATH=/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
```

### Systemd Timer (Linux/WSL)
```ini
[Unit]
Description=Run Codex-Flame Daily Liturgy
Requires=codex-flame-liturgy.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### Windows Task Scheduler (PowerShell)
```powershell
# Create daily liturgy task
$Action = New-ScheduledTaskAction -Execute "python" -Argument "eternal_flame_liturgy.py" -WorkingDirectory "C:\codex-flame"
$Trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "Codex-Flame-Daily-Liturgy" -Action $Action -Trigger $Trigger -Settings $Settings
```

### Cron (Unix/Linux)
```bash
# Daily at 6:00 AM
0 6 * * * cd /opt/codex-flame && python3 eternal_flame_liturgy.py >> /var/log/codex-liturgy.log 2>&1

# Weekly on Sunday at 8:00 AM (family/council liturgy)
0 8 * * 0 cd /opt/codex-flame && python3 eternal_flame_liturgy.py --mode=weekly >> /var/log/codex-liturgy.log 2>&1

# Monthly on 1st at 9:00 AM (seasonal observances)
0 9 1 * * cd /opt/codex-flame && python3 eternal_flame_liturgy.py --mode=monthly >> /var/log/codex-liturgy.log 2>&1

# Quarterly on solstices/equinoxes (annual ceremonial cycles)
0 10 21 3,6,9,12 * cd /opt/codex-flame && python3 eternal_flame_liturgy.py --mode=seasonal >> /var/log/codex-liturgy.log 2>&1
```

## Liturgical Cycle Types

### Daily Practice
- Morning invocation recall
- Honor inscription review
- Seasonal awareness
- Community connection

### Weekly Family/Council Liturgy
- Extended honor ceremonies
- Dispatch replay sessions
- Governance seal reviews
- Community announcements

### Monthly Seasonal Observances
- Seasonal transition ceremonies
- Extended honor broadcasts
- Quarterly governance reviews
- Community milestone celebrations

### Annual Ceremonial Cycles
- Solstice/Equinox major ceremonies
- Annual honor roll ceremonies
- Governance charter renewals
- Community covenant renewals

## Installation Commands

### Linux/WSL Systemd Setup
```bash
# Copy service files
sudo cp codex-flame-liturgy.service /etc/systemd/system/
sudo cp codex-flame-liturgy.timer /etc/systemd/system/

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable codex-flame-liturgy.timer
sudo systemctl start codex-flame-liturgy.timer

# Check status
sudo systemctl status codex-flame-liturgy.timer
```

### Windows Setup
```powershell
# Run the PowerShell task creation script above
# Or use Task Scheduler GUI to create the task manually
```

### Docker Container
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
CMD ["python", "eternal_flame_liturgy.py"]
```

## Logging and Monitoring

### Log Rotation
```bash
# /etc/logrotate.d/codex-liturgy
/var/log/codex-liturgy.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 codex codex
}
```

### Monitoring Script
```bash
#!/bin/bash
# check_liturgy.sh - Monitor liturgical cycles
LAST_LITURGY=$(find /opt/codex-flame/storage/liturgy -name "LIT-*.json" -mtime -1 | wc -l)
if [ "$LAST_LITURGY" -eq 0 ]; then
    echo "WARNING: No liturgical cycles in last 24 hours"
    exit 1
else
    echo "OK: $LAST_LITURGY liturgical cycles found"
    exit 0
fi
```