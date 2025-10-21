from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.department import DepartmentCreate, DepartmentRead
from app.repositories.department_repo import DepartmentRepository
from app.services.department_service import DepartmentService
from app.dependencies import get_db


router = APIRouter(prefix="/departments", tags=["Departments"])


def get_department_service(db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    return service

@router.post("/", response_model=DepartmentRead)
def create_department(department_in: DepartmentCreate, service: DepartmentService = Depends(get_department_service)):
    return service.create_department(department_in)

@router.get("/", response_model=list[DepartmentRead])
def list_departments(service: DepartmentService = Depends(get_department_service)):
    return service.get_all_departments()
