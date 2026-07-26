class AppException(Exception):

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
        super().__init__(message)

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

class TripNotFoundError(AppException):
    """
    Trip tidak ditemukan.
    """

class TripValidationError(AppException):
    """
    Data trip tidak valid.
    """

class ChatSessionNotFoundError(AppException):
    """
    Chat session tidak ditemukan.
    """

class DocumentNotFoundError(AppException):
    """
    Document tidak ditemukan.
    """

class EmbeddingError(AppException):
    """
    Embedding gagal dibuat.
    """

class RetrievalError(AppException):
    """
    Retrieval gagal.
    """

class ToolExecutionError(AppException):
    """
    Tool gagal dijalankan.
    """

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