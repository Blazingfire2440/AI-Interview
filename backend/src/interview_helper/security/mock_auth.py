"""Development-only mock authentication.

Enabled with MOCK_AUTH=true and ENVIRONMENT=development (see config.Settings,
which refuses to start if MOCK_AUTH is set outside development).
"""

import time

from interview_helper.security.http import OIDCUserInfo, TokenClaims

MOCK_AUTH_TOKEN = "mock-auth-dev-token"
MOCK_ISSUER = "mock-auth"
MOCK_USER_SUB = "mock-auth|test-user"
MOCK_USER_GIVEN_NAME = "Mock"
MOCK_USER_FAMILY_NAME = "Test User"
MOCK_USER_EMAIL = "mock.test.user@example.invalid"


def is_mock_token(token: str) -> bool:
    return token.removeprefix("Bearer ") == MOCK_AUTH_TOKEN


def mock_claims() -> TokenClaims:
    now = int(time.time())
    return TokenClaims(
        iss=MOCK_ISSUER,
        sub=MOCK_USER_SUB,
        exp=now + 3600,
        iat=now,
        name=f"{MOCK_USER_GIVEN_NAME} {MOCK_USER_FAMILY_NAME}",
        email=MOCK_USER_EMAIL,
        email_verified=True,
    )


def mock_user_info() -> OIDCUserInfo:
    return OIDCUserInfo(
        sub=MOCK_USER_SUB,
        email=MOCK_USER_EMAIL,
        email_verified=True,
        name=f"{MOCK_USER_GIVEN_NAME} {MOCK_USER_FAMILY_NAME}",
        given_name=MOCK_USER_GIVEN_NAME,
        family_name=MOCK_USER_FAMILY_NAME,
    )
