from sqlalchemy.orm import Session
from app.models.department import Department

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, department_id: int):
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_all(self):
        return self.db.query(Department).all()

    def create(self, department_in):
        db_dep = Department(**department_in.dict())
        self.db.add(db_dep)
        self.db.commit()
        self.db.refresh(db_dep)
        return db_dep
    
    def get_by_name(self, name: str):
        return self.db.query(Department).filter(Department.name == name).first()
