
import pandas as pd 
from pathlib import Path
from app.data.db import connect_database

def create_users_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    print("✅ Users table created successfully!")

def create_cyber_incidents_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL ,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            date TEXT,
            description TEXT,
            reported_by TEXT ,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("Cyber Incidents data table created successfully!")

def create_datasets_metadata_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL ,
            source TEXT ,
            category TEXT ,
            file_size REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated  TEXT ,
            record_count INTEGER
            
        )
    """)
    conn.commit()
    print("✅ datasets metadata table created successfully!")

def create_it_tickets_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL ,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subject TEXT NOT NULL,
            description TEXT,
            resolved_date TEXT,
            assigned_to TEXT
                
        )
    """)
    conn.commit()
    print("IT Tickets table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)




def load_csv_to_table(conn, csv_path, table_name):
    # 1. Check if file exists
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print("CSV file not found:", csv_path)
        return 0

    # 2. Read CSV
    df = pd.read_csv(csv_path)

    # 3. Insert into SQL table
    df.to_sql(
        name=table_name,
        con=conn,
        if_exists='append',
        index=False
    )

    # 4. Print success message
    print(f"Loaded {len(df)} rows into '{table_name}'")

    return len(df)
