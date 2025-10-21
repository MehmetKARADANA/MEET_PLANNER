from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.models.employee import Employee

class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, meeting_id: int):
        return self.db.query(Meeting).filter(Meeting.id == meeting_id).first()

    def create(self, meeting_in, participants):
        db_meeting = Meeting(
            title=meeting_in.title,
            start_time=meeting_in.start_time,
            end_time=meeting_in.end_time,
            organizer_id=meeting_in.organizer_id
        )
        db_meeting.participants = participants
        self.db.add(db_meeting)
        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def get_all(self):
        return self.db.query(Meeting).all()
