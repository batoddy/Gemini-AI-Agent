# tools/time_tool.py

from datetime import datetime
from typing import Any, Dict

from tools.base_tool import BaseTool


class TimeTool(BaseTool):
    """Tool for returning the current local date and time."""

    @property
    def name(self) -> str:
        return "time"

    @property
    def description(self) -> str:
        return "Returns the current local date and time."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {"type_": "OBJECT", "properties": {}, "required": []},
        }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        now = datetime.now()

        return {
            "status": "success",
            "tool": self.name,
            "current_date": now.strftime("%Y-%m-%d"),
            "current_time": now.strftime("%H:%M:%S"),
            "iso_datetime": now.isoformat(),
        }
