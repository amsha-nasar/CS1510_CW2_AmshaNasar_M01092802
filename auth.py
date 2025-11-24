import bcrypt
import os
import string


USER_DATA_FILE = "users.txt"
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


'''test_password = "SecurePassword123"

# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")
# Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")
# Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")

'''
def register_user(username, password):
    with open("users.txt", "r") as f: 
             for line in f.readlines(): 
                  user, hash = line.strip().split(',', 1) 
                  if user == username:
                       print("username already exissts")
                       return False
                 
    hashed=hash_password(password)
    with open("users.txt", "a") as f: 
     f.write(f"{username},{hashed}\n") 
     print(f"User '{username}' registered.")
     return True


                       

def user_exists(username):
   
   try:
        with open("users.txt", "r") as f: 
             for line in f.readlines(): 
                  user, hashed_pass = line.strip().split(',', 1) 
                  if user == username:
                       print("username already exissts")
                       return True

   
   except FileNotFoundError:
        print("file doesnt exisit yet")
        pass
   return False



def login_user(username, password): 
    try:     
        with open("users.txt", "r") as f: 
            lines = f.readlines()
            if not lines:
                print("No users registered")
                return False
            
            for line in lines: 
                user, hashed = line.strip().split(',', 1) 
                if user == username:
                    return verify_password(password, hashed) 
             
    except FileNotFoundError:
        print("No users registered yet")
        return False
    
    # Username not found
    return False






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

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("           MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("              Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")

                # Optional pause
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
