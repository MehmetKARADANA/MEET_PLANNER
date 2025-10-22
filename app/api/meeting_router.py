from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.meeting import MeetingCreate, MeetingRead,ParticipantUpdate,MeetingUpdate
from app.repositories.meeting_repo import MeetingRepository
from app.repositories.employee_repo import EmployeeRepository
from app.services.meeting_service import MeetingService
from app.core.dependencies import get_meeting_service, get_current_user
from fastapi import APIRouter, Depends, Query
from datetime import datetime

router = APIRouter(prefix="/meetings", tags=["Meetings"],dependencies=[Depends(get_current_user)])


@router.post("/", response_model=MeetingRead)
def create_meeting(meeting_in: MeetingCreate, service: MeetingService = Depends(get_meeting_service)):
    try:
        return service.create_meeting(meeting_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MeetingRead])
def list_meetings(service: MeetingService = Depends(get_meeting_service)):
    return service.get_all_meetings()

@router.put("/", response_model=MeetingCreate)
def update_meeting(meeting_in: MeetingUpdate, service: MeetingService = Depends(get_meeting_service)):
    return service.update_meeting(meeting_in.id, meeting_in)

@router.delete("/", response_model=MeetingCreate)
def delete_meeting(meeting_id: int, service: MeetingService = Depends(get_meeting_service)):
    return service.delete_meeting(meeting_id)


@router.post("/add-participant", response_model=MeetingCreate)
def add_participant(data: ParticipantUpdate, service: MeetingService = Depends(get_meeting_service)):
    return service.add_participant(data.meeting_id, data.emp_id)

@router.delete("/remove-participant", response_model=MeetingCreate)
def remove_participant(data: ParticipantUpdate, service: MeetingService = Depends(get_meeting_service)):
    return service.remove_participant(data.meeting_id, data.emp_id)

@router.get("/availability/{employee_id}")
def check_availability(
    employee_id: int,
    start_time: datetime = Query(..., description="Başlangıç zamanı, ISO formatında"),
    end_time: datetime = Query(..., description="Bitiş zamanı, ISO formatında"),
    service: MeetingService = Depends(get_meeting_service)
):
    try:
        available = service.check_employee_availability(employee_id, start_time, end_time)
        return {"employee_id": employee_id, "available": available}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))