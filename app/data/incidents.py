

from app.data.db import connect_database

from app.data.schema import create_users_table,create_cyber_incidents_table,create_datasets_metadata_table
import pandas as pd 




def insert_incident(conn, incident_type, severity, status, date, description, reported_by, created_at=None):
   cursor = conn.cursor()
    
   if created_at is None:
        cursor.execute(
            """INSERT INTO cyber 
            (incident_type, severity, status, date, description, reported_by) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (incident_type, severity, status, date, description, reported_by)
        )
   else:
        cursor.execute(
            """INSERT INTO cyber 
            (incident_type, severity, status, date, description, reported_by, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (incident_type, severity, status, date, description, reported_by, created_at)
        )
    
   conn.commit()
   return cursor.lastrowid




def get_all_incidents(conn):
    incidents=pd.read_sql_query( "SELECT * FROM cyber "  ,conn )
    return incidents

   
def update_incident_status(conn, incident_id, new_status):
    cursor=conn.cursor()
    cursor.execute(
        "UPDATE cyber SET status=? WHERE id=? ",(new_status,incident_id)
    )
    conn.commit()
    return (cursor.rowcount)


def delete_incident(conn, incident_id):
    cursor=conn.cursor()
    cursor.execute(
        "DELETE FROM cyber WHERE id=? ",(incident_id,)
    )
    conn.commit()
    return(cursor.rowcount)

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

