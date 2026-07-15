"""
Data Classes for database tables.
"""
from dataclasses import dataclass

@dataclass
class PlayerRecord:
    """Represents a row in the users database table."""
    username: str
    password_hash: str
