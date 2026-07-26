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

    def __init__(self) -> None:
        self.embedding_model = (
            OllamaModel.get_embedding_model()
        )

    def _embed(
        self,
        text: str,
    ) -> list[float]:

        return self.embedding_model.embed_query(
            text,
        )
    
    def embed_text(
        self,
        text: str,
    ) -> list[float]:

        return self._embed(
            text,
        )

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        
        if not texts:
            return []

        return self.embedding_model.embed_documents(
            texts,
        )

    def embed_document(
        self,
        document: Document,
    ) -> EmbeddedDocument:
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
    
