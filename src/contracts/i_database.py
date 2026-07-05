"""
Interface for Database operations.
"""
from abc import ABC, abstractmethod
from typing import List
from src.database.dtos import LeaderboardEntryDTO, MatchResultDTO

class IDatabase(ABC):
    """Abstract base class for database interactions."""

    @abstractmethod
    def authenticate_or_register(self, username: str, raw_password: str) -> bool:
        """Verify player password or register a new account if username doesn't exist."""
        pass

    @abstractmethod
    def save_match_result(self, match_dto: MatchResultDTO) -> bool:
        """Save a player's match result to the database."""
        pass

    @abstractmethod
    def get_top_scores(self, top_n: int = 10) -> List[LeaderboardEntryDTO]:
        """Return top N high scores from the database."""
        pass
