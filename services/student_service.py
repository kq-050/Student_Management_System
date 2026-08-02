import validators
from models.student import Student
import os
import csv
from logger import logger


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
        
    
    def get_student_statistics(self):
        
        statistics = self.student_repository.get_student_statistics()

        if statistics is None:
            return None
        
        if statistics["average_age"] is None:
            statistics["average_age"] = "N/A"
        else:
            statistics["average_age"] = f"{statistics['average_age']:.1f}"
        
        if statistics["youngest"] is None:
            statistics["youngest"] = "N/A"

        if statistics["oldest"] is None:
            statistics["oldest"] = "N/A"

        return statistics
    
    
    def export_students(self):
        students = self.student_repository.export_students()
        
        if students is None:
            return False, "Could not export students."
        
        if not students:
            return False, "No students found to export."
        
        if not os.path.exists("exports"):
            os.makedirs("exports", exist_ok=True)
        
        filename = os.path.join("exports", "students.csv")
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                 #Header
                writer.writerow([
                "Roll No",
                "First Name",
                "Last Name",
                "Age",
                "Gender",
                "Email",
                "Phone",
                "Department"
                ])
            
                #Data
                for student in students:
                    writer.writerow([
                    student.roll_no,
                    student.first_name,
                    student.last_name,
                    student.age,
                    student.gender,
                    student.email,
                    student.phone,
                    student.department_name
                    ])
            return True, f"Students exported successfully to '{filename}'."
        
        except OSError as error:
            logger.error(f"Failed to export students: {error}")
            return False, "Failed to export students."
