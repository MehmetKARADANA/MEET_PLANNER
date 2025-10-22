from pydantic import BaseModel
from typing import Optional, List
from app.schemas.employee import EmployeeRead

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentRead(DepartmentBase):
    id: int
    employees: Optional[List[EmployeeRead]] = []
    class Config:
        from_attributes=True
