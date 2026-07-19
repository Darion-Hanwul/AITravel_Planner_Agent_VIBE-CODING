"""
RAG Pipeline Service

Orchestrator utama yang menggabungkan proses Retrieval (pencarian dokumen di Weaviate)
dan Generation (pembuatan jawaban oleh Ollama LLM) menjadi satu kesatuan alur kerja.
"""

import httpx
from typing import Dict, Any, Optional
from app.config.settings import settings
from app.rag.retriever import InformationRetriever


class RagPipeline:
    def __init__(self) -> None:
        self.retriever = InformationRetriever()

    def _generate_rag_prompt(self, query: str, context: str) -> str:
        """
        Menyusun prompt terstruktur yang menggabungkan konteks dokumen ke dalam instruksi LLM.
        """
        if not context:
            # Fallback jika tidak ditemukan dokumen yang relevan
            return (
                f"Pertanyaan Pengguna: {query}\n\n"
                "Instruksi: Jawablah pertanyaan di atas dengan pengetahuan umum yang Anda miliki "
                "namun tetap berfokus pada topik perencanaan perjalanan (Travel Planner)."
            )

        return (
            "Anda adalah AI Travel Planner Agent yang cerdas dan detail. Anda bertugas membantu "
            "pengguna menyusun rencana perjalanan berdasarkan dokumen referensi yang mereka unggah.\n\n"
            "Gunakan Informasi Dokumen Referensi di bawah ini untuk menjawab pertanyaan pengguna dengan akurat. "
            "Jika jawaban tidak terdapat dalam dokumen tersebut, katakan dengan jujur bahwa informasi "
            "tidak ditemukan di dokumen Anda, namun berikan rekomendasi umum yang membantu.\n\n"
            f"--- MULAI DOKUMEN REFERENSI ---\n{context}\n--- AKHIR DOKUMEN REFERENSI ---\n\n"
            f"Pertanyaan Pengguna: {query}\n\n"
            "Jawaban Anda (berikan penjelasan yang rapi dan terstruktur):"
        )

    async def execute_rag(self, query: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Mengeksekusi alur RAG secara end-to-end:
        1. Mencari konteks terdekat berdasarkan kueri dari database Weaviate.
        2. Menyusun prompt gabungan yang kaya konteks.
        3. Menembak Ollama LLM untuk menghasilkan jawaban akhir.
        
        Args:
            query (str): Pertanyaan atau perintah dari pengguna.
            limit (Optional[int]): Batas jumlah chunk dokumen yang ditarik (Optional).
            
        Returns:
            Dict[str, Any]: Hasil response AI beserta teks konteks yang digunakan.
        """
        try:
            # 1. Mengambil konteks dokumen yang relevan dari retriever
            context = await self.retriever.retrieve_relevant_context(query, limit=limit)
            
            # 2. Menyusun template prompt kustom
            full_prompt = self._generate_rag_prompt(query, context)
            
            # 3. Kirim prompt yang sudah diperkaya ke Ollama Generate API
            url = f"{settings.OLLAMA_BASE_URL}/api/generate"
            payload = {
                "model": settings.OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False  # Kita set False agar response langsung diterima utuh
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                response_data = response.json()
                
                ai_response = response_data.get("response", "")
                
                return {
                    "status": "success",
                    "answer": ai_response,
                    "context_used": context if context else "Tidak ada dokumen relevan yang digunakan."
                }

        except Exception as e:
            return {
                "status": "error",
                "answer": f"Terjadi kesalahan pada sistem RAG Pipeline: {str(e)}",
                "context_used": ""
            }