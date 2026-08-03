import validators
from models.student import Student
import os
import csv
from logger import logger
import math


class StudentService:
    PAGE_SIZE = 10
    
    def __init__(self,student_repository):
        self.student_repository = student_repository
        
    
    # def view_students(self):
    #     return self.student_repository.view_students()
        
    def search_student(self, roll_no):
        student = self.student_repository.search_student(roll_no)
        if student:
            return True, student

        return False, "Student not found."
        
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


    def import_students(self, filename):

        if not os.path.exists(filename):
            return False, "CSV file not found."
        try:
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                
                imported = 0
                skipped = 0
                failed = 0
                
                for row in reader:

                    roll_no = row["Roll No"]
                    first_name = row["First Name"]
                    last_name = row["Last Name"]
                    gender = row["Gender"]
                    email = row["Email"]
                    phone = row["Phone"]
                    department_name = row["Department"]

                    # Convert age to integer
                    try:
                        age = int(row["Age"])
                    except ValueError:
                        failed += 1
                        continue

                    # Roll Number
                    is_valid, result = validators.validate_roll_no(roll_no)
                    if not is_valid:
                        failed += 1
                        continue
                    roll_no = result

                    # First Name
                    is_valid, result = validators.validate_name(first_name)
                    if not is_valid:
                        failed += 1
                        continue
                    first_name = result

                    # Last Name
                    is_valid, result = validators.validate_name(last_name)
                    if not is_valid:
                        failed += 1
                        continue
                    last_name = result

                    # Age
                    is_valid, result = validators.validate_age(age)
                    if not is_valid:
                        failed += 1
                        continue
                    age = result

                    # Gender
                    is_valid, result = validators.validate_gender(gender)
                    if not is_valid:
                        failed += 1
                        continue
                    gender = result

                    # Email
                    is_valid, result = validators.validate_email(email)
                    if not is_valid:
                        failed += 1
                        continue
                    email = result

                    # Phone
                    is_valid, result = validators.validate_phone(phone)
                    if not is_valid:
                        failed += 1
                        continue
                    phone = result


                    # Get department by name
                    department = self.department_repository.get_department_by_name(department_name)

                    if department is None:
                        failed += 1
                        continue

                    department_id = department.id
                    
                    # Create Student object
                    student = Student(
                        roll_no=roll_no,
                        first_name=first_name,
                        last_name=last_name,
                        age=age,
                        gender=gender,
                        email=email,
                        phone=phone,
                        department_id=department_id
                    )

                    success = self.student_repository.add_student(student)
                    
                    if success:
                        imported += 1
                    else:
                        skipped += 1
                    
                logger.info(
                    f"CSV Import -> Imported: {imported}, "
                    f"Skipped: {skipped}, "
                    f"Failed: {failed}"
                )
                
                return (
                        True,
                        f"Import completed.\n"
                        f"Imported: {imported}\n"
                        f"Skipped: {skipped}\n"
                        f"Failed: {failed}"
                    )       
        except KeyError as error:
            logger.error(error)
            return False, "Invalid CSV format. Please use the exported template." 
       
        except OSError as error:
            logger.error(error)
            return False, "Failed to read CSV file."
        
    def search_students_by_name(self, name):
        #validate name
        is_valid, result = validators.validate_name(name)
        
        if not is_valid:
            return False, result
        
        name = result
        
        #Call repo 
        students = self.student_repository.search_students_by_name(name)
        
        if students is None:
            return False, "An error occurred while searching."
        
        if not students:
            return False, "No students found."
        
        
        return True, students
    
    
    def search_students_by_department(self, department_name):

        department_name = department_name.strip()

        if not department_name:
            return False, "Department name cannot be empty."

        students = self.student_repository.search_students_by_department(department_name)

        if students is None:
            return False, "An error occurred while searching."

        if not students:
            return False, "No students found."

        return True, students
    
    def search_students_by_gender(self, gender):
        
        is_valid, result = validators.validate_gender(gender)
                
        if not is_valid:
            return False, result
                
        gender = result
        
        students = self.student_repository.search_students_by_gender(gender)
        
        if students is None:
            return False, "An error occurred while searching."
                
        if not students:
            return False, "No students found."
                
                
        return True, students
    
    def sort_students(self, sort_by):
        students = self.student_repository.sort_students(sort_by)

        if students is None:
            return False, "Invalid sort option."

        if not students:
            return False, "No students found."

        return True, students
    
    def view_students_paginated(self, page):
        students = self.student_repository.view_students_paginated(page,self.PAGE_SIZE)
        
        if students is None:
            return False, "An error occurred while retrieving students."
        
        total_students = self.student_repository.get_total_students()
        
        if total_students is None:
            return False, "An error occurred while retrieving student count."
        
        total_pages = math.ceil(total_students / self.PAGE_SIZE)
        
        if total_pages == 0:
            total_pages = 1
         
        if page < 1 or page > total_pages:
            return False, "Invalid page number."
         
        return True, {
            "students": students,
            "page": page,
            "total_pages": total_pages
        }   