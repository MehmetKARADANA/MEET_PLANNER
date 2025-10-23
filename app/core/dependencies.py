from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.repositories.employee_repo import EmployeeRepository
from app.config import SessionLocal
from sqlalchemy.orm import Session
from app.repositories.department_repo import DepartmentRepository
from app.repositories.meeting_repo import MeetingRepository
from app.services.employee_service import EmployeeService  
from app.services.meeting_service import MeetingService      
from app.services.department_service import DepartmentService
from fastapi import Header
from dotenv import load_dotenv
import os

load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def require_role(*allowed_roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission for this operation"
            )
        return current_user
    return role_checker

def get_current_user(Authorization: str = Header(default="")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = Authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"id" :int(user_id),"role": str(role)}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_employee_service(db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    service = EmployeeService(repo)
    return service

def get_meeting_service(db: Session = Depends(get_db)):
    meeting_repo = MeetingRepository(db)
    employee_repo = EmployeeRepository(db)
    service = MeetingService(meeting_repo, employee_repo)
    return service


def get_department_service(db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    service = DepartmentService(repo)
    return service

