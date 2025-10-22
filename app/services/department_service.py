class DepartmentService:
    def __init__(self, repo):
        self.repo = repo

    def create_department(self, department_in):
        existing = self.repo.get_by_name(department_in.name)
        if existing:
            raise ValueError("Department name already exists")
        return self.repo.create(department_in)

    def get_all_departments(self):
        return self.repo.get_all()
    
