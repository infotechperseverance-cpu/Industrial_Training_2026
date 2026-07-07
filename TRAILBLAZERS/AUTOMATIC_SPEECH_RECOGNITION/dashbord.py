

from datetime import datetime
import csv
import socket
import getpass

#---Display total commands
def totalCommands():

    history = get_command_history()

    print("-" * 70)
    print("Total Commands Executed")
    print()

    print(len(history))

#--Display notification    
def notifications():

    print("-" * 70)
    print("Notifications")
    print()

    print(get_notification())

#---Display history
def commandExecutionHistory():

    history = get_command_history()

    print("-" * 70)
    print("Command Execution History")
    print()

    if len(history) == 0:
        print("No Command History")

    else:
        for number, command in enumerate(history, start=1):
            print(f"{number}. {command}")

# --Dashboard heading
def dashboardHeading():

    print("=" * 70)
    print("                 VOICE ASSISTANT DASHBOARD")
    print("=" * 70)

#--User details
def userInformation():

    current_user = getpass.getuser()

    current_date = datetime.now().strftime("%d-%m-%Y")

    current_time = datetime.now().strftime("%I:%M:%S %p")

    print(f"Current User : {current_user}")
    print(f"Date         : {current_date}")
    print(f"Time         : {current_time}") 

#--Check internet
def internet_status():

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Connected"

    except OSError:
        return "Disconnected"
    
#--Check microphone
def microphone_status():

    return "Connected"

#---Display status
def systemStatus():

    print("-" * 70)
    print("System Status")
    print()

    print(f"Microphone : {microphone_status()}")
    print(f"Internet   : {internet_status()}")  

#--Display last command
def last_executed_command():

    print("-" * 70)
    print("Last Executed Voice Command")
    print()

    print(get_last_command())

#--Display schedule
def display_scheduled_commands():

    scheduled = get_scheduled_commands()

    print("-" * 70)
    print("Scheduled Commands")
    print()

    if len(scheduled) == 0:

        print("No Scheduled Commands")

    else:

        for number, command in enumerate(scheduled, start=1):

            print(f"{number}. {command}")

#--Quick access menu
def quick_access():

    print("-" * 70)
    print("Quick Access")
    print()

    print("1. Calculator")
    print("2. Email")
    print("3. Reminder")
    print("4. Command History")
    print("5. Voice Response")
    print("6. Speech Recognition")
    print("7. Exit")

    choice = input("\nEnter your choice: ").strip()

    if choice == "1":
        print("Calculator Module will open after integration.")

    elif choice == "2":
        print("Email Module will open after integration.")

    elif choice == "3":
        print("Reminder Module will open after integration.")

    elif choice == "4":
        print("Command History Module will open after integration.")

    elif choice == "5":
        print("Voice Response Module will open after integration.")

    elif choice == "6":
        print("Speech Recognition Module will open after integration.")

    elif choice == "7":
        print("Exiting Dashboard...")
        exit()

    else:
        print("Invalid Choice!")

#--Read history        
def get_command_history():

    history = []

    try:
        with open("command_history.csv", "r") as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:
                if row:
                    history.append(row[0])

    except FileNotFoundError:
        pass

    return history

#---Read last command
def get_last_command():

    try:
        with open("lastCammand.txt", "r") as file:
            return file.read().strip()

    except FileNotFoundError:
        return "No Command Executed"
    
#--Read schedule    
def get_scheduled_commands():

    scheduled = []

    try:

        with open("scheduled_commands.csv", "r") as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:

                if row:

                    scheduled.append(row[0])

    except FileNotFoundError:

        pass

    return scheduled 

#--Read notification   
def get_notification():

    try:
        with open("notification.txt", "r") as file:
            return file.read().strip()

    except FileNotFoundError:
        return "No Notifications"   
    
# ---Main function----    
def main():

    dashboardHeading()

    userInformation()

    systemStatus()

    last_executed_command()

    totalCommands()

    commandExecutionHistory()

    display_scheduled_commands()

    notifications()

    quick_access()

#call main function    
if __name__ == "__main__":
    main()
    