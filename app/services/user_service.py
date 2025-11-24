import bcrypt 
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import insert_user,get_user_by_username
from app.data.schema import create_users_table

DATA_DIR = Path("DATA")


def hash_password(plain_text_password):

    bytes=plain_text_password.encode("utf-8")
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(bytes,salt)
    hashed_str = hashed_password.decode("utf-8")

    return hashed_str


def verify_password(plain_text_password,hashed_password):

    bytes_password=plain_text_password.encode("utf-8")
    bytes_hashed=hashed_password.encode("utf-8")
    verify=bcrypt.checkpw(bytes_password,bytes_hashed)
    return verify 

def register_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    hashed=hash_password(password)   
    insert=insert_user(username,password)  
    return True, f"User '{username}' registered successfully!"



def login_user(username, password): 
    conn = connect_database()
    cursor = conn.cursor()
    
    # Find user
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."
    
    hashed=user[2]
    verify=verify_password(password,hashed)
    if verify:
        print("logged in sucessfully!")
    else:
        print("Invalid password, try again")



def validate_username(username):
    
    if len(username)<5:
        error_msg=("invalid username, too short")
        return False,error_msg
        

    if username[0].isupper():
         error_msg=("invalid username,First letter must be lowercase.")
         return False,error_msg
         

    return True,"valid username"

def validate_password(password):

  is_long_8 = len(password) >= 8    #check password length
  upper_flag = False            #flags to check for conditions
  lower_flag = False
  isdigit_flag = False
  
  for char in password:   
      if char.isupper():
         upper_flag=True
      if char.islower():
         lower_flag = True
      if char.isdigit():
           isdigit_flag = True
       
    

  if upper_flag and lower_flag and isdigit_flag  and is_long_8:
       error='The password is valid' #if all conditions/flags are true
       
       return True,error
  else:
     error='The password is really invalid'
     return False,error


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    """
    Migrate users from users.txt to the database.
    
    This is a COMPLETE IMPLEMENTATION as an example.
    
    Args:
        conn: Database connection
        filepath: Path to users.txt file
    """
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return
    
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")