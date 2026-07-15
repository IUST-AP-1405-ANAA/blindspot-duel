from pathlib import Path
from typing import List, Optional

from .connection_manager import DatabaseConnectionManager
from .models import MatchHistory, User
from .dtos import LeaderboardEntryDTO, MatchHistoryDTO, UserAuthDTO
import queries


class SQLiteRepository:

    def __init__(self, db_path: Path = Path("game_data.db")):
        self.db_path = db_path
        self.connection_manager = DatabaseConnectionManager(db_path)
        self._initialize_database()

    def _initialize_database(self) -> None:

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(queries.CREATE_USERS_TABLE)
            cursor.execute(queries.CREATE_MATCHES_TABLE)
            conn.commit()

    def save_match_result(self, player_name: str, score: int) -> None:

        if not player_name or len(player_name.strip()) == 0:
            raise ValueError("Player name cannot be empty")

        if score < 0:
            raise ValueError("Score cannot be negative")

        match_record = MatchHistory(player_name=player_name.strip(), score=score)

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(
                queries.INSERT_MATCH, (match_record.player_name, match_record.score)
            )
            conn.commit()

    def get_leaderboard(self, limit: int = 10) -> List[LeaderboardEntryDTO]:
        if limit < 1:
            raise ValueError("Limit must be at least 1")

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_LEADERBOARD)
            rows = cursor.fetchall()

            leaderboard = []
            for rank, row in enumerate(rows[:limit], start=1):
                entry = LeaderboardEntryDTO(
                    player_name=row["player_name"], score=row["score"], rank=rank
                )
                leaderboard.append(entry)

            return leaderboard

    def get_match_history(self) -> List[MatchHistoryDTO]:

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_ALL_MATCHES)
            rows = cursor.fetchall()

            history = []
            for row in rows:
                entry = MatchHistoryDTO(
                    player_name=row["player_name"],
                    score=row["score"],
                    timestamp=row["timestamp"],
                )
                history.append(entry)

            return history

    def get_player_stats(self, player_name: str) -> dict:
        with self.connection_manager as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) as total_matches,
                    SUM(score) as total_score,
                    AVG(score) as average_score,
                    MAX(score) as best_score,
                    MIN(score) as worst_score
                FROM matches
                WHERE player_name = ?
            """,
                (player_name,),
            )

            row = cursor.fetchone()

            if row is None or row["total_matches"] == 0:
                return {
                    "total_matches": 0,
                    "total_score": 0,
                    "average_score": 0.0,
                    "best_score": 0,
                    "worst_score": 0,
                }

            return {
                "total_matches": row["total_matches"],
                "total_score": row["total_score"] or 0,
                "average_score": round(row["average_score"] or 0, 2),
                "best_score": row["best_score"] or 0,
                "worst_score": row["worst_score"] or 0,
            }

    def create_user(self, username: str, password_hash: str) -> UserAuthDTO:
        user = User(username=username, password_hash=password_hash)

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(queries.COUNT_USER_EXISTS, (username,))
            result = cursor.fetchone()

            if result["exists"] > 0:
                raise ValueError(f"Username '{username}' already exists")

            cursor.execute(queries.INSERT_USER, (user.username, user.password_hash))
            conn.commit()

            user_id = cursor.lastrowid

        return UserAuthDTO(user_id=user_id, username=username)

    def get_user_by_username(self, username: str) -> Optional[UserAuthDTO]:

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(queries.SELECT_USER_BY_USERNAME, (username,))
            row = cursor.fetchone()

            if row is None:
                return None

            return UserAuthDTO(user_id=row["id"], username=row["username"])

    def _get_user_password_hash(self, username: str) -> Optional[str]:

        with self.connection_manager as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?", (username,)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return row["password_hash"]
