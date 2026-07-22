'''
@Module Name : file_operations.py

@Description : This module performs file-related operations.

@InputParam  : File name, Folder path / File path

@OutputParam : Status

@Author      : Bhoomi Sapke
'''

import os
from voice import speak
import asyncio

def create_file(file_name, folder_path):
    '''
    Creates a new file.
    '''
    try:

        if not file_name or not folder_path:
            return False

        # Convert spoken filename
        file_name = (
            file_name.lower()
            .strip()
            .replace(" dot ", ".")
            .replace(" underscore ", "_")
        )

        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w", encoding="utf-8"):
            pass

        return True

    except Exception as e:

        print("Error :", e)

        asyncio.run(
            speak("Unable to create the file.")
        )

        return False

def delete_file(file_path):
    '''
    Deletes a file after user confirmation.
    '''
    try:

        from voice_recognition import speech
        from config import YES_WORDS, NO_WORDS

        file_name = os.path.basename(file_path)

        asyncio.run(
            speak(
                f"Are you sure you want to delete {file_name}? Please say yes or no."
            )
        )

        answer = speech()

        if not answer:
            asyncio.run(speak("Deletion cancelled."))
            return False

        answer = answer.lower().strip()

        if any(word in answer for word in YES_WORDS):

            os.remove(file_path)

            # asyncio.run(
            #     speak("File deleted successfully.")
            # )

            return True

        elif any(word in answer for word in NO_WORDS):

            asyncio.run(
                speak("Deletion cancelled.")
            )

            return False

        else:

            asyncio.run(
                speak("Please answer with yes or no.")
            )

            return False

    except Exception as e:

        print("Error :", e)

        asyncio.run(
            speak("Unable to delete the file.")
        )

        return False


def open_file(file_path):
    '''
    Opens a file.
    '''
    try:
        os.startfile(file_path)
        return True

    except Exception as e:
        print("Error :", e)
        asyncio.run(speak(f"Error: {e}"))
        return False