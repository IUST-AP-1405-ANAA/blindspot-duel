import sqlite3
from pathlib import Path
from typing import Optional

class DatabaseConnectionManager:
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            self.db_path = Path("game_data.db")
        else:
            self.db_path = db_path
        
        self.connection: Optional[sqlite3.Connection] = None
        
    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()

            self.connection.close()
        
        return False
    