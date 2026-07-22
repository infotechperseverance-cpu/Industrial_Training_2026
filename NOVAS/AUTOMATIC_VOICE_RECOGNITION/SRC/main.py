"""
@Module Name : main.py

@Description : Entry point of the NOVA Voice Assistant.
               Initializes the GUI and starts the
               voice command processing in the background.

@Author : Bhoomi Sapke
"""

import threading
from gui import NovaGUI
from reminder import start_reminder_service
from command_processing import process_command


def main():

    start_reminder_service()

    gui = NovaGUI()

    threading.Thread(
        target=process_command,
        daemon=True
    ).start()

    gui.run()


if __name__ == "__main__":
    main()