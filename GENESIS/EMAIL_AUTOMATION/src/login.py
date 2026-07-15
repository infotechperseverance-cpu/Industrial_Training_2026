import smtplib
import ssl
import re
import mysql.connector
import msvcrt
import sys

# 1. Function to establish database connection
def db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="rootsql25@8", # ENTER YOUR ACTUAL MYSQL PASSWORD HERE
            database="email_login"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"\n[Database Error] Could not connect to MySQL: {err}")
        return None

# 2. Function to validate email format syntax
def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# 3. Function to mask password input with stars (*) on terminal
def get_password(prompt="Enter your Gmail App Password: "):
    print(prompt, end="", flush=True)
    password = ""
    
    while True:
        ch = msvcrt.getch()
        
        # Break loop when Enter key is pressed
        if ch in [b'\r', b'\n']:
            print() 
            break
            
        # Handle Backspace to erase star character properly
        elif ch == b'\x08':
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                
        # Append typed character to password and display star (*)
        else:
            try:
                char = ch.decode('utf-8')
                password += char
                sys.stdout.write('*') 
                sys.stdout.flush()
            except UnicodeDecodeError:
                pass 
                
    return password

# 4. Function to register a new user in the database (Sign Up)
def register(email, password):
    conn = db_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (user_id, password) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        conn.commit() 
        print("\n[Success] Registration successful! Your account is created in Database.")
        return True
    except mysql.connector.Error as err:
        print(f"\n[Error] Registration failed: Account might already exist.")
        return False
    finally:
        cursor.close()
        conn.close()

# 5. Core function to handle user login workflow (Sign In)
def login():
    print("\n-----------------------------------------")
    print("            USER LOGIN PANEL             ")
    print("-----------------------------------------")
    
    user_email = input("Enter your Gmail ID: ").strip()
    user_password = get_password() 
    
    if user_email == "" or user_password == "":
        print("\n[Error] Email or Password cannot be blank!")
        return None, None
        
    if not check_email(user_email):
        print("\n[Error] Invalid email format!")
        return None, None

    # Step 1: Check if user exists in the local database
    conn = db_connection()
    if conn is None:
        return None, None
        
    cursor = conn.cursor()
    query = "SELECT password FROM users WHERE user_id = %s"
    cursor.execute(query, (user_email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # Step 2: If user does not exist, ask them to Sign Up
    if result is None:
        print("\nThis Email is not registered in our Database.")
        choice = input("Do you want to sign up this account? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            success = register(user_email, user_password)
            if success:
                print(" Please run the login again to access the system.")
            return None, None
        else:
            print("\n Login cancelled.")
            return None, None

    # Step 3: Verify the password against database record
    db_password = result[0]
    if user_password != db_password:
        print("\n[Login Failed] Incorrect Password recorded in Database!")
        return None, None

    # Step 4: Perform real-time authentication via Google SMTP Server
    smtp_host = "smtp.gmail.com"
    smtp_port = 465
    secure_context = ssl.create_default_context()
    
    print("\nConnecting to Gmail server to verify active status...")
    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=secure_context)
        server.login(user_email, user_password)
        server.quit()

        print("\n[Success] Login successful! Welcome to the system.")
        return user_email, user_password
        
    except smtplib.SMTPAuthenticationError:
        print("\nERROR: Authentication Failed on Live Server!")
        print("Note: Password matches DB, but rejected by Gmail. Verify your 16-digit App Password.")
        return None, None
    except Exception as e:
        print(f"\nERROR: Could not reach Gmail Server: {e}")
        return None, None