from email.message import EmailMessage

from utils import send_with_retry, add_attachments


def retry_failed_email(provider,
                       provider_config,
                       sender_email,
                       sender_password,
                       receiver_email,
                       subject,
                       body,
                       attachments):

    msg = EmailMessage()

    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.set_content(body)

    if attachments:
        msg = add_attachments(msg, attachments)

    print(f"\nRetrying Email To : {receiver_email}")

    return send_with_retry(
        msg,
        sender_email,
        sender_password,
        provider_config["smtp_server"],
        provider_config["smtp_port"],
        provider
    )


def retry_multiple_failed_emails(provider,
                                 provider_config,
                                 sender_email,
                                 sender_password,
                                 failed_recipients,
                                 subject,
                                 body,
                                 attachments):

    if not failed_recipients:

        print("\nNo Failed Emails Found.")

        return

    print("\nRetrying Failed Emails...\n")

    success = 0
    failed = 0

    for receiver_email in failed_recipients:

        sent = retry_failed_email(
            provider,
            provider_config,
            sender_email,
            sender_password,
            receiver_email,
            subject,
            body,
            attachments
        )

        if sent:
            success += 1
        else:
            failed += 1

    print("\n====================================")
    print("        RETRY SUMMARY")
    print("====================================")
    print(f"Retried Successfully : {success}")
    print(f"Retry Failed         : {failed}")
    print("====================================")