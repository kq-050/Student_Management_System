class Student:
    
    def __init__(
        self,
        roll_no,
        first_name,
        last_name,
        age,
        gender,
        email,
        phone,
        department_id=None,
        department_name=None
    ):
        self.roll_no = roll_no
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.department_id = department_id
        self.department_name = department_name
        
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
        
    def to_tuple(self):
        return (
            self.roll_no,
            self.first_name,
            self.last_name,
            self.age,
            self.gender,
            self.email,
            self.phone,
            self.department_id
    )