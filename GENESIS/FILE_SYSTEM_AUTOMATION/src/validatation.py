import os
import re

def validate_name(filename):

    invalid_char = r'[\\/:*?"<>|]'

    if not filename:
        print("Filename cannot be empty.")
        return False

    elif re.search(invalid_char, filename):
        print("Filename contains invalid characters.")
        return False

    elif len(filename) > 50:
        print("Filename is too long.")
        return False

    elif os.path.exists(os.path.join(filename)):
        print("File already exists.")
        return False

    return True