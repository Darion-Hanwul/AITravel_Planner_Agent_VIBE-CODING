from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.preference import UserPreference
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self) -> None:
        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> Optional[User]:

        stmt = (
            select(User)
            .where(User.email == email)
        )

        return db.scalar(stmt)

    def exists_by_email(
        self,
        db: Session,
        email: str,
    ) -> bool:

        stmt = (
            select(User.id)
            .where(User.email == email)
            .limit(1)
        )

        return db.scalar(stmt) is not None

    def get_by_full_name(
        self,
        db: Session,
        full_name: str,
    ) -> list[User]:

        stmt = (
            select(User)
            .where(
                User.full_name.ilike(
                    f"%{full_name}%"
                )
            )
        )

        return list(
            db.scalars(stmt)
        )

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

    def __init__(self) -> None:
        super().__init__(UserPreference)

    def get_by_user_id(
        self,
        db: Session,
        user_id: UUID,
    ) -> Optional[UserPreference]:

        stmt = (
            select(UserPreference)
            .where(
                UserPreference.user_id == user_id
            )
        )

        return db.scalar(stmt)

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