from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.preference import UserPreference
from app.models.user import User
from app.repositories.user_repository import (
    UserPreferenceRepository,
    UserRepository,
)
from app.services.base_service import BaseService

from app.schemas.user import (
    UserPreferenceResponse,
    UserProfileResponse,
    UserResponse,
)

class UserService(BaseService):
    """
    User service.

    Bertanggung jawab terhadap seluruh business logic
    yang berkaitan dengan profile user.

    Scope:

    - User profile
    - Avatar
    - Preferences

    Tidak menangani authentication.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(db)

        self.user_repository = UserRepository()

        self.preference_repository = (
            UserPreferenceRepository()
        )

    # ======================================================
    # PRIVATE HELPERS
    # ======================================================

    def _get_user_by_id(
        self,
        user_id: UUID,
    ) -> User:
        """
        Mengambil user berdasarkan ID.

        Raises:
            UserNotFoundError
        """

        user = self.user_repository.get_by_id(
            self.db,
            user_id,
        )

        if user is None:

            raise UserNotFoundError(
                "User not found.",
            )

        return user

    def _get_preference(
        self,
        user_id: UUID,
    ) -> UserPreference:
        """
        Mengambil preference user.

        Raises:
            UserNotFoundError
        """

        preference = (
            self.preference_repository.get_by_user_id(
                self.db,
                user_id,
            )
        )

        if preference is None:

            raise UserNotFoundError(
                "User preference not found.",
            )

        return preference

    def _ensure_email_available(
        self,
        email: str,
        current_user_id: UUID | None = None,
    ) -> None:
        """
        Memastikan email belum digunakan
        oleh user lain.
        """

        existing_user = (
            self.user_repository.get_by_email(
                self.db,
                email,
            )
        )

        if existing_user is None:
            return

        if (
            current_user_id is not None
            and existing_user.id == current_user_id
        ):
            return

        raise UserAlreadyExistsError(
            "Email is already registered.",
        )

    def _save_changes(
        self,
    ) -> None:
        """
        Commit current transaction.

        Raises:
            SQLAlchemyError
        """

        try:

            self.commit()

        except SQLAlchemyError:

            self.rollback()

            raise

    def _rollback_transaction(
        self,
    ) -> None:
        """
        Rollback current transaction.
        """

        self.rollback()

    # ======================================================
    # PUBLIC METHODS
    # ======================================================

    from app.schemas.user import (
        UserProfileResponse,
    )

    def get_profile(
        self,
        user_id: UUID,
    ) -> UserProfileResponse:
        """
        Mengambil profile user beserta preference.
        """

        user = self._get_user_by_id(
            user_id,
        )

        preference = self.preference_repository.get_by_user_id(
            self.db,
            user.id,
        )

        return UserProfileResponse(
            **UserResponse.model_validate(
                user,
            ).model_dump(),
            preferences=(
                UserPreferenceResponse.model_validate(
                    preference,
                )
                if preference is not None
                else None
            ),
        )
    def update_profile(
        self,
        user_id: UUID,
        full_name: str | None = None,
        avatar_url: str | None = None,
    ) -> User:
        """
        Update profile user.

        Raises:
            UserNotFoundError
        """

        user = self._get_user_by_id(
            user_id,
        )

        if full_name is not None:
            user.full_name = full_name

        if avatar_url is not None:
            user.avatar_url = avatar_url

        try:

            self.user_repository.update(
                self.db,
                user,
            )

            self.commit()

            self.refresh(
                user,
            )

        except Exception:

            self.rollback()

            raise

        return user