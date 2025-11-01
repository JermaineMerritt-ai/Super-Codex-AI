#
# === Manual Run & Dashboard Integration ===

To run the backup script manually:

```
./codex-backup.sh
```

The script will print status for each step and finish with:

```
✅ Backup Ritual Complete — stored in /backups/YYYY-MM-DD
```

The dashboard widget can display the last backup time and status by reading this output or monitoring the backup directory.
# Codex Dominion Backup Script

This script automates daily backups for PostgreSQL, Redis, MinIO, configs, and logs. Intended for Dockerized deployments. Schedule with cron or run manually.

## Usage
- Make executable: `chmod +x codex-backup.sh`
- Place in `/usr/local/bin/` or a directory in your PATH
- Schedule with: `0 2 * * * /usr/local/bin/codex-backup.sh`

## Script

```bash
#!/bin/bash
set -e

# === Codex Dominion Backup Ritual ===
# Save as codex-backup.sh, make executable: chmod +x codex-backup.sh
# Run manually or via cron: ./codex-backup.sh

# === Paths ===
BACKUP_DIR=/backups/$(date +%F)
mkdir -p $BACKUP_DIR/{db,redis,minio,configs,logs}

echo "🌌 Codex Dominion Backup Ritual Initiated — $(date)"

# === PostgreSQL Backup ===
echo "📜 Backing up PostgreSQL..."
docker exec -t postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_DIR/db/codex.sql

# === Redis Snapshot ===
echo "🧠 Backing up Redis..."
docker exec redis redis-cli SAVE
cp ~/codex-suite/data/redis/dump.rdb $BACKUP_DIR/redis/dump.rdb

# === MinIO / Object Storage Sync ===
echo "📦 Backing up MinIO artifacts..."
mc alias set codex http://minio:9000 $MINIO_USER $MINIO_PASS
mc mirror codex/codex-bucket $BACKUP_DIR/minio

# === Configs ===
echo "⚙️ Backing up configs..."
tar -czf $BACKUP_DIR/configs/codex-configs.tar.gz \
  ~/codex-suite/.env.stack \
  ~/codex-suite/nginx/nginx.conf \
  ~/codex-suite/docker-compose.yml

# === Logs & Metrics ===
echo "📊 Backing up logs..."
docker exec loki logcli query '{job="codex"}' --since=24h > $BACKUP_DIR/logs/codex.log

echo "✅ Backup Ritual Complete — stored in $BACKUP_DIR"
```

## Dashboard Integration
- Dashboard widgets display last backup time, status, and next scheduled run.
- No changes to nginx.conf are required.
- For Windows, use the provided PowerShell scripts and Task Scheduler XMLs.
