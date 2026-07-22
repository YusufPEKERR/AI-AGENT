from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class ToolCallFunction(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    type: Literal["function"] = "function"
    function: ToolCallFunction


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[list[ToolCall]] = None


class ReasoningDelta(BaseModel):
    reasoning_content: str


class ToolResult(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None

    def to_output_str(self) -> str:
        if self.success:
            return self.output if self.output else "İşlem başarıyla tamamlandı (Çıktı yok)."
        return f"Hata: {self.error or self.output}"
