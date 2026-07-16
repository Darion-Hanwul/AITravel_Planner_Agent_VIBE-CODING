from __future__ import annotations

from typing import Any

from app.ai.agents.base_agent import BaseAgent, LLMModelProtocol
from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry


class MemoryAgent(BaseAgent):
    """
    MemoryAgent bertanggung jawab menganalisis riwayat percakapan secara asinkron/sinkron
    untuk mengekstrak fakta-fakta implisit pengguna dan menyimpannya secara terpisah (Prinsip 1, 18).

    Responsibility
    --------------
    - Mengidentifikasi preferensi tersembunyi (e.g. alergi makanan, ketertarikan museum).
    - Memisahkan penyimpanan memori jangka panjang dari riwayat chat kasual.

    Tidak bertanggung jawab terhadap:
    - Menyimpan log obrolan mentah (tugas ChatRepository/Service).
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
        return "Memory Agent"

    @property
    def task_prompt_filename(self) -> str:
        """Menggunakan system template untuk panduan penarikan informasi."""
        return "system.txt"

    def extract_implicit_preferences(self, history: list[str]) -> str:
        """
        Mengekstrak poin preferensi krusial dari histori obrolan pengguna (Prinsip 18).

        Args:
            history: List baris teks rekaman obrolan pengguna dan asisten.

        Returns:
            str: JSON String atau poin-poin preferensi hasil ekstraksi yang bersih.
        """
        analysis_question = (
            "Tugas: Analisislah seluruh riwayat percakapan di bawah ini.\n"
            "Ekstrak fakta-fakta spesifik mengenai preferensi pengguna, batasan fisik, "
            "alergi, penghematan anggaran, penginapan favorit, dan gaya liburan mereka.\n"
            "Format Hasil: Hanya kembalikan poin-poin data tanpa kata pengantar basa-basi."
        )

        return self.run(question=analysis_question, history=history)