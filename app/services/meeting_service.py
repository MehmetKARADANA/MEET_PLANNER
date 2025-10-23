from datetime import datetime
from app.repositories.meeting_repo import MeetingRepository
from app.repositories.employee_repo import EmployeeRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status



class MeetingService:
    def __init__(self, meeting_repo: MeetingRepository, employee_repo: EmployeeRepository):
        self.meeting_repo = meeting_repo
        self.employee_repo = employee_repo

    def create_meeting(self, meeting_in):
        try:
            participants = []
            for emp_id in meeting_in.participant_ids:
                emp = self.employee_repo.get_by_id(emp_id)
                if not emp:
                    raise HTTPException(status_code=404, detail=f"Employee with id {emp_id} not found")

                # Çakışma kontrolü
                for m in emp.meetings:
                    if not (meeting_in.end_time <= m.start_time or meeting_in.start_time >= m.end_time):
                        raise HTTPException(status_code=409, detail=f"Employee {emp.first_name} {emp.last_name} has a conflicting meeting")
                participants.append(emp)

            organizer = self.employee_repo.get_by_id(meeting_in.organizer_id)
            if not organizer:
                raise HTTPException(status_code=404, detail="Organizer not found")
            participants.append(organizer)

            meeting = self.meeting_repo.create(meeting_in, participants)
            return self.serialize_meeting(meeting)
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def get_all_meetings(self):
        try:
            meetings = self.meeting_repo.get_all()
            return [self.serialize_meeting(m) for m in meetings]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def get_meeting(self, meeting_id: int):
        try:
            m = self.meeting_repo.get_by_id(meeting_id)
            if not m:
                raise HTTPException(status_code=404, detail="Meeting not found")
            return self.serialize_meeting(m)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def update_meeting(self, meeting_id: int, meeting_in ):
        try:
            meeting = self.meeting_repo.get_by_id(meeting_id)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")

            participants = meeting.participants 
            if meeting_in.participant_ids is not None:
                participants = []
                for emp_id in meeting_in.participant_ids:
                    emp = self.employee_repo.get_by_id(emp_id)
                    if not emp:
                        raise HTTPException(status_code=404, detail=f"Employee with id {emp_id} not found")
              
                    for m in emp.meetings:
                        if m.id == meeting_id:
                            continue
                        if meeting_in.start_time and meeting_in.end_time:
                            if not (meeting_in.end_time <= m.start_time or meeting_in.start_time >= m.end_time):
                                raise HTTPException(
                                    status_code=409,
                                    detail=f"Employee {emp.first_name} {emp.last_name} has a conflicting meeting"
                                )
                    participants.append(emp)

            if meeting_in.title is not None:
                meeting.title = meeting_in.title
            if meeting_in.start_time is not None:
                meeting.start_time = meeting_in.start_time
            if meeting_in.end_time is not None:
                meeting.end_time = meeting_in.end_time

            meeting.participants = participants

            self.meeting_repo.db.commit()
            self.meeting_repo.db.refresh(meeting)
            return self.serialize_meeting(meeting)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


    def delete_meeting(self, meeting_id: int):
        try:
            meeting = self.meeting_repo.delete(meeting_id)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            return self.serialize_meeting(meeting)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def add_participant(self, meeting_id: int, emp_id: int):
        try:
            emp = self.employee_repo.get_by_id(emp_id)
            if not emp:
                raise HTTPException(status_code=404, detail="Employee not found")

            meeting = self.meeting_repo.add_participant(meeting_id, emp)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            return self.serialize_meeting(meeting)
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def remove_participant(self, meeting_id: int, emp_id: int):
        try:
            emp = self.employee_repo.get_by_id(emp_id)
            if not emp:
                raise HTTPException(status_code=404, detail="Employee not found")

            meeting = self.meeting_repo.remove_participant(meeting_id, emp)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            return self.serialize_meeting(meeting)
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


    def check_employee_availability(self, employee_id: int, start_time: datetime, end_time: datetime) -> bool:
        try:
            has_conflict = self.meeting_repo.has_conflict(employee_id, start_time, end_time)
            return not has_conflict
        except ValueError as ve:
            raise HTTPException(status_code=404, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        
    def serialize_meeting(self, meeting):
        return {
            "id": meeting.id,
            "title": meeting.title,
            "start_time": meeting.start_time,
            "end_time": meeting.end_time,
            "organizer_id": meeting.organizer_id,
            "participant_ids": [p.id for p in meeting.participants]
        }