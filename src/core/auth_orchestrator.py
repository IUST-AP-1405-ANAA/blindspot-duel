"""
Authentication flow manager.
"""
from src.contracts.i_database import IDatabase
from src.utils.exception_logger import ExceptionLogger

class AuthOrchestrator:
    """
    Manages communication between the login UI and the database.
    """

    def __init__(self, database: IDatabase):
        self.database = database

    def authenticate(self, username: str, raw_password: str) -> bool:
        """Verifies player credentials or registers a new account."""
        try:
            return self.database.authenticate_or_register(username, raw_password)
        except Exception as e:
            ExceptionLogger.log_error(f"Authentication failed: {str(e)}")
            return False
