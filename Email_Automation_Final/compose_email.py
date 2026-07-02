from email.message import EmailMessage

from templates import view_templates, load_template, generate_email


def create_email():

    msg = EmailMessage()

    print("\n==============================")
    print("      COMPOSE EMAIL")
    print("==============================")

    while True:

        print("\n1. Write New Email")
        print("2. Use Email Template")

        choice = input("Enter Choice: ").strip()

        if choice in ("1", "2"):
            break

        print("Invalid Choice.")

    # ------------------------------
    # Write New Email
    # ------------------------------

    if choice == "1":

        while True:

            subject = input("\nEnter Subject: ").strip()

            if subject:
                break

            print("Subject cannot be empty.")

        print("\nEnter Email Message")
        print("Type END in a new line to finish.\n")

        lines = []

        while True:

            line = input()

            if line.upper() == "END":
                break

            lines.append(line)

        body = "\n".join(lines).strip()

        while not body:

            print("Message cannot be empty.")
            print("Type END in a new line to finish.\n")

            lines = []

            while True:

                line = input()

                if line.upper() == "END":
                    break

                lines.append(line)

            body = "\n".join(lines).strip()

    # ------------------------------
    # Use Template
    # ------------------------------

    else:

        template_name = view_templates()

        if template_name is None:
            return None, None, None

        subject, body = load_template(template_name)

        if subject is None or body is None:

            print("Unable to load template.")

            return None, None, None

        subject, body = generate_email(subject, body)

    msg["Subject"] = subject
    msg.set_content(body)

    return msg, subject, body