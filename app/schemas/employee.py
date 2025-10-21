from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int]

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int
    class Config:
        orm_mode = True
