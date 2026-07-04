from Classify_file import load_data,main_dir
import os
import zipfile
from flask import Flask, send_file
import socket
import qrcode

def shareqr():

    files = load_data()

    #Showing available files

    print("Available Files")
    print("-" * 30)

    for i in range(len(files)):
        print(str(i + 1) + ". " + files[i]["filename"])

    #User can select multiple files

    choice = input("\nEnter file numbers separated by commas: ")

    numbers = choice.split(",")

    selected = []
    file_paths = []

    for num in numbers:
        index = int(num) - 1
        selected.append(files[index])

    #Accessing file paths

    print("\nSelected Files:")

    for file in selected:
        print(file["filename"])
        path = os.path.join(
            main_dir,
            file["category"],
            file["filename"]
        )
        file_paths.append(path)

    zip_file = zipfile.ZipFile("SharedFiles.zip", "w")

    for file in file_paths:
        zip_file.write(file, os.path.basename(file))

    zip_file.close()

    # Start Flask server
    app = Flask(__name__)

    @app.route("/download")
    def download():
        return send_file(
            "SharedFiles.zip",
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
    img.save("Share_QR.png")

    print("QR Code Generated Successfully")

    # Start server
    app.run(
        host="0.0.0.0",
        port=5000
    )