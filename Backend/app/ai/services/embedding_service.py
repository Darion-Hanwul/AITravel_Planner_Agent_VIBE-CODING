"""
Service untuk menghasilkan embedding menggunakan Ollama.

Service ini hanya bertanggung jawab mengubah
LangChain Document menjadi EmbeddedDocument.

Tidak bertanggung jawab terhadap:

- Weaviate
- Indexing
- Retrieval
- RAG
- AI Agent
"""

from __future__ import annotations

from langchain_core.documents import Document

from app.ai.models.embedded_document import EmbeddedDocument
from app.ai.models.ollama import OllamaModel


class EmbeddingService:
    """
    Service pembuat embedding dokumen.

    Seluruh AI Layer harus menggunakan service ini
    agar proses embedding terpusat dan konsisten.
    """

    def __init__(self) -> None:
        self.embedding_model = (
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
        Menghasilkan embedding dari sebuah teks.

        Args:
            text:
                Teks yang akan di-embedding.

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
        Menghasilkan embedding untuk satu dokumen.

        Args:
            document:
                LangChain Document.

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
        Menghasilkan embedding untuk banyak dokumen.

        Args:
            documents:
                Daftar LangChain Document.

        Returns:
            List EmbeddedDocument.
        """

        if not documents:
            return []

        texts = [
            document.page_content
            for document in documents
        ]

        embeddings = (
            self.embedding_model.embed_documents(
                texts,
            )
        )

        embedded_documents: list[
            EmbeddedDocument
        ] = []

        for document, embedding in zip(
            documents,
            embeddings,
            strict=True,
        ):
            embedded_documents.append(
                EmbeddedDocument(
                    document=document,
                    embedding=embedding,
                )
            )

        return embedded_documents