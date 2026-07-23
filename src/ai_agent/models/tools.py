from typing import Any
from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    type: Literal["function"] = "function"
    function: dict[str, Any]


class EditOp(BaseModel):
    filepath: str
    target_content: Optional[str] = None
    replacement_content: str
