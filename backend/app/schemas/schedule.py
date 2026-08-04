from pydantic import BaseModel
from typing import Optional

class ScheduleBase(BaseModel):
    check_in: str
    check_out: str
    date: Optional[str] = None
    worked_days: Optional[str] = None
    late_minutes: Optional[int] = 15

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        from_attributes = True