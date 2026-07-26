from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class ScheduleAgent(BaseAgent):

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
        return "Schedule Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Nama file template prompt schedule."""
        return "schedule.txt"

    def build_schedule(
        self,
        destination: str,
        duration_days: int,
        activities: list[str],
        documents: list[RetrievedDocument] | None = None,
    ) -> str:
        """
        Args:
            destination: Nama lokasi tujuan.
            duration_days: Durasi liburan dalam hitungan hari.
            activities: Daftar mentah tempat/atraksi yang ingin dikunjungi.
            documents: Konteks jam operasional atau jarak tempuh lokasi (RAG).

        Returns:
            str: Susunan jadwal harian mendetail dari LLM.
        """
        calendar_status: str = "Sinkronisasi kalender tidak aktif."
        
        if self.tools.exists("calendar_tool"):
            calendar_res = self.execute_tool("calendar_tool", destination=destination)
            calendar_status = str(calendar_res)

        formatted_question = (
            f"Buatkan itinerary terstruktur harian di {destination} selama {duration_days} hari.\n"
            f"Daftar Atraksi Target: {', '.join(activities)}\n"
            f"Status Kalender Pengguna: {calendar_status}"
        )

        return self.run(question=formatted_question, documents=documents)