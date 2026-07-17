from Classify_file import load_data, main_dir
import os
import zipfile
from flask import Flask, send_file
import socket
import qrcode

def shareqr():

    files = load_data()

    if not files:
        print("No files available to share.")
        return

    # Showing available files
    print("Available Files")
    print("-" * 30)

    for i in range(len(files)):
        print(str(i + 1) + ". " + files[i]["filename"])

    # User can select multiple files
    choice = input("\nEnter file numbers separated by commas: ")
    numbers = choice.split(",")

    selected = []
    file_paths = []

    for num in numbers:
        try:
            index = int(num.strip()) - 1

            if 0 <= index < len(files):
                selected.append(files[index])
            else:
                print(f"Invalid file number: {num}")
        except ValueError:
            print(f"'{num}' is not a valid number.")

    # Accessing file paths
    print("\nSelected Files:")

    # --- 🚀 [पाथ फिक्स] फाईल ज्या फोल्डरमध्ये आहे त्याचा ॲब्सोल्युट पाथ शोधणे ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    for file in selected:
        print(file["filename"])
        
        # main_dir जर पूर्ण पाथ नसेल, तर तो BASE_DIR ला जोडून खात्री करणे
        if not os.path.isabs(main_dir):
            current_main_dir = os.path.join(BASE_DIR, "File_Manager")
        else:
            current_main_dir = main_dir

        path = os.path.join(
            current_main_dir,
            file["category"],
            file["filename"]
        )
        file_paths.append(path)

    # झिप आणि क्यूआर कोड फाईल्स BASE_DIR च्या आत सुरक्षितपणे सेव्ह करणे
    zip_path = os.path.join(BASE_DIR, "SharedFiles.zip")
    qr_path = os.path.join(BASE_DIR, "Share_QR.png")

    zip_file = zipfile.ZipFile(zip_path, "w")

    for file in file_paths:
        if os.path.exists(file):
            zip_file.write(file, os.path.basename(file))
        else:
            print(f"Warning: Physical file not found at {file}")

    zip_file.close()

    # Start Flask server
    app = Flask(__name__)

    @app.route("/download")
    def download():
        return send_file(
            zip_path,
            as_attachment=True
        )

    # Generate share link
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    ip = s.getsockname()[0]
    s.close()

    share_link = "http://" + ip + ":5000/download"
    print("Share Link:", share_link)

    # Generate QR code
    img = qrcode.make(share_link)
    img.save(qr_path)

    print("QR Code Generated Successfully")

    # Start server
    app.run(
        host="0.0.0.0",
        port=5000
    )