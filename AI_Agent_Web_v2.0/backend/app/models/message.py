import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from app.core.database import Base


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    role = Column(String)  # user, assistant, tool_call, tool_result
    content = Column(Text, nullable=True)
    tool_name = Column(String, nullable=True)
    tool_args = Column(Text, nullable=True)
    tool_result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
