CREATE_USERS_TABLE = """
CREATE TABLE IF NO EXISTS users(
    id INTEGER PRIMERY KEY AUTOINCREMNT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_MATCHES_TABLE = """
CREATE TABLE IF NOT EXITS matches(
    id INTEGER PRIMERY KEY AUTOINCREMNT,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL CHECK(score>=0),
    timestamp DATETIME DEFUALT CURRENT_TIMESTAMP 
)
"""


INSERT_USER = """
INSERT INTO users (username, password_hash)
VALUES (?, ?)
"""

INSERT_MATCH = """
INSERT INTO matches (player_name, score)
VALUES (?, ?)
"""

SELECT_LEADERBOARD = """
SELECT player_name, score
FROM matches
ORDER BY score DESC
LIMIT 10
"""

SELECR_USER_BY_USERNAME = """
SELECT id, username, password_hash
FROM matches
WHERE username = ?
LIMIT 1 
"""

SELECT_MATCH_BY_ID = """
SELECT id, player_name, score, timestamp
FROM matches
WHERE id = ?
"""

SELECT_ALL_MATCHES = """
SELECT player_name, score, timestamp
FROM matches
ORDER BY timestamp DESC
"""

UPDATE_USER_PASSWORD = """
UPDATE users
SET password_hash = ?
WHERE id = ?
"""

DELETE_MATCH_BY_ID = """
DELETE FROM matches
WHERE id = ?
"""

DELETE_USER_BY_ID = """
DELETE FROM users
WHERE id = ?
"""

COUNT_TOTAL_MATCHES = """
SELECT COUNT(*) as total_count
FROM matches
"""

COUNT_USER_EXISTS = """
SELECT COUNT(*) as exists
FROM users
WHERE username = ?
"""
