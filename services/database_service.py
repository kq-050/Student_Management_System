

class DatabaseService:
    def __init__(self, database_repository):
        self.database_repository = database_repository
        
    
    def backup_database(self):
        success, result = self.database_repository.backup_database()
        
        if success:
            return True, f"Database backed up successfully.\nBackup Location:\n{result}"

        return False, result
    

    def restore_database(self, backup_path):
        success, result = self.database_repository.restore_database(backup_path)

        if success:
            return (
                True,
                "Database restored successfully.\n"
                "Please restart the application to use the restored database."
            )

        return False, result