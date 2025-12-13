
import pandas as pd

class User:
    """Represents a user in the intelligence platform."""

    def __init__(self, username: str, password_hash: str, role: str):
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def get_username(self) -> str:
        return self.username

    def get_role(self) -> str:
        return self.role

    def verify_password(self, plain_password: str, hasher) -> bool:
        """
        hasher: any object with a check_password(plain, hashed) method.
        """
        return hasher.check_password(plain_password, self.password_hash)

    def __str__(self):
        return f"User({self.username}, role={self.role})"

class UserRepository:

     def __init__(self, conn):
        self.conn = conn

     def create_user(self, username, password_hash, role):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role)
        )
        self.conn.commit()
        return cursor.lastrowid

    # ------------------------------
    # GET USER BY USERNAME (returns User object)
    # ------------------------------
     def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username=?"
        df = pd.read_sql_query(query, self.conn, params=(username,))

        if df.empty:
            return None

        row = df.iloc[0]
        return User(
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"]
        )

    # ------------------------------
    # GET ALL USERS (DataFrame)
    # ------------------------------
     def get_all_users(self):
        return pd.read_sql_query("SELECT * FROM users", self.conn)

    # ------------------------------
    # UPDATE USER (dynamic)
    # ------------------------------
     def update_user(self, username, **fields):
        """
        repo.update_user("admin", role="superadmin")
        repo.update_user("john", password_hash="new_hash")
        """
        if not fields:
            return 0

        columns = ", ".join(f"{k}=?" for k in fields.keys())
        values = list(fields.values()) + [username]

        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE users SET {columns} WHERE username=?",
            values
        )
        self.conn.commit()
        return cursor.rowcount

    # ------------------------------
    # DELETE USER
    # ------------------------------
     def delete_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()
        return cursor.rowcount