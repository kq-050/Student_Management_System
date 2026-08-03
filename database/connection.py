import sqlite3
from logger import logger


def connect_database():
    try:
        conn = sqlite3.connect("student.db")

        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    except sqlite3.Error as error:
        logger.error(error)
        return None


def create_tables(conn):
    cursor = conn.cursor()

    try:
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

        return True

    except sqlite3.Error as error:
        logger.error(error)
        conn.rollback()
        return False
