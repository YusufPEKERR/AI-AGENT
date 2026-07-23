import datetime
from typing import Optional
from pydantic import BaseModel


class SessionCreate(BaseModel):
    title: Optional[str] = "Yeni Sohbet"
    username: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    title: str
    username: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
