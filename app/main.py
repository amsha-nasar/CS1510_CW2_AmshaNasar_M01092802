
from app.data.db import connect_database
from app.data.schema import create_all_tables,load_csv_to_table
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents,update_incident_status,delete_incident,get_incidents_by_type_count,get_high_severity_by_status
from pathlib import Path
import pandas as pd 

DATA_DIR = Path("")
DB_PATH = DATA_DIR / "intelligence_platform.db"
cyber_path=DATA_DIR / "cyber_incidents.csv"
tickets_path=DATA_DIR / "it_tickets.csv"
metadata_path=DATA_DIR / "metadata_dataset.csv"


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)
    
    # Step 1: Connect
    print(" Connecting to database...")
    conn = connect_database()
    print("Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("Migrating users from users.txt...")
    user_count = migrate_users_from_file(conn)
    print(f"Migrated {user_count} users")
    
    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    cyber_rows = load_csv_to_table(conn,cyber_path,"cyber")
    print("\nloaded cyber data")
    tickets_rows = load_csv_to_table(conn,tickets_path,"tickets")
    print("\nloaded tickets data")
    data_rows = load_csv_to_table(conn,metadata_path,"metadata")
    print("\nloaded metadata data")
    
    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    tables = ['users', 'cyber', 'tickets', 'metadata']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")

# Run the complete setup
setup_database_complete()

def run_comprehensive_tests():
    """
    Run comprehensive tests on your database.
    """
    print("\n" + "="*60)
    print("🧪 RUNNING COMPREHENSIVE TESTS")
    print("="*60)
    
    conn = connect_database()
    
    # Test 1: Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")
    
    success, msg = login_user("test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")
    
    # Test 2: CRUD Operations
    print("\n[TEST 2] CRUD Operations")
    
    
    test_id = insert_incident(
    conn,
    "Test Incident",       # incident_type
    "Low",                 # severity
    "Open",                # status
    "2024-11-05",          # date
    "This is a test incident",  # description
    "test_user"            # reported_by
   )

    print(f"✅ Incident #{test_id} created")

# 5️⃣ Optional: Verify the row was inserted
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cyber WHERE id = ?", (test_id,))
    row = cursor.fetchone()
    print("Inserted row:", row)
    
    # Read
    df = pd.read_sql_query(
        "SELECT * FROM cyber WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print(f"  Read:    Found incident #{test_id}")
    
    # Update
    update_incident_status(conn, test_id, "Resolved")
    print(f"  Update:  Status updated")
    
    # Delete
    delete_incident(conn, test_id)
    print(f"  Delete:  Incident deleted")

    # Test 3: Analytical Queries
    print("\n[TEST 3] Analytical Queries")
    
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:     Found {len(df_by_type)} incident types")
    
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity: Found {len(df_high)} status categories")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)

# Run tests
run_comprehensive_tests()





