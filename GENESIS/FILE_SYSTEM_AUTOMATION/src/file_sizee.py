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

    for item in records:

        path = os.path.join(
            main_dir,
            item["category"],
            item["filename"]
        )

        if os.path.isfile(path):

            size = os.path.getsize(path)

            print(f"{item['filename']} : {size} bytes")

            total += size
            file_count += 1

            if size > largest[1]:
                largest = (item["filename"], size)

    print("--------------------------------------")
    print("Total Files       :", file_count)
    print("Total Size        :", total, "Bytes")
    print("Largest File      :", largest[0])
    print("Largest File Size :", largest[1], "Bytes")
    print("--------------------------------------")
