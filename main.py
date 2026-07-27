from database import database


def display_student(student):
    print("\n" + "-" * 40)
    print(f"Roll No    : {student[0]}")
    print(f"Name       : {student[1]} {student[2]}")
    print(f"Age        : {student[3]}")
    print(f"Gender     : {student[4]}")
    print(f"Email      : {student[5]}")
    print(f"Phone      : {student[6]}")
    print(f"Department : {student[7]}")
    print("-" * 40 + "\n")


conn = database.connect_database()
database.create_tables(conn)


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
8. Exit
""")

    try:
        command = int(input("Choose an option: "))
    except ValueError:
        print("Please enter a valid number.\n")
        continue

    if command == 1:
        department_name = input("Enter department name: ")

        success = database.add_department(conn, department_name)

        if success:
            print("\n✓ Department added successfully.\n")
        else:
            print("\n✗ Department already exists.\n")

    elif command == 2:
        departments = database.view_departments(conn)

        if not departments:
            print("\nNo departments found.\n")
        else:
            print("\nDepartments:")
            for department in departments:
                print(f"{department[0]} - {department[1]}")

    elif command == 3:
        departments = database.view_departments(conn)

        if not departments:
            print("\nNo departments found.\n")
            continue

        print("\nDepartments:")
        for department in departments:
            print(f"{department[0]} - {department[1]}")

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

        success = database.add_student(
            conn,
            roll_no,
            first_name,
            last_name,
            age,
            gender,
            email,
            phone,
            department_id
        )

        if success:
            print("\n✓ Student added successfully.\n")
        else:
            print("\n✗ Student could not be added. Check the Department ID or Roll Number.\n")

    elif command == 4:
        students = database.view_students(conn)

        if not students:
            print("\nNo students found.\n")
        else:
            for student in students:
                display_student(student)
                
    
    elif command == 5:
        roll_no = input("Enter the roll no of student you want to search: ")
        student = database.search_student(conn,roll_no)
        if student:
            display_student(student)
        else:
            print(f"\nNo student found with Roll Number '{roll_no}'.\n")
        

    elif command == 6:
        roll_no = input("Enter the Roll Number of the student you want to update: ")

        student = database.search_student(conn, roll_no)

        if not student:
            print(f"\nNo student found with Roll Number '{roll_no}'.\n")
        else:
            display_student(student)

            departments = database.view_departments(conn)

            print("\nDepartments:")
            for department in departments:
                 print(f"{department[0]} - {department[1]}")

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

            success = database.update_student(
                conn,
                roll_no,
                first_name,
                last_name,
                age,
                gender,
                email,
                phone,
                department_id
                )

            if success:
                print("\n✓ Student updated successfully.\n")
     
    elif command == 7:
         roll_no = input("Enter the Roll Number of the student you want to delete: ")
     
         student = database.search_student(conn, roll_no)
     
         if not student:
             print(f"\nNo student found with Roll Number '{roll_no}'.\n")
         else:
            display_student(student)  
            choice = input("Are you sure you want to delete this student? (Y/N): ").upper()   
            if choice == "Y":
                success = database.delete_student(conn,roll_no)
                if success:
                    print("✓ Student deleted successfully.")
            elif choice == "N":
                print("\nDeletion cancelled.\n")
            else:
                print("\nInvalid choice. Please enter Y or N.\n")
    
    elif command == 8:
        conn.close()
        print("Goodbye!")
        break

    else:
        print("Invalid option.")