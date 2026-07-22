import datetime
from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, default="Yeni Sohbet")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
