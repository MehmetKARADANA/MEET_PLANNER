from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.department import DepartmentCreate, DepartmentRead,DepartmentDeleteRequest,DepartmentUpdateRequest
from app.services.department_service import DepartmentService
from app.core.dependencies import get_department_service,get_current_user
from app.core.dependencies import require_role

router = APIRouter(prefix="/departments", tags=["Departments"],dependencies=[Depends(get_current_user)])


@router.post("/", response_model=DepartmentRead, dependencies=[Depends(require_role("ADMIN"))])
def create_department(department_in: DepartmentCreate, service: DepartmentService = Depends(get_department_service)):
    return service.create_department(department_in)

@router.get("/", response_model=list[DepartmentRead])
def list_departments(service: DepartmentService = Depends(get_department_service)):
    return service.get_all_departments()

@router.put("/", response_model=DepartmentRead, dependencies=[Depends(require_role("ADMIN"))])
def update_department( department_in: DepartmentUpdateRequest, service: DepartmentService = Depends(get_department_service)):
    return service.update_department(department_in.id,department_in)

@router.delete("/", response_model=DepartmentRead, dependencies=[Depends(require_role("ADMIN"))])
def delete_department(request: DepartmentDeleteRequest, service: DepartmentService = Depends(get_department_service)):
    return service.delete_department(request.id)