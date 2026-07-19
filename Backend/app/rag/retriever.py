"""
RAG Retriever Service

Bertugas menerima query pencarian teks dari user, mengubahnya menjadi vektor 
via Ollama, dan mencari potongan dokumen paling relevan dari database Weaviate.
"""

import httpx
from typing import List, Dict, Any, Optional # Tambahkan Optional di sini
from app.config.settings import settings
from app.rag.vector_store import WeaviateVectorStore


class InformationRetriever:
    def __init__(self) -> None:
        self.vector_store = WeaviateVectorStore()

    async def _get_query_embedding(self, query: str) -> List[float]:
        """
        Mengubah teks kueri/pertanyaan user menjadi token embedding melalui Ollama.
        """
        url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"
        payload = {
            "model": settings.OLLAMA_EMBED_MODEL,
            "prompt": query
        }
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                response_data = response.json()
                return response_data.get("embedding", [])
        except Exception as e:
            print(f"[Retriever Embedding Error] Gagal generate embedding kueri: {str(e)}")
            return []

    # Perbaikan tipe data di parameter limit menggunakan Optional[int]
    async def retrieve_relevant_context(self, query: str, limit: Optional[int] = None) -> str:
        """
        Mengambil potongan dokumen terdekat dan menggabungkannya menjadi 
        satu string konteks utuh untuk disuntikkan ke prompt LLM.
        """
        search_limit = limit or settings.TOP_K
        
        # 1. Ubah query teks user menjadi vektor
        query_vector = await self._get_query_embedding(query)
        if not query_vector:
            return ""

        # 2. Cari chunk terdekat di Weaviate menggunakan custom vector tersebut
        chunks = self.vector_store.search_similar_chunks(
            query_embedding=query_vector,
            limit=search_limit
        )

        if not chunks:
            return ""

        # 3. Gabungkan seluruh potongan teks menjadi satu kesatuan narasi konteks
        context_blocks = []
        for idx, chunk in enumerate(chunks, 1):
            content = chunk.get("content", "")
            source = chunk.get("source_name", "Unknown Source")
            
            block = f"[Dokumen Referensi {idx} | Sumber: {source}]\n{content}"
            context_blocks.append(block)

        return "\n\n".join(context_blocks)