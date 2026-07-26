from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service
from app.core.exceptions import (
    InvalidTokenError,
    UserNotFoundError,
)
from app.models.user import User
from app.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(
        get_auth_service,
    ),
) -> User:

    try:

        return auth_service.verify_access_token(
            token,
        )

    except (
        InvalidTokenError,
        UserNotFoundError,
    ) as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


def get_current_active_user(
    current_user: User = Depends(
        get_current_user,
    ),
) -> User:
    return current_user


def get_optional_user(
    token: str | None = Depends(
        oauth2_scheme,
    ),
    auth_service: AuthService = Depends(
        get_auth_service,
    ),
) -> User | None:

    if token is None:

        return None

    try:

        return auth_service.verify_access_token(
            token,
        )

    except (
        InvalidTokenError,
        UserNotFoundError,
    ):

        return None