from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.schemas.agent_schema import AgentCreate

def get_agents(db: Session, skip: int = 0, limit: int = 50, is_active: Optional[bool] = None) -> List[Agent]:
    """
    상담원 목록 조회 서비스
    - is_active : 필터링
    - skip, limit : 페이징
    """
    query = db.query(Agent)

    if is_active is not None:
        query = query.filter(Agent.is_active == is_active)

    return query.order_by(Agent.id.asc()).offset(skip).limit(limit).all()


def get_agent_by_id(db: Session, agent_id: int) -> Optional[Agent]:
    return db.query(Agent).filter(Agent.id == agent_id).first()

def get_agent_by_ext(db: Session, agent_ext: str) -> Optional[Agent]:
    return db.query(Agent).filter(Agent.agent_ext == agent_ext).first()

def create_agent(db: Session, agent_in: AgentCreate) -> Agent:
    """
    상담원 신규 등록
    - agent_ext는 중복등록 체크
    """
    existing = get_agent_by_ext(db, agent_in.agent_ext)
    if existing:
        raise ValueError("AGENT EXT ALREADY EXISTS")
    
    agent = Agent(
        agent_ext = agent_in.agent_ext,
        agent_name = agent_in.agent_name,
        password = agent_in.password,
        is_active = True
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent