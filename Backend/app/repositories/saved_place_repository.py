from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.place import SavedPlace
from app.repositories.base_repository import BaseRepository


class SavedPlaceRepository(
    BaseRepository[SavedPlace]
):

    def __init__(self) -> None:
        super().__init__(SavedPlace)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[SavedPlace]:

        stmt = (
            select(SavedPlace)
            .where(
                SavedPlace.user_id == user_id
            )
            .order_by(
                SavedPlace.name.asc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def search_place(
        self,
        db: Session,
        user_id: UUID,
        keyword: str,
    ) -> list[SavedPlace]:

        stmt = (
            select(SavedPlace)
            .where(
                SavedPlace.user_id == user_id,
                SavedPlace.name.ilike(
                    f"%{keyword}%"
                ),
            )
            .order_by(
                SavedPlace.name.asc()
            )
        )

        return list(
            db.scalars(stmt)
        )