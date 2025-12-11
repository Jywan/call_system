from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AgentBase(BaseModel):
    agent_ext: str
    agent_name: str
    is_active: bool = True


class AgentCreate(BaseModel):
    agent_ext: str
    agent_name: str
    password: Optional[str] = None


class AgentOut(BaseModel):
    id: int
    agent_ext: str
    agent_name: str
    is_active: bool
    last_login_at: Optional[datetime] = None
    last_logout_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    # Pydantic v2: orm_mode 대체
    model_config = {
        "from_attributes": True,
    }