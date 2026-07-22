from typing import Any, Callable, Dict, Optional
from ai_agent.models.messages import ToolResult


class BaseTool:
    def __init__(self, name: str, description: str, schema: dict[str, Any], handler: Callable[..., ToolResult]):
        self.name = name
        self.description = description
        self.schema = schema
        self.handler = handler

    def execute(self, **kwargs: Any) -> ToolResult:
        try:
            return self.handler(**kwargs)
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
