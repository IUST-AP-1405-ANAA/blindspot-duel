from dataclasses import dataclass

@dataclass(frozen=True)
class LeaderboardEntryDTO:
    player_name = str
    score = int
    rank = int
    def __post_init__(self):
        if not self.player_name or len(self.player_name.strip()) == 0:
            raise ValueError("player name cannot be empty")
        if self.score < 0:
            raise ValueError("score cannot be nagative")
        if self.rank < 1:
            raise ValueError("rank must be at least 1")

@dataclass(frozen=True)
class MatchHistoryDTO:
    player_name = str
    score = int
    timestrap = str
    
    def __post_init__(self):
        if not self.player_name or len(self.player_name.strip()) == 0:
            raise ValueError("player name cannot be empty")
        if self.score < 0:
            raise ValueError("score cannot be nagative")
        
@dataclass(frozen=True)
class UserAuthDTO:
    user_id = int
    username = str