from datetime import datetime
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
    
    def update(self, meeting_id: int, meeting_in, participants=None):
        db_meeting = self.get_by_id(meeting_id)
        if not db_meeting:
            return None

        db_meeting.title = meeting_in.title
        db_meeting.start_time = meeting_in.start_time
        db_meeting.end_time = meeting_in.end_time
        db_meeting.organizer_id = meeting_in.organizer_id

        if participants is not None:
            db_meeting.participants = participants

        self.db.commit()
        self.db.refresh(db_meeting)
        return db_meeting

    def delete(self, meeting_id: int):
        db_meeting = self.get_by_id(meeting_id)
        if not db_meeting:
            return None

        self.db.delete(db_meeting)
        self.db.commit()
        return db_meeting

    def add_participant(self, meeting_id: int, participant: Employee):
        db_meeting = self.get_by_id(meeting_id)
        if not db_meeting:
            return None

        if participant not in db_meeting.participants:
            db_meeting.participants.append(participant)
            self.db.commit()
            self.db.refresh(db_meeting)

        return db_meeting

    def remove_participant(self, meeting_id: int, participant: Employee):
        db_meeting = self.get_by_id(meeting_id)
        if not db_meeting:
            return None

        if participant in db_meeting.participants:
            db_meeting.participants.remove(participant)
            self.db.commit()
            self.db.refresh(db_meeting)

        return db_meeting
    
    def has_conflict(self, employee_id: int, start_time: datetime, end_time: datetime) -> bool:
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise ValueError(f"Employee with id {employee_id} not found")

        for meeting in employee.meetings:
            if not (end_time <= meeting.start_time or start_time >= meeting.end_time):
                return True
        return False