import traceback
import re
from typing import Dict, Any, Optional, AsyncGenerator

from app.rag.retriever import InformationRetriever
from app.ai.services.ollama_service import OllamaService

SESSION_STORAGE: Dict[str, Dict[str, Any]] = {}

class RagPipeline:

    def __init__(self) -> None:
        self.retriever = InformationRetriever()
        self.ollama = OllamaService()

    def _detect_trip_duration(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower().strip()
        number_pattern = r"(\d+(?:[.,]\d+)?)"

        units = {
            r"\s*(hari|day|days)\b": (1, "hari"),
            r"\s*(minggu|week|weeks)\b": (7, "minggu"),
            r"\s*(bulan|month|months)\b": (30, "bulan"),
            r"\s*(tahun|year|years)\b": (365, "tahun")
        }

        for pattern, (multiplier, unit_name) in units.items():
            match = re.search(number_pattern + pattern, query_lower)
            if match:
                value = float(match.group(1).replace(",", "."))
                return {
                    "days": max(int(value * multiplier), 1),
                    "unit": unit_name,
                    "value": value,
                }
        return {"days": None, "unit": None, "value": None}

    def _get_dynamic_strategy(self, days: int) -> Dict[str, Any]:
        num_ctx = 16384 if days > 30 else 8192
        return {
            "num_predict": 6789,
            "retrieval_limit": 5 if days > 30 else 3,
            "num_ctx": num_ctx,
        }

    def _prepare_context(self, context: str, max_chars: int = 6000) -> str:
        if not context:
            return "Tidak ada dokumen referensi khusus yang ditemukan."
        if len(context) <= max_chars:
            return context
        return context[:max_chars] + "\n\n[Context dipotong untuk efisiensi.]"

    async def execute_rag_stream(
        self,
        query: str,
        session_id: str = "default_user",
        limit: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        try:
            query_lower = query.lower().strip()

            if session_id not in SESSION_STORAGE:
                duration = self._detect_trip_duration(query)
                days = duration["days"] if duration["days"] else 7
                SESSION_STORAGE[session_id] = {
                    "stage": "waiting_format" if duration["days"] and duration["days"] > 30 else "standard",
                    "total_days": days,
                    "current_day": 0,
                    "user_list": [],
                    "metadata_unit": duration["unit"] or "hari"
                }
            
            state = SESSION_STORAGE[session_id]
            strategy = self._get_dynamic_strategy(state["total_days"])
            
            # Ambil data RAG relevan
            raw_context = await self.retriever.retrieve_relevant_context(
                query=query,
                limit=limit if limit is not None else strategy["retrieval_limit"]
            )
            context = self._prepare_context(raw_context)
            
            if state["stage"] == "waiting_format":
                prompt = f"""
                User ingin merencanakan perjalanan selama {state['total_days']} hari.
                Tugas Anda adalah BERTANYA BALIK dengan sopan. JANGAN membuat itinerary dulu.
                Berikan opsi kepada user apakah ingin direncanakan secara Harian, Mingguan, Bulanan, atau Tahunan.
                Jelaskan aturan main Anda: Jika memilih tahunan/bulanan, rincian akan diberikan per blok 30 hari (Tahun ke-x, Bulan ke-y, Minggu ke-z, Hari 1-30). Setelah hari ke-30, sistem akan berhenti untuk meminta konfirmasi kelanjutan.
                Tanyakan juga apakah user memiliki daftar rencana/aktivitas khusus (list custom) yang ingin disisipkan.
                
                User input saat ini: "{query}"
                """
                state["stage"] = "waiting_confirmation"
                
            # Tahap B: User sudah milih format & mungkin ngasih list custom awal
            elif state["stage"] == "waiting_confirmation":
                if any(x in query_lower for x in ["list", "rencana saya", "-", "*"]):
                    state["user_list"].append(query)
                
                state["current_day"] = 1
                state["stage"] = "generating_blocks"
                
                prompt = f"""
                User telah memilih format perencanaan. Sekarang saatnya menghasilkan Blok Pertama (Hari {state['current_day']} sampai {state['current_day'] + 29}).
                
                Format Output Wajib:
                Tahun 1 -> Bulan 1 -> Minggu 1 -> Hari 1 (Aktivitas secara ringkas).
                ... teruskan sampai Hari 30.
                
                Gunakan Referensi Tempat dari RAG ini jika relevan: {context}
                Berikut adalah list titipan aktivitas dari user yang WAJIB dimasukkan: {state['user_list']}
                
                Di akhir jawaban, Anda WAJIB memotong penjelasan dan bertanya: "Apakah Anda ingin melanjutkan ke blok 30 hari berikutnya? Atau ada aktivitas tambahan yang ingin dimasukkan ke list Anda?"
                """
                state["current_day"] += 30

            elif state["stage"] == "generating_blocks" and ("lanjut" in query_lower or "next" in query_lower or state["current_day"] > 1):
                if any(x in query_lower for x in ["tambah", "-", "*"]):
                    state["user_list"].append(query)
                    
                if state["current_day"] > state["total_days"]:
                    prompt = f"Informasikan kepada user bahwa seluruh rencana perjalanan selama {state['total_days']} hari telah selesai dirancang sepenuhnya. Tanyakan apakah ada bagian yang ingin direvisi."
                    SESSION_STORAGE.pop(session_id, None) 
                else:
                    next_limit = min(state["current_day"] + 29, state["total_days"])
                    current_month = (state["current_day"] // 30) + 1
                    current_year = (state["current_day"] // 365) + 1
                    
                    prompt = f"""
                    Lanjutkan pembuatan itinerary untuk Blok Berikutnya: Hari {state['current_day']} sampai {next_limit}.
                    Saat ini berada pada perkiraan kronologis: Tahun {current_year}, Bulan {current_month}.
                    
                    Gunakan dokumen referensi ini: {context}
                    Gunakan list aktivitas tambahan jika ada: {state['user_list']}
                    
                    Tampilkan rincian hari demi hari dari Hari {state['current_day']} hingga {next_limit}.
                    Di akhir jawaban, potong teks Anda kembali dan tanyakan: "Blok hari ke-{next_limit} selesai. Apakah kita lanjut ke blok berikutnya atau ada rencana tambahan?"
                    """
                    state["current_day"] = next_limit + 1
            
            else:
                prompt = f"""
                Buatkan rencana perjalanan komplit untuk {state['total_days']} hari.
                Referensi RAG: {context}
                Pertanyaan User: {query}
                """
                SESSION_STORAGE.pop(session_id, None)

            async for chunk in self.ollama.generate_stream(
                prompt=prompt.strip(),
                num_predict=strategy["num_predict"],
                temperature=0.4,
                top_p=0.9,
                num_ctx=strategy["num_ctx"],
                keep_alive="30m",
                timeout=600.0,
            ):
                yield chunk

        except Exception as e:
            print("\n[RAG PIPELINE STREAM ERROR]")
            traceback.print_exc()
            yield f"\n\n[Sistem] Terjadi kesalahan pada RAG Pipeline Stream: {type(e).__name__}: {str(e)}"

    async def execute_rag(
        self,
        query: str,
        session_id: str = "default_user",
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        chunks = []
        try:
            async for chunk in self.execute_rag_stream(query=query, session_id=session_id, limit=limit):
                chunks.append(chunk)

            answer = "".join(chunks)
            
            # Ambil info sisa data state untuk dilempar ke metadata response API jika diperlukan
            state = SESSION_STORAGE.get(session_id, {"total_days": 7, "metadata_unit": "default"})
            strategy = self._get_dynamic_strategy(state["total_days"])

            return {
                "status": "success",
                "answer": answer,
                "context_used": "Context retrieval digunakan selama proses RAG bertahap.",
                "metadata": {
                    "trip_days": state["total_days"],
                    "trip_unit": state.get("metadata_unit", "hari"),
                    "num_predict": strategy["num_predict"],
                    "streaming": False,
                },
            }
        except Exception as e:
            print("[RAG] execute_rag error:", str(e))
            return {
                "status": "error",
                "answer": f"Terjadi kesalahan pada RAG Pipeline: {type(e).__name__}: {str(e)}",
                "context_used": "",
                "metadata": {},
            }