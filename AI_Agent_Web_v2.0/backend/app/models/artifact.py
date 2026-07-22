import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from app.core.database import Base


class ArtifactModel(Base):
    __tablename__ = "artifacts"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    type = Column(String)  # code, markdown, mermaid, chart
    title = Column(String)
    content = Column(Text)
    language = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
