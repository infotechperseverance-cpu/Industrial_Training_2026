import os
import mimetypes

def add_attachments_to_email(email_message, attachments):

    if not attachments:
        return

    if isinstance(attachments, str):
        attachments = [a.strip() for a in attachments.split(",") if a.strip()]

    for attachment in attachments:

        if not os.path.exists(attachment):
            print(f"Attachment not found: {attachment}")
            continue

        mime_type, _ = mimetypes.guess_type(attachment)

        if mime_type:
            maintype, subtype = mime_type.split("/")
        else:
            maintype, subtype = "application", "octet-stream"

        with open(attachment, "rb") as file:

            email_message.add_attachment(
                file.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(attachment)
            )