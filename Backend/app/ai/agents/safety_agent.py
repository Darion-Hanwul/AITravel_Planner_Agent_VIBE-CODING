from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class SafetyAgent(BaseAgent):
    """
    SafetyAgent bertanggung jawab melakukan analisis risiko, travel advisory,
    kebijakan visa, larangan adat istiadat setempat, serta keamanan destinasi (Prinsip 1).

    Responsibility
    --------------
    - Memberikan info visa, asuransi wajib, dan vaksinasi yang dibutuhkan.
    - Menganalisis potensi bencana alam lokal atau isu keamanan regional terkini.

    Tidak bertanggung jawab terhadap:
    - Memilih hotel atau restoran terbaik (tugas ResearchAgent).
    - Memotong anggaran biaya belanja (tugas BudgetAgent).
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
        return "Safety Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Nama file template prompt safety."""
        return "safety.txt"

    def evaluate_safety(
        self,
        destination: str,
        user_nationality: str,
        documents: list[RetrievedDocument] | None = None,
    ) -> str:
        """
        Mengevaluasi tingkat keamanan dan kepatuhan hukum legalitas di negara tujuan.

        Args:
            destination: Nama negara/kota tujuan.
            user_nationality: Kebangsaan paspor milik pengguna (untuk validasi visa).
            documents: Regulasi visa terbaru, berita travel advisory (RAG).

        Returns:
            str: Laporan analisis keamanan, regulasi hukum, dan visa dari LLM.
        """
        visa_rules: str = "Informasi aturan visa otomatis tidak tersedia."
        
        if self.tools.exists("visa_tool"):
            visa_res = self.execute_tool(
                "visa_tool", 
                destination=destination, 
                nationality=user_nationality
            )
            visa_rules = str(visa_res)

        formatted_question = (
            f"Analisis regulasi dan keamanan perjalanan ke {destination}.\n"
            f"Kebangsaan Pengguna (Paspor): {user_nationality}\n"
            f"Aturan Visa Dasar: {visa_rules}\n"
            "Tugas: Susun rekomendasi keamanan penting dan panduan kepatuhan budaya lokal."
        )

        return self.run(question=formatted_question, documents=documents)