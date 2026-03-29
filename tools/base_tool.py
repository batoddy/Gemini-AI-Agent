# tools/base_tool.py

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name used by the registry and LLM."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the tool."""
        pass

    @abstractmethod
    def get_declaration(self) -> Dict[str, Any]:
        """
        Return the function declaration/schema that will be sent to Gemini.
        """
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute the tool logic with the provided keyword arguments.

        Returns:
            A structured dictionary result.
        """
        pass
