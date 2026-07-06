from uuid import UUID

from sqlalchemy.orm import Session

from app.models.place import SavedPlace
from app.repositories.base_repository import BaseRepository


class SavedPlaceRepository(BaseRepository[SavedPlace]):

    def __init__(self):
        super().__init__(SavedPlace)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[SavedPlace]:

        return (
            db.query(SavedPlace)
            .filter(SavedPlace.user_id == user_id)
            .order_by(SavedPlace.name.asc())
            .all()
        )

    def search_place(
        self,
        db: Session,
        user_id: UUID,
        keyword: str,
    ) -> list[SavedPlace]:

        return (
            db.query(SavedPlace)
            .filter(
                SavedPlace.user_id == user_id,
                SavedPlace.name.ilike(f"%{keyword}%")
            )
            .all()
        )