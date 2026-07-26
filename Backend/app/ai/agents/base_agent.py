from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Protocol

from app.ai.prompt_builder import PromptBuilder
from app.ai.tools.tool_registry import ToolRegistry
from app.ai.models.retrieved_document import RetrievedDocument

logger = logging.getLogger("app.ai.agents")
class LLMModelProtocol(Protocol):
    """
    Protocol untuk wrapper LLM guna memastikan decoupling total 
    antara Agent dan HTTP Client (Prinsip 11, 12).
    """
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Mengirimkan prompt ke LLM dan mengembalikan teks respons.
        """
        ...


class BaseAgent(ABC):

    def __init__(
        self,
        *,
        prompt_builder: PromptBuilder,
        llm_model: LLMModelProtocol,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        """
        Inisialisasi BaseAgent.

        Args:
            prompt_builder: Instance pembangun prompt terpusat.
            llm_model: Wrapper model LLM yang patuh terhadap LLMModelProtocol.
            tool_registry: Registry untuk alat bantu eksternal agen.
        """
        self.prompt_builder = prompt_builder
        self.llm_model = llm_model
        self.tools = tool_registry or ToolRegistry()

        self._cached_task_prompt: str | None = None

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

    def _get_task_prompt(self) -> str:
        """
        Mengambil isi file prompt dengan memanfaatkan cache internal.
        """
        if self._cached_task_prompt is None:
            logger.debug(f"[{self.name}] Membaca file template prompt '{self.task_prompt_filename}' dari disk.")
            self._cached_task_prompt = self.prompt_builder._load_prompt(self.task_prompt_filename)
        return self._cached_task_prompt

    def _prepare_prompt(
        self,
        question: str,
        documents: list[RetrievedDocument] | None = None,
        history: list[str] | None = None,
    ) -> str:
        """
        Args:
            question: Pertanyaan atau instruksi user terkini.
            documents: Dokumen konteks hasil retrieval (jika ada).
            history: Catatan riwayat percakapan sebelumnya (jika ada).

        Returns:
            str: Prompt akhir yang siap dikirimkan ke LLM.
        """
        system_prompt = self.prompt_builder.system_prompt()
        task_prompt = self._get_task_prompt()

        return self.prompt_builder.build(
            system_prompt=system_prompt,
            task_prompt=task_prompt,
            question=question,
            documents=documents,
            history=history,
        )

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """
        Args:
            tool_name: Nama tool yang ingin dieksekusi.
            **kwargs: Parameter dinamis untuk kebutuhan eksekusi tool.

        Returns:
            Any: Hasil kembalian dari tool atau pesan kegagalan yang terkendali.
        """
        try:
            logger.info(f"[{self.name}] Mengeksekusi tool '{tool_name}' dengan argumen: {kwargs}")
            return self.tools.execute(tool_name, **kwargs)
        except Exception as exc:
            # Fail Gracefully & Log detailed trace (Prinsip 8 & 10)
            logger.exception(f"[{self.name}] Kegagalan eksekusi tool '{tool_name}'.")
            return f"Tool '{tool_name}' is temporarily unavailable. Error: {str(exc)}"

    def run(
        self,
        question: str,
        documents: list[RetrievedDocument] | None = None,
        history: list[str] | None = None,
    ) -> str:
        """
        Args:
            question: Pertanyaan atau instruksi user.
            documents: Konteks dokumen RAG.
            history: Catatan riwayat percakapan.

        Returns:
            str: Respons tekstual final dari LLM.
        """
        compiled_prompt = self._prepare_prompt(
            question=question,
            documents=documents,
            history=history,
        )
        
        try:
            logger.info(f"[{self.name}] Mengirimkan prompt reasoning ke LLM.")
            return self.llm_model.generate(compiled_prompt)
        except Exception as exc:
            logger.exception(f"[{self.name}] Kegagalan fatal saat menghubungi LLM.")
            return (
                f"Asisten [{self.name}] mengalami kendala saat memproses permintaan Anda. "
                f"Detail: {str(exc)}. Silakan coba beberapa saat lagi."
            )