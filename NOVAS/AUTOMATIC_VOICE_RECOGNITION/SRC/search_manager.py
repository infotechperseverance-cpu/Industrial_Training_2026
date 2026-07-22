'''
@Module Name : search_operations.py

@Description : This module searches files and folders from the
               default search locations and returns their
               complete path.

@InputParam  : File Name / Folder Name

@OutputParam : Complete File / Folder Path

@Author      : Bhoomi Sapke
'''

import os
import asyncio

from config import DEFAULT_SEARCH_PATHS
from voice import speak


def normalize_name(name):
    '''
    Normalizes spoken file or folder names.
    '''
    return (
        name.lower()
            .strip()
            .replace(" dot ", ".")
            .replace(" underscore ", "_")
    )


def find_file(file_name):
    '''
    Searches for a file and returns its complete path.
    '''
    try:

        if not file_name:
            return None

        file_name = normalize_name(file_name)

        matches = []

        for search_path in DEFAULT_SEARCH_PATHS:

            if not os.path.exists(search_path):
                continue

            for root, directories, files in os.walk(search_path):

                for file in files:

                    # Exact Match
                    if file.lower() == file_name:
                        return os.path.join(root, file)

                    # Partial Match
                    if file_name in file.lower():
                        matches.append(
                            os.path.join(root, file)
                        )

        # Return only if exactly one partial match exists
        if len(matches) == 1:
            return matches[0]

        return None

    except Exception as e:

        print(f"Search Error: {e}")

        asyncio.run(
            speak(
                "An error occurred while searching the file."
            )
        )

        return None


def find_folder(folder_name):
    '''
    Searches for a folder and returns its complete path.
    '''
    try:

        if not folder_name:
            return None

        folder_name = normalize_name(folder_name)

        # Check default folders first
        for search_path in DEFAULT_SEARCH_PATHS:

            if not os.path.exists(search_path):
                continue

            if os.path.basename(search_path).lower() == folder_name:
                return search_path

        matches = []

        # Recursive Search
        for search_path in DEFAULT_SEARCH_PATHS:

            if not os.path.exists(search_path):
                continue

            for root, directories, files in os.walk(search_path):

                for directory in directories:

                    # Exact Match
                    if directory.lower() == folder_name:
                        return os.path.join(root, directory)

                    # Partial Match
                    if folder_name in directory.lower():
                        matches.append(
                            os.path.join(root, directory)
                        )

        # Return only if exactly one partial match exists
        if len(matches) == 1:
            return matches[0]

        return None

    except Exception as e:

        print(f"Search Error: {e}")

        asyncio.run(
            speak(
                "An error occurred while searching the folder."
            )
        )

        return None