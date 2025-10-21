from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.config import Base
from app.models.employee import Employee

meeting_participants = Table(
    "meeting_participants",
    Base.metadata,
    Column("meeting_id", ForeignKey("meetings.id"), primary_key=True),
    Column("employee_id", ForeignKey("employees.id"), primary_key=True)
)

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    organizer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    organizer = relationship("Employee", backref="organized_meetings")
    participants = relationship("Employee", secondary=meeting_participants, backref="meetings")
