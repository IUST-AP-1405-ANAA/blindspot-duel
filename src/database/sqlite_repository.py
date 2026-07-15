"""
High-level DB repository.
"""
from typing import List
import sqlite3
from src.contracts.i_database import IDatabase
from src.database.dtos import LeaderboardEntryDTO, MatchResultDTO
from src.database.connection_manager import DatabaseConnection
from src.database import queries
from src.utils.exception_logger import ExceptionLogger

from src.config.settings import DB_PATH, LEADERBOARD_LIMIT

class SQLiteRepository(IDatabase):
    """
    Provides high-level methods to interact with SQLite database.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        # Setup tables
        with DatabaseConnection(self.db_path) as conn:
            conn.execute(queries.CREATE_USERS_TABLE)
            conn.execute(queries.CREATE_MATCHES_TABLE)

    def authenticate_or_register(self, username: str, raw_password: str) -> bool:
        """Check credentials. Register if username does not exist."""
        p_hash = queries.hash_password(raw_password)
        with DatabaseConnection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_USER, (username,))
            row = cursor.fetchone()
            
            if row is None:
                # Register
                cursor.execute(queries.INSERT_USER, (username, p_hash))
                ExceptionLogger.log_info(f"Registered new user: {username}")
                return True
            else:
                # Login validation
                stored_hash = row[0]
                return stored_hash == p_hash

    def save_match_result(self, match_dto: MatchResultDTO) -> bool:
        """Save score result to matches history."""
        try:
            with DatabaseConnection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(queries.INSERT_MATCH, (match_dto.username, match_dto.score, match_dto.max_combo))
            return True
        except Exception as e:
            ExceptionLogger.log_error(f"Error saving score: {str(e)}")
            return False

    def get_top_scores(self, top_n: int = LEADERBOARD_LIMIT) -> List[LeaderboardEntryDTO]:
        """Get top player scores."""
        entries = []
        try:
            with DatabaseConnection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(queries.SELECT_LEADERBOARD, (top_n,))
                rows = cursor.fetchall()
                for rank, row in enumerate(rows, 1):
                    username, score = row
                    entries.append(LeaderboardEntryDTO(rank, username, score))
        except Exception as e:
            ExceptionLogger.log_error(f"Error loading leaderboard: {str(e)}")
        return entries
