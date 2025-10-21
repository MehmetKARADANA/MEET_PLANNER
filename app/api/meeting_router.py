from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.meeting import MeetingCreate, MeetingRead
from app.repositories.meeting_repo import MeetingRepository
from app.repositories.employee_repo import EmployeeRepository
from app.services.meeting_service import MeetingService
from app.dependencies import get_db


router = APIRouter(prefix="/meetings", tags=["Meetings"])


def get_meeting_service(db: Session = Depends(get_db)):
    meeting_repo = MeetingRepository(db)
    employee_repo = EmployeeRepository(db)
    service = MeetingService(meeting_repo, employee_repo)
    return service

@router.post("/", response_model=MeetingRead)
def create_meeting(meeting_in: MeetingCreate, service: MeetingService = Depends(get_meeting_service)):
    try:
        return service.create_meeting(meeting_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MeetingRead])
def list_meetings(service: MeetingService = Depends(get_meeting_service)):
    return service.get_all_meetings()
