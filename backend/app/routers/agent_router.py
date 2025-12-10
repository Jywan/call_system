from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.agent import AgentOut, AgentCreate
from app.services.agent_service import (get_agents, get_agent_by_id, create_agent)

router = APIRouter(prefix="/agents", tags=["agents"])

"""
상담원 목록 조회
"""
@router.get("/", response_model=List[AgentOut])
def list_agents(skip: int = Query(0, ge=0), 
                limit: int = Query(50, ge=1, le= 100),
                is_active: Optional[bool] = Query(None),
                db: Session = Depends(get_db)):
    agents = get_agents(db=db, skip=skip, limit=limit, is_active=is_active)
    return agents


"""
상담원 단건 조회
"""
@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = get_agent_by_id(db=db, agent_id=agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

"""
상담원 등록
"""
@router.post("/", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
def register_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    try:
        agent = create_agent(db, payload)
    except ValueError as e:
        if str(e) == "AGENT EXT ALREADY EXISTS":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="내선번호 중복"
            )
        raise
    return agent