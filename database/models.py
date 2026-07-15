from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MatchHistory:
    id: Optional[int] = None
    player_name: str = ""
    score: int = 0
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.player_name == None or len(self.player_name.strip()) == 0:
            raise ValueError("Player name cannot be empty")
        if self.score < 0:
            raise ValueError("score cannot be negative")
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class User:
    username : str
    password_hash : str

    def __post_init__(self):
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("The username must be at least 3 characters long.")
        if not self.password_hash:
            raise ValueError("password hash cannot be empty")
