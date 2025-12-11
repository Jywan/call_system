from __future__ import annotations

from datetime import datetime, timezone
from xml.etree import ElementTree as ET

from app.schemas.cdr_schema import FreeSwitchCdr

def _get_text(parent: ET.Element | None, tag: str) -> str | None:
    if parent is None:
        return None
    el = parent.find(tag)
    return el.text if el is not None else None

def parse_freeswitch_xml_cdr(raw_body: str) -> FreeSwitchCdr:
    """
    FreeSwitch mo_xml_cdr이 보내는
    'cdr=<xml ... </cdr>' 문자열을 FreeSwitchCdr 모델로 변환 
    """

    # 1. 앞의 'cdr=' 제거
    if raw_body.startswith("cdr="):
        xml_str = raw_body[4:]
    else:
        xml_str = raw_body

    # 2. XML 파싱
    root = ET.fromstring(xml_str)

    variables = root.find("variables")
    callflow = root.find("callflow")
    caller_profile = callflow.find("caller_profile") if callflow is not None else None

    # 3. 필드 추출
    uuid = (
        _get_text(variables, "uuid")
        or _get_text(caller_profile, "uuid")
    )

    caller_id_number = (
        _get_text(caller_profile, "caller_id_number")
        or _get_text(variables, "caller_id")
    )

    destination_number = (
        _get_text(caller_profile, "destination_number")
        or _get_text(variables, "origination_callee_id_number")
    )

    direction = _get_text(variables, "direction") or "outbound"

    # epoch -> datetime
    def _epoch_to_dt(value: str | None):
        if not value:
            return None
        iv = int(value)
        if iv <= 0:
            return None
        return datetime.fromtimestamp(iv, tz=timezone.utc)
    
    start_stamp = _epoch_to_dt(_get_text(variables, "start_epoch"))
    end_stamp = _epoch_to_dt(_get_text(variables, "end_epoch"))
    answer_stamp = _epoch_to_dt(_get_text(variables, "answer_epoch"))

    duration = int(_get_text(variables, "duration") or 0)
    billsec = int(_get_text(variables, "billsec") or 0)
    hangup_cause = _get_text(variables, "hangup_cause")


    # ===== A-leg/B-leg 판별 정보 추가 =====
    # <loopback_leg>A</loopback_leg>
    loopback_leg = _get_text(variables, "loopback_leg")

    # <is_outbound>true</is_outbound>
    is_outbound_text = _get_text(variables, "is_outbound")
    is_outbound = None
    if is_outbound_text is not None:
        is_outbound = is_outbound_text.lower() in ("true", "1")

    # 4. FreeSwitchCdr Pydantic 모델 생성
    return FreeSwitchCdr(
        uuid=uuid,
        caller_id_number=caller_id_number,
        destination_number=destination_number,
        direction=direction,
        start_stamp=start_stamp or end_stamp or datetime.now(timezone.utc),
        answer_stamp=answer_stamp,
        end_stamp=end_stamp or start_stamp or datetime.now(timezone.utc),
        duration=duration,
        billsec=billsec,
        hangup_cause=hangup_cause,

        loopback_leg=loopback_leg,
        is_outbound=is_outbound,
    )

