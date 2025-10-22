from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MeetingBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime

class MeetingCreate(MeetingBase):
    organizer_id: int
    participant_ids: List[int] = []

class MeetingRead(MeetingBase):
    id: int
    organizer_id: int
    participant_ids: List[int] = []

    class Config:
        from_attributes=True
