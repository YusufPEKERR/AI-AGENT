class AgentError(Exception):
    """Base exception for all agent runtime errors."""
    pass


class SecurityError(AgentError):
    """Raised when a security guardrail or path traversal violation occurs."""
    pass


class ToolExecutionError(AgentError):
    """Raised when a tool execution fails unexpectedly."""
    pass


class LLMAPIError(AgentError):
    """Raised when the LLM API provider fails or reaches rate limits."""
    pass


class ConfigurationError(AgentError):
    """Raised when invalid settings or environment parameters are supplied."""
    pass
