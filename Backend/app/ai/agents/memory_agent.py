from __future__ import annotations

import httpx
from app.ai.agents.base_agent import BaseAgent
from app.config.settings import settings


class MemoryAgent(BaseAgent):
    """
    MemoryAgent bertugas menganalisis interaksi chat untuk mengekstrak
    preferensi pengguna yang implisit (misal: 'Saya tidak suka seafood', 'Saya bepergian dengan bayi').
    """

    @property
    def name(self) -> str:
        return "Memory Agent"

    @property
    def task_prompt_filename(self) -> str:
        return "system.txt"  # Menggunakan system atau prompt khusus analisis memori jika ada

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

    def extract_user_preferences(self, conversation_history: list[str]) -> str:
        """
        Mengekstrak fakta-fakta kunci dari riwayat chat.
        """
        question = (
            "Analisislah percakapan di bawah ini dan ambil poin penting mengenai preferensi, "
            "hobi, alergi, atau kebiasaan travel pengguna dalam format poin-poin singkat."
        )
        return self.run(question=question, history=conversation_history)