import pytest
import os
from tempfile import TemporaryDirectory
from datetime import datetime, timedelta, timezone

from ..tasks.purge import TOKENS
from codex_project.backend.models.token import RefreshToken


@pytest.fixture()
def expired_token_db():
    """Temporary expired token DB for testing purge lifecycle.

    Creates a temp file with token rows (one per line) and seeds TOKENS list
    with expired tokens read from that file. Cleans up after yield.
    """
    with TemporaryDirectory() as tempdirname:
        db_path = os.path.join(tempdirname, "test_temp_tokens.db")

        # write 3 tokens to the file (the file content is not used directly by app,
        # but this matches the idea of a file-backed test DB)
        with open(db_path, "w") as f:
            f.write("token1\n")
            f.write("token2\n")
            f.write("token3\n")

        # Seed TOKENS with expired tokens
        TOKENS.clear()
        now = datetime.now(timezone.utc)
        TOKENS.append(RefreshToken(id=1, email='a@example.com', issued_at=now - timedelta(days=1), expires_at=now - timedelta(hours=2)))
        TOKENS.append(RefreshToken(id=2, email='b@example.com', issued_at=now - timedelta(days=1), expires_at=now - timedelta(hours=3)))
        TOKENS.append(RefreshToken(id=3, email='c@example.com', issued_at=now - timedelta(days=1), expires_at=now - timedelta(hours=4)))

        yield db_path

        # cleanup
        TOKENS.clear()