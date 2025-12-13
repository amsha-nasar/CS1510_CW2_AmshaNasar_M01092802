
import sqlite3
from typing import Any, Iterable
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path: Path | str):
        """
        Database manager for SQLite.

        Args:
            db_path (Path | str): Path to the SQLite database file
        """
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
    
     return sqlite3.connect(str(self.db_path))


    def execute(self, sql: str, params: Iterable[Any] = ()) -> None:
        """
        Execute INSERT, UPDATE, DELETE queries.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()

    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        """
        Fetch a single row from the database.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()

    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        """
        Fetch all rows from the database.
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
