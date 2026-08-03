def display_student(student):
    print("\n" + "-" * 40)
    print(f"Roll No    : {student.roll_no}")
    print(f"Name       : {student.get_full_name()}")
    print(f"Age        : {student.age}")
    print(f"Gender     : {student.gender}")
    print(f"Email      : {student.email}")
    print(f"Phone      : {student.phone}")
    print(f"Department : {student.department_name or student.department_id}")
    print("-" * 40 + "\n")


def display_department(department):
    print(f"{department.id} - {department.department_name}")
