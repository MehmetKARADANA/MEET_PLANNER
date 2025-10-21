class EmployeeService:
    def __init__(self, repo):
        self.repo = repo

    def create_employee(self, employee_in):
        existing = self.repo.get_by_email(employee_in.email)
        if existing:
            raise ValueError("Email already exists")
        return self.repo.create(employee_in)

    def get_all_employees(self):
        return self.repo.get_all_employees()

    def update_employee(self, employee_id: int, employee_in):
        updated = self.repo.update(employee_id, employee_in)
        if not updated:
            raise ValueError("Employee not found")
        return updated

    def delete_employee(self, employee_id: int):
        deleted = self.repo.delete(employee_id)
        if not deleted:
            raise ValueError("Employee not found")
        return deleted
