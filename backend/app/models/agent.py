from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Agent(Base):
    __tablename__ = "agent"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    agent_ext = Column(String(16), unique=True, nullable=False)
    agent_name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    last_login_at = Column(DateTime, nullable=True)
    last_logout_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())