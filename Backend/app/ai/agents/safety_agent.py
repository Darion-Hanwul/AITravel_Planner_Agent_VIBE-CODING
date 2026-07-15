from __future__ import annotations

import httpx
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.config.settings import settings


class SafetyAgent(BaseAgent):
    """
    SafetyAgent bertanggung jawab menganalisis risiko perjalanan, imbauan keamanan,
    kondisi cuaca ekstrem, regulasi visa, serta aturan lokal yang sensitif.
    """

    @property
    def name(self) -> str:
        return "Safety Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "safety.txt"

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

    def assess_safety(self, destination: str, travel_dates: str) -> str:
        """
        Melakukan asesmen keselamatan perjalanan untuk destinasi tertentu.
        """
        weather_alert = ""
        if self.tools.exists("weather"):
            weather_alert = self.execute_tool("weather", location=destination, type="forecast")

        enhanced_query = (
            f"Destinasi Analisis: {destination}\n"
            f"Tanggal Perjalanan: {travel_dates}\n"
            f"Kondisi Cuaca Terkini: {weather_alert}\n"
            f"Tugas: Berikan analisis visa, regulasi, dan keamanan setempat."
        )
        
        return self.run(question=enhanced_query)