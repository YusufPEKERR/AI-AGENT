import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.session import SessionModel
from app.schemas.session import SessionCreate, SessionResponse

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("", response_model=List[SessionResponse])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).order_by(SessionModel.updated_at.desc()).all()


@router.post("", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db)):
    sid = str(uuid.uuid4())
    sess = SessionModel(id=sid, title=data.title or "Yeni Sohbet")
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    sess = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(sess)
    db.commit()
    return {"status": "success"}
