# observers/usage_observer.py

from core.events import AgentEvent, EventType
from core.observer import BaseObserver


class UsageObserver(BaseObserver):
    """Observer that tracks tool usage and agent activity statistics."""

    def __init__(self) -> None:
        self.total_events = 0
        self.total_tool_calls = 0
        self.total_tool_failures = 0
        self.total_final_responses = 0
        self.tool_usage = {}

    def update(self, event: AgentEvent) -> None:
        self.total_events += 1

        if event.event_type == EventType.TOOL_EXECUTION_SUCCEEDED:
            self.total_tool_calls += 1
            tool_name = event.payload.get("tool_name", "unknown")
            self.tool_usage[tool_name] = self.tool_usage.get(tool_name, 0) + 1

        elif event.event_type == EventType.TOOL_EXECUTION_FAILED:
            self.total_tool_failures += 1
            tool_name = event.payload.get("tool_name", "unknown")
            self.tool_usage[tool_name] = self.tool_usage.get(tool_name, 0) + 1

        elif event.event_type == EventType.FINAL_RESPONSE_GENERATED:
            self.total_final_responses += 1

    def get_summary(self) -> dict:
        return {
            "total_events": self.total_events,
            "total_tool_calls": self.total_tool_calls,
            "total_tool_failures": self.total_tool_failures,
            "total_final_responses": self.total_final_responses,
            "tool_usage": dict(self.tool_usage),
        }
