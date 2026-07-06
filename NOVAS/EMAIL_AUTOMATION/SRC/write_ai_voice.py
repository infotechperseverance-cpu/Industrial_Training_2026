import json
import speech_recognition as sr
from email_management import validate_email
from voice import speak

FILE_NAME = "email_records.json"


def store_msg(memail, u_msg):
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            file_contents = json.load(file)

        found = False

        for record in file_contents:
            if ( record["email_id"] == memail and record["status"].lower() == "pending"):
                record["message"] = u_msg
                found = True
                break

        if found:
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(file_contents, file, indent=4)

            speak("Message saved successfully.")
        else:
            speak("Email not found.")

    except FileNotFoundError:
        speak("JSON file not found.")

    except json.JSONDecodeError:
        speak("Invalid JSON format.")


def email():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            file_contents = json.load(file)

        if len(file_contents) == 0:
            speak("No email records found.")
            return None

        while True:
            try:
                email_id = int(input("Enter Email ID To Write Message: "))
            except ValueError:
                speak("Please enter a valid numeric Email ID.")
                continue

            email_found = False

            for record in file_contents:

                if record["email_id"] == email_id:
                    email_found = True

                    if record["status"].lower() == "pending":
                        return email_id
                    else:
                        speak("This email is not in pending status.")
                        return None

            if not email_found:
                speak("Email ID not found. Please try again.")

    except FileNotFoundError:
        speak("JSON file not found.")
        return None

    except json.JSONDecodeError:
        speak("Invalid JSON format.")
        return None
    

def message():
    speak("----------- Voice Message Writing -----------")

    memail = email()

    if memail is None:
        return

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("Speak your message...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="en-IN")

        speak("You said:")
        speak(text)

        choice = input("Do you want to save this message? (y/n): ").lower()

        if choice == "y":
            store_msg(memail, text)
        else:
            speak("Message not saved.")

    except sr.UnknownValueError:
        speak("Sorry, I could not understand your voice.")

    except sr.RequestError:
        speak("Could not connect to the speech recognition service.")
