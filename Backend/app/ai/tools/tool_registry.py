from __future__ import annotations

from typing import Any
from collections.abc import Iterator
from collections.abc import Iterable

from app.ai.tools.base_tool import BaseTool


class ToolRegistry:
    """
    Registry seluruh AI Tool.

    Responsibility
    --------------

    - Register tool
    - Unregister tool
    - Lookup tool
    - Execute tool
    - Enable / Disable tool
    - Metadata provider

    Tidak bertanggung jawab terhadap:

    - Database
    - Logging
    - LangGraph
    - LLM
    """

    def __init__(self) -> None:

        self._tools: dict[str, BaseTool] = {}

    # =====================================================
    # REGISTER
    # =====================================================

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register satu tool.
        """

        name = tool.name.lower()

        if name in self._tools:

            raise ValueError(
                f"Tool '{name}' already exists."
            )

        self._tools[name] = tool

    def register_many(
        self,
        tools: Iterable[BaseTool],
    ) -> None:
        """
        Register banyak tool.
        """

        for tool in tools:

            self.register(
                tool,
            )

    # =====================================================
    # REMOVE
    # =====================================================

    def unregister(
        self,
        tool_name: str,
    ) -> None:
        """
        Menghapus tool.
        """

        self._tools.pop(
            tool_name.lower(),
            None,
        )

    def clear(
        self,
    ) -> None:
        """
        Menghapus seluruh tool.
        """

        self._tools.clear()

    # =====================================================
    # LOOKUP
    # =====================================================

    def get(
        self,
        tool_name: str,
    ) -> BaseTool:
        """
        Mengambil tool berdasarkan nama.
        """

        try:

            return self._tools[
                tool_name.lower()
            ]

        except KeyError as exc:

            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            ) from exc

    def exists(
        self,
        tool_name: str,
    ) -> bool:
        """
        Mengecek apakah tool tersedia.
        """

        return (
            tool_name.lower()
            in self._tools
        )

    # =====================================================
    # ENABLE / DISABLE
    # =====================================================

    def enable(
        self,
        tool_name: str,
    ) -> None:
        """
        Mengaktifkan tool.
        """

        self.get(
            tool_name,
        ).enable()

    def disable(
        self,
        tool_name: str,
    ) -> None:
        """
        Menonaktifkan tool.
        """

        self.get(
            tool_name,
        ).disable()

    # =====================================================
    # EXECUTION
    # =====================================================

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Menjalankan tool.
        """

        tool = self.get(
            tool_name,
        )

        return tool.execute(
            **kwargs,
        )

    # =====================================================
    # INFORMATION
    # =====================================================

    def list_tools(
        self,
        enabled_only: bool = False,
    ) -> list[BaseTool]:
        """
        Mengambil seluruh tool.
        """

        tools = list(
            self._tools.values()
        )

        if enabled_only:

            tools = [
                tool
                for tool in tools
                if tool.enabled
            ]

        return sorted(
            tools,
            key=lambda tool: tool.name,
        )

    def tool_names(
        self,
        enabled_only: bool = False,
    ) -> list[str]:
        """
        Mengambil nama seluruh tool.
        """

        return [
            tool.name
            for tool in self.list_tools(
                enabled_only=enabled_only,
            )
        ]

    def metadata(
        self,
        enabled_only: bool = False,
    ) -> list[dict[str, Any]]:
        """
        Metadata seluruh tool.
        """

        return [
            tool.to_dict()
            for tool in self.list_tools(
                enabled_only=enabled_only,
            )
        ]

    # =====================================================
    # MAGIC
    # =====================================================

    def __contains__(
        self,
        tool_name: str,
    ) -> bool:

        return self.exists(
            tool_name,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._tools,
        )

    def __iter__(
        self,
    )-> Iterator[BaseTool]:

        return iter(
            self.list_tools(),
        )

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(tools={self.tool_names()})"
        )