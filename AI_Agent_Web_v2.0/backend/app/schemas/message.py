import datetime
from typing import Optional
from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: Optional[str] = None
    tool_name: Optional[str] = None
    tool_args: Optional[str] = None
    tool_result: Optional[str] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True
