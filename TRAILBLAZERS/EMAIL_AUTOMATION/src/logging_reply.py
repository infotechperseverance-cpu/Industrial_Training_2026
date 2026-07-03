import csv
import os
import imaplib
import email

from datetime import datetime
from email.utils import parseaddr


# --------------------------------------------------
# Log Email Activity
# --------------------------------------------------

def log_email(receiver_email,
              subject,
              action,
              status):

    file_exists = os.path.exists("email_logs.csv")

    with open(
        "email_logs.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "Email Address",
                    "Subject",
                    "Action",
                    "Status",
                    "Date",
                    "Time"
                ]
            )

        current_datetime = datetime.now()

        writer.writerow(
            [
                receiver_email,
                subject,
                action,
                status,
                current_datetime.strftime("%d-%m-%Y"),
                current_datetime.strftime("%H:%M:%S")
            ]
        )


# --------------------------------------------------
# Load Successfully Sent Emails
# --------------------------------------------------

def load_successful_receivers():

    successful_receivers = set()

    if not os.path.exists("email_logs.csv"):

        return successful_receivers

    try:

        with open(
            "email_logs.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (
                    row["Action"].strip().lower() == "sent"
                    and
                    row["Status"].strip().lower() == "success"
                ):

                    successful_receivers.add(
                        row["Email Address"].strip().lower()
                    )

    except Exception as e:

        print(f"Error Reading Log File : {e}")

    return successful_receivers


# --------------------------------------------------
# Read Replies
# --------------------------------------------------

def read_replies(sender_email,
                 sender_password):

    replies = []

    successful_receivers = load_successful_receivers()

    if not successful_receivers:

        print("No Sent Email Records Found.")

        return replies

    try:

        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:

            mail.login(
                sender_email,
                sender_password
            )

            status, _ = mail.select("INBOX")

            if status != "OK":

                print("Unable to Open Inbox.")

                return replies

            status, data = mail.search(
                None,
                "ALL"
            )

            if status != "OK":

                print("Unable to Read Inbox.")

                return replies

            # Read only latest 50 emails

            email_ids = data[0].split()
            print(f"Total Emails Found : {len(email_ids)}")

            email_ids.reverse()

            email_ids = email_ids[:50]
            print(f"Checking {len(email_ids)} Emails...")

            for email_id in email_ids:

                status, msg_data = mail.fetch(
                    email_id,
                    "(RFC822)"
                )

                if status != "OK":

                    continue

                for response in msg_data:

                    if not isinstance(
                        response,
                        tuple
                    ):

                        continue

                    msg = email.message_from_bytes(
                        response[1]
                    )

                    sender = parseaddr(
                        msg.get(
                            "From",
                            ""
                        )
                    )[1].lower()

                    print(f"\nSender  : {sender}")
                    print(f"Subject : {subject}")

                    subject = msg.get(
                        "Subject",
                        ""
                    ).strip()

                    if sender not in successful_receivers:
                        print("Ignored (Sender not in sent list)")

                        continue

                    lower_subject = subject.lower()

                    if not (
                        lower_subject.startswith("re:")
                        or lower_subject.startswith("aw:")
                        or lower_subject.startswith("sv:")
                        or lower_subject.startswith("fw:")
                    ):

                        continue

                    body = ""
                    # ------------------------------------
                    # Read Email Body
                    # ------------------------------------

                    if msg.is_multipart():

                        for part in msg.walk():

                            if (
                                    part.get_content_type() == "text/plain"
                                    and not part.get("Content-Disposition")
                            ):

                                payload = part.get_payload(
                                    decode=True
                                )

                                if payload:
                                    body = payload.decode(
                                        errors="ignore"
                                    )

                                    break

                    else:

                        payload = msg.get_payload(
                            decode=True
                        )

                        if payload:
                            body = payload.decode(
                                errors="ignore"
                            )

                    replies.append(
                        {
                            "from": sender,
                            "subject": subject,
                            "date": msg.get(
                                "Date",
                                ""
                            ),
                            "message": body.strip()
                        }
                    )



        return replies

    except imaplib.IMAP4.error as e:

        print(e)

        return []

    except Exception as e:

        print(f"\nFailed to Read Replies : {e}")

        return []


# --------------------------------------------------
# Display Replies
# --------------------------------------------------

def display_replies(sender_email,
                    sender_password):
    replies = read_replies(
        sender_email,
        sender_password
    )

    print(f"\nReplies Found : {len(replies)}")

    successful_receivers = load_successful_receivers()

    replied_emails = set()

    print("\n==================================================")
    print("              REPLIES RECEIVED")
    print("==================================================")

    if replies:

        displayed = set()

        for reply in replies:

            if reply["from"] in displayed:
                continue

            displayed.add(
                reply["from"]
            )

            replied_emails.add(
                reply["from"]
            )

            print("\n--------------------------------------------------")
            print(f"From    : {reply['from']}")
            print(f"Subject : {reply['subject']}")
            print(f"Date    : {reply['date']}")
            print("--------------------------------------------------")
            print(reply["message"])
            print("--------------------------------------------------")

            log_email(
                reply["from"],
                reply["subject"],
                "Received",
                "Success"
            )

    else:

        print("No Replies Received.")

    pending_replies = (
            successful_receivers
            - replied_emails
    )

    print("\n==================================================")
    print("             PENDING REPLIES")
    print("==================================================")

    if pending_replies:

        for receiver_email in sorted(
                pending_replies
        ):
            print(receiver_email)

    else:

        print("Everyone has replied.")

    print("==================================================")


# --------------------------------------------------
# View Email Logs
# --------------------------------------------------

def view_logs():
    if not os.path.exists(
            "email_logs.csv"
    ):
        print("\nNo Email Logs Found.")

        return

    print("\n==============================================================")
    print("                     EMAIL LOGS")
    print("==============================================================")

    try:

        with open(
                "email_logs.csv",
                "r",
                newline="",
                encoding="utf-8"
        ) as file:

            reader = csv.reader(file)

            for row in reader:
                print(" | ".join(row))

    except Exception as e:

        print(f"Unable to Read Logs : {e}")

    print("==============================================================")