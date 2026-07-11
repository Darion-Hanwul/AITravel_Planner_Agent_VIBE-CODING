from __future__ import annotations

from weaviate import WeaviateClient
from weaviate.connect import ConnectionParams

from app.config.settings import settings


class WeaviateModel:
    """
    Singleton Weaviate Client.

    Bertanggung jawab terhadap:

    - Membuat koneksi ke Weaviate
    - Menyediakan singleton client
    - Menutup koneksi

    Class ini TIDAK menangani:

    - Collection
    - Insert Object
    - Delete Object
    - Vector Search
    - Hybrid Search

    Seluruh business logic tersebut berada
    pada RetrieverService / DocumentIndexer.
    """

    _client: WeaviateClient | None = None

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    @classmethod
    def get_client(
        cls,
    ) -> WeaviateClient:
        """
        Mengembalikan singleton Weaviate Client.

        Returns:
            WeaviateClient
        """

        if cls._client is None:

            cls._client = WeaviateClient(
                connection_params=ConnectionParams.from_url(
                    url=settings.WEAVIATE_URL,
                    grpc_port=settings.WEAVIATE_GRPC_PORT,
                ),
            )

            cls._client.connect()

        return cls._client

    @classmethod
    def close(
        cls,
    ) -> None:
        """
        Menutup koneksi Weaviate.
        """

        if cls._client is not None:

            cls._client.close()

            cls._client = None

    @classmethod
    def is_connected(
        cls,
    ) -> bool:
        """
        Mengecek apakah client sudah terhubung.

        Returns:
            bool
        """

        return (
            cls._client is not None
            and cls._client.is_connected()
        )