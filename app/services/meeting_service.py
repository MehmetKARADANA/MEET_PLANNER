from app.repositories.meeting_repo import MeetingRepository
from app.repositories.employee_repo import EmployeeRepository
from sqlalchemy.orm import Session



class MeetingService:
    def __init__(self, meeting_repo: MeetingRepository, employee_repo: EmployeeRepository):
        self.meeting_repo = meeting_repo
        self.employee_repo = employee_repo

    def create_meeting(self, meeting_in):
        participants = []
        for emp_id in meeting_in.participant_ids:
            emp = self.employee_repo.get_by_id(emp_id)
            if not emp:
                raise ValueError(f"Employee with id {emp_id} not found")
            # Çakışma kontrolü
            for m in emp.meetings:
                if not (meeting_in.end_time <= m.start_time or meeting_in.start_time >= m.end_time):
                    raise ValueError(f"Employee {emp.first_name} {emp.last_name} has a conflicting meeting")
            participants.append(emp)

        organizer = self.employee_repo.get_by_id(meeting_in.organizer_id)
        if not organizer:
            raise ValueError("Organizer not found")
        participants.append(organizer)

       # return self.meeting_repo.create(meeting_in, participants)
        meeting = self.meeting_repo.create(meeting_in, participants)
        return self.serialize_meeting(meeting)

   # def get_all_meetings(self):
   #     return self.meeting_repo.get_all()
    def get_all_meetings(self):
        meetings = self.meeting_repo.get_all()
        return [self.serialize_meeting(m) for m in meetings]

    def serialize_meeting(self, meeting):
        """Meeting objesini JSON uyumlu dict’e çevirir"""
        return {
            "id": meeting.id,
            "title": meeting.title,
            "start_time": meeting.start_time,
            "end_time": meeting.end_time,
            "organizer_id": meeting.organizer_id,
            "participant_ids": [p.id for p in meeting.participants]
        }
