from sqlalchemy.orm import Session
from uuid import UUID

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    WeakPasswordError,
    UserNotFoundError,
)
from app.core.security import (
    validate_password_strength,
    verify_password,
)

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
)

from app.core.security import (
    hash_password,
)

from app.schemas.auth import (
    TokenResponse,
)

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(db)

        self.user_repository: UserRepository = UserRepository()
    
    def _get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Mengambil user berdasarkan email.
        """

        return self.user_repository.get_by_email(
            self.db,
            email,
        )
    
    def _get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        user = self.user_repository.get_by_id(
            self.db,
            user_id,
        )

        if user is None:

            raise UserNotFoundError(
                "User not found.",
            )

        return user  


    def _validate_new_password(
        self,
        password: str,
    ) -> None:
        valid, message = validate_password_strength(
            password,
        )

        if not valid:
            raise WeakPasswordError(message)

    def _authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User:
        user = self._get_user_by_email(
            email,
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid email or password."
            )

        return user

    def _ensure_email_available(
        self,
        email: str,
    ) -> None:
        existing_user = self._get_user_by_email(
            email,
        )

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "Email is already registered."
            )
        
    def _generate_access_token(
        self,
        user: User,
    ) -> str:
        return create_access_token(
            subject=str(user.id),
        )
    
    def _generate_refresh_token(
        self,
        user: User,
    ) -> str:
        return create_refresh_token(
            subject=str(user.id),
        )
    
    def _update_password(
        self,
        user: User,
        password: str,
    ) -> None:

        user.password_hash = hash_password(
            password,
        )

        self.user_repository.update(
            self.db,
            user,
        )

    def register(
        self,
        full_name: str,
        email: str,
        password: str,
    ) -> TokenResponse:
        self._validate_new_password(
            password,
        )

        self._ensure_email_available(
            email,
        )

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(
                password,
            ),
        )

        try:

            self.user_repository.create(
                self.db,
                user,
            )

            self.commit()

            self.refresh(user)

        except Exception:

            self.rollback()

            raise

        return TokenResponse(
            access_token=self._generate_access_token(
                user,
            ),
            refresh_token=self._generate_refresh_token(
                user,
            ),
        )
    
    def login(
        self,
        email: str,
        password: str,
    ) -> TokenResponse:
        user = self._authenticate_user(
            email=email,
            password=password,
        )

        return TokenResponse(
            access_token=self._generate_access_token(
                user,
            ),
            refresh_token=self._generate_refresh_token(
                user,
            ),
        )
    
    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> TokenResponse:
        payload = decode_refresh_token(
            refresh_token,
        )

        user_id = UUID(
            payload["sub"],
        )

        user = self._get_user_by_id(
            user_id,
        )

        return TokenResponse(
            access_token=self._generate_access_token(
                user,
            ),
            refresh_token=refresh_token,
        )
    
    def change_password(
        self,
        user_id: UUID,
        old_password: str,
        new_password: str,
    ) -> None:
        user = self._get_user_by_id(
            user_id,
        )

        if not verify_password(
            old_password,
            user.password_hash,
        ):

            raise InvalidCredentialsError(
                "Current password is incorrect.",
            )
        
        if old_password == new_password:
            raise WeakPasswordError(
                "New password must be different from the current password.",
            )
        
        self._validate_new_password(
            new_password,
        )

        self._update_password(
            user,
            new_password,
        )

        self.commit()

    def verify_access_token(
        self,
        access_token: str,
    ) -> User:
        payload = decode_access_token(
            access_token,
        )

        user_id = UUID(
            payload["sub"],
        )

        user = self._get_user_by_id(
            user_id,
        )

        return user