import time
import httpx

from typing import List, Optional

from app.config.settings import settings
from app.rag.vector_store import WeaviateVectorStore


class InformationRetriever:

    def __init__(self) -> None:

        self.vector_store = (
            WeaviateVectorStore()
        )

        self.embedding_url = (
            f"{settings.OLLAMA_BASE_URL}"
            "/api/embeddings"
        )

        self.embedding_model = (
            settings.OLLAMA_EMBED_MODEL
        )

        self.embedding_timeout = (
            httpx.Timeout(
                connect=10.0,
                read=60.0,
                write=30.0,
                pool=30.0,
            )
        )

        self.max_query_length = 2000

        self.max_retrieval_limit = 8

        self.max_context_chars = 12000

    async def _get_query_embedding(
        self,
        query: str,
    ) -> List[float]:

        query = (
            query
            .strip()
            .replace("\x00", "")
        )

        if not query:
            print(
                "[Retriever] Query kosong."
            )

            return []

        if len(query) > self.max_query_length:

            query = query[
                :self.max_query_length
            ]

            print(
                "[Retriever] Query dipotong "
                f"menjadi {self.max_query_length} karakter."
            )

        payload = {

            "model":
                self.embedding_model,

            "prompt":
                query,

            "keep_alive":
                "30m",

        }

        start_time = time.perf_counter()

        try:

            print(
                "[Retriever] Membuat query embedding..."
            )

            print(
                "[Retriever] Embedding Model:",
                self.embedding_model,
            )

            async with httpx.AsyncClient(
                timeout=self.embedding_timeout,
                limits=httpx.Limits(
                    max_connections=10,
                    max_keepalive_connections=5,
                    keepalive_expiry=30.0,
                ),
            ) as client:

                response = await client.post(
                    self.embedding_url,
                    json=payload,
                )

                response.raise_for_status()

                response_data = (
                    response.json()
                )

            embedding = (
                response_data.get(
                    "embedding",
                    [],
                )
            )

            if not embedding:

                print(
                    "[Retriever] Embedding kosong."
                )

                return []

            elapsed = (
                time.perf_counter()
                - start_time
            )

            print(
                "[Retriever] Embedding berhasil."
            )

            print(
                "[Retriever] Vector dimension:",
                len(embedding),
            )

            print(
                "[Retriever] Embedding time:",
                f"{elapsed:.2f}",
                "detik",
            )

            return embedding

        except httpx.TimeoutException as e:

            print(
                "[Retriever Embedding Timeout]"
            )

            print(
                "Error:",
                str(e),
            )

            return []

        except httpx.HTTPStatusError as e:

            print(
                "[Retriever Embedding HTTP Error]"
            )

            print(
                "Status:",
                e.response.status_code,
            )

            print(
                "Response:",
                e.response.text,
            )

            return []

        except httpx.ConnectError as e:

            print(
                "[Retriever Embedding Connection Error]"
            )

            print(
                "Tidak dapat terhubung ke Ollama."
            )

            print(
                "URL:",
                self.embedding_url,
            )

            print(
                "Error:",
                str(e),
            )

            return []

        except Exception as e:

            print(
                "[Retriever Embedding Error]"
            )

            print(
                "Error Type:",
                type(e).__name__,
            )

            print(
                "Error:",
                str(e),
            )

            return []

    def _normalize_limit(
        self,
        limit: Optional[int],
    ) -> int:

        if limit is None:
            normalized_limit = int(
                getattr(
                    settings,
                    "TOP_K",
                    5,
                )
            )
        else:
            normalized_limit = int(limit)

        if normalized_limit < 1:
            normalized_limit = 1

        return normalized_limit

    def _build_context(
        self,
        chunks: list,
    ) -> str:

        if not chunks:

            return ""

        context_blocks = []

        current_length = 0

        for idx, chunk in enumerate(
            chunks,
            1,
        ):

            content = (
                chunk.get(
                    "content",
                    "",
                )
                or ""
            )

            source = (
                chunk.get(
                    "source_name",
                    "Unknown Source",
                )
                or "Unknown Source"
            )

            content = content.strip()

            if not content:

                continue

            block = (
                f"[Dokumen Referensi {idx} "
                f"| Sumber: {source}]\n"
                f"{content}"
            )

            block_length = len(block)

            if (
                current_length
                + block_length
                > self.max_context_chars
            ):

                remaining = (
                    self.max_context_chars
                    - current_length
                )

                if remaining > 200:

                    block = block[
                        :remaining
                    ]

                    context_blocks.append(
                        block
                    )

                break

            context_blocks.append(
                block
            )

            current_length += (
                block_length
            )

        return "\n\n".join(
            context_blocks
        )

    async def retrieve_relevant_context(
        self,
        query: str,
        limit: Optional[int] = None,
    ) -> str:

        start_time = time.perf_counter()

        search_limit = (
            self._normalize_limit(
                limit
            )
        )

        print(
            "[Retriever] Search limit:",
            search_limit,
        )

        query_vector = (
            await self._get_query_embedding(
                query
            )
        )

        if not query_vector:

            print(
                "[Retriever] Retrieval "
                "dihentikan karena embedding kosong."
            )

            return ""

        try:

            print(
                "[Retriever] Mencari chunk "
                "relevan di Weaviate..."
            )

            chunks = (
                self.vector_store
                .search_similar_chunks(
                    query_embedding=query_vector,
                    limit=search_limit,
                )
            )

            if not chunks:

                print(
                    "[Retriever] Tidak ditemukan "
                    "chunk relevan."
                )

                return ""

            print(
                "[Retriever] Ditemukan",
                len(chunks),
                "chunk relevan.",
            )

            context = (
                self._build_context(
                    chunks
                )
            )

            elapsed = (
                time.perf_counter()
                - start_time
            )

            print(
                "[Retriever] Context length:",
                len(context),
            )

            print(
                "[Retriever] Total retrieval time:",
                f"{elapsed:.2f}",
                "detik",
            )

            return context

        except Exception as e:

            print(
                "[Retriever Vector Search Error]"
            )

            print(
                "Error Type:",
                type(e).__name__,
            )

            print(
                "Error:",
                str(e),
            )

            return ""