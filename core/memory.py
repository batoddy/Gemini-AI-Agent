# core/memory.py

from pathlib import Path
from typing import Any, Dict, List, Optional

from app.exceptions import MemoryError


class MemoryManager:
    """Stores session-based conversation history."""

    def __init__(self, dump_file_path: Optional[Path] = None) -> None:
        self._history: List[Dict[str, Any]] = []
        self._dump_file_path = dump_file_path

    def add_message(
        self,
        role: str,
        content: Any,
        tool_name: Optional[str] = None,
    ) -> None:
        """
        Add a message to memory.

        Args:
            role: Message role such as 'user', 'assistant', 'tool', or 'system'
            content: The actual message content
            tool_name: Optional tool name for tool messages
        """
        if not role:
            raise MemoryError("Message role cannot be empty.")

        entry: Dict[str, Any] = {
            "role": role,
            "content": content,
        }

        if tool_name is not None:
            entry["tool_name"] = tool_name

        self._history.append(entry)
        self._dump_to_file()

    def add_user_message(self, content: str) -> None:
        self.add_message(role="user", content=content)

    def add_assistant_message(self, content: str) -> None:
        self.add_message(role="assistant", content=content)

    def add_tool_message(self, tool_name: str, content: Dict[str, Any]) -> None:
        self.add_message(role="tool", content=content, tool_name=tool_name)

    def add_system_message(self, content: str) -> None:
        self.add_message(role="system", content=content)

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history.copy()

    def clear(self) -> None:
        self._history.clear()
        self._dump_to_file()

    def last_message(self) -> Optional[Dict[str, Any]]:
        if not self._history:
            return None
        return self._history[-1]

    def _dump_to_file(self) -> None:
        """
        Write the full memory history to a text file for debugging/inspection.
        """
        if self._dump_file_path is None:
            return

        try:
            self._dump_file_path.parent.mkdir(parents=True, exist_ok=True)

            lines = []
            lines.append("==== MEMORY DUMP ====\n")

            for index, item in enumerate(self._history, start=1):
                lines.append(f"[{index}] role: {item.get('role')}\n")

                if "tool_name" in item:
                    lines.append(f"    tool_name: {item.get('tool_name')}\n")

                lines.append(f"    content: {item.get('content')}\n")
                lines.append("\n")

            self._dump_file_path.write_text("".join(lines), encoding="utf-8")

        except Exception as exc:
            raise MemoryError(f"Failed to dump memory to file: {exc}") from exc
