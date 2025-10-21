from sqlalchemy.orm import Session
from app.models.employee import Employee

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(Employee).filter(Employee.email == email).first()

    def create(self, employee_in):
        db_employee = Employee(**employee_in.dict())
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def get_all_employees(self):
        return self.db.query(Employee).all()

    def get_by_id(self, employee_id: int):
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def update(self, employee_id: int, employee_in):
        db_employee = self.get_by_id(employee_id)
        if not db_employee:
            return None
        for field, value in employee_in.dict(exclude_unset=True).items():
            setattr(db_employee, field, value)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def delete(self, employee_id: int):
        db_employee = self.get_by_id(employee_id)
        if not db_employee:
            return None
        self.db.delete(db_employee)
        self.db.commit()
        return db_employee
