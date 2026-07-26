from __future__ import annotations

from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.exceptions import UnauthorizedError

PUBLIC_PATHS = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
    "/auth/login",
    "/auth/register",
    "/auth/refresh",
}

class AuthenticationMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        request.state.access_token = None

        if self._is_public_path(request.url.path):
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if authorization is None:
            raise UnauthorizedError(
                "Authorization header is missing.",
            )

        scheme, _, token = authorization.partition(" ")

        if scheme.lower() != "bearer" or not token:
            raise UnauthorizedError(
                "Invalid Authorization header format.",
            )

        request.state.access_token = token

        return await call_next(request)

    @staticmethod
    def _is_public_path(
        path: str,
    ) -> bool:
        """
        Mengecek apakah endpoint termasuk endpoint publik.
        """

        return (
            path in PUBLIC_PATHS
            or path.startswith("/docs")
            or path.startswith("/redoc")
            or path.startswith("/openapi")
        )