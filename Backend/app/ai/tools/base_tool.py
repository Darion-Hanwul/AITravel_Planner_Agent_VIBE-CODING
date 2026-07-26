from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    def __init__(
        self,
        *,
        enabled: bool = True,
    ) -> None:

        self._enabled = enabled

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

    def execute(
        self,
        **kwargs: Any,
    ) -> Any:
 
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

    def to_dict(
        self,
    ) -> dict[str, Any]:
        
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