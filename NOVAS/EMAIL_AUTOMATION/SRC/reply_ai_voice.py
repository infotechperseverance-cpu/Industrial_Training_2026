import imaplib        
from email.utils import parseaddr
import email            
from email.header import decode_header
import time             
from voice import speak

def login_gmail(sender_email, sender_password):

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

    mail.login(sender_email, sender_password)

    mail.select("INBOX")

    return mail

def check_new_email(mail):

    status, messages = mail.search(None, "UNSEEN")

    email_id = messages[0].split()

    if len(email_id) == 0:
        return None

    return email_id[-1]


def read_email(mail, email_id):

    status, msg_data = mail.fetch(email_id, "(RFC822)")

    for response in msg_data:

        if isinstance(response, tuple):

            msg = email.message_from_bytes(response[1])

          
            name, email_address = parseaddr(msg.get("From"))

            if name:
              sender = name
            else:
                sender = email_address

        
            subject = msg.get("Subject")

            if subject:
                subject, encoding = decode_header(subject)[0]

                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
            else:
                subject = "No Subject"

          
            message = ""

            if msg.is_multipart():

                for part in msg.walk():

                    content_type = part.get_content_type()
                    disposition = str(part.get("Content-Disposition"))

                    if content_type == "text/plain" and "attachment" not in disposition:

                        payload = part.get_payload(decode=True)

                        if payload:
                            message = payload.decode(errors="ignore")

                        break

            else:

                payload = msg.get_payload(decode=True)

                if payload:
                    message = payload.decode(errors="ignore")

            if message.strip() == "":
                message = "Email body is empty."

            if "\nOn " in message:
                message = message.split("\nOn ")[0]


            clean_message = []

            for line in message.splitlines():

             if line.strip().startswith(">"):
                 break

             clean_message.append(line)

            message = "\n".join(clean_message).strip()


            return sender, subject, message

    return None, None, None

def announce_email(sender, subject, message):

    text = "You have received a new email."

    print("\n📧", text)

    if sender:
        text += f" From {sender}."

    if subject:
        text += f" Subject {subject}."

    if message:
        text += f" Message. {message}"

    speak(text)

def monitor_inbox(sender_email, sender_password):

    mail = login_gmail(sender_email, sender_password)

  
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    if email_ids:
        last_email_id = email_ids[-1]
    else:
        last_email_id = None

  

    while True:

        mail.select("INBOX")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        if email_ids:

            current_email_id = email_ids[-1]

            # Only if a NEW email has arrived
            if current_email_id != last_email_id:

                last_email_id = current_email_id

                sender, subject, message = read_email(mail, current_email_id)

            
                announce_email(sender, subject, message)

        time.sleep(5)