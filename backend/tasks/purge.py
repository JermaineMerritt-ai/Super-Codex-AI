from datetime import datetime, timezone
from typing import List
from ..models.token import RefreshToken
import os

# Simulated in-memory token store for demo/tests
TOKENS: List[RefreshToken] = []


def purge_expired_tokens_from_file(file_path: str) -> int:
    """Read tokens from a simple file (one per line), remove all lines and return count.

    This is a simple, demo-friendly file-backed purge mode.
    """
    if not os.path.exists(file_path):
        return 0
    # Read all lines and then truncate the file
    with open(file_path, 'r+', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]
        count = len(lines)
        f.seek(0)
        f.truncate()
    return count


def purge_expired_tokens(actor: str = None) -> int:
    """Remove expired tokens.

    If environment variable TOKEN_FILE_PATH is set, use file-backed mode (simple all-lines purge).
    Otherwise use in-memory TOKENS list.
    """
    token_file = os.environ.get('TOKEN_FILE_PATH') or os.environ.get('TOKEN_FILE')
    if token_file:
        return purge_expired_tokens_from_file(token_file)

    now = datetime.now(timezone.utc)
    before = len(TOKENS)
    remaining = [t for t in TOKENS if (t.expires_at > now and not t.revoked)]
    removed = before - len(remaining)
    TOKENS.clear()
    TOKENS.extend(remaining)
    return removed
