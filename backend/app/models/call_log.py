from sqlalchemy import (Column, BigInteger, String, Integer, DateTime, Enum)
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class DirectionEnum(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"

class CallLog(Base):
    __tablename__ = "call_log"

    call_log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    call_uuid = Column(String(64), nullable=False, index=True)
    direction = Column(Enum(DirectionEnum), nullable=False)

    caller = Column(String(32), nullable=False)
    callee = Column(String(32), nullable=False)
    agent_ext = Column(String(16), nullable=True, index=True)

    started_at = Column(DateTime(fsp=6), nullable=False)
    ringing_at = Column(DateTime(fsp=6), nullable=True)
    answered_at = Column(DateTime(fsp=6), nullable=True)
    ended_at = Column(DateTime(fsp=6), nullable=False)

    ring_sec = Column(Integer, default=0)
    talk_sec = Column(Integer, default=0)
    total_sec = Column(Integer, default=0)

    hangup_cause = Column(String(64), nullable=True)

    created_at = Column(DateTime(fsp=6), server_default=func.now())
    updated_at = Column(DateTime(fsp=6), server_default=func.now(), onupdate=func.now())