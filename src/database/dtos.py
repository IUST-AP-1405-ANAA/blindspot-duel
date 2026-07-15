"""
Data Transfer Objects.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LeaderboardEntryDTO:
    """This DTO only includes secure display data and is frozen."""
    rank: int
    player_name: str
    score: int

@dataclass(frozen=True)
class MatchResultDTO:
    """This DTO wraps the match result information for saving."""
    username: str
    score: int
    max_combo: int
