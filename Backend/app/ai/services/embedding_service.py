from __future__ import annotations

from langchain_core.documents import Document

from app.ai.models.embedded_document import (
    EmbeddedDocument,
)
from app.ai.models.ollama import OllamaModel

from langchain_ollama import OllamaEmbeddings

class EmbeddingService:
    """
    Service untuk menghasilkan vector embedding.

    Responsibility:

    - Generate embedding menggunakan Ollama.
    - Menghasilkan EmbeddedDocument.

    Tidak bertanggung jawab terhadap:

    - Weaviate
    - RAG
    - Retrieval
    - Database
    """

    def __init__(
        self,
    ) -> None:

        self.embedding_model: OllamaEmbeddings = (
            OllamaModel.get_embedding_model()
        )

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Menghasilkan embedding untuk satu text.

        Args:
            text:
                Text yang akan di-embedding.

        Returns:
            Vector embedding.
        """

        return self.embedding_model.embed_query(
            text,
        )

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def embed_document(
        self,
        document: Document,
    ) -> EmbeddedDocument:
        """
        Menghasilkan embedding untuk satu document.

        Args:
            document:
                LangChain document.

        Returns:
            EmbeddedDocument.
        """

        embedding = self._embed(
            document.page_content,
        )

        return EmbeddedDocument(
            document=document,
            embedding=embedding,
        )

    def embed_documents(
        self,
        documents: list[Document],
    ) -> list[EmbeddedDocument]:
        """
        Menghasilkan embedding untuk banyak document.

        Args:
            documents:
                List LangChain document.

        Returns:
            List EmbeddedDocument.
        """

        return [
            self.embed_document(
                document,
            )
            for document in documents
        ]