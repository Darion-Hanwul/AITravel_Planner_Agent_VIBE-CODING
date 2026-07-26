from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class BudgetAgent(BaseAgent):
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
        return "Budget Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Nama file template prompt budget."""
        return "budget.txt"

    def analyze_budget(
        self,
        destination: str,
        budget_tier: str,
        duration_days: int,
        query: str,
        documents: list[RetrievedDocument] | None = None,
    ) -> str:
        """
        Args:
            destination: Nama lokasi tujuan.
            budget_tier: Kategori budget (e.g., 'backpacker', 'moderate', 'luxury').
            duration_days: Durasi total perjalanan dalam hari.
            query: Informasi tambahan atau batasan biaya dari user.
            documents: Dokumen referensi harga lokal (RAG).

        Returns:
            str: Rincian anggaran biaya terstruktur dari LLM.
        """
        currency_rate: str = "Informasi mata uang lokal tidak tersedia."
        
        if self.tools.exists("currency_tool"):
            currency_res = self.execute_tool("currency_tool", destination=destination)
            currency_rate = str(currency_res)

        formatted_question = (
            f"Susun rancangan biaya untuk destinasi: {destination}.\n"
            f"Kategori Anggaran: {budget_tier}\n"
            f"Durasi Perjalanan: {duration_days} Hari\n"
            f"Informasi Mata Uang & Kurs: {currency_rate}\n"
            f"Catatan Anggaran Tambahan: {query}"
        )

        return self.run(question=formatted_question, documents=documents)