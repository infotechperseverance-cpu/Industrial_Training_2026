max_attempt=3
def login():
    count =0
    while True:
        if count > max_attempt:
            print("Too many attempt ,unsuccessful login")
            return False

        u = input("Enter Username: ")
        p = input("Enter Password: ")
        #usename is enigmas and password is 1234
        if u == "enigmas" and p == "1234":
            print("Login Successful")
            return True
        else:
            count +=1
            print("Invalid Login")
            


