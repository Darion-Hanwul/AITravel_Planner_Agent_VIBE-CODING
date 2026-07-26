from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):

    def __init__(self) -> None:
        super().__init__(Document)

    def get_by_title(
        self,
        db: Session,
        title: str,
    ) -> Optional[Document]:

        stmt = (
            select(Document)
            .where(
                Document.title.ilike(f"%{title}%")
            )
            .limit(1)
        )

        return db.scalar(stmt)

    def get_all_documents(
        self,
        db: Session,
    ) -> list[Document]:

        stmt = (
            select(Document)
            .order_by(
                Document.uploaded_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def get_by_source(
        self,
        db: Session,
        source: str,
    ) -> list[Document]:

        stmt = (
            select(Document)
            .where(
                Document.source == source
            )
            .order_by(
                Document.uploaded_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def delete_document(
        self,
        db: Session,
        document: Document,
    ) -> None:

        self.delete(
            db,
            document,
        )