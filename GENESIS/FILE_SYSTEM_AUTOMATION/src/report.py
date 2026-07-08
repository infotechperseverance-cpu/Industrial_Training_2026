import os
import json
import smtplib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file = os.path.join(BASE_DIR, "File_Manager", "file_data.json")
backup = os.path.join(BASE_DIR, "backup_log.json")
REPORT_FILE = os.path.join(BASE_DIR, "weekly_report.json")
# ------------------------------------------------------------------------

# ---------------- Load File Records ----------------

def load_file():
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# ---------------- Load Backup Records ----------------

def load_backup():
    if os.path.exists(backup):
        try:
            with open(backup, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"backups": []}
    return {"backups": []}

# ---------------- Generate Report Data ----------------

def generate_report():
    files = load_file()
    backups = load_backup()

    report = {
        "report_date": datetime.now().strftime("%d-%m-%Y"),
        "report_time": datetime.now().strftime("%H:%M:%S"),
        "file_summary": {
            "total_files": len(files),
            "pdf_files": 0,
            "word_files": 0,
            "excel_files": 0,
            "powerpoint_files": 0,
            "image_files": 0,
            "video_files": 0,
            "audio_files": 0,
            "python_files": 0,
            "java_files": 0,
            "html_files": 0,
            "css_files": 0,
            "javascript_files": 0,
            "other_files": 0
        },
        "backup_summary": {
            "total_backups": len(backups["backups"]),
            "copied_backups": 0,
            "failed_backups": 0,
            "skipped_backups": 0
        },
        "storage_summary": {
            "total_storage_used": 0,
            "largest_file": "",
            "largest_file_size": 0
        },
        "status": "Weekly Health Report Generated"
    }

    largest_size = 0
    total_size = 0

    # ---------- File Summary ----------
    for item in files:
        category = item["category"]
        filename = item["filename"]
        
        path = os.path.join(BASE_DIR, "File_Manager", category, filename)

        if os.path.exists(path):
            size = os.path.getsize(path)
            total_size += size

            if size > largest_size:
                largest_size = size
                report["storage_summary"]["largest_file"] = filename
                report["storage_summary"]["largest_file_size"] = size

        if category == "Documents/PDF":
            report["file_summary"]["pdf_files"] += 1
        elif category == "Documents/Word":
            report["file_summary"]["word_files"] += 1
        elif category == "Documents/Excel":
            report["file_summary"]["excel_files"] += 1
        elif category == "Documents/PowerPoint":
            report["file_summary"]["powerpoint_files"] += 1
        elif category == "Media/Pictures":
            report["file_summary"]["image_files"] += 1
        elif category == "Media/Videos":
            report["file_summary"]["video_files"] += 1
        elif category == "Media/Audio":
            report["file_summary"]["audio_files"] += 1
        elif category == "Programming/Python":
            report["file_summary"]["python_files"] += 1
        elif category == "Programming/Java":
            report["file_summary"]["java_files"] += 1
        elif category == "Programming/HTML":
            report["file_summary"]["html_files"] += 1
        elif category == "Programming/CSS":
            report["file_summary"]["css_files"] += 1
        elif category == "Programming/JavaScript":
            report["file_summary"]["javascript_files"] += 1
        else:
            report["file_summary"]["other_files"] += 1

    report["storage_summary"]["total_storage_used"] = total_size

    # ---------- Backup Summary ----------
    for item in backups["backups"]:
        status = item["status"]

        if status == "Copied":
            report["backup_summary"]["copied_backups"] += 1
        elif status == "Failed":
            report["backup_summary"]["failed_backups"] += 1
        elif status == "Skipped":
            report["backup_summary"]["skipped_backups"] += 1

    return report

# ---------------- Save Weekly Report ----------------

def save_weekly_report(report):
    with open(REPORT_FILE, "w") as file:
        json.dump(report, file, indent=4)

    print("\nWeekly Report Generated Successfully.")
    print("Report Saved As :", REPORT_FILE)


# ---------------- Display Weekly Report ----------------

def display_weekly_report(report):
    print("\n============= WEEKLY HEALTH REPORT =============")
    print("\nReport Date :", report["report_date"])
    print("Report Time :", report["report_time"])

    print("\n----------- File Summary -----------")
    for key, value in report["file_summary"].items():
        print(f"{key.replace('_',' ').title()} : {value}")

    print("\n---------- Backup Summary ----------")
    for key, value in report["backup_summary"].items():
        print(f"{key.replace('_',' ').title()} : {value}")

    print("\n---------- Storage Summary ----------")
    print("Total Storage Used :", report["storage_summary"]["total_storage_used"], "Bytes")
    print("Largest File :", report["storage_summary"]["largest_file"])
    print("Largest File Size :", report["storage_summary"]["largest_file_size"], "Bytes")

    print("\nStatus :", report["status"])
    print("==============================================")


# ---------------- Weekly Health Report ----------------

def weekly_health_report():
    report = generate_report()
    save_weekly_report(report)
    display_weekly_report(report)