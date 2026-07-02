from authentication import authenticate_user
from provider import configure_email_provider, provider_login
from compose_email import create_email
from attachments import attachment_menu
from email_processing import process_csv_emails
from scheduler import schedule_email
from templates import template_menu
from logging_reply import display_replies
from logging_reply import view_logs


def main():

    print("=" * 50)
    print("      EMAIL AUTOMATION SYSTEM")
    print("=" * 50)

    if not authenticate_user():
        return

    print("\nWelcome to the Email Automation System.")

    provider = None
    provider_config = None
    sender_email = None
    sender_password = None

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Configure Email Provider")
        print("2. Send Emails")
        print("3. Schedule Emails")
        print("4. Manage Templates")
        print("5. View Email Logs")
        print("6. Read Replies")
        print("7. Exit")

        choice = input("Enter Choice : ").strip()

        match choice:

            # ---------------------------------------------------

            case "1":

                provider, provider_config = configure_email_provider()

                sender_email, sender_password = provider_login(provider_config)

                if sender_email is None:
                    provider = None
                    provider_config = None

            # ---------------------------------------------------

            case "2":

                if provider is None:

                    print("Please Configure Email Provider First.")

                    continue

                msg, subject, body = create_email()

                if msg is None:
                    continue

                attachments = attachment_menu()

                process_csv_emails(
                    provider,
                    provider_config,
                    sender_email,
                    sender_password,
                    msg,
                    subject,
                    body,
                    attachments
                )

            # ---------------------------------------------------

            case "3":

                if provider is None:

                    print("Please Configure Email Provider First.")

                    continue

                msg, subject, body = create_email()

                if msg is None:
                    continue

                attachments = attachment_menu()

                schedule_email(
                    provider,
                    provider_config,
                    sender_email,
                    sender_password,
                    subject,
                    body,
                    attachments
                )

            # ---------------------------------------------------

            case "4":

                template_menu()

            # ---------------------------------------------------

            case "5":

                view_logs()

            # ---------------------------------------------------

            case "6":

                if provider is None:

                    print("Please Configure Email Provider First.")

                    continue

                display_replies(
                    sender_email,
                    sender_password
                )
            # ---------------------------------------------------

            case "7":

                print("\nThank You for Using Email Automation System.")

                break

            # ---------------------------------------------------

            case _:

                print("Invalid Choice.")


if __name__ == "__main__":

    main()