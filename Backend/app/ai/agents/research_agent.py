from __future__ import annotations

import httpx # Menggunakan HTTPX client untuk pemicu LLM lokal/cloud
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.config.settings import settings


class ResearchAgent(BaseAgent):
    """
    ResearchAgent bertanggung jawab melakukan pencarian informasi mendalam
    mengenai destinasi, akomodasi, atraksi, dan transportasi.
    """

    @property
    def name(self) -> str:
        return "Research Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "research.txt"

    def call_llm(self, prompt: str) -> str:
        """
        Implementasi pemanggilan LLM. Di sini diasumsikan menggunakan Ollama
        sesuai arsitektur backend lokal Anda, atau bisa disesuaikan dengan OpenAI.
        """
        # Contoh integrasi sederhana & bersih dengan API Ollama / OpenAI
        payload = {
            "model": settings.OLLAMA_MODEL if hasattr(settings, "OLLAMA_MODEL") else "llama3",
            "prompt": prompt,
            "stream": False,
        }
        
        try:
            # Hubungkan dengan host Ollama dari settings
            ollama_url = f"{settings.OLLAMA_BASE_URL}/api/generate"
            response = httpx.post(ollama_url, json=payload, timeout=60.0)
            response.raise_for_status()
            return str(response.json().get("response", ""))
        except Exception as exc:
            raise RuntimeError(f"Gagal memanggil LLM pada {self.name}: {exc}") from exc

    def execute_research_flow(self, destination: str, query: str) -> str:
        """
        Metode khusus agen untuk melakukan riset menggunakan tools yang tersedia.
        """
        # Contoh memanggil tool cuaca (weather_tool) yang terdaftar di registry
        weather_info = ""
        if self.tools.exists("weather"):
            weather_info = self.execute_tool("weather", location=destination)

        # Gabungkan hasil tool ke dalam query riset sebelum dikirim ke LLM
        enhanced_query = f"{query}\nInfo Tambahan Cuaca Terkini: {weather_info}"
        
        return self.run(question=enhanced_query)