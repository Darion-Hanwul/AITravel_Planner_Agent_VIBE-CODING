from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class PlannerAgent(BaseAgent):
    """
    PlannerAgent bertindak sebagai koordinator utama (Orchestrator).
    Bertanggung jawab mengonsolidasikan analisis dari seluruh agen spesialis
    menjadi satu proposal rencana perjalanan yang padu, estetik, dan harmonis (Prinsip 1, 19).

    Responsibility
    --------------
    - Menggabungkan laporan riset, anggaran biaya, jadwal harian, dan berkas keselamatan.
    - Menyelaraskan informasi yang bertentangan (misal atraksi di luar anggaran atau di luar jam operasional).

    Tidak bertanggung jawab terhadap:
    - Melakukan pemanggilan database SQL secara langsung (Prinsip 2).
    - Melakukan crawling atau koneksi eksternal langsung (Prinsip 12).
    """

    def __init__(
        self,
        *,
        prompt_builder: PromptBuilder,
        llm_model: LLMModelProtocol,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        super().__init__(
            prompt_builder=prompt_builder,
            llm_model=llm_model,
            tool_registry=tool_registry,
        )

    @property
    def name(self) -> str:
        """Nama identifikasi agen."""
        return "Planner Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Nama file template prompt planner."""
        return "planner.txt"

    def orchestrate_itinerary(
        self,
        destination: str,
        research_report: str,
        budget_report: str,
        schedule_report: str,
        safety_report: str,
        documents: list[RetrievedDocument] | None = None,
    ) -> str:
        """
        Mengompilasi semua laporan agen menjadi rancangan akhir terintegrasi (Prinsip 19).

        Args:
            destination: Nama kota/negara tujuan utama liburan.
            research_report: Laporan teks komprehensif dari ResearchAgent.
            budget_report: Rancangan anggaran dari BudgetAgent.
            schedule_report: Itinerary harian terperinci dari ScheduleAgent.
            safety_report: Evaluasi visa & keamanan dari SafetyAgent.
            documents: Informasi tambahan pendukung (RAG).

        Returns:
            str: Dokumen Travel Plan final yang terstruktur indah dan ramah pengguna.
        """
        consolidated_facts = (
            f"PROYEK REKOMENDASI LIBURAN: {destination.upper()}\n\n"
            f"=== DATA AGENT 1: RISET TEMPAT ===\n{research_report}\n\n"
            f"=== DATA AGENT 2: RENCANA ANGGARAN ===\n{budget_report}\n\n"
            f"=== DATA AGENT 3: SUSUNAN JADWAL ===\n{schedule_report}\n\n"
            f"=== DATA AGENT 4: KEAMANAN & VISA ===\n{safety_report}\n\n"
            "TUGAS UTAMA:\n"
            "Gabungkan, harmonisasikan, dan eliminasi ketidaksesuaian data di atas "
            "menjadi satu naskah proposal panduan liburan resmi yang komprehensif, logis, "
            "dan memiliki tata letak visual (markdown) yang sangat rapi."
        )

        return self.run(question=consolidated_facts, documents=documents)