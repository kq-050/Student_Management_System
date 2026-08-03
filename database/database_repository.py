import os
import shutil
from datetime import datetime
from logger import logger


class DatabaseRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def backup_database(self):
        backup_folder = "backups"

        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"student_management_{timestamp}.db"

        backup_path = os.path.join(backup_folder, backup_filename)

        try:
            shutil.copy2(self.db_path, backup_path)

            logger.info(f"Database backup created: {backup_path}")

            return True, backup_path

        except OSError as error:
            logger.error(f"Database backup failed: {error}")
            return False, "Failed to create database backup."

    def restore_database(self, backup_path):

        # Check if the backup file exists
        if not os.path.exists(backup_path):
            return False, "Backup file not found."

        try:
            # Copy the backup over the current database
            shutil.copy2(backup_path, self.db_path)

            logger.info(f"Database restored from: {backup_path}")

            return True, "Database restored successfully."

        except OSError as error:
            logger.error(f"Database restore failed: {error}")
            return False, "Failed to restore database."
