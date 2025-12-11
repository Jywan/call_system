from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.cdr_schema import FreeSwitchCdr
from app.services.call_log_service import create_call_log_from_cdr
from app.services.cdr_parser import parse_freeswitch_xml_cdr
from app.models.call_log import CallLog

router = APIRouter(prefix="/freeswitch", tags=["freeswitch"])

@router.post("/cdr", status_code=status.HTTP_201_CREATED)
async def receive_cdr(request: Request, db: Session = Depends(get_db)):
    raw_bytes = await request.body()
    raw_body = raw_bytes.decode("utf-8", errors="ignore")


    # XML → FreeSwitchCdr
    cdr: FreeSwitchCdr = parse_freeswitch_xml_cdr(raw_body)

    # 기존 서비스 로직 그대로 사용
    call_log: CallLog = create_call_log_from_cdr(db, cdr)

    if call_log is None:
        return {
            "status": "ignored",
            "reason": "non A-leg or filtered CDR",
            "uuid": cdr.uuid,
            "direction": cdr.direction,
            "loopback_leg": cdr.loopback_leg,
        }

    return {
        "call_log_id": call_log.call_log_id,
        "call_uuid": call_log.call_uuid,
    }