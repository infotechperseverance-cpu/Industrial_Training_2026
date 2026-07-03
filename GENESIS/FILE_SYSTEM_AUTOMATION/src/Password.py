import pwinput

def password_protection():

    while True:

        choice = input("Do you want to protect the file with a password? (Y/N): ").strip().upper()

        if choice == "Y":

            while True:

                password = pwinput.pwinput("Enter password: ", mask="*")
                confirm = pwinput.pwinput("Confirm password: ", mask="*")

                if password == "":
                    print("Password cannot be empty.")

                elif password == confirm:
                    print("Password set successfully.")
                    return True, password

                else:
                    print("Passwords do not match. Please try again.")

        elif choice == "N":
            return False, None

        else:
            print("Invalid choice! Please enter Y or N.")