from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.repositories.employee_repo import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services.employee_service import EmployeeService
from app.core.dependencies import get_db, get_employee_service
from app.core.security import hash_password, create_access_token, verify_password
from app.schemas.auth import  EmployeeWithToken,LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login",response_model=EmployeeWithToken)
def login(login_in: LoginRequest,  service: EmployeeService = Depends(get_employee_service)):
    user = service.get_employee(login_in.email)
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id),"role" : str(user.role.name)})
    return EmployeeWithToken(
        employee=user,  
        access_token=token,
        token_type="Bearer"
    )

@router.post("/register", response_model=EmployeeWithToken, status_code=status.HTTP_201_CREATED)
def register(employee_in: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):

    hashed_pwd = hash_password(employee_in.password)
    employee_data = employee_in.model_dump()
    print(f"Registering employee with email: {employee_data['email']}")
    del employee_data['password']
    employee_data['hashed_password'] = hashed_pwd
    print(f"Registering employee with email: {employee_data['email']}")
    try:
        employee = service.create_employee(employee_data)
    except ValueError as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    token = create_access_token({"sub": str(employee.id),"role" : str(employee.role.name)})
    return EmployeeWithToken(
        employee=employee,
        access_token=token,
        token_type="Bearer"
    )