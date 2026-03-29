# core/registry.py

from typing import Dict, List

from app.exceptions import ToolExecutionError, ToolNotFoundError
from tools.base_tool import BaseTool


class ToolRegistry:
    """Registry responsible for managing and executing tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance by its unique name."""
        self._tools[tool.name] = tool

    def has_tool(self, tool_name: str) -> bool:
        """Check whether a tool is registered."""
        return tool_name in self._tools

    def get_tool(self, tool_name: str) -> BaseTool:
        """Retrieve a tool by name or raise ToolNotFoundError."""
        tool = self._tools.get(tool_name)
        if tool is None:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered.")
        return tool

    def get_all_declarations(self) -> List[dict]:
        """Return Gemini-compatible declarations for all registered tools."""
        return [tool.get_declaration() for tool in self._tools.values()]

    def list_tool_names(self) -> List[str]:
        """Return a list of registered tool names."""
        return list(self._tools.keys())

    def execute_tool(self, tool_name: str, **kwargs) -> dict:
        """
        Execute a registered tool with the provided keyword arguments.
        """
        tool = self.get_tool(tool_name)

        try:
            return tool.execute(**kwargs)
        except Exception as exc:
            raise ToolExecutionError(
                f"Execution failed for tool '{tool_name}': {exc}"
            ) from exc
