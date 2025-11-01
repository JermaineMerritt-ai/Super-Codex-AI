from codex_project.backend.tasks.purge import TOKENS, purge_expired_tokens
from codex_project.backend.models.token import RefreshToken
from datetime import datetime, timedelta, timezone


def test_purge_removes_expired():
    TOKENS.clear()
    now = datetime.now(timezone.utc)
    TOKENS.append(RefreshToken(id=1, email='a@example.com', issued_at=now, expires_at=now - timedelta(minutes=5)))
    TOKENS.append(RefreshToken(id=2, email='b@example.com', issued_at=now, expires_at=now + timedelta(minutes=5)))
    removed = purge_expired_tokens('test')
    assert removed == 1
    assert len(TOKENS) == 1
