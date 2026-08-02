import sqlite3
from logger import logger
from models.department import Department

class DepartmentRepository:
    
    def __init__(self, conn):
        self.conn = conn
    
    def add_department(self,department_name):
        cursor = self.conn.cursor()
            
        try:
            cursor.execute(
                "SELECT id FROM Department WHERE department_name = ?",
                (department_name,)
                )
        
            department = cursor.fetchone()
        
            if department:
                    return False
        
            cursor.execute(
                "INSERT INTO Department (department_name) VALUES (?)",
                (department_name,)
                )
        
            self.conn.commit()
            logger.info(f"Department {department_name} added successfully")
        
            return True
            
        except sqlite3.IntegrityError as error:
            logger.error(error)
            self.conn.rollback()
            return False
                
        except sqlite3.Error as error:
            logger.error(error)
            self.conn.rollback()
            return False
    
    def view_departments(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
             SELECT
              id,
              department_name
             FROM Department
                ORDER BY department_name
            """)
        
            rows = cursor.fetchall()
            departments = [Department(row[0], row[1]) for row in rows]
            return departments
            
        except sqlite3.Error as error:
            logger.error(error)
            return False
        
    
    def get_department_name(self, department_id):
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "SELECT department_name FROM Department WHERE id = ?",
                (department_id,)
             )

            department = cursor.fetchone()

            if department:
                return department[0]

            return "Unknown"

        except sqlite3.Error as error:
            logger.error(error)
            return "Unknown"