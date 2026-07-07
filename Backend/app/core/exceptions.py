"""
Application Exceptions.

Berisi seluruh custom exception yang digunakan
oleh Service Layer.

Service Layer tidak boleh melempar HTTPException.
HTTPException hanya digunakan pada API Layer
atau Exception Handler.
"""


class AppException(Exception):
    """
    Base exception untuk seluruh aplikasi.
    """

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
        super().__init__(message)


# ==========================================================
# AUTH
# ==========================================================

class AuthenticationError(AppException):
    """
    Login gagal.
    """


class InvalidCredentialsError(AuthenticationError):
    """
    Email atau password salah.
    """


class InvalidTokenError(AuthenticationError):
    """
    JWT tidak valid.
    """


class ExpiredTokenError(AuthenticationError):
    """
    JWT expired.
    """


class UnauthorizedError(AuthenticationError):
    """
    User belum login.
    """


class ForbiddenError(AuthenticationError):
    """
    User tidak memiliki hak akses.
    """


# ==========================================================
# USER
# ==========================================================

class UserNotFoundError(AppException):
    """
    User tidak ditemukan.
    """


class UserAlreadyExistsError(AppException):
    """
    Email sudah digunakan.
    """


class WeakPasswordError(AppException):
    """
    Password tidak memenuhi syarat.
    """


# ==========================================================
# TRIP
# ==========================================================

class TripNotFoundError(AppException):
    """
    Trip tidak ditemukan.
    """


class TripValidationError(AppException):
    """
    Data trip tidak valid.
    """


# ==========================================================
# CHAT
# ==========================================================

class ChatSessionNotFoundError(AppException):
    """
    Chat session tidak ditemukan.
    """


# ==========================================================
# DOCUMENT
# ==========================================================

class DocumentNotFoundError(AppException):
    """
    Document tidak ditemukan.
    """


# ==========================================================
# RAG
# ==========================================================

class EmbeddingError(AppException):
    """
    Embedding gagal dibuat.
    """


class RetrievalError(AppException):
    """
    Retrieval gagal.
    """


# ==========================================================
# TOOL
# ==========================================================

class ToolExecutionError(AppException):
    """
    Tool gagal dijalankan.
    """


# ==========================================================
# VALIDATION
# ==========================================================

class ValidationError(AppException):
    """
    Validasi gagal.
    """


class ResourceNotFoundError(AppException):
    """
    Resource tidak ditemukan.
    """


class ConflictError(AppException):
    """
    Terjadi konflik data.
    """