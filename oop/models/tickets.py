
import pandas as pd


class ITTicket:
    """Represents an IT support ticket."""

    def __init__(self, id, ticket_id, category, priority, status, created_date,
                 created_at, subject, description, resolved_date, assigned_to):
        self.id = id
        self.ticket_id = ticket_id
        self.category = category
        self.priority = priority
        self.status = status
        self.created_date = created_date
        self.created_at = created_at
        self.subject = subject
        self.description = description
        self.resolved_date = resolved_date
        self.assigned_to = assigned_to

    def assign_to(self, staff: str):
        self.assigned_to = staff

    def close_ticket(self):
        self.status = "Closed"

    def reopen_ticket(self):
        self.status = "Open"

    def __str__(self):
        return (
            f"Ticket {self.ticket_id}: {self.subject} "
            f"[{self.priority}] – {self.status} "
            f"(assigned to: {self.assigned_to})"
        )



class ITTicketRepository:
    """Handles all database operations for the tickets table."""

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # INSERT
    # -----------------------------
    def create_ticket(self, ticket_id, category, priority, created_date,
                      subject, description, assigned_to=None, status="open"):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO tickets
            (ticket_id, category, priority, status, created_date, subject, 
             description, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, category, priority, status, created_date,
             subject, description, assigned_to)
        )
        self.conn.commit()
        return cursor.lastrowid

    # -----------------------------
    # SELECT ALL
    # -----------------------------
    def get_all_tickets(self):
        query = "SELECT * FROM tickets ORDER BY created_at DESC"
        return pd.read_sql_query(query, self.conn)

    # -----------------------------
    # SELECT ONE (return model object)
    # -----------------------------
    def get_ticket_by_ticket_id(self, ticket_id):
        query = "SELECT * FROM tickets WHERE ticket_id = ?"
        df = pd.read_sql_query(query, self.conn, params=(ticket_id,))

        if df.empty:
            return None

        row = df.iloc[0]
        return ITTicket(
            id=row["id"],
            ticket_id=row["ticket_id"],
            category=row["category"],
            priority=row["priority"],
            status=row["status"],
            created_date=row["created_date"],
            created_at=row["created_at"],
            subject=row["subject"],
            description=row["description"],
            resolved_date=row["resolved_date"],
            assigned_to=row["assigned_to"]
        )

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_ticket(self, ticket_id, **fields):
        """
        Example:
        repo.update_ticket("TCK-001", status="Closed", assigned_to="Admin")
        """
        if not fields:
            return 0

        columns = ", ".join(f"{key}=?" for key in fields.keys())
        values = list(fields.values()) + [ticket_id]

        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE tickets SET {columns} WHERE ticket_id=?",
            values
        )
        self.conn.commit()
        return cursor.rowcount

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_ticket(self, ticket_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tickets WHERE ticket_id=?", (ticket_id,))
        self.conn.commit()
        return cursor.rowcount

    # -----------------------------
    # ANALYTICS QUERIES
    # -----------------------------
    def count_by_category(self):
        query = """
        SELECT category, COUNT(*) AS count
        FROM tickets
        GROUP BY category
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def count_by_priority(self):
        query = """
        SELECT priority, COUNT(*) AS count
        FROM tickets
        GROUP BY priority
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def count_by_status(self):
        query = """
        SELECT status, COUNT(*) AS count
        FROM tickets
        GROUP BY status
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def get_open_tickets(self):
        query = "SELECT * FROM tickets WHERE status='open'"
        return pd.read_sql_query(query, self.conn)

    def get_closed_tickets(self):
        query = "SELECT * FROM tickets WHERE status='Closed'"
        return pd.read_sql_query(query, self.conn)
