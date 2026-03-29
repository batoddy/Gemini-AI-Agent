# core/observer.py

from abc import ABC, abstractmethod
from typing import List

from app.exceptions import ObserverError
from core.events import AgentEvent


class BaseObserver(ABC):
    """Abstract base class for all observers."""

    @abstractmethod
    def update(self, event: AgentEvent) -> None:
        """React to an emitted event."""
        pass


class Observable:
    """
    Mixin-like class that provides observer registration and notification.
    """

    def __init__(self) -> None:
        self._observers: List[BaseObserver] = []

    def attach(self, observer: BaseObserver) -> None:
        """Attach an observer if it is not already registered."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: BaseObserver) -> None:
        """Detach an observer if it is registered."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: AgentEvent) -> None:
        """
        Notify all registered observers about an event.

        Observer failures are isolated so that one broken observer
        does not break the entire agent.
        """
        for observer in self._observers:
            try:
                observer.update(event)
            except Exception as exc:
                raise ObserverError(
                    f"Observer {observer.__class__.__name__} failed: {exc}"
                ) from exc