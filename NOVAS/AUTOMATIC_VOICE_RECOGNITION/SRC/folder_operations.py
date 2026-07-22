'''
@Module Name : folder_operations.py

@Description : This module performs folder-related operations
               such as creating, deleting, and opening folders.

@InputParam  : Folder Name, Parent Path / Folder Path

@OutputParam : Operation Status

@Author      : Bhoomi Sapke
'''
import os
import shutil
import asyncio
from voice import speak

def create_folder(folder_name, parent_path):
    '''
    Creates a new folder.
    '''
    try:
        folder_path = os.path.join(parent_path, folder_name)
        os.mkdir(folder_path)
        return True

    except FileExistsError:
        asyncio.run(speak("Folder already exists."))
        print("Folder already exists.")
        return False

    except Exception as e:
        print("Error :", e)
        asyncio.run(speak(f"Error: {e}"))
        return False

def delete_folder(folder_path):
    '''
    Deletes a folder after user confirmation.
    '''
    try:

        from voice_recognition import speech
        from config import YES_WORDS, NO_WORDS

        folder_name = os.path.basename(folder_path)

        asyncio.run(
            speak(
                f"Are you sure you want to delete {folder_name}? Please say yes or no."
            )
        )

        answer = speech()

        if not answer:
            asyncio.run(
                speak("Deletion cancelled.")
            )
            return False

        answer = answer.lower().strip()

        if any(word in answer for word in YES_WORDS):

            shutil.rmtree(folder_path)

            asyncio.run(
                speak("Folder deleted successfully.")
            )

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
            speak("Unable to delete the folder.")
        )

        return False

def open_folder(folder_path):
    '''
    Opens a folder.
    '''
    try:
        os.startfile(folder_path)
        return True

    except Exception as e:
        print("Error :", e)
        asyncio.run(speak(f"Error: {e}"))        
        return False