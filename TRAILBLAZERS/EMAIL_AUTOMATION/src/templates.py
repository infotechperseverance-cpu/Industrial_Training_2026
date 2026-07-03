import os

TEMPLATE_FILE = "email_templates.txt"


def save_template():

    print("\n========== SAVE EMAIL TEMPLATE ==========")

    while True:

        template_name = input("Enter Template Name : ").strip()

        if template_name:
            break

        print("Template Name cannot be empty.")

    while True:

        subject = input("Enter Subject : ").strip()

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

    if not body:
        print("Message cannot be empty.")
        return

    if os.path.exists(TEMPLATE_FILE):

        with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:

            content = file.read()

            if f"[{template_name}]" in content:
                print("Template already exists.")
                return

    with open(TEMPLATE_FILE, "a", encoding="utf-8") as file:

        file.write(f"[{template_name}]\n")
        file.write(subject + "\n")
        file.write(body.replace("\n", "\\n") + "\n")
        file.write("-----\n")

    print("\nTemplate Saved Successfully.")


def get_template_names():

    templates = []

    if not os.path.exists(TEMPLATE_FILE):
        return templates

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if line.startswith("[") and line.endswith("]"):
                templates.append(line[1:-1])

    return templates


def view_templates():

    templates = get_template_names()

    if not templates:

        print("No Templates Available.")

        return None

    print("\n========== AVAILABLE TEMPLATES ==========\n")

    for index, template in enumerate(templates, start=1):
        print(f"{index}. {template}")

    while True:

        try:

            choice = int(input("\nSelect Template : "))

            if 1 <= choice <= len(templates):
                return templates[choice - 1]

            print("Invalid Choice.")

        except ValueError:

            print("Enter a valid number.")


def load_template(template_name):

    if not os.path.exists(TEMPLATE_FILE):

        print("Template File Not Found.")

        return None, None

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:

        lines = file.readlines()

    i = 0

    while i < len(lines):

        if lines[i].strip() == f"[{template_name}]":

            subject = lines[i + 1].rstrip()
            body = lines[i + 2].rstrip().replace("\\n", "\n")

            return subject, body

        i += 1

    print("Template Not Found.")

    return None, None


def generate_email(subject, body):

    print("\n========== PLACEHOLDER VALUES ==========")

    while "{name}" in body:

        name = input("Enter Name : ").strip()

        body = body.replace("{name}", name, 1)

    while "{date}" in body:

        date = input("Enter Date : ").strip()

        body = body.replace("{date}", date, 1)

    return subject, body


def template_menu():

    while True:

        print("\n========== TEMPLATE MENU ==========")
        print("1. Save Template")
        print("2. View Templates")
        print("3. Back")

        choice = input("Enter Choice : ").strip()

        match choice:

            case "1":
                save_template()

            case "2":

                template = view_templates()

                if template:
                    print(f"\nSelected Template : {template}")

            case "3":
                break

            case _:
                print("Invalid Choice.")