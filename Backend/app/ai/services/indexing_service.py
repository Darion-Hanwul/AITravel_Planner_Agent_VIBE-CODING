from __future__ import annotations

from langchain_core.documents import Document

from app.ai.loaders.chunk_loader import ChunkLoader
from app.ai.loaders.text_loader import TextLoader
from app.ai.loaders.web_loader import WebLoader
from app.ai.models.weaviate import WeaviateModel
from app.ai.services.embedding_service import EmbeddingService
from app.ai.sources.registry import SourceRegistry


class IndexingService:
    """
    Service untuk melakukan indexing seluruh
    knowledge source ke Weaviate.
    """

    def __init__(
        self,
    ) -> None:

        self.registry = SourceRegistry()

        self.web_loader = WebLoader()

        self.text_loader = TextLoader()

        self.chunk_loader = ChunkLoader()

        self.embedding_service = (
            EmbeddingService()
        )

        self.weaviate = WeaviateModel()

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    async def _load_documents(
        self,
    ) -> list[Document]:
        """
        Mengambil seluruh document dari seluruh
        source yang ada pada registry.
        """

        documents: list[Document] = []

        for source in self.registry.get_all():

            web_documents = await self.web_loader.load(
                source,
            )

            clean_documents = (
                self.text_loader.transform_many(
                    web_documents,
                )
            )

            documents.extend(
                clean_documents,
            )

        return documents

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    async def index_collection(
        self,
        collection_name: str,
    ) -> int:
        """
        Melakukan indexing seluruh knowledge source.

        Returns
        -------
        int
            Jumlah chunk yang berhasil diindex.
        """

        documents = await self._load_documents()

        chunks = self.chunk_loader.split_documents(
            documents,
        )

        embedded_documents = (
            self.embedding_service.embed_documents(
                chunks,
            )
        )

        if not self.weaviate.collection_exists(
            collection_name,
        ):
            self.weaviate.create_collection(
                collection_name,
            )

        self.weaviate.insert_documents(
            collection_name=collection_name,
            documents=embedded_documents,
        )

        return len(
            embedded_documents,
        )

    async def reindex_collection(
        self,
        collection_name: str,
    ) -> int:
        """
        Menghapus collection lama kemudian
        melakukan indexing ulang.
        """

        if self.weaviate.collection_exists(
            collection_name,
        ):
            self.weaviate.delete_collection(
                collection_name,
            )

        return await self.index_collection(
            collection_name,
        )

    def close(
        self,
    ) -> None:
        """
        Menutup koneksi Weaviate.
        """

        self.weaviate.close()