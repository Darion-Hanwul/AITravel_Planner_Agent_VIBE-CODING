from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from jose import ExpiredSignatureError
from jose import JWTError
from jose import jwt

from app.config.settings import settings
from app.core.exceptions import ExpiredTokenError
from app.core.exceptions import InvalidTokenError

SECRET_KEY = settings.JWT_SECRET

ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

REFRESH_TOKEN_EXPIRE_DAYS = (
    settings.REFRESH_TOKEN_EXPIRE_DAYS
)

def _now() -> datetime:

    return datetime.now(timezone.utc)


def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": _now(),
        "exp": _now() + expires_delta,
    }

    if additional_claims:

        payload.update(
            additional_claims,
        )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=(
            expires_delta
            or timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        ),
        additional_claims=additional_claims,
    )

def create_refresh_token(
    subject: str,
) -> str:

    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS,
        ),
    )

def decode_token(
    token: str,
) -> dict[str, Any]:

    try:

        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except ExpiredSignatureError as exc:

        raise ExpiredTokenError(
            "Token has expired."
        ) from exc

    except JWTError as exc:

        raise InvalidTokenError(
            "Invalid token."
        ) from exc

def get_token_type(
    token: str,
) -> str:

    payload = decode_token(
        token,
    )

    return str(
        payload["type"],
    )

def get_subject(
    token: str,
) -> str:

    payload = decode_token(
        token,
    )

    return str(
        payload["sub"],
    )

def decode_access_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(
        token,
    )

    if payload.get("type") != "access":

        raise InvalidTokenError(
            "Access token required."
        )

    return payload

def decode_refresh_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(
        token,
    )

    if payload.get("type") != "refresh":

        raise InvalidTokenError(
            "Refresh token required."
        )

    return payload

def is_access_token(
    token: str,
) -> bool:

    try:

        decode_access_token(
            token,
        )

        return True

    except InvalidTokenError:

        return False


def is_refresh_token(
    token: str,
) -> bool:

    try:

        decode_refresh_token(
            token,
        )

        return True

    except InvalidTokenError:

        return False