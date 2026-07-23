import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from app.core.database import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), index=True)
    filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
