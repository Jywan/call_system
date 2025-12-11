from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FreeSwitchCdr(BaseModel):
    uuid: str
    caller_id_number: str
    destination_number: str
    direction: str
    start_stamp: datetime
    answer_stamp: Optional[datetime] = None
    end_stamp: datetime
    duration: int
    billsec: int
    hangup_cause: Optional[str] = None

    # A-leg / B-leg 판별용 메타데이터
    is_outbound: Optional[bool] = None    # <is_outbound>true</is_outbound>
    loopback_leg: Optional[str] = None    # <loopback_leg>A</loopback_leg>