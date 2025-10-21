from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.repositories.employee_repo import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.config import SessionLocal
from fastapi import Path
from app.dependencies import get_db


router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    service = EmployeeService(repo)
    return service

@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(employee_in: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    try:
        employee = service.create_employee(employee_in)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=list[EmployeeRead])
def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return service.get_all_employees()


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int = Path(..., description="Employee ID"),
    employee_in: EmployeeCreate = ...,
    service: EmployeeService = Depends(get_employee_service)
):
    try:
        return service.update_employee(employee_id, employee_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{employee_id}", response_model=EmployeeRead)
def delete_employee(
    employee_id: int = Path(..., description="Employee ID"),
    service: EmployeeService = Depends(get_employee_service)
):
    try:
        return service.delete_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

