from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):

    def __init__(self):
        super().__init__(Document)

    def get_by_title(
        self,
        db: Session,
        title: str,
    ) -> Optional[Document]:

        return (
            db.query(Document)
            .filter(Document.title.ilike(f"%{title}%"))
            .first()
        )

    def get_all_documents(
        self,
        db: Session,
    ) -> list[Document]:

        return (
            db.query(Document)
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    def get_by_source(
        self,
        db: Session,
        source: str,
    ) -> list[Document]:

        return (
            db.query(Document)
            .filter(Document.source == source)
            .all()
        )

    def delete_document(
        self,
        db: Session,
        document: Document,
    ) -> None:

        db.delete(document)
        db.commit()