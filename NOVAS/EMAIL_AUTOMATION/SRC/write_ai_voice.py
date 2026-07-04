import json
import speech_recognition as sr   
from voice import speak       

FILE_NAME = "email_records.json"

def update_msg(u_msg):
  try:

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        file_contents = json.load(file)

        if len(file_contents) == 0:
            print("No email records found.")
            return
    
    file_contents[-1]["message"] = u_msg
    
    with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(file_contents, file, indent=4)

    print("Message saved successfully.")

  except FileNotFoundError:
        print("JSON file not found.")

  except json.JSONDecodeError:
        print("Invalid JSON format.")
    

def message():

    speak("\n----------- Voice Meassage Writing -------------")
    recognizer = sr.Recognizer()


    with sr.Microphone() as source:
       text1 = "Speak your Message..."
       speak(text1)
       recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise

       audio = recognizer.listen(source)

    try:
    # Convert speech to text
       text2 = recognizer.recognize_google(audio , language="en-IN")
      
       speak("You Said:")
       speak(text2)


       choice = input("Do you want to save this message? (y/n): ").lower()
       if choice == "y":
           update_msg(text2)
           return
       else:
           speak("Message not save")

    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")

    except sr.RequestError:
         print("Could not connect to the speech recognition service.")

    