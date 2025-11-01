# Codex Restore Script Documentation

## Overview
The `codex-restore.sh` script restores the full Codex Dominion system from a specified backup directory. It restores PostgreSQL, Redis, MinIO, configuration files, and logs. The script is integrated with the dashboard for live status streaming and audit logging.

## Usage

```bash
./codex-restore.sh /backups/YYYY-MM-DD
```
- Replace `/backups/YYYY-MM-DD` with your backup directory.
- Ensure the script is executable: `chmod +x codex-restore.sh`
- Required environment variables: `POSTGRES_USER`, `POSTGRES_DB`, `MINIO_USER`, `MINIO_PASS`

## What It Restores
- **PostgreSQL**: Restores from `db/codex.sql` if present.
- **Redis**: Restores from `redis/dump.rdb` if present.
- **MinIO**: Mirrors `minio/` to the MinIO bucket if present.
- **Configs**: Extracts `configs/codex-configs.tar.gz` if present.
- **Logs**: Notes archived logs if present.

## Integration
- The script is called by the dashboard restore widget via the `/api/restore` FastAPI endpoint.
- Output is streamed live to the dashboard and logged in `codex-restore.log`.

## Security
- Restrict restore access to admin users.
- Always confirm the backup directory before running a restore.

## Example Dashboard Flow
1. Admin enters backup directory in the dashboard restore widget.
2. Widget POSTs to `/api/restore`.
3. Backend runs `codex-restore.sh` and streams output.
4. Widget displays progress and result.
5. All actions are logged for audit.

---
For more, see `dashboard/codex-restore-widget.html` and `backend/codex_restore_api.py`.
