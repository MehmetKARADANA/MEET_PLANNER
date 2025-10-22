from sqlalchemy import Column, Integer, String, ForeignKey,Enum
from app.config import Base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class RoleEnum(PyEnum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    department_id = Column(Integer,ForeignKey("departments.id"), nullable=True)

    department = relationship("Department", back_populates="employees")
    role = Column(Enum(RoleEnum), default=RoleEnum.EMPLOYEE, nullable=False)
