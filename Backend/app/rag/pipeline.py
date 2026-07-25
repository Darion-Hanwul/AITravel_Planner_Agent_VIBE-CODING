import traceback
import re

from typing import Dict, Any, Optional, AsyncGenerator

from app.rag.retriever import InformationRetriever
from app.ai.services.ollama_service import OllamaService


class RagPipeline:

    def __init__(self) -> None:
        self.retriever = InformationRetriever()
        self.ollama = OllamaService()

    # ==========================================================
    # 1. DETEKSI DURASI
    # ==========================================================

    def _detect_trip_duration(
        self,
        query: str,
    ) -> Dict[str, Any]:

        query_lower = query.lower().strip()

        number_pattern = r"(\d+(?:[.,]\d+)?)"

        # HARI
        match = re.search(
            number_pattern + r"\s*(hari|day|days)\b",
            query_lower,
        )

        if match:
            value = float(
                match.group(1).replace(",", ".")
            )

            return {
                "days": max(int(value), 1),
                "unit": "hari",
                "value": value,
            }

        # MINGGU
        match = re.search(
            number_pattern + r"\s*(minggu|week|weeks)\b",
            query_lower,
        )

        if match:
            value = float(
                match.group(1).replace(",", ".")
            )

            return {
                "days": max(int(value * 7), 1),
                "unit": "minggu",
                "value": value,
            }

        # BULAN
        match = re.search(
            number_pattern + r"\s*(bulan|month|months)\b",
            query_lower,
        )

        if match:
            value = float(
                match.group(1).replace(",", ".")
            )

            return {
                "days": max(int(value * 30), 1),
                "unit": "bulan",
                "value": value,
            }

        # TAHUN
        match = re.search(
            number_pattern + r"\s*(tahun|year|years)\b",
            query_lower,
        )

        if match:
            value = float(
                match.group(1).replace(",", ".")
            )

            return {
                "days": max(int(value * 365), 1),
                "unit": "tahun",
                "value": value,
            }

        # DEFAULT
        return {
            "days": 7,
            "unit": "default",
            "value": 7,
        }

    # ==========================================================
    # 2. ADAPTIVE STRATEGY
    # ==========================================================

    def _get_adaptive_strategy(
        self,
        days: int,
    ) -> Dict[str, Any]:

        # 1 - 3 HARI

        if days <= 3:
            return {
                "type": "short_trip",
                "label": "Perjalanan Pendek",
                "planning_unit": "hari",
                "num_predict": 256,
                "retrieval_limit": 3,
                "num_ctx": 2048,
                "instruction": (
                    "Buat itinerary detail untuk setiap hari. "
                    "Gunakan struktur Pagi, Siang, Sore, dan Malam. "
                    "Jaga jawaban tetap ringkas."
                ),
            }

        # 4 - 14 HARI

        if days <= 14:
            return {
                "type": "medium_trip",
                "label": "Perjalanan Menengah",
                "planning_unit": "hari",
                "num_predict": 512,
                "retrieval_limit": 4,
                "num_ctx": 2048,
                "instruction": (
                    "Buat itinerary setiap hari secara ringkas. "
                    "Untuk setiap hari tampilkan destinasi utama, "
                    "aktivitas utama, dan area menginap. "
                    "Hindari penjelasan panjang."
                ),
            }

        # 15 - 30 HARI

        if days <= 30:
            return {
                "type": "long_trip",
                "label": "Perjalanan Panjang",
                "planning_unit": "minggu",
                "num_predict": 640,
                "retrieval_limit": 4,
                "num_ctx": 2048,
                "instruction": (
                    "Gunakan hierarchical planning. "
                    "Bagi perjalanan menjadi beberapa minggu. "
                    "Untuk setiap minggu tampilkan wilayah, "
                    "destinasi utama, aktivitas utama, "
                    "dan estimasi durasi. "
                    "Jangan membuat itinerary harian."
                ),
            }

        # 31 - 90 HARI

        if days <= 90:
            return {
                "type": "extended_trip",
                "label": "Perjalanan Extended",
                "planning_unit": "minggu dan wilayah",
                "num_predict": 768,
                "retrieval_limit": 4,
                "num_ctx": 2048,
                "instruction": (
                    "Gunakan hierarchical travel planning. "
                    "Bagi perjalanan berdasarkan minggu dan wilayah geografis. "
                    "Untuk setiap fase tampilkan wilayah, "
                    "destinasi utama, aktivitas utama, "
                    "estimasi lama tinggal, dan transportasi. "
                    "Jangan membuat itinerary harian."
                ),
            }

        # 91 - 365 HARI

        if days <= 365:
            return {
                "type": "year_trip",
                "label": "Perjalanan Jangka Panjang",
                "planning_unit": "bulan dan fase",
                "num_predict": 896,
                "retrieval_limit": 5,
                "num_ctx": 2048,
                "instruction": (
                    "Gunakan hierarchical planning. "
                    "Jangan membuat itinerary harian. "
                    "Bagi perjalanan berdasarkan bulan atau fase geografis. "
                    "Untuk setiap fase tampilkan wilayah, "
                    "negara atau kota prioritas, destinasi utama, "
                    "musim terbaik, estimasi durasi, "
                    "dan strategi transportasi. "
                    "Fokus pada blueprint perjalanan."
                ),
            }

        # > 1 TAHUN

        return {
            "type": "strategic_multi_year",
            "label": "Strategic Multi-Year Travel Plan",
            "planning_unit": "tahun dan fase geografis",
            "num_predict": 768,
            "retrieval_limit": 5,
            "num_ctx": 2048,
            "instruction": (
                "Gunakan strategic hierarchical planning. "
                "Jangan membuat itinerary harian. "
                "Jangan membuat itinerary mingguan. "
                "Jangan mencoba menjelaskan seluruh perjalanan secara detail. "

                "Bagi perjalanan berdasarkan tahun dan fase geografis. "

                "Untuk setiap fase tampilkan secara ringkas: "
                "kawasan utama, negara prioritas, destinasi utama, "
                "musim terbaik, estimasi durasi, "
                "dan strategi transportasi. "

                "Buat blueprint strategis yang realistis. "
                "Prioritaskan struktur dan keputusan perjalanan "
                "daripada deskripsi panjang."
            ),
        }

    # ==========================================================
    # 3. BATASI CONTEXT
    # ==========================================================

    def _prepare_context(
        self,
        context: str,
        max_chars: int = 6000,
    ) -> str:

        if not context:
            return (
                "Tidak ada dokumen referensi khusus "
                "yang ditemukan."
            )

        if len(context) <= max_chars:
            return context

        return (
            context[:max_chars]
            + "\n\n"
            "[Context dipotong untuk efisiensi.]"
        )

    # ==========================================================
    # 4. GENERATE PROMPT
    # ==========================================================

    def _generate_rag_prompt(
        self,
        query: str,
        context: str,
        duration: Dict[str, Any],
        strategy: Dict[str, Any],
    ) -> str:

        days = duration["days"]

        context = self._prepare_context(
            context
        )

        return f"""
Anda adalah AI Travel Planner Agent.

Tugas Anda adalah membuat rencana perjalanan
yang realistis, terstruktur, dan ringkas.

DURASI PERJALANAN
-----------------
{days} hari

STRATEGI
--------
{strategy["label"]}

UNIT PLANNING
-------------
{strategy["planning_unit"]}

INSTRUKSI UTAMA
---------------
{strategy["instruction"]}

ATURAN
------
- Gunakan bahasa Indonesia.
- Prioritaskan informasi paling penting.
- Jangan membuat jawaban berlebihan.
- Kelompokkan destinasi berdasarkan lokasi geografis.
- Hindari perpindahan yang tidak efisien.
- Jangan mengarang isi dokumen referensi.
- Jika dokumen referensi tidak cukup, gunakan pengetahuan umum.
- Untuk perjalanan panjang, prioritaskan blueprint.
- Untuk perjalanan multi-tahun, prioritaskan strategi dan fase.

DOKUMEN REFERENSI
-----------------
{context}

PERTANYAAN USER
---------------
{query}

JAWABAN:
""".strip()

    # ==========================================================
    # 5. STREAMING RAG
    # ==========================================================

    async def execute_rag_stream(
        self,
        query: str,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:

        duration: Optional[Dict[str, Any]] = None
        strategy: Optional[Dict[str, Any]] = None

        try:

            # --------------------------------------------------
            # STEP 1: DURASI
            # --------------------------------------------------

            duration = self._detect_trip_duration(
                query
            )

            days = duration["days"]

            print(
                f"\n[RAG] Trip Duration: {days} hari"
            )

            # --------------------------------------------------
            # STEP 2: STRATEGY
            # --------------------------------------------------

            strategy = self._get_adaptive_strategy(
                days
            )

            print(
                f"[RAG] Strategy: {strategy['type']}"
            )

            print(
                f"[RAG] Planning Unit: "
                f"{strategy['planning_unit']}"
            )

            print(
                f"[RAG] Num Predict: "
                f"{strategy['num_predict']}"
            )

            # --------------------------------------------------
            # STEP 3: RETRIEVAL LIMIT
            # --------------------------------------------------

            retrieval_limit = (
                limit
                if limit is not None
                else strategy["retrieval_limit"]
            )

            print(
                f"[RAG] Retrieval Limit: "
                f"{retrieval_limit}"
            )

            # --------------------------------------------------
            # STEP 4: RETRIEVAL
            # --------------------------------------------------

            print(
                "\n[RAG] Memulai retrieval..."
            )

            context = await (
                self.retriever
                .retrieve_relevant_context(
                    query=query,
                    limit=retrieval_limit,
                )
            )

            print(
                "[RAG] Retrieval berhasil."
            )

            print(
                f"[RAG] Context length: "
                f"{len(context) if context else 0}"
            )

            # --------------------------------------------------
            # STEP 5: PROMPT
            # --------------------------------------------------

            prompt = self._generate_rag_prompt(
                query=query,
                context=context,
                duration=duration,
                strategy=strategy,
            )

            print(
                f"[RAG] Prompt length: "
                f"{len(prompt)}"
            )

            # --------------------------------------------------
            # STEP 6: OLLAMA STREAMING
            # --------------------------------------------------

            print(
                "\n[RAG] Memulai Ollama streaming..."
            )

            async for chunk in (
                self.ollama.generate_stream(
                    prompt=prompt,
                    num_predict=strategy[
                        "num_predict"
                    ],
                    temperature=0.4,
                    top_p=0.9,
                    num_ctx=strategy[
                        "num_ctx"
                    ],
                    keep_alive="30m",
                    timeout=600.0,
                )
            ):

                yield chunk

            print(
                "\n[RAG] Generation selesai."
            )

        except Exception as e:

            print(
                "\n[RAG PIPELINE ERROR]"
            )

            print(
                f"Error Type: {type(e).__name__}"
            )

            print(
                f"Error Detail: {str(e)}"
            )

            traceback.print_exc()

            yield (
                "\n\n"
                "[Sistem] Terjadi kesalahan pada "
                "RAG Pipeline: "
                f"{type(e).__name__}: {str(e)}"
            )

    # ==========================================================
    # 6. NON-STREAMING COMPATIBILITY
    # ==========================================================

    async def execute_rag(
        self,
        query: str,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:

        chunks = []

        try:

            async for chunk in (
                self.execute_rag_stream(
                    query=query,
                    limit=limit,
                )
            ):
                chunks.append(chunk)

            answer = "".join(
                chunks
            )

            duration = (
                self._detect_trip_duration(
                    query
                )
            )

            strategy = (
                self._get_adaptive_strategy(
                    duration["days"]
                )
            )

            return {
                "status": "success",
                "answer": answer,
                "context_used": (
                    "Context retrieval digunakan "
                    "selama proses RAG."
                ),
                "metadata": {
                    "trip_days": duration[
                        "days"
                    ],
                    "trip_unit": duration[
                        "unit"
                    ],
                    "strategy": strategy[
                        "type"
                    ],
                    "planning_unit": strategy[
                        "planning_unit"
                    ],
                    "num_predict": strategy[
                        "num_predict"
                    ],
                    "streaming": True,
                },
            }

        except Exception as e:

            print(
                "[RAG] execute_rag error:",
                str(e),
            )

            return {
                "status": "error",
                "answer": (
                    "Terjadi kesalahan pada "
                    "RAG Pipeline: "
                    f"{type(e).__name__}: "
                    f"{str(e)}"
                ),
                "context_used": "",
                "metadata": {},
            }