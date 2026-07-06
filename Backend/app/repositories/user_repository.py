from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.preference import UserPreference

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self):

        super().__init__(User)

    # =====================================================
    # GET USER BY EMAIL
    # =====================================================

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Optional[User]:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    # =====================================================
    # GET USER BY FULL NAME
    # =====================================================

    def get_by_full_name(
        self,
        db: Session,
        full_name: str,
    ):

        return (
            db.query(User)
            .filter(User.full_name.ilike(f"%{full_name}%"))
            .all()
        )

    # =====================================================
    # UPDATE AVATAR
    # =====================================================

    def update_avatar(
        self,
        db: Session,
        user: User,
        avatar_url: str,
    ) -> User:

        user.avatar_url = avatar_url

        return self.update(
            db,
            user,
        )


class UserPreferenceRepository(
    BaseRepository[UserPreference]
):

    def __init__(self):

        super().__init__(UserPreference)

    # =====================================================
    # GET BY USER ID
    # =====================================================

    def get_by_user_id(
        self,
        db: Session,
        user_id: UUID,
    ) -> Optional[UserPreference]:

        return (
            db.query(UserPreference)
            .filter(
                UserPreference.user_id == user_id
            )
            .first()
        )

    # =====================================================
    # UPDATE PREFERENCE
    # =====================================================

    def update_preference(
        self,
        db: Session,
        preference: UserPreference,
        **kwargs,
    ) -> UserPreference:

        for key, value in kwargs.items():

            if hasattr(preference, key):

                setattr(
                    preference,
                    key,
                    value,
                )

        return self.update(
            db,
            preference,
        )