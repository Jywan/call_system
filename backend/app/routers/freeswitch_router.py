from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cdr_schema import FreeSwitchCdr
from app.services.call_log_service import create_call_log_from_cdr
from app.models.call_log import CallLog

router = APIRouter(prefix="/freeswitch", tags=["freeswitch"])

@router.post("/cdr", status_code=status.HTTP_201_CREATED)
def receive_cdr(payload: FreeSwitchCdr, db: Session = Depends(get_db)):
    """
    CallLog 적재 테스트 API
    """
    call_log: CallLog = create_call_log_from_cdr(db, payload)
    return {
        "call_log_id": call_log.call_log_id,
        "call_uuid": call_log.call_uuid,
    }