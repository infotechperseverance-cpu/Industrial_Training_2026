import json
from datetime import datetime
from voice import speak

def load_json():
    try:
        with open("templates.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_json(templates):
    with open("templates.json", "w") as f:
        json.dump(templates, f, indent=4)


def create_template():
    templates = load_json()

    template_id = len(templates) + 1
    template_name = input("Enter Template Name: ")
    message = input("Enter Message: ")

    templates.append({
        "template_id": template_id,
        "template_name": template_name,
        "message": message,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        #"updated_at": ""
    })

    save_json(templates)
    print("Template Created Successfully!")


def update_template():
    templates = load_json()

    template_name = input("Enter Template Name to Update: ")

    for template in templates:
        if template["template_name"] == template_name:

            template["message"] = input("Enter New Message: ")
            template["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

            save_json(templates)
            print("Template Updated Successfully!")
            return

    print("Template Not Found!")


def delete_template():
    templates = load_json()

    template_name = input("Enter Template Name to Delete: ")

    for template in templates:
        if template["template_name"] == template_name:
            templates.remove(template)
            save_json(templates)
            print("Template Deleted Successfully!")
            return

    print("Template Not Found!")


def view_template():
    templates = load_json()

    if len(templates) == 0:
        print("No Templates Found!")
        return

    for template in templates:
        print("\nTemplate ID:", template["template_id"])
        print("Template Name:", template["template_name"])
        print("Message:", template["message"])
        print("Created At:", template["created_at"])
        print("Updated At:", template["updated_at"])



def template_menu():

    speak("\n========== Templates ==========")

    while True:
      print("\n1. Create Template")
      print("2. Update Template")
      print("3. Delete Template")
      print("4. View Template")
      print("5. Exit")

      choice = input("Enter Choice: ")

      if choice == "1":
        create_template()

      elif choice == "2":
        update_template()

      elif choice == "3":
        delete_template()

      elif choice == "4":
        view_template()

      elif choice == "5":
        print("Thank You!")
        break

      else:
        print("Invalid Choice!")