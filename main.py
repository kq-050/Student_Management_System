import os
from database import connection
from database.department_repository import DepartmentRepository
from database.student_repository import StudentRepository
from database.database_repository import DatabaseRepository
import validators
from models.student import Student
from utils.display import display_student, display_department
from services.student_service import StudentService
from services.department_service import DepartmentService
from services.database_service import DatabaseService

conn = connection.connect_database()
if conn is None:
    print("Database connection failed.")
    exit()


connection.create_tables(conn)
department_repository = DepartmentRepository(conn)
student_repository = StudentRepository(conn)
database_repository = DatabaseRepository("student.db")
student_service = StudentService(student_repository,department_repository)
department_service = DepartmentService(department_repository)
database_service = DatabaseService(database_repository)


while True:
    print("""
========================================
      Student Management System
========================================
1. Add Department
2. View Departments
3. Add Student
4. View Students
5. Search Student
6. Update Student
7. Delete Student
8. Student Statistics
9. Export Students to CSV
10. Import Students from CSV
11. Sort Students
12. Backup Database
13. Restore Database
14. Exit
""")

    try:
        command = int(input("Choose an option: "))
    except ValueError:
        print("Please enter a valid number.\n")
        continue

    if command == 1:
        department_name = input("Enter department name: ")

        success = department_service.add_department(department_name)

        if success:
            print("\n✓ Department added successfully.\n")
        else:
            print("\n✗ Department already exists.\n")

    elif command == 2:
        departments = department_service.view_departments()

        if not departments:
            print("\nNo departments found.\n")
        else:
            print("\nDepartments:")
            for department in departments:
                display_department(department)

    elif command == 3:
        departments = department_service.view_departments()

        if not departments:
            print("\nNo departments found.\n")
            continue

        print("\nDepartments:")
        for department in departments:
            display_department(department)

        try:
            department_id = int(input("Enter Department ID: "))
            age = int(input("Enter Age: "))
        except ValueError:
            print("\nDepartment ID and Age must be numbers.\n")
            continue

        roll_no = input("Enter Roll Number: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        gender = input("Enter Gender: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone Number: ")

        success, message = student_service.add_student(
            roll_no, first_name, last_name, age, gender, email, phone, department_id
        )

        if success:
            print(f"\n {message}\n")
        else:
            print(f"\n {message} \n")

    elif command == 4:
        page = 1

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            success, result = student_service.view_students_paginated(page)

            if not success:
                print(f"\n✗ {result}\n")
                break

            students = result["students"]
            current_page = result["page"]
            total_pages = result["total_pages"]

            print("\n" + "=" * 50)
            print("              Student List")
            print(f"             Page {current_page} of {total_pages}")
            print("=" * 50)

            if not students:
                print("\nNo students found.\n")
            else:
                for student in students:
                    display_student(student)

            print("\nNavigation")
            print("N - Next Page")
            print("P - Previous Page")
            print("Q - Back")

            choice = input("\nChoose an option: ").strip().upper()

            if choice == "N":
                if page < total_pages:
                    page += 1
                else:
                    print("\nAlready on the last page.\n")

            elif choice == "P":
                if page > 1:
                    page -= 1
                else:
                    print("\nAlready on the first page.\n")

            elif choice == "Q":
                break

            else:
                print("\nInvalid option.\n")

    elif command == 5:
        while True:
            print("""
                  ========== Search Students ==========

                1. By Roll Number
                2. By Name
                3. By Department
                4. By Gender
                5. Back""")

            try:
                search_choice = int(input("Choose an option: "))
                if search_choice == 1:
                    roll_no = input("Enter Roll Number: ")

                    is_valid, result = validators.validate_roll_no(roll_no)

                    if not is_valid:
                        print(f"\n✗ {result}\n")
                        continue

                    roll_no = result

                    success, result = student_service.search_student(roll_no)

                    if success:
                        display_student(result)
                    else:
                        print(f"\n✗ {result}\n")

                elif search_choice == 2:
                    name = input("Enter Name: ")

                    success, result = student_service.search_students_by_name(name)

                    if success:
                        for student in result:
                            display_student(student)
                    else:
                        print(f"\n✗ {result}\n")

                elif search_choice == 3:
                    department_name = input("Enter Department Name: ")

                    success, result = student_service.search_students_by_department(
                        department_name
                    )

                    if success:
                        for student in result:
                            display_student(student)
                    else:
                        print(f"\n✗ {result}\n")

                elif search_choice == 4:
                    gender = input("Enter Gender: ")

                    success, result = student_service.search_students_by_gender(gender)

                    if success:
                        for student in result:
                            display_student(student)
                    else:
                        print(f"\n✗ {result}\n")

                elif search_choice == 5:
                    break

                else:
                    print("Invalid Option!!")

            except ValueError:
                print("Please enter a valid number.")
                continue

    elif command == 6:
        roll_no = input("Enter the Roll Number of the student you want to update: ")

        student = student_service.search_student(roll_no)

        if not student:
            print(f"\nNo student found with Roll Number '{roll_no}'.\n")
        else:
            display_student(student)

            departments = department_service.view_departments()

            print("\nDepartments:")
            for department in departments:
                display_department(department)

            first_name = input("Enter New First Name: ")
            last_name = input("Enter New Last Name: ")
            gender = input("Enter New Gender: ")
            email = input("Enter New Email: ")
            phone = input("Enter New Phone Number: ")

            try:
                age = int(input("Enter New Age: "))
                department_id = int(input("Enter Department ID: "))
            except ValueError:
                print("\nAge and Department ID must be numbers.\n")
                continue

            success, message = student_service.update_student(
                roll_no, first_name, last_name, age, gender, email, phone, department_id
            )

            if success:
                print(f"\n {message}\n")
            else:
                print(f"\n {message}\n")

    elif command == 7:
        roll_no = input("Enter the Roll Number of the student you want to delete: ")

        success, student = student_service.search_student(roll_no)

        if not success:
            print(f"\n{student}\n")
        else:
            display_student(student)

            choice = (
                input("Are you sure you want to delete this student? (Y/N): ")
                .strip()
                .upper()
            )

            if choice == "Y":
                success, message = student_service.delete_student(roll_no)

                if success:
                    print(f"\n✓ {message}\n")
                else:
                    print(f"\n✗ {message}\n")

            elif choice == "N":
                print("\nDeletion cancelled.\n")

            else:
                print("\nInvalid choice. Please enter Y or N.\n")

    elif command == 8:
        statistics = student_service.get_student_statistics()
        if statistics is None:
            print("\nCould not load statistics.\n")
            continue

        print("\n" + "=" * 45)
        print("        Student Statistics")
        print("=" * 45)

        print(f"Total Students         :{statistics['total_students']}")
        print(f"Total Departments      :{statistics['total_departments']}")

        print(f"Average Age            :{statistics['average_age']}")
        print(f"Youngest Student       :{statistics['youngest']}")
        print(f"Oldest Student         :{statistics['oldest']}")

        print(f"Students by Department")
        print("-" * 45)

        for department_name, total in statistics["students_per_department"]:
            print(f"{department_name:>25} : {total}")

        print("=" * 45)

    elif command == 9:
        success, message = student_service.export_students()

        print(message)

    elif command == 10:
        path = input("Enter CSV file path: ")

        success, message = student_service.import_students(path)

        print(message)

    elif command == 11:
        while True:
            print("""
                ========== Sort Students ==========
                1. By Name
                2. By Roll Number
                3. By Age
                4. By Department
                5. Back  """)

            try:
                sort_choice = int(input("Choose an option: "))
            except ValueError:
                print("\nPlease enter a valid number.\n")
                continue

            if sort_choice == 1:
                success, result = student_service.sort_students("name")

            elif sort_choice == 2:
                success, result = student_service.sort_students("roll_no")

            elif sort_choice == 3:
                success, result = student_service.sort_students("age")

            elif sort_choice == 4:
                success, result = student_service.sort_students("department")

            elif sort_choice == 5:
                break

            else:
                print("Invalid option!")
                continue

            if success:
                for student in result:
                    display_student(student)
            else:
                print(f"\n✗ {result}\n")

    elif command == 12:
        success, message = database_service.backup_database()

        print(f"\n{message}\n")

    elif command == 13:
        backup_path = input("Enter the backup file path: ").strip()

        success, message = database_service.restore_database(backup_path)

        print(f"\n{message}\n")

    elif command == 14:
        conn.close()
        print("Goodbye!")
        break

    else:
        print("Invalid option.")
