import smtplib
import imaplib


def configure_email_provider():

    providers = {
        "gmail": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_server": "imap.gmail.com"
        },
        "outlook": {
            "smtp_server": "smtp.office365.com",
            "smtp_port": 587,
            "imap_server": "outlook.office365.com"
        },
        "yahoo": {
            "smtp_server": "smtp.mail.yahoo.com",
            "smtp_port": 587,
            "imap_server": "imap.mail.yahoo.com"
        }
    }

    while True:

        provider = input("\nEnter Email Provider (gmail/outlook/yahoo): ").strip().lower()

        if provider in providers:
            print(f"\n{provider.title()} Provider Selected Successfully.")
            return provider, providers[provider]

        print("Invalid Provider. Please enter Gmail, Outlook or Yahoo.")


def provider_login(provider_config):

    while True:

        sender_email = input("Enter Sender Email: ").strip()

        if sender_email:
            break

        print("Email cannot be empty.")

    while True:

        sender_password = input("Enter App Password: ").strip()

        if sender_password:
            break

        print("Password cannot be empty.")

    try:

        smtp = smtplib.SMTP(provider_config["smtp_server"], provider_config["smtp_port"])
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.quit()

        print("SMTP Authentication Successful.")

        return sender_email, sender_password

    except Exception as e:

        print(f"SMTP Authentication Failed : {e}")

        return None, None


def imap_login(provider_config, sender_email, sender_password):

    try:

        mail = imaplib.IMAP4_SSL(provider_config["imap_server"])
        mail.login(sender_email, sender_password)

        return mail

    except Exception as e:

        print(f"IMAP Login Failed : {e}")

        return None