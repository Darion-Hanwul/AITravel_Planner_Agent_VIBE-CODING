"""
Factory dan helper untuk seluruh interaksi
dengan Weaviate Vector Database.

Seluruh AI Service harus mengakses Weaviate
melalui class ini agar konfigurasi dan akses
tetap terpusat.
"""

from __future__ import annotations

from typing import Optional
import weaviate
from weaviate.classes.config import Configure
from weaviate.classes.init import AdditionalConfig, Timeout

from app.ai.models.embedded_document import EmbeddedDocument
from app.config.settings import settings

from weaviate.collections.collection import Collection

from app.ai.models.retrieved_document import (
    RetrievedDocument,
)
from weaviate.classes.query import MetadataQuery

class WeaviateModel:
    """
    Wrapper untuk koneksi dan operasi Weaviate.

    Bertanggung jawab terhadap:

    - Connection (Embedded Mode)
    - Collection Management
    - Insert Object
    - Vector Search
    - Hybrid Search

    Tidak bertanggung jawab terhadap:

    - Embedding
    - Chunking
    - RAG
    - AI Agent
    """

    def __init__(self) -> None:
        # Menambahkan type hint Optional agar linter tahu client bisa bernilai None
        self.client: Optional[weaviate.WeaviateClient] = None
        try:
            self.client = weaviate.connect_to_embedded(
                version="1.24.24",
                persistence_data_path="./weaviate_data",
                additional_config=AdditionalConfig(
                    timeout=Timeout(init=120, query=60, insert=120),
                )
            )
        except Exception as e:
            print(f"[Weaviate Critical Error] Gagal menginisialisasi mode Embedded: {e}")
            self.client = None

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _get_collection(
        self,
        collection_name: str,
    ) -> Collection:

        if not self.client:
            raise RuntimeError("Weaviate client is not initialized.")

        if not self.collection_exists(
            collection_name,
        ):
            raise ValueError(
                f"Collection '{collection_name}' does not exist."
            )

        collection = self.client.collections.get(
            collection_name,
        )

        return collection

    def close(self) -> None:
        """
        Menutup koneksi Weaviate.
        """
        if self.client:
            self.client.close()


    # =====================================================
    # COLLECTION
    # =====================================================

    def collection_exists(
        self,
        collection_name: str,
    ) -> bool:
        """
        Mengecek apakah collection sudah ada.
        """
        if not self.client:
            return False

        return self.client.collections.exists(
            collection_name,
        )

    def create_collection(
        self,
        collection_name: str,
    ) -> None:
        """
        Membuat collection apabila belum ada.
        """
        if not self.client:
            raise RuntimeError("Weaviate client is not initialized.")

        if self.collection_exists(collection_name):
            return

        self.client.collections.create(
            name=collection_name,
            vectorizer_config=Configure.Vectorizer.none(),
        )

    def delete_collection(
        self,
        collection_name: str,
    ) -> None:
        """
        Menghapus collection.
        """
        if not self.client:
            raise RuntimeError("Weaviate client is not initialized.")

        if not self.collection_exists(collection_name):
            return

        self.client.collections.delete(
            collection_name,
        )

    # =====================================================
    # INSERT
    # =====================================================

    def insert_documents(
        self,
        collection_name: str,
        documents: list[EmbeddedDocument],
    ) -> None:
        """
        Menyimpan seluruh embedding ke Weaviate.
        """
        if not self.client:
            raise RuntimeError("Weaviate client is not initialized.")

        collection = self._get_collection(
            collection_name,
        )

        with collection.batch.dynamic() as batch:

            for item in documents:

                batch.add_object(
                    properties={
                        "content": item.document.page_content,
                        **item.document.metadata,
                    },
                    vector=item.embedding,
                )

    # =====================================================
    # SEARCH
    # =====================================================

    def vector_search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[RetrievedDocument]:
        
        if not self.client:
            return []

        collection = self._get_collection(
            collection_name,
        )

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            return_metadata=MetadataQuery(
                distance=True,
            ),
        )

        documents: list[RetrievedDocument] = []

        for obj in response.objects:

            properties: dict[str, object] = {}

            if obj.properties is not None:

                properties = {
                    str(key): value
                    for key, value in obj.properties.items()
                }

            content = str(
                properties.pop(
                    "content",
                    "",
                )
            )

            distance = 0.0

            if (
                obj.metadata is not None
                and obj.metadata.distance is not None
            ):
                distance = float(
                    obj.metadata.distance
                )

            documents.append(
                RetrievedDocument(
                    content=content,
                    metadata=properties,
                    score=distance,
                )
            )

        return documents
    
    def hybrid_search(
        self,
        collection_name: str,
        query: str,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[RetrievedDocument]:

        if not self.client:
            return []

        collection = self._get_collection(
            collection_name,
        )

        response = collection.query.hybrid(
            query=query,
            vector=query_vector,
            limit=limit,
            return_metadata=MetadataQuery(
                score=True,
            ),
        )

        documents: list[RetrievedDocument] = []

        for obj in response.objects:

            properties: dict[str, object] = {}

            if obj.properties is not None:

                properties = {
                    str(key): value
                    for key, value in obj.properties.items()
                }

            content = str(
                properties.pop(
                    "content",
                    "",
                )
            )

            score = 0.0

            if (
                obj.metadata is not None
                and obj.metadata.score is not None
            ):
                score = float(
                    obj.metadata.score
                )

            documents.append(
                RetrievedDocument(
                    content=content,
                    metadata=properties,
                    score=score,
                )
            )

        return documents