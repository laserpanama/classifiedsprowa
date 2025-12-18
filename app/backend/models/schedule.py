from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class ScheduleBase(BaseModel):
    republish_interval_hours: int
    is_active: bool = True

class ScheduleCreate(ScheduleBase):
    ad_id: str

class ScheduleUpdate(BaseModel):
    republish_interval_hours: Optional[int] = None
    is_active: Optional[bool] = None

class Schedule(ScheduleBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ad_id: str
    next_republish_at: datetime

    class Config:
        from_attributes = True
