from fastapi import HTTPException, status
class DepartmentService:
    def __init__(self, repo):
        self.repo = repo

    def create_department(self, department_in):
        if self.repo.get_by_name(department_in.name):
            raise HTTPException(status_code=409, detail="Department name already exists")
        return self.repo.create(department_in)

    def get_all_departments(self):
        return self.repo.get_all()

    def update_department(self, department_id: int, department_in):
        department = self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return self.repo.update(department, department_in)

    def delete_department(self, department_id: int):
        department = self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return self.repo.delete(department)