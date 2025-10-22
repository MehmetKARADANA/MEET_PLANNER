from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int]

class EmployeeCreate(EmployeeBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str  
    department_id: int | None
    role: RoleEnum = RoleEnum.EMPLOYEE
 
class EmployeeRead(EmployeeBase):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int | None
    role: RoleEnum


    class Config:
        from_attributes=True
