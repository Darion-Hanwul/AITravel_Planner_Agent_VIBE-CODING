from __future__ import annotations

from typing import Any
from collections.abc import Iterator
from collections.abc import Iterable

from app.ai.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self) -> None:

        self._tools: dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:

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

    def unregister(
        self,
        tool_name: str,
    ) -> None:

        self._tools.pop(
            tool_name.lower(),
            None,
        )

    def clear(
        self,
    ) -> None:

        self._tools.clear()

    def get(
        self,
        tool_name: str,
    ) -> BaseTool:

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
        return (
            tool_name.lower()
            in self._tools
        )

    def enable(
        self,
        tool_name: str,
    ) -> None:
        self.get(
            tool_name,
        ).enable()

    def disable(
        self,
        tool_name: str,
    ) -> None:

        self.get(
            tool_name,
        ).disable()

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:

        tool = self.get(
            tool_name,
        )

        return tool.execute(
            **kwargs,
        )

    def list_tools(
        self,
        enabled_only: bool = False,
    ) -> list[BaseTool]:

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
        
        return [
            tool.to_dict()
            for tool in self.list_tools(
                enabled_only=enabled_only,
            )
        ]

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