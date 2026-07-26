from typing import Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType],
    ) -> None:
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        db.add(obj)
        return obj

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

        stmt = (
            select(self.model)
            .offset(skip)
            .limit(limit)
        )

        return list(db.scalars(stmt))

    def first(
        self,
        db: Session,
    ) -> Optional[ModelType]:

        stmt = (
            select(self.model)
            .limit(1)
        )

        return db.scalar(stmt)

    def count(
        self,
        db: Session,
    ) -> int:

        stmt = select(func.count()).select_from(self.model)

        return db.scalar(stmt) or 0

    def exists(
        self,
        db: Session,
        id: UUID,
    ) -> bool:

        return self.get_by_id(db, id) is not None

    def update(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> ModelType:

        db.add(db_obj)

        return db_obj

    def delete(
        self,
        db: Session,
        db_obj: ModelType,
    ) -> None:

        db.delete(db_obj)

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

    def commit(
        self,
        db: Session,
    ) -> None:

        db.commit()

    def rollback(
        self,
        db: Session,
    ) -> None:

        db.rollback()