import sqlite3
from logger import logger
from models.student import Student


class StudentRepository:

    def __init__(self, conn):
        self.conn = conn

    def add_student(self, student):
        cursor = self.conn.cursor()

        try:
            # Check department exists
            cursor.execute(
                "SELECT id FROM Department WHERE id = ?", (student.department_id,)
            )

            department = cursor.fetchone()

            if not department:
                return False, "Department does not exist."

            # Check duplicate roll number
            cursor.execute(
                "SELECT id FROM Student WHERE roll_no = ?", (student.roll_no,)
            )

            existing_student = cursor.fetchone()

            if existing_student:
                return False, "Roll number already exists."

            # Check duplicate email
            cursor.execute("SELECT id FROM Student WHERE email = ?", (student.email,))

            existing_email = cursor.fetchone()

            if existing_email:
                return False, "Email already exists."

            # Insert student
            cursor.execute(
                """
                    INSERT INTO Student(
                     roll_no,
                     first_name,
                     last_name,
                     age,
                     gender,
                     email,
                     phone,
                     department_id
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student.roll_no,
                    student.first_name,
                    student.last_name,
                    student.age,
                    student.gender,
                    student.email,
                    student.phone,
                    student.department_id,
                ),
            )

            self.conn.commit()
            logger.info(f"Student {student.roll_no} added successfully")

            return True, "Student added successfully."

        except sqlite3.IntegrityError as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Database error."

        except sqlite3.Error as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Database error."

    def _create_student(self, row):
        return Student(
            roll_no=row[0],
            first_name=row[1],
            last_name=row[2],
            age=row[3],
            gender=row[4],
            email=row[5],
            phone=row[6],
            department_id=row[7],
            department_name=row[8],
        )

    def view_students(self):
        cursor = self.conn.cursor()

        try:

            cursor.execute("""
              SELECT
                Student.roll_no,
                Student.first_name,
                Student.last_name,
                Student.age,
                Student.gender,
                Student.email,
                Student.phone,
                Student.department_id,
                Department.department_name
              FROM Student
              INNER JOIN Department
                ON Student.department_id = Department.id
                ORDER BY Student.roll_no
                """)

            rows = cursor.fetchall()
            students = []
            for row in rows:
                student = Student(
                    roll_no=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    age=row[3],
                    gender=row[4],
                    email=row[5],
                    phone=row[6],
                    department_id=row[7],
                    department_name=row[8]
                )
                students.append(student)
            return students

        except sqlite3.Error as error:
                logger.error(error)
                return False

    def search_student(self, roll_no):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                 SELECT
                    Student.roll_no,
                    Student.first_name,
                    Student.last_name,
                    Student.age,
                    Student.gender,
                    Student.email,
                    Student.phone,
                    Student.department_id,
                    Department.department_name
                 FROM Student
                 INNER JOIN Department
                 ON Student.department_id = Department.id
                  WHERE Student.roll_no = ?
             """,
                (roll_no,),
            )

            row = cursor.fetchone()
            if row:
                return Student(
                    roll_no=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    age=row[3],
                    gender=row[4],
                    email=row[5],
                    phone=row[6],
                    department_id=row[7],
                    department_name=row[8],
                )
            return None

        except sqlite3.Error as error:
            logger.error(error)
            return False

    def update_student(self, student):
        cursor = self.conn.cursor()

        try:
            # Check student exists
            cursor.execute(
                "SELECT id FROM Student WHERE roll_no = ?", (student.roll_no,)
            )
            if not cursor.fetchone():
                return False, "Student not found."

            # Check department exists
            cursor.execute(
                "SELECT id FROM Department WHERE id = ?", (student.department_id,)
            )
            if not cursor.fetchone():
                return False, "Department does not exist."

            # Check duplicate email
            cursor.execute(
                "SELECT id FROM Student WHERE email = ? AND roll_no != ?",
                (student.email, student.roll_no),
            )
            if cursor.fetchone():
                return False, "Email already exists."

            cursor.execute(
                """
                    UPDATE Student
                    SET
                        first_name = ?,
                        last_name = ?,
                        age = ?,
                        gender = ?,
                        email = ?,
                        phone = ?,
                        department_id = ?
                    WHERE roll_no = ?
                """,
                (
                    student.first_name,
                    student.last_name,
                    student.age,
                    student.gender,
                    student.email,
                    student.phone,
                    student.department_id,
                    student.roll_no,
                ),
            )

            self.conn.commit()
            logger.info(f"Student {student.roll_no} updated successfully")

            return True, "Student updated successfully."

        except sqlite3.IntegrityError as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Student could not be updated."

        except sqlite3.Error as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Student could not be updated."

    def delete_student(self, roll_no):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
                    DELETE FROM Student
                    WHERE roll_no = ?
                """,
                (roll_no,),
            )

            # Check if any student was deleted
            if cursor.rowcount == 0:
                self.conn.rollback()
                return False, "Student not found."

            self.conn.commit()
            logger.info(f"Student {roll_no} deleted successfully")

            return True, "Student deleted successfully."

        except sqlite3.IntegrityError as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Student could not be deleted."

        except sqlite3.Error as error:
            logger.error(error)
            self.conn.rollback()
            return False, "Student could not be deleted."

    def search_students_by_name(self, name):
        cursor = self.conn.cursor()

        try:
            search = f"%{name}%"
            cursor.execute(
                """
                SELECT
                    Student.roll_no,
                    Student.first_name,
                    Student.last_name,
                    Student.age,
                    Student.gender,
                    Student.email,
                    Student.phone,
                    Department.id,
                    Department.department_name
                FROM Student
                INNER JOIN Department
                    ON Student.department_id = Department.id
                WHERE
                    Student.first_name LIKE ?
                    OR Student.last_name LIKE ?
                ORDER BY Student.first_name;""",
                (search, search),
            )

            students_data = cursor.fetchall()

            students = [self._create_student(row) for row in students_data]
            return students

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def search_students_by_department(self, department_name):
        cursor = self.conn.cursor()

        try:
            search = f"%{department_name}%"
            cursor.execute(
                """
                SELECT
                    Student.roll_no,
                    Student.first_name,
                    Student.last_name,
                    Student.age,
                    Student.gender,
                    Student.email,
                    Student.phone,
                    Department.id,
                    Department.department_name
                FROM Student
                INNER JOIN Department
                    ON Student.department_id = Department.id
                WHERE Department.department_name LIKE ?
                ORDER BY Student.first_name;""",
                (search,),
            )

            students_data = cursor.fetchall()

            students = [self._create_student(row) for row in students_data]
            return students

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def search_students_by_gender(self, gender):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                """
            SELECT
                Student.roll_no,
                Student.first_name,
                Student.last_name,
                Student.age,
                Student.gender,
                Student.email,
                Student.phone,
                Department.id,
                Department.department_name
            FROM Student
            INNER JOIN Department
                ON Student.department_id = Department.id
            WHERE Student.gender = ?
            ORDER BY Student.first_name;
        """,
                (gender,),
            )

            students_data = cursor.fetchall()

            students = [self._create_student(row) for row in students_data]

            return students

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def get_student_statistics(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM Student")

            total_students = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(age) FROM Student")

            avg_age = cursor.fetchone()[0]

            cursor.execute("SELECT MIN(age) FROM Student")

            youngest = cursor.fetchone()[0]

            cursor.execute("SELECT MAX(age) FROM Student")

            oldest = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Department")

            total_departments = cursor.fetchone()[0]

            # Students Per Department:
            cursor.execute("""SELECT
                    Department.department_name,
                    COUNT(Student.id)
                    FROM Department
                    LEFT JOIN Student
                    ON Department.id = Student.department_id
                    GROUP BY Department.id
                    ORDER BY Department.department_name;""")

            students_per_department = cursor.fetchall()

            return {
                "total_students": total_students,
                "total_departments": total_departments,
                "average_age": avg_age,
                "youngest": youngest,
                "oldest": oldest,
                "students_per_department": students_per_department,
            }

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def export_students(self):
        return self.view_students()

    def sort_students(self, sort_by):
        cursor = self.conn.cursor()

        try:
            sort_columns = {
                "name": "Student.first_name",
                "roll_no": "Student.roll_no",
                "age": "Student.age",
                "department": "Department.department_name",
            }

            order_by = sort_columns.get(sort_by)

            if order_by is None:
                return None

            cursor.execute(f"""
                SELECT
                    Student.roll_no,
                    Student.first_name,
                    Student.last_name,
                    Student.age,
                    Student.gender,
                    Student.email,
                    Student.phone,
                    Department.id,
                    Department.department_name
                FROM Student
                INNER JOIN Department
                    ON Student.department_id = Department.id 
                    ORDER BY {order_by};""")

            students_data = cursor.fetchall()

            students = [self._create_student(row) for row in students_data]

            return students

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def view_students_paginated(self, page, page_size):
        cursor = self.conn.cursor()

        offset = (page - 1) * page_size

        try:
            cursor.execute(
                """
                SELECT
                    Student.roll_no,
                    Student.first_name,
                    Student.last_name,
                    Student.age,
                    Student.gender,
                    Student.email,
                    Student.phone,
                    Student.department_id,
                    Department.department_name
                FROM Student
                INNER JOIN Department
                ON Student.department_id = Department.id
                ORDER BY Student.first_name
                LIMIT ?
                OFFSET ?;""",
                (page_size, offset),
            )

            students_data = cursor.fetchall()

            students = [self._create_student(row) for row in students_data]

            return students

        except sqlite3.Error as error:
            logger.error(error)
            return None

    def get_total_students(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM Student;")

            student_count = cursor.fetchone()[0]

            return student_count

        except sqlite3.Error as error:
            logger.error(error)
            return None
