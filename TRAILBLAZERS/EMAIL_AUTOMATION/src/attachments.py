import os

MAX_ATTACHMENTS = 25
MAX_FILE_SIZE = 10 * 1024 * 1024      # 10 MB

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc", ".docx",
    ".xls", ".xlsx",
    ".ppt", ".pptx",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".txt",
    ".csv",
    ".zip", ".rar"
}


def get_attachments():

    attachments = []

    while True:

        try:

            count = int(input("Enter Number of Attachments : "))

            if count < 0:
                print("Number of attachments cannot be negative.")

            elif count > MAX_ATTACHMENTS:
                print(f"Maximum {MAX_ATTACHMENTS} attachments are allowed.")

            else:
                break

        except ValueError:
            print("Please enter a valid integer.")

    if count == 0:
        return attachments

    for i in range(1, count + 1):

        while True:

            file_path = input(f"Enter Attachment {i} Path : ").strip()

            file_path = file_path.strip('"').strip("'")
            file_path = os.path.normpath(file_path)

            if not file_path:
                print("File path cannot be empty.")
                continue

            if not os.path.isfile(file_path):
                print("File not found.")
                continue

            extension = os.path.splitext(file_path)[1].lower()

            if extension not in ALLOWED_EXTENSIONS:
                print("Unsupported File Type.")
                continue

            file_size = os.path.getsize(file_path)

            if file_size > MAX_FILE_SIZE:
                print("File size exceeds 10 MB.")
                continue

            absolute_path = os.path.abspath(file_path)

            if absolute_path in attachments:
                print("Duplicate attachment.")
                continue

            attachments.append(absolute_path)

            print("Attachment Added Successfully.")

            break

    return attachments


def attachment_menu():

    choice = input("\nDo you want to attach files? (Y/N) : ").strip().upper()

    if choice == "Y":

        attachments = get_attachments()

        if attachments:

            print("\nSelected Attachments")

            for index, file in enumerate(attachments, start=1):
                print(f"{index}. {os.path.basename(file)}")

        return attachments

    return []