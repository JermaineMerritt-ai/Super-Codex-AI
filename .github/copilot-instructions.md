# Copilot Instructions for Codex Project

## Architecture Overview
- **Backend**: Python (FastAPI), organized under `backend/` with submodules for models, services, and tasks. Key entrypoint: `codex_restore_api.py` (exposes `/api/restore` for dashboard integration).
- **Capsule Video**: Modular video pipeline in `capsule_video/` with `scene.py`, `render.py`, and `publish.py`. Each supports multiple call signatures for flexibility (see tests for usage patterns).
- **Testing**: Both `unittest` and `pytest` are used. Tests for backend logic are in `backend/tests/`, while capsule video tests are in `tests/` at the project root.
- **Docs & Scripts**: Operational scripts (`codex-backup.sh`, `codex-restore.sh`) and their documentation are in `docs/`. Environment and ingress configs are also documented here.

## Key Patterns & Conventions
- **Token Purge Logic**: `backend/tasks/purge.py` supports both in-memory and file-backed token stores, toggled by the `TOKEN_FILE_PATH` env var. Purge functions are tested with both real and monkeypatched environments.
- **User Roles**: `backend/models/user.py` and `services/auth.py` define a simple council/custodian role model. Use `is_council(user)` for role checks.
- **Capsule Video API**: All main functions (`create_scene`, `render_video`, `publish_video`) accept either a config dict or expanded arguments. See `tests/test_capsule_video.py` for canonical usage.
- **Restore Endpoint**: `/api/restore` POST streams output from `codex-restore.sh` and logs to `codex-restore.log`. Only admins should access this endpoint (enforce in dashboard/frontend).

## Developer Workflows
- **Run All Tests**: Use `pytest` for both backend and capsule video tests. Some tests use fixtures and monkeypatching for file/env simulation.
- **Manual Backup/Restore**: Run `./codex-backup.sh` and `./codex-restore.sh /backups/YYYY-MM-DD` (see docs for details and required env vars).
- **Environment Reference**: All key env vars are documented in `codex-env-settings.ipynb` (see workspace root).

## Integration & External Dependencies
- **Dockerized Services**: Backup/restore scripts assume Docker containers for Postgres, Redis, MinIO, and Loki.
- **Ingress**: NGINX config and subdomain routing are documented in `docs/codex-ingress-nginx.md`.
- **Dashboard**: Integrates with backend via REST endpoints and parses script output/logs for status.

## Examples
- **Token Purge (file mode):**
  ```python
  os.environ['TOKEN_FILE_PATH'] = '/tmp/tokens.db'
  purge_expired_tokens()
  ```
- **Capsule Video:**
  ```python
  scene = create_scene('Title', 'Script', ['img.png'])
  video = render_video([scene])
  publish_video(video, 'CapsuleX')
  ```

---
For onboarding, see `docs/README.md` and referenced notebooks/scripts. Update this file as workflows or conventions evolve.
