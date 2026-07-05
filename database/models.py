from dataclasses import dataclass
from typing import  Optional

@dataclass
class MachRecord:
    id : Optional[int] = None
    player_name : str = ""
    score : int = 0
    timestamp  : Optional[str] = None
    
    def __post_init__(self):
        if self.player_name == None or self.player_name.strip() == 0:
            raise ValueError("نام نمی‌میتواند خالی باشد")
        if self.score < 0:
            raise ValueError("امتیاز نمی‌تواند منفی باشد")