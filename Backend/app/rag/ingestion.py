"""
RAG Ingestion Service

Mengelola alur end-to-end masuknya dokumen baru: memuat file, memotong teks,
membuat vector embedding via Ollama API, dan menyimpannya ke Weaviate v4.
"""

import httpx
from pathlib import Path
from typing import Dict, Any, List

from app.config.settings import settings
from app.rag.loader import DocumentLoader
from app.rag.splitter import TextSplitter
from app.rag.vector_store import WeaviateVectorStore


class DataIngestionService:
    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.splitter = TextSplitter()
        self.vector_store = WeaviateVectorStore()

    async def _get_ollama_embedding(self, text: str) -> List[float]:
        """
        Menembak API lokal Ollama untuk mendapatkan vektor embedding dari teks chunk.
        """
        url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"
        payload = {
            "model": settings.OLLAMA_EMBED_MODEL,
            "prompt": text
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                response_data = response.json()
                return response_data.get("embedding", [])
        except Exception as e:
            print(f"[Ollama Embedding Error] Gagal mendapatkan embedding: {str(e)}")
            return []

    async def ingest_document(self, file_path_str: str, document_id: Any) -> Dict[str, Any]:
        """
        Memproses dokumen dari file fisik hingga masuk ke dalam database Weaviate.
        
        Args:
            file_path_str (str): Path lokasi file disimpan.
            document_id (Any): ID unik dokumen untuk relasi database SQL.
            
        Returns:
            Dict[str, Any]: Laporan status eksekusi ingestion.
        """
        file_path = Path(file_path_str)
        if not file_path.exists():
            return {"status": "error", "message": f"File tidak ditemukan di path: {file_path_str}"}

        try:
            # 1. Load teks mentah dokumen
            raw_text = self.loader.load_file(file_path_str)
            if not raw_text.strip():
                return {"status": "error", "message": "Dokumen kosong atau tidak mengandung teks."}

            # 2. Potong teks menjadi beberapa chunks
            chunks = self.splitter.split_text(raw_text)
            
            # Meta data untuk relasi pencarian nantinya
            meta_data = {
                "document_id": str(document_id),
                "source_name": file_path.name
            }

            successful_chunks = 0
            
            # 3. Looping untuk membuat embedding dan simpan ke Weaviate per chunk
            for chunk in chunks:
                if not chunk.strip():
                    continue
                    
                embedding = await self._get_ollama_embedding(chunk)
                
                # Jika embedding berhasil digenerate, masukkan ke Weaviate v4
                if embedding:
                    success = self.vector_store.add_document_chunk(
                        content=chunk,
                        embedding=embedding,
                        meta_data=meta_data
                    )
                    if success:
                        successful_chunks += 1

            return {
                "status": "success",
                "message": f"Ingestion berhasil. Memproses {successful_chunks} dari {len(chunks)} chunks.",
                "total_chunks": len(chunks),
                "inserted_chunks": successful_chunks
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Terjadi kegagalan sistem saat proses ingestion: {str(e)}"
            }