

import json
import os
from datetime import datetime


#---JSON file to store command history---
history_file = "history.json"


#---Create history.json file if it does not exist---
def create_history_file():
    if not os.path.exists(history_file):
        with open(history_file, "w") as file:
            json.dump([], file, indent=4)



#---Save executed command details in history.json---
def save_command(command_name, status):

    #---Ensure history file exists---
    create_history_file()

    with open(history_file, "r") as file:
        history = json.load(file)   

    now = datetime.now()     


    
    command = {               
        "Command Name": command_name,
        "Date": now.strftime("%d-%m-%Y"),
        "Time": now.strftime("%H:%M:%S"),
        "Status": status
    } 

    history.append(command)   
    

    
    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


#---Display all saved command history---
def view_history():
    create_history_file()

    with open(history_file, "r") as file:
        history = json.load(file)        

    if len(history) == 0:
        print("\nNo Command History Found.\n")
        return
    


    #---Display each command record---
    print("\n------ Command History ------\n")

    for i, item in enumerate(history, start=1):
        print(f"{i}. Command Name : {item['Command Name']}")
        print(f"   Date         : {item['Date']}")
        print(f"   Time         : {item['Time']}")
        print(f"   Status       : {item['Status']}")
        print()    