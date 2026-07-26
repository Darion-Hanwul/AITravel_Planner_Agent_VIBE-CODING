from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
)

from app.models.place import SavedPlace

from app.repositories.saved_place_repository import (
    SavedPlaceRepository,
)

from app.schemas.saved_place import (
    SavedPlaceCreate,
    SavedPlaceResponse,
    SavedPlaceUpdate,
)

from app.services.base_service import BaseService


class SavedPlaceService(BaseService):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.saved_place_repository = (
            SavedPlaceRepository()
        )

    def _get_place(
        self,
        place_id: UUID,
    ) -> SavedPlace:
        place = (
            self.saved_place_repository.get_by_id(
                self.db,
                place_id,
            )
        )

        if place is None:

            raise ResourceNotFoundError(
                "Saved place not found.",
            )

        return place

    def _to_response(
        self,
        place: SavedPlace,
    ) -> SavedPlaceResponse:
        return SavedPlaceResponse.model_validate(
            place,
        )
    
    def create_place(
        self,
        user_id: UUID,
        data: SavedPlaceCreate,
    ) -> SavedPlaceResponse:

        place = SavedPlace(
            user_id=user_id,
            name=data.name,
            country=data.country,
            city=data.city,
            latitude=data.latitude,
            longitude=data.longitude,
            category=data.category,
            notes=data.notes,
        )

        try:

            self.saved_place_repository.create(
                self.db,
                place,
            )

            self.commit()

            self.refresh(
                place,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            place,
        )

    def get_place(
        self,
        place_id: UUID,
    ) -> SavedPlaceResponse:
        place = self._get_place(
            place_id,
        )

        return self._to_response(
            place,
        )

    def get_user_places(
        self,
        user_id: UUID,
    ) -> list[SavedPlaceResponse]:
        places = (
            self.saved_place_repository.get_by_user(
                self.db,
                user_id,
            )
        )

        return [
            self._to_response(
                place,
            )
            for place in places
        ]

    def search_place(
        self,
        user_id: UUID,
        keyword: str,
    ) -> list[SavedPlaceResponse]:
        places = (
            self.saved_place_repository.search_place(
                self.db,
                user_id,
                keyword,
            )
        )

        return [
            self._to_response(
                place,
            )
            for place in places
        ]

    def update_place(
        self,
        place_id: UUID,
        data: SavedPlaceUpdate,
    ) -> SavedPlaceResponse:

        place = self._get_place(
            place_id,
        )

        update_data = (
            data.model_dump(
                exclude_unset=True,
            )
        )

        for field, value in update_data.items():

            setattr(
                place,
                field,
                value,
            )

        try:

            self.saved_place_repository.update(
                self.db,
                place,
            )

            self.commit()

            self.refresh(
                place,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            place,
        )

    def delete_place(
        self,
        place_id: UUID,
    ) -> None:
        place = self._get_place(
            place_id,
        )

        try:

            self.saved_place_repository.delete(
                self.db,
                place,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise