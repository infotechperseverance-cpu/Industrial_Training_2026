import pwinput

def password_protection():
    while True:
        choice = input("Do you want to protect the file with a password? (Y/N): ").strip().upper()

        if choice == "Y":
            while True:
                password = pwinput.pwinput("Enter password: ", mask="*")
                
                if password == "":
                    print("Password cannot be empty. Please enter a valid password.")
                    continue  # रिकामा पासवर्ड असल्यास थेट वर जाऊन पुन्हा 'Enter password' विचारेल

                confirm = pwinput.pwinput("Confirm password: ", mask="*")

                if password == confirm:
                    print("Password set successfully.")
                    return True, password
                else:
                    print("Passwords do not match. Please try again.")

        elif choice == "N":
            return False, ""  # None ऐवजी रिकाकी स्ट्रिंग पाठवणे जास्त सेफ राहील

        else:
            print("Invalid choice! Please enter Y or N.")