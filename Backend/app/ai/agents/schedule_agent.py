from __future__ import annotations

import httpx
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.config.settings import settings


class ScheduleAgent(BaseAgent):
    """
    ScheduleAgent bertanggung jawab untuk menyusun manajemen waktu, rute logistik harian,
    serta sinkronisasi jadwal agar efisien dan tidak tumpang tindih.
    """

    @property
    def name(self) -> str:
        return "Schedule Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "schedule.txt"

    def call_llm(self, prompt: str) -> str:
        payload = {
            "model": getattr(settings, "OLLAMA_MODEL", "llama3"),
            "prompt": prompt,
            "stream": False,
        }
        
        try:
            ollama_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
            response = httpx.post(ollama_url, json=payload, timeout=60.0)
            response.raise_for_status()
            return str(response.json().get("response", ""))
        except Exception as exc:
            raise RuntimeError(f"Gagal memanggil LLM pada {self.name}: {exc}") from exc

    def create_itinerary(self, days: int, destinations: list[str], query: str) -> str:
        """
        Menyusun rancangan alokasi waktu per hari.
        """
        calendar_status = ""
        if self.tools.exists("calendar"):
            calendar_status = self.execute_tool("calendar", action="get_availability")

        enhanced_query = (
            f"Jumlah Hari: {days} Hari\n"
            f"Daftar Tempat: {', '.join(destinations)}\n"
            f"Status Kalender: {calendar_status}\n"
            f"Detail Tambahan: {query}"
        )
        
        return self.run(question=enhanced_query)