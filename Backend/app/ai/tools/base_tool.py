from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Base class untuk seluruh AI Tool.

    Responsibility
    --------------

    - Menyediakan interface yang konsisten
    - Validasi enable/disable
    - Metadata tool
    - Entry point eksekusi

    Tidak bertanggung jawab terhadap:

    - LLM
    - LangGraph
    - Prompt
    - Memory
    """

    def __init__(
        self,
        *,
        enabled: bool = True,
    ) -> None:

        self._enabled = enabled

    # =====================================================
    # METADATA
    # =====================================================

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Nama tool.

        Contoh:
            weather
            currency
            rag
        """

    @property
    @abstractmethod
    def description(
        self,
    ) -> str:
        """
        Deskripsi tool.

        Dipakai untuk Tool Calling.
        """

    # =====================================================
    # STATUS
    # =====================================================

    @property
    def enabled(
        self,
    ) -> bool:

        return self._enabled

    def enable(
        self,
    ) -> None:

        self._enabled = True

    def disable(
        self,
    ) -> None:

        self._enabled = False

    # =====================================================
    # EXECUTION
    # =====================================================

    def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Entry point seluruh tool.

        LangGraph maupun Agent cukup
        memanggil execute().
        """

        if not self.enabled:
            raise RuntimeError(
                f"{self.name} tool is disabled."
            )

        return self.run(
            **kwargs,
        )

    @abstractmethod
    def run(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Business logic tool.
        """

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Metadata tool.

        Berguna untuk Agent Registry.
        """

        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
        }

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(name={self.name!r}, "
            f"enabled={self.enabled})"
        )