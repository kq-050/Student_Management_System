class Department:
    def __init__(self, department_id, department_name):
        self.id = department_id
        self.department_name = department_name

    def __str__(self):
        return f"{self.id} - {self.department_name}"

    def to_tuple(self):
        return (
            self.id,
            self.department_name
        )