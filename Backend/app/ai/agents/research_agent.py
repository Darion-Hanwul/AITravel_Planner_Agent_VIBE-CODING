from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class ResearchAgent(BaseAgent):
    """
    ResearchAgent bertanggung jawab melakukan pencarian informasi mendalam
    mengenai destinasi, akomodasi, atraksi, dan transportasi (Prinsip 1).

    Responsibility
    --------------
    - Mengumpulkan data dasar destinasi wisata dari tools maupun dokumen.
    - Menyusun analisis awal mengenai objek wisata yang relevan bagi user.

    Tidak bertanggung jawab terhadap:
    - Kalkulasi anggaran belanja (tugas BudgetAgent).
    - Penyusunan kalender detail (tugas ScheduleAgent).
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
        return "Research Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Nama file template prompt riset."""
        return "research.txt"

    def research_destination(
        self, 
        destination: str, 
        query: str,
        documents: list[RetrievedDocument] | None = None,
    ) -> str:
        """
        Melakukan riset terhadap destinasi tertentu dengan memanfaatkan tools yang tersedia (Prinsip 16).

        Args:
            destination: Nama kota atau negara tujuan riset.
            query: Detail pertanyaan spesifik dari user.
            documents: Dokumen pendukung hasil semantic search (RAG).

        Returns:
            str: Ringkasan hasil riset komprehensif dari LLM.
        """
        weather_info: str = "Informasi cuaca tidak tersedia."
        
        if self.tools.exists("weather_tool"):
            # Isolasi pemanggilan Tool (Prinsip 12)
            weather_res = self.execute_tool("weather_tool", location=destination)
            weather_info = str(weather_res)

        # Menyusun formulasi pertanyaan yang kaya konteks tanpa merusak prompt dasar
        enhanced_question = (
            f"Lakukan riset mendalam untuk destinasi: {destination}.\n"
            f"Kondisi Cuaca Saat Ini: {weather_info}\n"
            f"Kebutuhan Khusus Pengguna: {query}"
        )

        return self.run(question=enhanced_question, documents=documents)