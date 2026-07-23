import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.session import SessionModel
from app.models.message import MessageModel
from app.models.user import UserModel
from app.schemas.session import SessionCreate, SessionResponse
from app.schemas.message import MessageResponse
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.get("", response_model=List[SessionResponse])
def get_sessions(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return db.query(SessionModel).filter(SessionModel.user_id == current_user.id).order_by(SessionModel.updated_at.desc()).all()


@router.post("", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    sid = str(uuid.uuid4())
    sess = SessionModel(id=sid, user_id=current_user.id, title=data.title or "Yeni Sohbet")
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
def get_session_messages(session_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    sess = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı veya erişim yetkiniz yok.")
    messages = db.query(MessageModel).filter(MessageModel.session_id == session_id).order_by(MessageModel.created_at.asc()).all()
    return messages


@router.delete("/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    sess = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı veya erişim yetkiniz yok.")
    
    # Delete associated messages
    db.query(MessageModel).filter(MessageModel.session_id == session_id).delete()
    db.delete(sess)
    db.commit()
    return {"status": "success"}


@router.put("/{session_id}", response_model=SessionResponse)
def update_session(session_id: str, data: SessionCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    sess = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    if not sess:
        raise HTTPException(status_code=404, detail="Sohbet bulunamadı veya erişim yetkiniz yok.")
    if data.title:
        sess.title = data.title
    db.commit()
    db.refresh(sess)
    return sess


