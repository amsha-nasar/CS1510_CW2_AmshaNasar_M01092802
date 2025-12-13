


import pandas as pd
from oop.services.database_manager import DatabaseManager
from pathlib import  Path 

db_path = Path(__file__).parent.parent / "database" / "intelligence_platform.db"
print("DB path:", db_path.resolve())
print("Exists:", db_path.exists())


db=DatabaseManager(db_path)
conn= db.connect()

class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(self, incident_id: int, incident_type: str, severity: str,
                 status: str, description: str):
        self.__id = incident_id
        self.__incident_type = incident_type
        self.__severity = severity
        self.__status = status
        self.__description = description

    def get_id(self) -> int:
        return self.__id

    def get_type(self) -> str:
        return self.__incident_type

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

    def update_status(self, new_status: str) -> None:
        self.__status = new_status

    def get_severity_level(self) -> int:
        """Return a numeric severity level."""
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def __str__(self) -> str:
        return f"Incident {self.__id} [{self.__severity.upper()}] - {self.__incident_type}: {self.__status}"



class IncidentManager():
    def __init__(self, conn):
        """Initialize the repository with a database connection."""
        self.conn = conn

    # -----------------------------
    # CRUD OPERATIONS
    # -----------------------------
    def insert_incident(self, incident_type, severity, status, date, description, reported_by, created_at=None):
        cursor = self.conn.cursor()

        if created_at is None:
            cursor.execute(
                """
                INSERT INTO cyber 
                (incident_type, severity, status, date, description, reported_by)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (incident_type, severity, status, date, description, reported_by)
            )
        else:
            cursor.execute(
                """
                INSERT INTO cyber 
                (incident_type, severity, status, date, description, reported_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (incident_type, severity, status, date, description, reported_by, created_at)
            )

        self.conn.commit()
        return cursor.lastrowid

    def get_all_incidents(self):
        query = "SELECT * FROM cyber"
        return pd.read_sql_query(query, self.conn)

    def update_incident_status(self, incident_id, new_status):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE cyber SET status=? WHERE id=?",
            (new_status, incident_id)
        )
        self.conn.commit()
        return cursor.rowcount

    def delete_incident(self, incident_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM cyber WHERE id=?",
            (incident_id,)
        )
        self.conn.commit()
        return cursor.rowcount

    # -----------------------------
    # ANALYTICS OPERATIONS
    # -----------------------------
    def get_incidents_by_type_count(self):
        query = """
        SELECT incident_type, COUNT(*) as count
        FROM cyber
        GROUP BY incident_type
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_high_severity_by_status(self):
        query = """
        SELECT status, COUNT(*) as count
        FROM cyber
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_incident_types_with_many_cases(self, min_count=5):
        query = """
        SELECT incident_type, COUNT(*) as count
        FROM cyber
        GROUP BY incident_type
        HAVING COUNT(*) > ?
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn, params=(min_count,))
