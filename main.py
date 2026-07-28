from database import database
import validators

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
if conn is None:
    print("Database connection failed.")
    exit()
    
    
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

        #Age
        is_valid, result = validators.validate_age(age)
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        age = result
        
        #Roll Number
        roll_no = input("Enter Roll Number: ")
        is_valid, result = validators.validate_roll_no(roll_no)

        if not is_valid:
            print(f"\n✗ {result}\n")
            continue

        roll_no = result
        
        #First Name
        first_name = input("Enter First Name: ")
        is_valid, result = validators.validate_name(first_name)
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        first_name = result
        
        #Last Name
        last_name = input("Enter Last Name: ")
        is_valid, result = validators.validate_name(last_name)
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        last_name = result
    
        #Gender
        gender = input("Enter Gender: ")
        is_valid, result = validators.validate_gender(gender)
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        gender = result
        
        #Email
        email = input("Enter Email: ")
        is_valid, result = validators.validate_email(email)
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        email = result
        
        #Phone
        phone = input("Enter Phone Number: ")
        is_valid, result = validators.validate_phone(phone)
        if not is_valid:
             print(f"\n✗ {result}\n")
             continue
        phone = result

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
            print(f"\n✓ Student '{roll_no}' added successfully.\n")
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
        is_valid, result = validators.validate_roll_no(roll_no)

        if not is_valid:
            print(f"\n✗ {result}\n")
            continue

        roll_no = result
        student = database.search_student(conn,roll_no)
        if student:
            display_student(student)
        else:
            print(f"\nNo student found with Roll Number '{roll_no}'.\n")
        

    elif command == 6:
        roll_no = input("Enter the Roll Number of the student you want to update: ")
        is_valid, result = validators.validate_roll_no(roll_no)
        
        if not is_valid:
            print(f"\n✗ {result}\n")
            continue
        
        roll_no = result

        student = database.search_student(conn, roll_no)

        if not student:
            print(f"\nNo student found with Roll Number '{roll_no}'.\n")
        else:
            display_student(student)

            departments = database.view_departments(conn)

            print("\nDepartments:")
            for department in departments:
                 print(f"{department[0]} - {department[1]}")

            #First Name
            first_name = input("Enter New First Name: ")
            is_valid, result = validators.validate_name(first_name)
            if not is_valid:
                print(f"\n✗ {result}\n")
                continue
            first_name = result
            
            #Last Name
            last_name = input("Enter New Last Name: ")
            is_valid, result = validators.validate_name(last_name)
            if not is_valid:
                print(f"\n✗ {result}\n")
                continue
            last_name = result
            
            #Gender
            gender = input("Enter New Gender: ")
            is_valid, result = validators.validate_gender(gender)
            if not is_valid:
                 print(f"\n✗ {result}\n")
                 continue
            gender = result
            
            #Email
            email = input("Enter New Email: ")
            is_valid, result = validators.validate_email(email)
            if not is_valid:
                print(f"\n✗ {result}\n")
                continue
            email = result
            
            #Phone
            phone = input("Enter New Phone Number: ")
            is_valid, result = validators.validate_phone(phone)
            if not is_valid:
                print(f"\n✗ {result}\n")
                continue
            phone = result

            try:
                age = int(input("Enter New Age: "))
                department_id = int(input("Enter Department ID: "))
            except ValueError:
                print("\nAge and Department ID must be numbers.\n")
                continue

            is_valid, result = validators.validate_age(age)
            if not is_valid:
                print(f"\n✗ {result}\n")
                continue
            age = result
            
            
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
                print(f"\n✓ Student '{roll_no}' updated successfully.\n")
            else:
                print("\n✗ Student could not be updated.\n")
     
    elif command == 7:
         roll_no = input("Enter the Roll Number of the student you want to delete: ")
         is_valid, result = validators.validate_roll_no(roll_no)

         if not is_valid:
            print(f"\n✗ {result}\n")
            continue

         roll_no = result
         student = database.search_student(conn, roll_no)
     
         if not student:
             print(f"\nNo student found with Roll Number '{roll_no}'.\n")
         else:
            display_student(student)  
            choice = input("Are you sure you want to delete this student? (Y/N): ").strip().upper()   
            if choice == "Y":
                success = database.delete_student(conn,roll_no)
                if success:
                    print(f"\n✓ Student '{roll_no}' deleted successfully.\n")
                else:
                    print("\n✗ Student could not be deleted.\n")
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