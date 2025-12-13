
import pandas as pd

class Dataset:
    """Represents a dataset stored in the metadata table."""

    def __init__(self, dataset_id, name, source, category, file_size_mb, created_at, last_updated, record_count):
        self.id = dataset_id
        self.name = name
        self.source = source
        self.category = category
        self.file_size_mb = file_size_mb
        self.created_at = created_at
        self.last_updated = last_updated
        self.record_count = record_count

    def calculate_size_mb(self) -> float:
        return float(self.file_size_mb)

    def __str__(self):
        return (
            f"Dataset {self.id}: {self.name} "
            f"({self.file_size_mb:.2f} MB, {self.record_count} rows, "
            f"Source: {self.source})"
        )



class DatasetRepository:
    """Handles all database operations for the metadata (datasets) table."""

    def __init__(self, conn):
        self.conn = conn

    # -----------------------------
    # INSERT
    # -----------------------------
    def insert_dataset(self, name, source, category, file_size_mb, last_updated, record_count):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO metadata 
            (dataset_name, source, category, file_size_mb, last_updated, record_count)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, source, category, file_size_mb, last_updated, record_count)
        )
        self.conn.commit()
        return cursor.lastrowid

    # -----------------------------
    # SELECT ALL
    # -----------------------------
    def get_all_datasets(self):
        query = "SELECT * FROM metadata"
        df = pd.read_sql_query(query, self.conn)
        return df

    # -----------------------------
    # SELECT ONE
    # -----------------------------
    def get_dataset_by_id(self, dataset_id):
        query = "SELECT * FROM metadata WHERE id = ?"
        df = pd.read_sql_query(query, self.conn, params=(dataset_id,))
        if df.empty:
            return None

        row = df.iloc[0]
        return Dataset(
            dataset_id=row["id"],
            name=row["dataset_name"],
            source=row["source"],
            category=row["category"],
            file_size_mb=row["file_size_mb"],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
            record_count=row["record_count"]
        )

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update_dataset(self, dataset_id, **fields):
        """
        Allows dynamic updating:
        repo.update_dataset(3, category="Financial", file_size_mb=120.4)
        """
        if not fields:
            return 0

        columns = ", ".join(f"{key}=?" for key in fields.keys())
        values = list(fields.values()) + [dataset_id]

        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE metadata SET {columns} WHERE id=?", values)
        self.conn.commit()
        return cursor.rowcount

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete_dataset(self, dataset_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM metadata WHERE id=?", (dataset_id,))
        self.conn.commit()
        return cursor.rowcount

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    def count_by_category(self):
        query = """
        SELECT category, COUNT(*) AS count
        FROM metadata
        GROUP BY category
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, self.conn)

    def largest_datasets(self, limit=5):
        query = """
        SELECT * FROM metadata
        ORDER BY file_size_mb DESC
        LIMIT ?
        """
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def total_storage_used(self):
        query = "SELECT SUM(file_size_mb) AS total_mb FROM metadata"
        df = pd.read_sql_query(query, self.conn)
        return df["total_mb"].iloc[0] if not df.empty else 0
