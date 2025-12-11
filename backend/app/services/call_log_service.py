from sqlalchemy.orm import Session
from datetime import datetime
from app.models.call_log import CallLog, DirectionEnum
from app.schemas.cdr_schema import FreeSwitchCdr

def create_call_log_from_cdr(db: Session, cdr: FreeSwitchCdr) -> CallLog:

    if cdr.loopback_leg and cdr.loopback_leg != "A":
        # B-leg → 저장하지 않음
        return None
    
    if cdr.direction.lower() == "inbound":
        direction = DirectionEnum.INBOUND
    else:
        direction = DirectionEnum.OUTBOUND

    # 시간 계산 
    total_sec = cdr.duration
    talk_sec = cdr.billsec
    ring_sec = max(total_sec - talk_sec, 0)

    call_log = CallLog(
        call_uuid=cdr.uuid,
        direction=direction,
        caller=cdr.caller_id_number,
        callee=cdr.destination_number,
        agent_ext=None,  # 추후 라우팅 로직 추가 예정

        started_at=cdr.start_stamp,
        answered_at=cdr.answer_stamp,
        ended_at=cdr.end_stamp,
        ringing_at=None,

        ring_sec = ring_sec,
        talk_sec=talk_sec,
        total_sec=total_sec,
        hangup_cause=cdr.hangup_cause,
    )

    db.add(call_log)
    db.commit()
    db.refresh(call_log)
    return call_log
