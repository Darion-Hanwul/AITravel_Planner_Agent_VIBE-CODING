from __future__ import annotations

import logging
import re
from typing import Literal

from app.config.settings import settings

logger = logging.getLogger("app.ai.graph.router")


class QueryRouter:
    """
    Responsibility
    --------------
    - Menganalisis query pengguna menggunakan metode deterministik (Regex & Keywords).
    - Mengarahkan aliran eksekusi ke rute "planning_workflow" (Multi-Agent) atau "casual_chat" (Direct).
    - Memastikan query yang tidak relevan dengan travel tidak memicu LLM secara berlebihan.

    Tidak bertanggung jawab terhadap:
    - Melakukan pemanggilan LLM untuk klasifikasi (Prinsip 14 - Guardrails must be deterministic).
    - Menyusun rencana perjalanan (tugas PlannerAgent).
    """

    def __init__(self) -> None:
        # Load keywords dari konfigurasi atau gunakan default jika belum ada di settings.py (Prinsip 4)
        self._planning_keywords: list[str] = getattr(
            settings, 
            "PLANNING_KEYWORDS", 
            [
                "plan", "itinerary", "perjalanan", "liburan", "jadwal", "budget", 
                "wisata", "travel", "vacation", "trip", "rute", "rekomendasi destinasi"
            ]
        )
        
        # Compile regex pattern secara pra-eksekusi untuk efisiensi performa (Prinsip 24)
        # Mencari pola tanggal (e.g., 12-15 Nov, 3 hari, 5 days, dd/mm/yyyy)
        self._duration_pattern = re.compile(
            r"(\b\d+\s*(hari|day|days|malam|night|nights)\b)|(\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b)"
        )

    def _contains_planning_keywords(self, query: str) -> bool:
        """
        Memeriksa apakah query mengandung kata kunci yang merujuk pada perencanaan perjalanan.
        """
        lowered_query = query.lower()
        return any(keyword in lowered_query for keyword in self._planning_keywords)

    def _contains_temporal_indicators(self, query: str) -> bool:
        """
        Memeriksa apakah query mengandung durasi waktu atau indikator tanggal perjalanan.
        """
        return bool(self._duration_pattern.search(query.lower()))

    def route_query(self, query: str) -> Literal["planning_workflow", "casual_chat"]:
        """
        Menentukan rute eksekusi berdasarkan analisis deterministik dari query pengguna (Prinsip 14).

        Args:
            query: Teks pertanyaan atau instruksi mentah dari pengguna.

        Returns:
            Literal["planning_workflow", "casual_chat"]: Target rute berikutnya.
        """
        logger.info(f"[QueryRouter] Mengevaluasi query: '{query[:50]}...'")

        if not query.strip():
            logger.warning("[QueryRouter] Query kosong, diarahkan ke casual_chat.")
            return "casual_chat"

        # 1. Cek kecocokan kata kunci perencanaan (Murah & Cepat - Prinsip 24)
        has_keywords = self._contains_planning_keywords(query)
        
        # 2. Cek kecocokan indikator temporal/durasi (Prinsip 24)
        has_temporal = self._contains_temporal_indicators(query)

        # 3. Logika penentuan rute yang deterministik
        if has_keywords or has_temporal:
            logger.info("[QueryRouter] Query terdeteksi sebagai 'Planning Request'. Mengarahkan ke Multi-Agent Graph.")
            return "planning_workflow"

        logger.info("[QueryRouter] Query terdeteksi sebagai 'Casual Chat'. Mengarahkan ke Direct Response.")
        return "casual_chat"