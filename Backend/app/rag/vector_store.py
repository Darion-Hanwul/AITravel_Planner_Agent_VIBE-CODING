import weaviate

from typing import List, Dict, Any, Optional

from app.config.settings import settings


class WeaviateVectorStore:

    def __init__(self) -> None:

        self.client = None
        self.collection = None

        self.collection_name = (
            settings.WEAVIATE_CLASS
        )

        self._connect()

    def _connect(self) -> None:

        try:

            self.client = weaviate.connect_to_local(
                host="localhost",
                port=int(
                    settings.WEAVIATE_PORT
                ),
                grpc_port=int(
                    settings.WEAVIATE_GRPC_PORT
                ),
            )

            print(
                "[Weaviate] Berhasil terhubung "
                "ke Weaviate."
            )

            self._ensure_collection()

        except Exception as e:

            print(
                "[Weaviate Connection Error]",
                str(e),
            )

            self.client = None
            self.collection = None

    def _ensure_collection(self) -> None:

        if self.client is None:
            return

        try:

            exists = (
                self.client.collections.exists(
                    self.collection_name
                )
            )

            if not exists:

                print(
                    f"[Weaviate] Collection "
                    f"'{self.collection_name}' "
                    f"belum tersedia."
                )

                self.collection = None

                return

            self.collection = (
                self.client.collections.get(
                    self.collection_name
                )
            )

            print(
                f"[Weaviate] Collection "
                f"'{self.collection_name}' "
                f"sudah tersedia."
            )

        except Exception as e:

            print(
                "[Weaviate Collection Error]",
                str(e),
            )

            self.collection = None

    def _normalize_limit(
        self,
        limit: Optional[int],
    ) -> int:

        if limit is not None:

            normalized_limit = limit

        else:

            top_k = getattr(
                settings,
                "TOP_K",
                5,
            )

            if top_k is None:

                normalized_limit = 5

            else:

                normalized_limit = int(
                    top_k
                )

        if normalized_limit < 1:

            normalized_limit = 1

        if normalized_limit > 20:

            normalized_limit = 20

        return normalized_limit
    
    def add_document_chunk(
        self,
        content: str,
        embedding: List[float],
        meta_data: Dict[str, Any],
    ) -> bool:
        if self.client is None or self.collection is None:
            print("[Weaviate] Gagal menyimpan chunk: Client atau Collection tidak tersedia.")
            return False

        try:
            # Menggunakan batch dynamic untuk memasukkan single object secara aman
            with self.collection.batch.dynamic() as batch:
                batch.add_object(
                    properties={
                        "content": content,
                        **meta_data
                    },
                    vector=embedding
                )
            return True

        except Exception as e:
            print(f"[Weaviate Insert Error] Gagal menyimpan chunk: {str(e)}")
            return False

    def search_similar_chunks(
        self,
        query_embedding: List[float],
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:

        if not query_embedding:

            print(
                "[Weaviate] Query embedding kosong."
            )

            return []

        if self.client is None:

            print(
                "[Weaviate] Client tidak tersedia."
            )

            return []

        if self.collection is None:

            print(
                "[Weaviate] Collection tidak tersedia."
            )

            return []

        search_limit = (
            self._normalize_limit(
                limit
            )
        )

        try:

            response = (
                self.collection.query.near_vector(
                    near_vector=query_embedding,
                    limit=search_limit,
                )
            )

            objects = (
                response.objects
                if response
                else []
            )

            if not objects:

                print(
                    "[Weaviate] Tidak ditemukan "
                    "dokumen relevan."
                )

                return []

            results = []

            for obj in objects:

                properties = (
                    obj.properties
                    if obj.properties
                    else {}
                )

                content = (
                    properties.get(
                        "content",
                        "",
                    )
                )

                source_name = (
                    properties.get(
                        "source_name",
                        "Unknown Source",
                    )
                )

                if not content:

                    continue

                result = {

                    "content":
                        str(
                            content
                        ),

                    "source_name":
                        str(
                            source_name
                        ),

                }

                if (
                    hasattr(
                        obj,
                        "metadata",
                    )
                    and obj.metadata
                ):

                    distance = getattr(
                        obj.metadata,
                        "distance",
                        None,
                    )

                    if distance is not None:

                        result[
                            "distance"
                        ] = distance

                results.append(
                    result
                )

            return results

        except Exception as e:

            print(
                "[Weaviate Search Error]",
                str(e),
            )

            return []

    def close(self) -> None:

        if self.client is None:

            return

        try:

            self.client.close()

            print(
                "[Weaviate] Connection "
                "berhasil ditutup."
            )

        except Exception as e:

            print(
                "[Weaviate Close Error]",
                str(e),
            )

        finally:

            self.client = None
            self.collection = None