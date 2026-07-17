import file_handling
import time

# Automatic task execute karun file madhe save karnar
def auto_execute():
    tasks = ["Backup Data", "Send Email", "Clean Folder"]
    
    for task in tasks:
        print("Automatic execute hotoy:", task)
        time.sleep(2)  # 2 second delay
        file_handling.save_task(task + " - Auto Completed")
    
    print("Sagale automatic tasks complete zale")