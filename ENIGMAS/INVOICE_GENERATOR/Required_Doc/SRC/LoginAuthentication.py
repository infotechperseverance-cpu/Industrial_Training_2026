# Different usernames, same password
users = {
    "counter1": "admin123",
    "counter2": "admin123",
    "counter3": "admin123",
    "counter4": "admin123",
    "counter5": "admin123",
    "counter6": "admin123"
}
'''
@Function Name : dashboard
@Description   : This function displays the dashboard after
                 successful login and welcomes the user.
@Input Param   : username (String)
@Output Param  : NONE
@Author        : Prashik Dabhade
'''
def dashboard(username):
    print("\n===== DASHBOARD =====")
    print("Welcome,", username)
    print("Access Granted")
    
'''
@Function Name : login
@Description   : This function accepts username and password
                 from the user and validates the credentials.
                 If the credentials are correct, the dashboard
                 is displayed; otherwise an error message is shown.
@Input Param   : NONE
@Output Param  : NONE
@Author        : Prashik Dabhade
'''
def login():
    print("===== LOGIN PAGE =====")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if username in users and users[username] == password:
        print("\nLogin Successful!")
        print("Logged-in User:", username)
        dashboard(username)
        return username
    else:
        print("\nError: Invalid Username or Password!")
        return None
            
