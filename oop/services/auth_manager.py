

import bcrypt
import sqlite3
from typing import Tuple
from pathlib import Path

from oop.services.database_manager import DatabaseManager


class AuthManager:
    """Handles authentication logic: hashing, login, registration, validation."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    
    # Password Hashing
   
    def hash_password(self, plain_text_password: str) -> bytes:
        password_bytes = plain_text_password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt)

    def verify_password(self, plain_text_password: str, hashed_password: bytes) -> bool:
        password_bytes = plain_text_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_password)

    
    # Validation Helpers
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        if len(username) < 5:
            return False, "Username must be at least 5 characters."
        if username[0].isupper():
            return False, "First letter of username must be lowercase."
        return True, "Valid username."

    def validate_password(self, password: str) -> Tuple[bool, str]:
        if (
            len(password) >= 8
            and any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
        ):
            return True, "Valid password."

        return False, "Password must contain 8+ chars, uppercase, lowercase, and a digit."

    # -------------------------------------------------------
    # Registration
    # -------------------------------------------------------
    def register_user(self, username: str, password: str, role: str = "user"):
        # Check existing user
        existing = self.db.fetch_one(
            "SELECT 1 FROM users WHERE username = ?",
            (username,)
        )
        if existing:
            return False, f"Username '{username}' already exists."

        ok, msg = self.validate_username(username)
        if not ok:
            return False, msg

        ok, msg = self.validate_password(password)
        if not ok:
            return False, msg

        hashed = self.hash_password(password)

        self.db.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )

        return True, f"User '{username}' registered successfully!"

    
    # Login
    
    def login_user(self, username: str, password: str):
        user = self.db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,)
        )

        if not user:
            return False, "Username not found."

        _, stored_hash, _ = user

        if self.verify_password(password, stored_hash):
            return True, "Logged in successfully!"

        return False, "Invalid password."

    

    def migrate_users_from_file(self, filepath: Path):
        if not filepath.exists():
            print(f"No migration file found at {filepath}")
            return

        migrated = 0

        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                username, password_hash = line.split(",")[:2]

                try:
                    self.db.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, "user")
                    )
                    migrated += 1
                except sqlite3.Error as e:
                    print(f"Migration error for {username}: {e}")

        print(f"Migrated {migrated} users.")
