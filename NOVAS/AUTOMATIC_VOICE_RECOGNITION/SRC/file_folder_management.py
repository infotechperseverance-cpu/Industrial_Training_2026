'''
@Module Name : file_folder_management.py

@Description : This module manages the complete workflow of
               file and folder operations. It receives commands
               from command_processing.py, interacts with the
               user, and calls the required operation modules.

@InputParam  : Voice Command

@OutputParam : Operation Status

@Author      : Bhoomi Sapke
'''
import os
from message_handler import *
from voice import speak
from voice_recognition import speech
from search_manager import *
from folder_operations import *
from file_operations import *
import asyncio
import config

def process(command):

    command = command.lower().strip()

    if "create folder" in command:
        create_folder_workflow()

    elif "create file" in command:
        create_file_workflow()

    elif "open folder" in command:
        open_folder_workflow()

    elif "open file" in command:
        open_file_workflow()

    elif "delete folder" in command:
        delete_folder_workflow()

    elif "delete file" in command:
        delete_file_workflow()

    else:
        error("Invalid file or folder command.")


def create_folder_workflow():

    ask("What should be the folder name?")
    folder_name = speech()

    if not folder_name:
        error("No folder name received.")
        return

    folder_name = folder_name.lower().strip()

    ask("Where do you want to create this folder?")
    parent_folder = speech()

    if not parent_folder:
        error("No parent folder received.")
        return

    parent_folder = parent_folder.lower().strip()

    information("Searching for the destination folder...")

    parent_path = find_folder(parent_folder)

    if parent_path:
        confirm("Destination folder found.")

        if create_folder(folder_name, parent_path):
            success("Folder created successfully.")

        else:
            error("Unable to create folder.")

    else:
        error("Parent folder not found.")


def create_file_workflow():

    ask("What should be the file name with extension?")
    file_name = speech()
    if not file_name:
        error("No file name received.")
        return

    file_name = file_name.lower().replace(" dot ", ".")
    ask("Where do you want to create this file?")
    parent_folder = speech()

    if not parent_folder:
        error("No parent folder received.")
        return

    parent_folder = parent_folder.lower().strip()
    information("Searching for the destination folder...")

    parent_path = find_folder(parent_folder)

    if parent_path:
        confirm("Destination folder found.")

        if create_file(file_name, parent_path):
            success("File created successfully.")

        else:
            error("Unable to create file.")

    else:
        error("Parent folder not found.")

def delete_file_workflow():
    '''
    Deletes a file.
    '''

    ask("What is the file name?")
    file_name = speech()
    if not file_name:
        error("No file name received.")
        return

    file_name = file_name.lower().replace(" dot ", ".")
    information("Searching for the file...")

    file_path = find_file(file_name)

    if file_path:
        confirm("File found. Deleting file.")

        if delete_file(file_path):
            success("File deleted successfully.")
        else:
            error("Unable to delete file.")

    else:
        error("File not found.")


def delete_folder_workflow():
    '''
    Deletes a folder.
    '''

    ask("What is the folder name?")
    folder_name = speech()

    if not folder_name:
        error("No folder name received.")
        return

    folder_name = folder_name.lower().strip()
    information("Searching for the folder...")
    folder_path = find_folder(folder_name)
    print("Deleting :", folder_path)
    if folder_path:
        confirm("Folder found. Deleting folder.")
        if delete_folder(folder_path):
            success("Folder deleted successfully.")

        else:
            error("Unable to delete folder.")

    else:
        error("Folder not found.")



def open_file_workflow():

    ask("What is the file name?")
    file_name = speech()

    if not file_name:
        error("No file name received.")
        return

    information("Searching for the file...")

    file_path = find_file(file_name)

    if file_path:
        confirm("File found.")

        if open_file(file_path):
            success("Opening file.")
        else:
            error("Unable to open file.")

    else:
        error("File not found.")


def open_folder_workflow():

    ask("What is the folder name?")
    folder_name = speech()

    if not folder_name:
        error("No folder name received.")
        return

    folder_name = folder_name.lower().strip()
    information("Searching for the folder...")
    folder_path = find_folder(folder_name)

    if folder_path:
        confirm("Folder found. Deleting folder.")
        if open_folder(folder_path):
            success("Opening folder.")
        else:
            error("Unable to open folder.")

    else:
        error("Folder not found.")

