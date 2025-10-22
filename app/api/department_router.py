from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.department import DepartmentCreate, DepartmentRead
from app.services.department_service import DepartmentService
from app.core.dependencies import get_department_service,get_current_user


router = APIRouter(prefix="/departments", tags=["Departments"],dependencies=[Depends(get_current_user)])


@router.post("/", response_model=DepartmentRead)
def create_department(department_in: DepartmentCreate, service: DepartmentService = Depends(get_department_service)):
    return service.create_department(department_in)

@router.get("/", response_model=list[DepartmentRead])
def list_departments(service: DepartmentService = Depends(get_department_service)):
    return service.get_all_departments()
