from fastapi import HTTPException, status

class EmployeeService:
    def __init__(self, repo):
        self.repo = repo

    def create_employee(self, employee_in):
        try:
            email = employee_in.email if hasattr(employee_in, "email") else employee_in.get("email")
            existing = self.repo.get_by_email(email)
            if existing:
                raise HTTPException(status_code=409, detail="Email already exists")
            return self.repo.create(employee_in)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def get_employee(self, email: str):
        try:
            employee = self.repo.get_by_email(email)
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            return employee
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def get_all_employees(self):
        try:
            return self.repo.get_all_employees()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def update_employee(self, employee_in, current_user):
        try:
            employee_id = current_user["id"]
            updated = self.repo.update(employee_id, employee_in)
            if not updated:
                raise HTTPException(status_code=404, detail="Employee not found")
            return updated
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def delete_employee(self, current_user):
        try:
            employee_id = current_user["id"]
            deleted = self.repo.delete(employee_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Employee not found")
            return deleted
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")