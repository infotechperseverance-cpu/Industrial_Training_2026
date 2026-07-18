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
        asyncio.run(print("Folder already exists."))
        return False

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False


def delete_folder(folder_path):
    '''
    Deletes a folder.
    '''
    try:
        shutil.rmtree(folder_path)
        return True

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False


def open_folder(folder_path):
    '''
    Opens a folder.
    '''
    try:
        os.startfile(folder_path)
        return True

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False