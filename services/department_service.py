class DepartmentService:

    def __init__(self, department_repository):
        self.department_repository = department_repository

    def view_departments(self):
        return self.department_repository.view_departments()

    def add_department(self, department_name):
        return self.department_repository.add_department(department_name)
