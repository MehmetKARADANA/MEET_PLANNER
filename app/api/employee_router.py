from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services.employee_service import EmployeeService
from fastapi import Path
from app.core.dependencies import get_employee_service, get_current_user
from app.core.dependencies import require_role


router = APIRouter(prefix="/employees", tags=["Employees"],dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[EmployeeRead], dependencies=[Depends(require_role("EMPLOYEE","ADMIN"))])
def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return service.get_all_employees()


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int = Path(..., description="Employee ID"),
    employee_in: EmployeeCreate = ...,
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_user)
):
    if current_user.id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )
    try:
        return service.update_employee(employee_id, employee_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{employee_id}", response_model=EmployeeRead)
def delete_employee(
    employee_id: int = Path(..., description="Employee ID"),
    service: EmployeeService = Depends(get_employee_service),
    current_user = Depends(get_current_user)
):
    if current_user.id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own profile"
        )
    try:
        return service.delete_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

