"""Simple script to call the backend purge task."""
import sys
import argparse
from codex_project.backend.tasks.purge import purge_expired_tokens, TOKENS
from codex_project.backend.models.token import RefreshToken
from datetime import datetime, timedelta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reason', default='manual', help='Reason for purge')
    parser.add_argument('--seed', action='store_true', help='Seed demo tokens')
    args = parser.parse_args()

    if args.seed:
        # Add two expired tokens and one active token
        TOKENS.clear()
        now = datetime.now(timezone.utc)
        TOKENS.append(RefreshToken(id=1, email='x@example.com', issued_at=now, expires_at=now - timedelta(minutes=10)))
        TOKENS.append(RefreshToken(id=2, email='y@example.com', issued_at=now, expires_at=now - timedelta(minutes=5)))
        TOKENS.append(RefreshToken(id=3, email='z@example.com', issued_at=now, expires_at=now + timedelta(minutes=60)))

    n = purge_expired_tokens(actor=args.reason)
    print(f'Purged {n} tokens (reason={args.reason})')


if __name__ == '__main__':
    main()
