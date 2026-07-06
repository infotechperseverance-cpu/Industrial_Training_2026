"""
=========================================
Main Module
Purpose:
Start the Smart Voice Assistant.
=========================================
"""

import threading
import sys
from authentication import authentication_menu
from speech_recognition_module import listen
from command_processing import process_command
from voice_scheduler import auto_runner
from voice_engine import speak



# ---------------- START SCHEDULER ----------------
def start_scheduler():

    thread = threading.Thread(target=auto_runner, daemon=True)

    thread.start()



def exit_assistant():
    speak("Goodbye.")
    sys.exit()

# ---------------- MAIN ----------------
def main():

    print("===================================")
    print(" SMART VOICE ASSISTANT ")
    print("===================================")

    # User Login
    # Authentication Menu
    current_user = authentication_menu()

    if current_user is None:
        print("Authentication Failed.")

        speak("Authentication failed. Exiting program.")

        return
    speak("Welcome to Smart Voice Assistant.")

    # Start Scheduler
    start_scheduler()

    print("\nAssistant is Ready.\n")

    while True:
        try:
            voice_text = listen()

            if voice_text is None:
                continue

            process_command(voice_text)

        except KeyboardInterrupt:
            speak("Assistant stopped.")
            break

        except Exception as e:
            print(e)
            speak("An unexpected error occurred.")

# ---------------- PROGRAM START ----------------
if __name__ == "__main__":

    main()