from fastapi import APIRouter
from app.services.agent_service import agent_service

router = APIRouter(prefix="/api/tools", tags=["tools"])


@router.get("")
def get_tools():
    return agent_service.get_schemas()
