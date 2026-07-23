from database import database

conn = database.connect_database()
database.create_tables(conn)

while True:
    print("""
===== Student Management System =====
1. Add Department
2. View Departments
3. Add Student
4. View Students
5. Exit
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
            print("Department added successfully.")
        else:
            print("Department already exists.")

    elif command == 2:
        departments = database.view_departments(conn)

        if not departments:
            print("No departments found.")
        else:
            print("\nDepartments:")
            for department in departments:
                print(f"{department[0]} - {department[1]}")

    elif command == 3:
        departments = database.view_departments(conn)

        if not departments:
            print("No departments found.")
            continue

        print("\nDepartments:")
        for department in departments:
            print(f"{department[0]} - {department[1]}")

        try:
            department_id = int(input("Enter Department ID: "))
            age = int(input("Enter Age: "))
        except ValueError:
            print("Department ID and Age must be numbers.")
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
            print("Student added successfully.")
        else:
            print("Student could not be added. Check the department ID or roll number.")

    elif command == 4:
        print("View Students - Coming Tomorrow!")

    elif command == 5:
        conn.close()
        print("Goodbye!")
        break

    else:
        print("Invalid option.")