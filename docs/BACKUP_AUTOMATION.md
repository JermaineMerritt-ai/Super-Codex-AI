#
# === Manual Backup Run ===

To run the backup script manually, use:

```
./codex-backup.sh
```

This will initiate the Codex Dominion backup process. The script outputs status messages for each backup step and ends with:

```
✅ Backup Ritual Complete — stored in /backups/YYYY-MM-DD
```

The dashboard can display the last backup time and status by parsing this output or monitoring the backup directory.
# Codex System Backup & Restore Automation

## Linux (crontab)
To schedule daily backups at 2:00 AM, add this line to your crontab (run `crontab -e`):

```
0 2 * * * /usr/local/bin/codex-backup.sh
```

This will run the backup script every day at 2:00 AM. Do not add this line to your nginx.conf.

## Windows (Task Scheduler)
Use the provided Task Scheduler XMLs and PowerShell scripts (see `codex-db-backup-task.xml`, `codex-db-backup.ps1`, etc.) to automate daily backups. Import the XML in Task Scheduler and set the schedule as needed.

## Dashboard Integration
The dashboard displays backup/restore status and next scheduled run for both Linux (crontab) and Windows (Task Scheduler) systems. No nginx.conf changes are required for backup automation.
