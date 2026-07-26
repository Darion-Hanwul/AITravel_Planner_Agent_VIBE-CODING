from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DocumentNotFoundError,
)

from app.models.document import Document

from app.repositories.document_repository import (
    DocumentRepository,
)

from app.schemas.document import (
    DocumentBase,
    DocumentResponse,
)

from app.services.base_service import BaseService


class DocumentService(BaseService):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.document_repository = (
            DocumentRepository()
        )

    def _get_document(
        self,
        document_id: UUID,
    ) -> Document:

        document = (
            self.document_repository.get_by_id(
                self.db,
                document_id,
            )
        )

        if document is None:

            raise DocumentNotFoundError(
                "Document not found.",
            )

        return document

    def _to_response(
        self,
        document: Document,
    ) -> DocumentResponse:

        return DocumentResponse.model_validate(
            document,
        )

    def create_document(
        self,
        data: DocumentBase,
    ) -> DocumentResponse:

        document = Document(
            title=data.title,
            file_name=data.file_name,
            source=data.source,
        )

        try:

            self.document_repository.create(
                self.db,
                document,
            )

            self.commit()

            self.refresh(
                document,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            document,
        )

    def get_document(
        self,
        document_id: UUID,
    ) -> DocumentResponse:
        document = self._get_document(
            document_id,
        )

        return self._to_response(
            document,
        )

    def get_documents(
        self,
    ) -> list[DocumentResponse]:

        documents = (
            self.document_repository.get_all_documents(
                self.db,
            )
        )

        return [
            self._to_response(
                document,
            )
            for document in documents
        ]

    def search_by_title(
        self,
        title: str,
    ) -> DocumentResponse | None:
        document = (
            self.document_repository.get_by_title(
                self.db,
                title,
            )
        )

        if document is None:
            return None

        return self._to_response(
            document,
        )

    def get_by_source(
        self,
        source: str,
    ) -> list[DocumentResponse]:

        documents = (
            self.document_repository.get_by_source(
                self.db,
                source,
            )
        )

        return [
            self._to_response(
                document,
            )
            for document in documents
        ]

    def delete_document(
        self,
        document_id: UUID,
    ) -> None:
        document = self._get_document(
            document_id,
        )

        try:

            self.document_repository.delete_document(
                self.db,
                document,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise