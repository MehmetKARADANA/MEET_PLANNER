from datetime import datetime
from app.repositories.meeting_repo import MeetingRepository
from app.repositories.employee_repo import EmployeeRepository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status



class MeetingService:
    def __init__(self, meeting_repo: MeetingRepository, employee_repo: EmployeeRepository):
        self.meeting_repo = meeting_repo
        self.employee_repo = employee_repo

    def _check_conflicts_for_employees(
        self,
        employee_ids: list[int],
        start_time: datetime,
        end_time: datetime,
        exclude_meeting_id: int = None
    ):
        """
        Birden fazla çalışan için çakışma kontrolü yapar.
        - exclude_meeting_id parametresi, güncellenen toplantının kendi çakışma kontrolünden muaf tutulmasını sağlar.
        """
        for emp_id in employee_ids:
            emp = self.employee_repo.get_by_id(emp_id)
            if not emp:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {emp_id} not found"
                )

            #  Güncelleme mi create mi
            if exclude_meeting_id:
                has_conflict = self.meeting_repo.check_conflict_for_employee(
                    emp_id,
                    start_time,
                    end_time,
                    exclude_meeting_id
                )
            else:
                has_conflict = self.meeting_repo.has_conflict(
                    emp_id,
                    start_time,
                    end_time
                )

            if has_conflict:
                raise HTTPException(
                    status_code=409,
                    detail=f"Employee {emp.first_name} {emp.last_name} has a conflicting meeting"
                )
            
    def create_meeting(self, meeting_in):
        try:
       
            organizer = self.employee_repo.get_by_id(meeting_in.organizer_id)
            if not organizer:
                raise HTTPException(status_code=404, detail="Organizer not found")

            all_participant_ids = list(set(meeting_in.participant_ids + [meeting_in.organizer_id]))
            
            self._check_conflicts_for_employees(all_participant_ids, meeting_in.start_time, meeting_in.end_time)

            participants = []
            for emp_id in all_participant_ids:
                emp = self.employee_repo.get_by_id(emp_id)
                participants.append(emp)

            meeting = self.meeting_repo.create(meeting_in, participants)
            return self.serialize_meeting(meeting)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def update_meeting(self, meeting_id: int, meeting_in):
        try:
            meeting = self.meeting_repo.get_by_id(meeting_id)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")

            new_start_time = meeting_in.start_time if meeting_in.start_time is not None else meeting.start_time
            new_end_time = meeting_in.end_time if meeting_in.end_time is not None else meeting.end_time
            new_organizer_id = meeting_in.organizer_id if meeting_in.organizer_id is not None else meeting.organizer_id

            if meeting_in.organizer_id is not None:
                organizer = self.employee_repo.get_by_id(meeting_in.organizer_id)
                if not organizer:
                    raise HTTPException(status_code=404, detail="Organizer not found")

            if meeting_in.participant_ids is not None:
                all_participant_ids = list(set(meeting_in.participant_ids + [new_organizer_id]))
            else:
                all_participant_ids = list(set([p.id for p in meeting.participants] + [new_organizer_id]))

            self._check_conflicts_for_employees(
                all_participant_ids, 
                new_start_time, 
                new_end_time, 
                exclude_meeting_id=meeting_id  # Kendi toplantısını hariç tut
            )

            if meeting_in.title is not None:
                meeting.title = meeting_in.title
            if meeting_in.start_time is not None:
                meeting.start_time = meeting_in.start_time
            if meeting_in.end_time is not None:
                meeting.end_time = meeting_in.end_time
            if meeting_in.organizer_id is not None:
                meeting.organizer_id = meeting_in.organizer_id

            if meeting_in.participant_ids is not None:
                participants = []
                for emp_id in all_participant_ids:
                    emp = self.employee_repo.get_by_id(emp_id)
                    participants.append(emp)
                meeting.participants = participants

            updated_meeting = self.meeting_repo.update(meeting)
            return self.serialize_meeting(updated_meeting)

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
            
            meeting = self.meeting_repo.get_by_id(meeting_id)
            if not meeting:
                raise HTTPException(status_code=404, detail="Meeting not found")
            
            
            has_conflict = self.meeting_repo.has_conflict(emp_id, meeting.start_time, meeting.end_time)
            if has_conflict:
                raise HTTPException(
                    status_code=409,
                    detail=f"Employee {emp.first_name} {emp.last_name} has a conflicting meeting"
                )
            
            meeting = self.meeting_repo.add_participant(meeting_id, emp)
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