import sqlite3


def connect_database():
    conn = sqlite3.connect("student.db")

    # Enable foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Department(
            id INTEGER PRIMARY KEY,
            department_name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Student(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            department_id INTEGER REFERENCES Department(id)
        );
    """)

    conn.commit()


def add_department(conn, department_name):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Department WHERE department_name = ?",
        (department_name,)
    )

    department = cursor.fetchone()

    if department:
        return False

    cursor.execute(
        "INSERT INTO Department (department_name) VALUES (?)",
        (department_name,)
    )

    conn.commit()

    return True


def view_departments(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Department")

    departments = cursor.fetchall()

    return departments


def add_student(
    conn,
    roll_no,
    first_name,
    last_name,
    age,
    gender,
    email,
    phone,
    department_id
):
    cursor = conn.cursor()

    # Check department exists
    cursor.execute(
        "SELECT * FROM Department WHERE id = ?",
        (department_id,)
    )

    department = cursor.fetchone()

    if not department:
        return False

    # Check duplicate roll number
    cursor.execute(
        "SELECT * FROM Student WHERE roll_no = ?",
        (roll_no,)
    )

    student = cursor.fetchone()

    if student:
        return False

    # Insert student
    cursor.execute("""
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
    """, (
        roll_no,
        first_name,
        last_name,
        age,
        gender,
        email,
        phone,
        department_id
    ))

    conn.commit()

    return True