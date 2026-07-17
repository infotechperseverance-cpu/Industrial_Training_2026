# Task file madhe save ani read karnyasathi

def save_task(task):
    f = open("task.txt", "a")  # append mode
    f.write(task + "\n")
    f.close()
    print("Task save zala:", task)

def read_task():
    try:
        f = open("task.txt", "r")  # read mode
        data = f.read()
        f.close()
        print("\n--- Tujhe Sagale Tasks ---")
        print(data)
    except:
        print("Adhi kuthla task add kara")