# Copilot Instructions — Super-Codex-AI

These notes give an AI coding agent the minimal, practical context to be productive in this repository.

## Big Picture
- **Primary apps**: a Python/FastAPI backend under `backend/` (APIs, tasks, services) and a modular `capsule_video/` pipeline for scene/render/publish workflows.
- **Entry points**: `backend/main.py`, `backend/codex_restore_api.py` (restore endpoint), and `capsule_video/__init__.py` (library surface).
- **Design rationale**: long-running operational scripts (backup/restore) are intentionally script-driven and isolated from the API surface so streaming output and logging can be consumed by the dashboard and orchestration tooling.
- **Ceremonial/Governance**: The `axiom-flame/` subdirectory contains a ceremonial governance system with structured ledger entries, replay auditing, and honor management (Flask API + Node CLI). All ceremonial operations use validated JSON schemas with governance seals, authority levels, and audit trails.

## Key files & examples (use these as anchors)
- `backend/codex_restore_api.py`: POST `/api/restore` streams `codex-restore.sh` output and writes `codex-restore.log`.
- `backend/tasks/purge.py`: token purge logic — supports in-memory and file-backed stores. Toggle with `TOKEN_FILE_PATH`.
- `backend/models/user.py` and `services/auth.py`: role model; prefer `is_council(user)` for council checks.
- `capsule_video/scene.py`, `capsule_video/render.py`, `capsule_video/publish.py`: pipeline functions accept either a config dict or expanded args.
- `axiom-flame/packages/api/app.py`: Flask API for ceremonial reasoning, replay auditing, and registry management.
- `axiom-flame/packages/cli/`: Node.js CLI for ceremony dispatch, honor granting, and broadcast operations.

Examples:
```python
# token purge (file-backed)
os.environ['TOKEN_FILE_PATH'] = '/tmp/tokens.db'
purge_expired_tokens()

# capsule pipeline
scene = create_scene('Title', 'Script', ['img.png'])
video = render_video([scene])
publish_video(video, 'CapsuleX')
```

```bash
# axiom-flame operations (global CLI)
cd axiom-flame/packages/cli
npm install -g .  # install global axiom command
axiom reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown" --intent "Crown.Invocation"
axiom replay AXF-2025-11-10-12345678
axiom audit AXF-2025-11-10-12345678
axiom health

# axiom-flame local CLI operations  
node index.js reason --actor "Custodian" --realm "PL-001" --capsule "Sovereign Crown"
node index.js replay AXF-2025-11-10-12345678
node index.js audit AXF-2025-11-10-12345678
node index.js health
```

## Developer workflows & commands
- Create and activate a venv (Windows PowerShell):
  ```powershell
  py -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt   # if present
  ```
- Run tests (repo root): `py -m pytest -q`.
- Run the FastAPI app locally: `uvicorn backend.main:app --reload` (confirm import path in `backend/main.py`).
- Run axiom-flame API locally (PowerShell):
  ```powershell
  cd axiom-flame/packages/api
  python app.py
  curl http://localhost:8080/health
  ```
- Backup/restore: use `docs/` and scripts (`codex-backup.sh`, `codex-restore.sh`) — these expect Dockerized infra (Postgres, Redis, MinIO, Loki).

## Project-specific conventions
- Tests frequently use `monkeypatch` and fixture-based env/file simulation — prefer monkeypatching `os.environ` and temporary paths in tests (see `backend/tests/`).
- Public library functions in `capsule_video` accept both a `config` dict and expanded args — maintain that dual signature when extending.
- Preserve streaming and logging behavior for the restore endpoint; the dashboard and restore scripts rely on streamed stdout and `codex-restore.log`.
- **Ceremonial data structures**: All axiom-flame operations use structured JSON with required fields: `dispatch_id`, `timestamp`, `actor`, `realm`, `capsule`, `intent`, governance seals, and audit trails. Follow the pattern in `axiom-flame/artifacts/ceremonies/` for new ceremonial entries.
- **Registry system**: Realms have structured IDs (PL-001, ST-007, etc.), status levels, and capsule permissions. Actors are validated against realm access and capsule availability before ceremonies.
- **Honors ledger**: Centralized ledger (`honors-ledger.json`) with HK-NNNN IDs, insignia awards, authority levels, and seal classifications. Supports both individual honor files and consolidated ledger format.
- **Ceremonial data structures**: All axiom-flame operations use structured JSON with required fields: `dispatch_id`, `timestamp`, `actor`, `realm`, `capsule`, `intent`, governance seals, and audit trails. Follow the pattern in `axiom-flame/artifacts/ceremonies/` for new ceremonial entries.

## Integration points & CI
- CI workflows: `.github/workflows/ci.yml` and `.github/workflows/codex-ci-cd.yaml` — changes to tests or packaging may require CI updates.
- External infra: Docker containers for Postgres/Redis/MinIO/Loki are assumed by operational scripts.

## Practical rules for an AI contributor
- Keep changes small and focused; prefer refactors that preserve public function signatures.
- When modifying storage or token behavior, keep the `TOKEN_FILE_PATH` toggle and ensure tests cover both modes.
- Use existing tests in `backend/tests/` and `tests/` as canonical examples of expected behavior and signatures.

## Where to look for more detail
- `docs/` for runbooks and ingress config.
- `codex-env-settings.ipynb` for environment variable expectations.
- `backend/tests/` and `tests/` for usage patterns and examples.

---
If you want this shorter, or want additional sections (CI, local dev setup, or test patterns expanded), tell me which and I will update this file.
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
