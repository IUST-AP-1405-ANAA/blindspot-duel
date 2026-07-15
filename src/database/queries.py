"""
Raw SQL queries.
"""
import hashlib

def hash_password(password: str) -> str:
    """Encapsulate hashing of password with SHA256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

CREATE_USERS_TABLE = \
"""CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL
);"""

CREATE_MATCHES_TABLE = \
"""CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    score INTEGER NOT NULL,
    max_combo INTEGER NOT NULL,
    date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

INSERT_USER = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
SELECT_USER = "SELECT password_hash FROM users WHERE username = ?"
INSERT_MATCH = "INSERT INTO matches (username, score, max_combo) VALUES (?, ?, ?)"
SELECT_LEADERBOARD = \
"""SELECT username, MAX(score) as high_score FROM matches GROUP BY username ORDER BY high_score DESC LIMIT ?"""
