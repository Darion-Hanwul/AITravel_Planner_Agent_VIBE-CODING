from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument


class BaseAgent(ABC):
    """
    Abstract Base Class untuk seluruh AI Agent di dalam sistem.

    Responsibility
    --------------
    - Mengelola instansiasi PromptBuilder dan ToolRegistry.
    - Menyediakan antarmuka standar untuk eksekusi tugas agen (solve/run).
    - Menangani alur penyiapan prompt secara otomatis.

    Tidak bertanggung jawab terhadap:
    - Logika spesifik masing-masing domain agen (budget, planning, etc.).
    - Alur routing graf (LangGraph).
    """

    def __init__(
        self,
        *,
        prompt_builder: PromptBuilder,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.tools = tool_registry or ToolRegistry()

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nama unik identifikasi agen.
        """
        pass

    @property
    @abstractmethod
    def task_prompt_filename(self) -> str:
        """
        Nama file prompt spesifik agen di folder prompts/ (e.g., 'budget.txt').
        """
        pass

    @abstractmethod
    def call_llm(self, prompt: str) -> str:
        """
        Metode abstrak untuk memanggil LLM yang digunakan proyek Anda.
        Harus diimplementasikan berdasarkan LLM Wrapper yang dipakai (misal Ollama/OpenAI).
        """
        pass

    def _prepare_prompt(
        self,
        question: str,
        documents: list[RetrievedDocument] | None = None,
        history: list[str] | None = None,
    ) -> str:
        """
        Menyusun prompt lengkap menggunakan PromptBuilder.
        """
        system_prompt = self.prompt_builder.system_prompt()
        task_prompt = self.prompt_builder._load_prompt(self.task_prompt_filename)

        return self.prompt_builder.build(
            system_prompt=system_prompt,
            task_prompt=task_prompt,
            question=question,
            documents=documents,
            history=history,
        )

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """
        Helper untuk mengeksekusi tool yang terdaftar di agen ini.
        """
        return self.tools.execute(tool_name, **kwargs)

    def run(
        self,
        question: str,
        documents: list[RetrievedDocument] | None = None,
        history: list[str] | None = None,
    ) -> str:
        """
        Alur eksekusi utama agen (Sync).
        """
        compiled_prompt = self._prepare_prompt(
            question=question,
            documents=documents,
            history=history,
        )
        return self.call_llm(compiled_prompt)