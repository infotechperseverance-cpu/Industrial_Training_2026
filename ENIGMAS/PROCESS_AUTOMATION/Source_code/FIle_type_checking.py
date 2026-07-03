from pathlib import Path
"""this function get file path and file type name
ex. check_file_type("D:\Harsh\task6_B.docx") written  word document then you can print
if in case any error it written false"""

file_types = {
    ".txt": "Text File",
    ".csv": "CSV File",
    ".json": "JSON File",
    ".xml": "XML File",
    ".html": "HTML File",
    ".py": "Python File",
    ".pdf": "PDF Document",
    ".doc": "Word Document",          #check all extensions 
    ".docx": "Word Document",
    ".xls": "Excel Spreadsheet",
    ".xlsx": "Excel Spreadsheet",
    ".ppt": "PowerPoint Presentation",
    ".pptx": "PowerPoint Presentation",
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".png": "PNG Image",
    ".gif": "GIF Image",
    ".bmp": "Bitmap Image",
    ".mp3": "MP3 Audio",
    ".wav": "WAV Audio",
    ".mp4": "MP4 Video",
    ".avi": "AVI Video",
    ".zip": "ZIP Archive",
    ".rar": "RAR Archive",
    ".7z": "7-Zip Archive",
    ".exe": "Executable File"
}


def check_file_type(file_path):

    try:

        # Input validation
        if file_path is None or file_path.strip() == "":
            print("Error : File path is required")
            return False

        # Remove spaces and quotes
        file_path = file_path.strip()
        file_path = file_path.strip('"').strip("'")

        # Convert '\' to '/'
        file_path = file_path.replace("\\", "/")

        # Create Path object
        file_path = Path(file_path)

        # Validation
        if not file_path.exists():
            print("Error : File does not exist")
            return False

        if not file_path.is_file():
            print("Error : Path is not a file")
            return False

        # Get extension
        extension = file_path.suffix.lower()

        # Return only file type
        if extension in file_types:
            return file_types[extension]

        return "Unknown / Valid File"

    except PermissionError:
        print("Error : Permission denied")
        return False

    except FileNotFoundError:
        print("Error : File not found")
        return False

    except OSError as e:
        print("Error :", e)
        return False

    except Exception as e:
        print("Unexpected Error :", e)
    return False

#####################################End############################################