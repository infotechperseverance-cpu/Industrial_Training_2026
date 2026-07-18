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
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "w"):
            pass

        return True

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False


def delete_file(file_path):
    '''
    Deletes a file.
    '''
    try:
        os.remove(file_path)
        return True

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False


def open_file(file_path):
    '''
    Opens a file.
    '''
    try:
        os.startfile(file_path)
        return True

    except Exception as e:
        asyncio.run(print("Error :", e))
        asyncio.run(speak("Error :", e))
        return False