from __future__ import annotations

from app.ai.models.ollama import OllamaModel
from app.ai.models.retrieved_document import RetrievedDocument
from app.ai.models.weaviate import WeaviateModel
from app.config.settings import settings


class RetrieverService:
    """
    Service untuk melakukan document retrieval
    dari Weaviate.

    Responsibility
    --------------

    - Query Embedding
    - Vector Search
    - Hybrid Search

    Tidak bertanggung jawab terhadap

    - Crawling
    - Chunking
    - Embedding Indexing
    - Prompt
    - LLM
    """

    def __init__(
        self,
    ) -> None:

        self.embedding_model = (
            OllamaModel.get_embedding_model()
        )

        self.weaviate = WeaviateModel()

        self.collection_name = (
            settings.WEAVIATE_CLASS
        )

    # =====================================================
    # PRIVATE
    # =====================================================

    def _embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Mengubah query menjadi embedding vector.
        """

        return self.embedding_model.embed_query(
            query,
        )

    # =====================================================
    # PUBLIC
    # =====================================================

    def vector_search(
        self,
        query: str,
        limit: int | None = None,
    ) -> list[RetrievedDocument]:
        """
        Pure Vector Search.
        """

        query_vector = self._embed_query(
            query,
        )

        return self.weaviate.vector_search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit or settings.TOP_K,
        )

    def hybrid_search(
        self,
        query: str,
        limit: int | None = None,
    ) -> list[RetrievedDocument]:
        """
        Hybrid Search.

        Menggunakan:

        - embedding
        - keyword
        """

        query_vector = self._embed_query(
            query,
        )

        return self.weaviate.hybrid_search(
            collection_name=self.collection_name,
            query=query,
            query_vector=query_vector,
            limit=limit or settings.TOP_K,
        )
    
    def close(self) -> None:
        """
        Menutup resource retriever.
        """
        self.weaviate.close()