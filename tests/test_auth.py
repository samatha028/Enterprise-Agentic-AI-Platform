from backend.token_utils import (
    create_access_token,
    verify_access_token
)


def test_valid_token():
    token = create_access_token({"sub": "1"})

    payload = verify_access_token(token)

    assert payload is not None
    assert payload["sub"] == "1"


def test_invalid_token():
    payload = verify_access_token("invalid-token")

    assert payload is None
def test_token_payload_contains_expiry():
    token = create_access_token({"sub": "1"})

    payload = verify_access_token(token)

    assert "exp" in payload    