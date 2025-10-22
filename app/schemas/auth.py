from pydantic import BaseModel,EmailStr
from .employee import EmployeeRead

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class EmployeeWithToken(BaseModel):
    employee: EmployeeRead
    access_token: str
    token_type: str
