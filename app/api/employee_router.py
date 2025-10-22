from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeRead,EmployeeUpdate
from app.services.employee_service import EmployeeService
from fastapi import Path
from app.core.dependencies import get_employee_service, get_current_user
from app.core.dependencies import require_role


router = APIRouter(prefix="/employees", tags=["Employees"],dependencies=[Depends(get_current_user)])

@router.get("/", response_model=list[EmployeeRead], dependencies=[Depends(require_role("ADMIN"))])
def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return service.get_all_employees()


@router.put("/", response_model=EmployeeRead)
def update_employee(
    employee_in: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
    current_user=Depends(get_current_user)
):
    return service.update_employee(employee_in, current_user)


@router.delete("/", response_model=EmployeeRead)
def delete_employee(
    service: EmployeeService = Depends(get_employee_service),
    current_user=Depends(get_current_user)
):
    return service.delete_employee(current_user)