def test_purge_with_fixture(expired_token_db):
    from codex_project.backend.tasks.purge import purge_expired_tokens

    result = purge_expired_tokens("fixture-test")
    assert result == 3
