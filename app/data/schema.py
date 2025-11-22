


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

def create_cyber_incidents_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL ,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'open'
            date TEXT
        )
    """)
    conn.commit()

def create_datasets_metadata_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL ,
            source TEXT =
            category TEXT 
            size INTEGER
        )
    """)
    conn.commit()

def create_it_tickets_table(conn):
    """Create users table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL ,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open'
            created_date TEXT
        )
    """)
    conn.commit()
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)



