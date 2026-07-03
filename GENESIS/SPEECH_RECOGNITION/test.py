import pyaudiowpatch as pyaudio
import speech_recognition as sr
import pyttsx3
import os
import csv
from datetime import datetime
import webbrowser

#engine = pyttsx3.init()



def speak(text):
    engine =  pyttsx3.init()


    try:
        print("Assistant:", text)
        pyttsx3.speak(text)
        #engine.stop()  # clear any pending speech
        
        #engine.say(text)
        #engine.say("Debugging the code ")
        #engine.say("enhancing the code ")
        #print("Busy1 : ",engine.isBusy())
        #engine.runAndWait()
        #print("Busy2 : ",engine.isBusy())
        #engine.stop()

    except Exception as e:
        print("Speech Error:", e)

def listen():
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            command = recognizer.recognize_google(audio)

            print("You:", command)

            return command.lower()

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""

        except sr.RequestError as e:
            print("Google Speech Recognition error:", e)
            return ""

        except Exception as e:
            print("Unexpected error:", e)
            return ""

speak("Assistant Started")

FILE_NAME = "task.csv"
NOTE = "notes.csv"

# Create CSV file if not exists
def create_files():
 if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Task", "Status"])
 if not os.path.exists(NOTE):
        with open(NOTE,'w', newline='', encoding='utf-8') as file:
            wo = csv.writer(file)
            wo.writerow(["Id", "Note text", "Created at"])



def add_task(task):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([task, "Pending"])
    speak("Task is created")

def show_tasks():
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)

        count = 0
        print("\nTasks:")
        for row in reader:
            count += 1
            print(f"{count}. {row[0]} - {row[1]}")

        speak(f"Total {count} tasks found")

def complete_task(task_name):
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows[1:]:
        if row[0].lower() == task_name.lower():
            row[1] = "Completed"

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    speak("Task marked as completed")

def delete_task(task_name):
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    new_rows = [rows[0]]

    for row in rows[1:]:
        if row[0].lower() != task_name.lower():
            new_rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_rows)

    speak("Task is deleted")

# Greeting
#speak("Hello. How can I help you?")

    
def get_nextid():            #auto incrementation of id function
    if not os.path.exists(NOTE):
        return 1
    with open(NOTE,'r', encoding='utf-8') as file:
        ro = csv.reader(file)
        lines = list(ro)
        if len(lines) <= 1:
            return 1
        last_id = int(lines[-1][0])
        return last_id + 1

def take_note(text):        # taking note function
    if not text.strip():
        return "Note text cannot be empty."        
    create_files()
    note_id = get_nextid()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(NOTE,'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([note_id, text, timestamp])
        
    return "Assistant: Note saved successfully" 

def show_notes():      #showing note function
    if not os.path.exists(NOTE):
        speak("Assistant: No notes found.")
        return
        
    with open(NOTE,'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Skip header
        note_list = list(reader)
        if not note_list:
            speak("Assistant: No notes found.")
            return
            
        print("\nSaved notes:")
        for row in note_list:
            print(f"ID: {row[0]} | NOTE: {row[1]} | SAVED ON: {row[2]}")
        print()




if __name__ == "__main__":        #main function
    speak("Voice Assistant Active.")



def open_youtube():
   webbrowser.open("https://www.youtube.com")
   speak("Opening Youtube.")   
def open_google():
   webbrowser.open("https://www.google.com")
   speak("Opening Google.")    
def google_search(Search_text): 
   if Search_text == "":
      speak(" Please say what you want to search.")
      return 
   search_url = "https://www.google.com/search?q=" + Search_text.replace(" ", "+")
   webbrowser.open_new_tab(search_url)
   speak(f"Searching Google for {Search_text}")

def tell_Time():
   current_time=datetime.now().strftime("%I:%M,%p")
   speak(f"The Current Time is{current_time}")
def tell_Date():
   current_date=datetime.now().strftime(" %d %B %Y")
   speak(f"Today's Date is{current_date}")
def tell_Day():
   current_day=datetime.now().strftime("%A")
   speak(f"Today is{current_day}")
def show_help():
    print("\n---------- SUPPORTED COMMANDS ----------")
    print("hello siri")
    print("create task complete project")
    print("show tasks")
    print("complete task complete project")
    print("delete task complete project")
    print("take note meeting at 5 pm")
    print("show notes")
    print("what is the time")
    print("what is today's date")
    print("what day is today")
    print("open calculator")
    print("open notepad")
    print("open google")
    print("open youtube")
    print("search python csv tutorial")
    print("stop assistant")
    print("----------------------------------------")

    speak("You can create tasks, show tasks, complete tasks, delete tasks, take notes, show notes, open applications, search Google, and ask for time, date, or day.")

def process_command(command):
 
    if "hello siri" in command or "hello assistant" in command:
        speak("Hello. How can I help you?")

    elif "create task" in command or "add task" in command:
        task = command.replace("create task", "").replace("add task", "").strip()
        add_task(task)

    elif "show tasks" in command:
        show_tasks()

    elif "complete task" in command or "finish task" in command:
        task = command.replace("complete task", "").replace("finish task", "").strip()
        complete_task(task)

    elif "delete task" in command:
        task = command.replace("delete task", "").strip()
        speak("Are you sure? Say yes or no")
        answer = listen()

        if "yes" in answer:
            delete_task(task)
        else:
            speak("Task deletion cancelled")
    #command take note<notes>

    elif "take note" in command:
    #except "take note" all next data extracted here
        note_content = command.replace("take note", "").strip()
        
        if note_content:
            result = take_note(note_content)
            speak(result) # Assistant: Note saved successfully
        else:
            speak("Assistant: What text should I save in the note?")
            #if user only said "take note then we said this
            extra_text = listen()
            if extra_text:
                result = take_note(extra_text)
                speak(result)
         
    #if user say show notes then       
    
    elif "show notes" in command or "show my notes" in command:
        speak("Assistant: Displays all saved notes with ID and timestamp")
        show_notes()
        

    elif "open google" in command:
         open_google()

    elif "open youtube" in command:
        open_youtube()

    elif command.startswith("search "):
        search_text = command.replace("search ", "").strip()
        google_search(search_text)


    elif "what is today's date" in command or "what is the date " in command:  
        tell_Date()

    elif "what day is today" in command:
        tell_Day()
    

    elif "what is the time" in command or "tell me the time" in command:
        tell_Time()

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")   

    # Open Notepad 
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    

    
    
    elif "help" in command or "show help" in command:
        show_help()

    elif (
        "stop assistant" in command
        or command == "stop"
        or command == "exit"
        or command == "quit"
    ):
        speak("Goodbye")
        return False

    
    else:
        speak("Command not recognized. Say help to know available commands.")

    return True
        
create_files()

#speak("Voice assistant started. Say Hello Siri or Hello Assistant.")

running = True

while running:
    voice_command = listen()
    print("Running")
    if voice_command != "":
        running = process_command(voice_command)
