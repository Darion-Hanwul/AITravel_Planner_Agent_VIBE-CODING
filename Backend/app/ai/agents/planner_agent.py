from __future__ import annotations

import httpx
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.config.settings import settings


class PlannerAgent(BaseAgent):
    """
    PlannerAgent bertindak sebagai koordinator utama (Orchestrator).
    Bertanggung jawab mengonsolidasikan analisis dari Research, Budget, Schedule,
    dan Safety Agent menjadi satu draf rencana perjalanan yang utuh dan harmonis.
    """

    @property
    def name(self) -> str:
        return "Planner Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "planner.txt"

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

    def consolidate_plan(
        self,
        destination: str,
        research_data: str,
        budget_data: str,
        schedule_data: str,
        safety_data: str,
    ) -> str:
        """
        Mengompilasi semua laporan dari agen-agen spesifik menjadi satu rencana final.
        """
        consolidated_input = (
            f"--- LAPORAN RISET DESTINASI ({destination}) ---\n{research_data}\n\n"
            f"--- LAPORAN ANGGARAN & BIAYA ---\n{budget_data}\n\n"
            f"--- RANCANGAN JADWAL & ITINERARY ---\n{schedule_data}\n\n"
            f"--- EVALUASI KEAMANAN & REGULASI ---\n{safety_data}\n\n"
            "Tugas: Gabungkan, harmonisasikan, dan susun menjadi Travel Plan yang indah dan ramah dibaca."
        )
        
        return self.run(question=consolidated_input)