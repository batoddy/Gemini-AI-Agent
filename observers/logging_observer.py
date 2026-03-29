# observers/logging_observer.py

from core.events import AgentEvent
from core.observer import BaseObserver


class LoggingObserver(BaseObserver):
    """Observer that logs agent events to the console."""

    def update(self, event: AgentEvent) -> None:
        timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{timestamp}] [{event.event_type.value}] {event.message} | Payload: {event.payload}"
        )
