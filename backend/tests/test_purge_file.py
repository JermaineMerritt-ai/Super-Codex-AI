import os
from tempfile import NamedTemporaryFile

from codex_project.backend.tasks.purge import purge_expired_tokens


def test_purge_file_mode(monkeypatch):
    with NamedTemporaryFile('w+', delete=False) as f:
        f.write('token1\n')
        f.write('token2\n')
        f.write('token3\n')
        f.flush()
        path = f.name

    try:
        monkeypatch.setenv('TOKEN_FILE_PATH', path)
        removed = purge_expired_tokens(actor='file-test')
        assert removed == 3
        # file should now be empty
        with open(path, 'r') as r:
            assert r.read().strip() == ''
    finally:
        os.remove(path)
