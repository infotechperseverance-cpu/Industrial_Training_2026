def login():

    u = input("Enter Username: ")
    p = input("Enter Password: ")
    #usename is enigmas and password is 1234
    if u == "enigmas" and p == "1234":
        print("Login Successful")
        return True
    else:
        print("Invalid Login")
        return False


if login():
    print("Welcome")
else:
    print("Try Again")