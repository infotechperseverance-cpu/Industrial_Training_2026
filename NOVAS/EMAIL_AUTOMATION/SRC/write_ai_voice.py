import json
import speech_recognition as sr
from voice import speak

FILE_NAME = "email_records.json"

'''
@Function Name: store_msg
@Description  : This function store the message in
                valid emil_id 
@inputParam   : memail(email_id)
                u-msg(update message)
@outParam     : NONE
@Author       : Vaishnvi Teli

'''


def store_msg(memail, u_msg):
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            file_contents = json.load(file)

        found = False

        for record in file_contents:
            if ( int(record["email_id"]) == int(memail) and record["status"].lower() == "pending"):
                record["message"] = u_msg
                found = True
                break

        if found:
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(file_contents, file, indent=4)

            print("Message saved successfully.")
            speak("Message saved successfully.")
        else:
            print("Email not found.")

    except FileNotFoundError:
        print("JSON file not found.")

    except json.JSONDecodeError:
        print("Invalid JSON format.")

'''
@Function Name: email
@Description  : This function check valid eamil and status 
                should be pending
@inputParam   : NONE
@outParam     : NONE

'''


def email():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            file_contents = json.load(file)

        if len(file_contents) == 0:
            print("No email records found.")
            return None

        while True:
            try:
                email_id = int(input("Enter Email ID To Write Message: "))
            except ValueError:
                speak("Please enter a valid numeric Email ID.")
                continue

            email_found = False

            for record in file_contents:

                if int(record["email_id"]) == email_id:
                    email_found = True

                    if record["status"].lower() == "pending":
                        return email_id
                    else:
                        print("This email is not in pending status.")
                        speak("This email is not in pending status.")
                        return None

            if not email_found:
                speak("Email ID not found. Please try again.")

    except FileNotFoundError:
        print("JSON file not found.")
        return None

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None
    
'''

@Function Name: message
@Description  : This function is take messge through a voice 
@inputParam   : memail(email_id)
                u-msg(update message)
@outParam     : NONE
@Author       : Vaishnvi Teli

'''
    
def message():
    print("----------- Voice Message Writing -----------")
    speak("Voice Message Writing")

    memail = email()

    if memail is None:
        return

    recognizer = sr.Recognizer()
    all_messages = []

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            print("\nSpeak your message...")
            print("Say 'STOP' anytime to finish.")
            speak("Speak your message. Say stop to finish.")

            try:
                audio = recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=20
                )

                text = recognizer.recognize_google(
                    audio,
                    language="en-IN"
                ).strip()

                print(f"You said : {text}")

                # Stop if STOP appears anywhere
                if "stop" in text.lower():
                    print("Recording stopped.")
                    speak("Recording stopped.")
                    break

                all_messages.append(text)
                speak("Message recorded.")

                choice = input("\nDo you want to add another message? (y/n): ").strip().lower()

                if choice == "n":
                    break

            except sr.UnknownValueError:
                print("Sorry, I could not understand your voice.")
                speak("Sorry, I could not understand your voice.")

            except sr.WaitTimeoutError:
                print("No speech detected.")
                speak("No speech detected.")

            except sr.RequestError:
                print("Speech recognition service unavailable.")
                speak("Speech recognition service unavailable.")
                return

    # No message recorded
    if len(all_messages) == 0:
        print("No message recorded.")
        speak("No message recorded.")
        return

    # Combine all messages
    final_message = "\n".join(all_messages)

    print("\n----------- Final Message -----------")
    print(final_message)

    speak("Your message has been recorded.")

    # Save message
    choice = input("\nDo you want to save this message? (y/n): ").strip().lower()

    if choice == "y":
        store_msg(memail, final_message)
    else:
        print("Message not saved.")
        speak("Message not saved.")