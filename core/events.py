# core/events.py

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class EventType(str, Enum):
    USER_MESSAGE_RECEIVED = "USER_MESSAGE_RECEIVED"
    LLM_REQUEST_STARTED = "LLM_REQUEST_STARTED"
    LLM_TOOL_REQUESTED = "LLM_TOOL_REQUESTED"
    TOOL_EXECUTION_STARTED = "TOOL_EXECUTION_STARTED"
    TOOL_EXECUTION_SUCCEEDED = "TOOL_EXECUTION_SUCCEEDED"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    FINAL_RESPONSE_GENERATED = "FINAL_RESPONSE_GENERATED"
    AGENT_ERROR = "AGENT_ERROR"


class AgentEvent:
    """Represents a structured event emitted by the agent."""

    def __init__(
        self,
        event_type: EventType,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> None:
        self.event_type = event_type
        self.message = message
        self.payload = payload if payload is not None else {}
        self.timestamp = timestamp if timestamp is not None else datetime.now()
