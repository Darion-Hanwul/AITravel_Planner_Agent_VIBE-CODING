from __future__ import annotations

import httpx
from typing import Any

from app.ai.agents.base_agent import BaseAgent
from app.config.settings import settings


class BudgetAgent(BaseAgent):
    """
    BudgetAgent bertanggung jawab melakukan kalkulasi estimasi biaya perjalanan,
    menyusun breakdown anggaran harian, serta konversi mata uang jika diperlukan.
    """

    @property
    def name(self) -> str:
        return "Budget Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "budget.txt"

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

    def calculate_budget(self, destination: str, preferences: dict[str, Any], query: str) -> str:
        """
        Menghitung estimasi biaya berdasarkan preferensi pengguna (misal: budget limit, hotel tier).
        """
        currency_info = ""
        if self.tools.exists("currency"):
            # Contoh pemanggilan currency tool jika ada
            currency_info = self.execute_tool("currency", destination=destination)

        enhanced_query = (
            f"Destinasi: {destination}\n"
            f"Preferensi Budget: {preferences.get('budget_tier', 'medium')}\n"
            f"Mata Uang Lokal: {currency_info}\n"
            f"Permintaan Detail: {query}"
        )
        
        return self.run(question=enhanced_query)