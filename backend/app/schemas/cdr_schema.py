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