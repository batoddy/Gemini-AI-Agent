# app/exceptions.py


class AgentError(Exception):
    """Base exception for all agent-related errors."""

    pass


class ConfigurationError(AgentError):
    """Raised when application configuration is invalid or missing."""

    pass


class MemoryError(AgentError):
    """Raised when there is an issue with memory operations."""

    pass


class ToolError(AgentError):
    """Base exception for all tool-related errors."""

    pass


class ToolNotFoundError(ToolError):
    """Raised when a requested tool is not registered in the ToolRegistry."""

    pass


class ToolExecutionError(ToolError):
    """Raised when a tool fails during execution."""

    pass


class ToolValidationError(ToolError):
    """Raised when tool arguments are missing or invalid."""

    pass


class LLMClientError(AgentError):
    """Raised when the LLM client fails to generate or parse a response."""

    pass


class ObserverError(AgentError):
    """Raised when an observer-related operation fails."""

    pass
