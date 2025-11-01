from codex_project.backend.models.token import RefreshToken


def test_token_create():
    t = RefreshToken.create(1, 'a@example.com', lifetime_minutes=1)
    assert t.email == 'a@example.com'
    assert t.expires_at > t.issued_at
