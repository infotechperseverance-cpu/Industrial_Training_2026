import os
from Classify_file import load_data, main_dir

def analyze():
    total = 0
    largest = ("", 0)
    file_count = 0

    print("\n========== FILE SIZE DETAILS ==========")

    records = load_data()
    if not records:
        print("\nNo files found.")
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    for item in records:
        if not os.path.isabs(main_dir):
            current_main_dir = os.path.join(BASE_DIR, "File_Manager")
        else:
            current_main_dir = main_dir

        path = os.path.join(
            current_main_dir,
            item["category"],
            item["filename"]
        )

        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                print(f"{item['filename']} : {size} bytes")

                total += size
                file_count += 1

                if size > largest[1]:
                    largest = (item["filename"], size)
        except Exception as e:
            print(f"Error scanning {item['filename']}: {e}")

    print("--------------------------------------")
    print("Total Files       :", file_count)
    print("Total Size        :", total, "Bytes")
    if file_count > 0:
        print("Largest File      :", largest[0])
        print("Largest File Size :", largest[1], "Bytes")
    else:
        print("Largest File      : None")
        print("Largest File Size : 0 Bytes")
    print("--------------------------------------")