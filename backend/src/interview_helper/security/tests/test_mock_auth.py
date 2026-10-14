import pytest
from pydantic import SecretStr, ValidationError

from interview_helper.config import Settings
from interview_helper.security.mock_auth import (
    MOCK_AUTH_TOKEN,
    MOCK_USER_SUB,
    is_mock_token,
    mock_claims,
    mock_user_info,
)

# pyright: reportCallIssue=none, reportArgumentType=none


def _settings(**overrides: object) -> Settings:
    base: dict[str, object] = dict(
        CORS_ALLOW_ORIGINS="http://localhost:5173",
        OPENAI_API_ENDPOINT="https://endpoint.com",
        OPENAI_API_KEY=SecretStr("k"),
        AZURE_DEPLOYMENT="gpt-5",
        AZURE_EVAL_DEPLOYMENT="gpt-4o-mini",
        AZURE_SPEECH_KEY=None,
        AZURE_SPEECH_REGION=None,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)  # pyright: ignore[reportUnknownVariableType]


def test_mock_auth_allowed_in_development_without_oidc():
    s = _settings(MOCK_AUTH=True, ENVIRONMENT="development")
    assert s.mock_auth


def test_mock_auth_rejected_outside_development():
    with pytest.raises(ValidationError):
        _settings(MOCK_AUTH=True)
    with pytest.raises(ValidationError):
        _settings(MOCK_AUTH=True, ENVIRONMENT="production")


def test_oidc_required_when_mock_auth_disabled():
    with pytest.raises(ValidationError):
        _settings(ENVIRONMENT="development")
    s = _settings(OIDC_AUTHORITY="a", OIDC_CLIENT_ID="b")
    assert not s.mock_auth


def test_mock_identity_is_stable():
    assert is_mock_token(f"Bearer {MOCK_AUTH_TOKEN}")
    assert not is_mock_token("other")
    assert mock_claims().sub == MOCK_USER_SUB == mock_user_info().sub
