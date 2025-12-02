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
    return hashed_password


def verify_password(plain_text_password,hashed_password):

    bytes_password=plain_text_password.encode("utf-8")
    verify=bcrypt.checkpw(bytes_password,hashed_password)
    return verify 

def register_user(username, password,role):
    conn = connect_database()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."
    
    u_valid, u_msg = validate_username(username)
    if not u_valid:
        return False, u_msg

    # Validate password
    p_valid, p_msg = validate_password(password)
    if not p_valid:
        return False, p_msg
    

    
    hashed=hash_password(password)   
    insert=insert_user(username,hashed,role)  
    print(insert)
    return True, f"User '{username}' registered successfully!"



def login_user(username, password):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Username not found."

    stored_hash = user[2]   # must be bytes

    if verify_password(password, stored_hash):
        return True, "Logged in successfully!"
    else:
        return False, "Invalid password."




def validate_username(username):
    if len(username) < 5:
        return False, "Username must be at least 5 characters."

    if username[0].isupper():
        return False, "First letter of username must be lowercase."

    return True, "Valid username."

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
       print('The password is valid' )#if all conditions/flags are true
       
       return True, "Valid password."
  else:
        return False, "Password must contain: 8+ characters, uppercase, lowercase, and a digit."


def migrate_users_from_file(conn, filepath=DATA_DIR / "users.txt"):
    
    if not filepath.exists():
        print(f" File not found: {filepath}")
        print("No users to migrate.")
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
    print(f"Migrated {migrated_count} users from {filepath.name}")