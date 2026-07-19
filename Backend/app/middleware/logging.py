"""
Logging Middleware.

Middleware ini bertanggung jawab untuk:

- Mencatat seluruh HTTP request.
- Menghitung waktu pemrosesan request.
- Menambahkan informasi request ke log aplikasi.

Middleware ini tidak mengubah response.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware untuk mencatat seluruh request dan response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        start_time = time.perf_counter()

        try:

            response = await call_next(request)

        except Exception:

            duration = (time.perf_counter() - start_time) * 1000

            logger.exception(
                (
                    "[%s] %s %s | %.2f ms | Client=%s"
                ),
                request_id,
                request.method,
                request.url.path,
                duration,
                request.client.host if request.client else "-",
            )

            raise

        duration = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            (
                "[%s] %s %s -> %s | %.2f ms | Client=%s"
            ),
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration,
            request.client.host if request.client else "-",
        )

        return response