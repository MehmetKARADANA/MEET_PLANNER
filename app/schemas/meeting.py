from pydantic import BaseModel ,Field
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

class ParticipantUpdate(BaseModel):
    meeting_id: int
    emp_id: int

class MeetingDelete(BaseModel):
    id: int

class MeetingUpdate(BaseModel):
    id: int
    title: Optional[str] = Field(None, description="Toplantı başlığı")
    start_time: Optional[datetime] = Field(None, description="Toplantı başlangıç zamanı")
    end_time: Optional[datetime] = Field(None, description="Toplantı bitiş zamanı")
    participant_ids: Optional[List[int]] = Field(None, description="Toplantıya katılacak kullanıcıların ID'leri")

    class Config:
        from_attributes = True

class AvailabilityRequest(BaseModel):
    employee_id: int = Field(..., description="Çalışan ID'si")
    start_time: datetime = Field(..., description="Toplantı başlangıç zamanı")
    end_time: datetime = Field(..., description="Toplantı bitiş zamanı")


