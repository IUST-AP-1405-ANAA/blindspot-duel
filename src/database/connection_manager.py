"""
SQLite Connection manager (Context Manager).
"""
import sqlite3
import os

from src.config.settings import DB_PATH

class DatabaseConnection:
    """
    Context manager for safely connecting and closing the database.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
