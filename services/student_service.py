import validators
from models.student import Student


class StudentService:
    
    def __init__(self,student_repository):
        self.student_repository = student_repository
        
    
    def view_students(self):
        return self.student_repository.view_students()
        
    def search_student(self, roll_no):
        return self.student_repository.search_student(roll_no)
        
    def delete_student(self, roll_no):
        return self.student_repository.delete_student(roll_no)
        
    def update_student(self,
    roll_no,
    first_name,
    last_name,
    age,
    gender,
    email,
    phone,
    department_id):
        
        #Age
        is_valid, result = validators.validate_age(age)
        if not is_valid:
            return False, result
        
        age = result
        
        #Roll Number
        is_valid, result = validators.validate_roll_no(roll_no)
        if not is_valid:
            return False, result
        roll_no = result
            
        #First Name       
        is_valid, result = validators.validate_name(first_name)
        if not is_valid:
            return False,result
        first_name = result
                
        #Last Name
        is_valid, result = validators.validate_name(last_name)
        if not is_valid:
            return False, result      
        last_name = result
            
        #Gender
        is_valid, result = validators.validate_gender(gender)
        if not is_valid:
            return False, result
        gender = result
                
        #Email
        is_valid, result = validators.validate_email(email)
        if not is_valid:
            return False,result
        email = result
                
        #Phone
        is_valid, result = validators.validate_phone(phone)
        if not is_valid:
            return False, result    
        phone = result    
        
        student = Student(
            roll_no,
            first_name,
            last_name,
            age,
            gender,
            email,
            phone,
            department_id
        ) 
        
        return self.student_repository.update_student(student)
    
    def add_student(self,
    roll_no,
    first_name,
    last_name,
    age,
    gender,
    email,
    phone,
    department_id):
        
        #Age
        is_valid, result = validators.validate_age(age)
        if not is_valid:
            return False, result
        
        age = result
        
        #Roll Number
        is_valid, result = validators.validate_roll_no(roll_no)
        
        if not is_valid:
            return False, result
            
        roll_no = result
            
        #First Name       
        is_valid, result = validators.validate_name(first_name)
        if not is_valid:
            return False,result
        
        first_name = result
                
        #Last Name
        is_valid, result = validators.validate_name(last_name)
        if not is_valid:
            return False, result      
                
        last_name = result
            
        #Gender

        is_valid, result = validators.validate_gender(gender)
        if not is_valid:
            return False, result
               
        gender = result
                
        #Email
        is_valid, result = validators.validate_email(email)
        if not is_valid:
            return False,result
        
        email = result
                
        #Phone
        is_valid, result = validators.validate_phone(phone)
        if not is_valid:
            return False, result    
        phone = result    
        
        
        student = Student(
            roll_no,
            first_name,
            last_name,
            age,
            gender,
            email,
            phone,
            department_id
                ) 
        
        return self.student_repository.add_student(student)  
        
                