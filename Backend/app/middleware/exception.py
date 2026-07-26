from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from Backend.app.core.exceptions import (
    AppException,
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    ResourceNotFoundError,
    UnauthorizedError,
    ValidationError,
)
from app.core.logger import logger

def error_response(
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
        },
    )

def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:

        logger.warning(
            "%s - %s",
            request.url.path,
            exc.message,
        )

        status_code = status.HTTP_400_BAD_REQUEST

        if isinstance(exc, AuthenticationError):
            status_code = status.HTTP_401_UNAUTHORIZED

        elif isinstance(exc, UnauthorizedError):
            status_code = status.HTTP_401_UNAUTHORIZED

        elif isinstance(exc, ForbiddenError):
            status_code = status.HTTP_403_FORBIDDEN

        elif isinstance(exc, ResourceNotFoundError):
            status_code = status.HTTP_404_NOT_FOUND

        elif isinstance(exc, ConflictError):
            status_code = status.HTTP_409_CONFLICT

        elif isinstance(exc, ValidationError):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        return error_response(
            status_code=status_code,
            code=getattr(
                exc,
                "error_code",
                exc.__class__.__name__.upper(),
            ),
            message=exc.message,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:

        logger.warning(
            "Validation Error: %s",
            exc.errors(),
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "REQUEST_VALIDATION_ERROR",
                    "message": "Request validation failed.",
                    "details": exc.errors(),
                },
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:

        logger.exception(
            "Database Error: %s",
            exc,
        )

        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DATABASE_ERROR",
            message="Internal database error.",
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        logger.exception(
            "Unhandled Exception",
            exc_info=exc,
        )

        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
        )