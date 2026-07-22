import os
import shutil


class AutomaticFileClassification:

    '''
    @Function Name : __init__

    @Description   : Initializes classification folder and creates
                     required category folders.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def __init__(self):
        self.classification_folder = os.path.join(os.getcwd(), "Classification")
        self.create_classification_folders()

    '''
    @Function Name : create_classification_folders

    @Description   : Creates Classification folder and all category
                     folders if they do not already exist.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def create_classification_folders(self):

        folders = ["PDF", "WORD", "EXCEL", "PPT", "IMAGE", "VIDEO", "AUDIO", "ARCHIVE", "TEXT", "EXECUTABLE", "OTHERS"]

        os.makedirs(self.classification_folder, exist_ok=True)

        for folder in folders:
            os.makedirs(os.path.join(self.classification_folder, folder), exist_ok=True)

    '''
    @Function Name : get_category

    @Description   : Returns category according to file extension.

    @InputParam    : extension

    @OutParam      : Category Name

    @Author        : Srushti Subhash Mahajan
    '''

    def get_category(self, extension):

        mapping = {
            ".pdf": "PDF",
            ".doc": "WORD",
            ".docx": "WORD",
            ".xls": "EXCEL",
            ".xlsx": "EXCEL",
            ".ppt": "PPT",
            ".pptx": "PPT",
            ".jpg": "IMAGE",
            ".jpeg": "IMAGE",
            ".png": "IMAGE",
            ".gif": "IMAGE",
            ".bmp": "IMAGE",
            ".mp4": "VIDEO",
            ".avi": "VIDEO",
            ".mkv": "VIDEO",
            ".mp3": "AUDIO",
            ".wav": "AUDIO",
            ".zip": "ARCHIVE",
            ".rar": "ARCHIVE",
            ".7z": "ARCHIVE",
            ".txt": "TEXT",
            ".exe": "EXECUTABLE"
        }

        return mapping.get(extension.lower(), "OTHERS")

    '''
    @Function Name : destination_exists

    @Description   : Checks whether file already exists in the
                     destination folder.

    @InputParam    : destination_path

    @OutParam      : True / False

    @Author        : Srushti Subhash Mahajan
    '''

    def destination_exists(self, destination_path):
        return os.path.exists(destination_path)
    
    '''
    @Function Name : get_unique_filename
    @Description   : Generates a unique filename if the same file
                 already exists in the destination folder.
    @InputParam    : destination_folder
                 file_name
    @OutParam      : Unique file path
    @Author        : Srushti Subhash Mahajan
    '''
    def get_unique_filename(self, destination_folder, file_name):

     name, extension = os.path.splitext(file_name)

     destination_path = os.path.join(destination_folder, file_name)

     count = 1

     while os.path.exists(destination_path):

        new_name = "{}_{}{}".format(name, count, extension)

        destination_path = os.path.join(destination_folder, new_name)

        count += 1

     return destination_path
    
    '''
    @Function Name : classify_from_folder

    @Description   : Classifies files from the selected folder into
                     category folders.

    @InputParam    : folder_path
                     operation (copy/move)

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def classify_from_folder(self, folder_path, operation):

        if not os.path.exists(folder_path):
            print("\nInvalid Folder Path.")
            return

        classified = 0
        skipped = 0

        print("\n" + "=" * 70)
        print(f"{'File Name':<35} {'':<6} Classified Folder")
        print("=" * 70)

        for root, dirs, files in os.walk(folder_path):

            dirs[:] = [directory for directory in dirs if directory != "Classification"]

            for file_name in files:

                original_path = os.path.join(root, file_name)

                extension = os.path.splitext(file_name)[1]
                category = self.get_category(extension)

                destination_folder = os.path.join(self.classification_folder, category)
                destination_path = self.get_unique_filename(destination_folder,file_name)
    
                try:

                    if operation == "copy":
                        shutil.copy2(original_path, destination_path)
                    else:
                        shutil.move(original_path, destination_path)

                    classified += 1
                    print(f"{file_name: <35} {'->': ^6} {category}")

                except Exception as error:
                    print(f"Error while classifying {file_name}")
                    print(error)

        print("\nClassification Completed Successfully.")
        print(f"Total Classified : {classified}")
        print(f"Skipped          : {skipped}")

    '''
    @Function Name : get_operation

    @Description   : Allows user to select Copy or Move operation.

    @InputParam    : NONE

    @OutParam      : copy / move

    @Author        : Srushti Subhash Mahajan
    '''

    def get_operation(self):

        while True:

            print("\n========== Select Operation ==========")
            print("1. Copy Files")
            print("2. Move Files")

            choice = input("\nEnter Choice : ").strip()

            if choice == "1":
                return "copy"
            elif choice == "2":
                return "move"
            else:
                print("\nInvalid Choice. Please Try Again.")

    '''
    @Function Name : view_classification_summary

    @Description   : Displays category-wise classified file count.

    @InputParam    : NONE

    @OutParam      : NONE

    @Author        : Srushti Subhash Mahajan
    '''

    def view_classification_summary(self):

        print("\n========== Classification Summary ==========")

        folders = ["PDF", "WORD", "EXCEL", "PPT", "IMAGE", "VIDEO", "AUDIO", "ARCHIVE", "TEXT", "EXECUTABLE", "OTHERS"]

        total_files = 0

        for folder in folders:

            folder_path = os.path.join(self.classification_folder, folder)

            if os.path.exists(folder_path):
                count = len([file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))])
            else:
                count = 0

            print(f"{folder:<12} : {count} File(s)")
            total_files += count

        print("============================================")
        print(f"Total Files : {total_files}")

def main():

    classifier = AutomaticFileClassification()

    while True:

        print("\n==================================================")
        print("        AUTOMATIC FILE CLASSIFICATION")
        print("==================================================")
        print("1. Classify Files")
        print("2. View Classification Summary")
        print("3. Exit")

        choice = input("\nEnter Your Choice : ").strip()

        if choice == "1":

            folder_path = input("\nEnter Folder Path : ").strip()

            if folder_path == "":
                print("\nFolder path cannot be empty.")
                continue

            if not os.path.isdir(folder_path):
                print("\nInvalid Folder Path.")
                continue

            operation = classifier.get_operation()

            try:
                classifier.classify_from_folder(folder_path, operation)
            except Exception as error:
                print(f"\nError : {error}")

        elif choice == "2":

            classifier.view_classification_summary()

        elif choice == "3":

            print("\nThank You For Using Automatic File Classification.")
            print("Program Closed Successfully.")
            break

        else:

            print("\nInvalid Choice. Please Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()