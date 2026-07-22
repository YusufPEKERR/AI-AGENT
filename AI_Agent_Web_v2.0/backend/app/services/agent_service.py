import sys
import os
from pathlib import Path
from typing import Any

# Add main workspace src/ to path so existing 31 tools can be imported cleanly
workspace_src = Path(__file__).resolve().parents[4] / "src"
if str(workspace_src) not in sys.path and workspace_src.exists():
    sys.path.insert(0, str(workspace_src))

try:
    from ai_agent.tools import tool_registry
    HAS_NATIVE_AGENT = True
except Exception:
    HAS_NATIVE_AGENT = False


class AgentService:
    def __init__(self) -> None:
        self.has_native = HAS_NATIVE_AGENT

    async def execute_tool(self, name: str, args: dict[str, Any]) -> Any:
        if self.has_native:
            res = tool_registry.execute(name, args)
            return res.to_output_str()
        return f"Simulated tool execution for '{name}' with args {args}"

    def get_schemas(self) -> list[dict[str, Any]]:
        from app.services.tool_schemas import TOOL_SCHEMAS
        return list(TOOL_SCHEMAS.values())


agent_service = AgentService()
