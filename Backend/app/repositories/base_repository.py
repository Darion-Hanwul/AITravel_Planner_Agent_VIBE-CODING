from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic Base Repository.

    Menyediakan operasi CRUD dasar
    yang digunakan oleh seluruh repository.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ==========================================================
    # CREATE
    # ==========================================================

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    # ==========================================================
    # READ
    # ==========================================================

    def get_by_id(
        self,
        db: Session,
        id: UUID,
    ) -> Optional[ModelType]:

        return db.get(self.model, id)

    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:

        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def first(
        self,
        db: Session,
    ) -> Optional[ModelType]:

        return db.query(self.model).first()

    def count(
        self,
        db: Session,
    ) -> int:

        return db.query(self.model).count()

    def exists(
        self,
        db: Session,
        id: UUID,
    ) -> bool:

        return db.get(self.model, id) is not None

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> ModelType:

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> None:

        db.delete(db_obj)
        db.commit()

    # ==========================================================
    # SESSION HELPERS
    # ==========================================================

    def flush(
        self,
        db: Session,
    ) -> None:

        db.flush()

    def refresh(
        self,
        db: Session,
        obj: ModelType,
    ) -> None:

        db.refresh(obj)

    def save(
        self,
        db: Session,
        obj: Optional[ModelType] = None,
    ) -> Optional[ModelType]:

        db.commit()

        if obj is not None:
            db.refresh(obj)

        return obj

    def rollback(
        self,
        db: Session,
    ) -> None:

        db.rollback()