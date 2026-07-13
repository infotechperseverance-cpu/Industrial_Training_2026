import json
from datetime import datetime
from voice import speak

'''

@Function Name: load_json
@Description  : This function store templates in templates.json
@inputParam   : NONE
@outParam     : NONE
@Author       : Unnati Thakur

'''

def load_json():
    try:
        with open("templates.json", "r") as f:
            return json.load(f)
    except:
        return []
    
'''

@Function Name: save_json
@Description  : This function save user templates in templates.json
@inputParam   : templates
@outParam     : NONE

'''


def save_json(templates):
    with open("templates.json", "w") as f:
        json.dump(templates, f, indent=4)

'''

@Function Name: create_template
@Description  : This function create templates with name , message 
                and automatic create template_id,created time and
                save it
@inputParam   : NONE
@outParam     : NONE
@Author       : Unnati Thakur

'''

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
        "updated_at": ""
    })

    save_json(templates)
    print("Template Created Successfully!")

'''

@Function Name: update_template
@Description  : This function update templates by there name with 
                message and automatic create update date
                save it
@inputParam   : NONE
@outParam     : NONE
@Author       : Unnati Thakur

'''


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

'''

@Function Name: delete_template
@Description  : This function delete templates by the name
@inputParam   : NONE
@outParam     : NONE
@Author       : Unnati Thakur

'''

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


'''

@Function Name: view_template
@Description  : This function view all templates in 
                templates.json
@inputParam   : NONE
@outParam     : NONE
@Author       : Unnati Thakur

'''

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
        print("Updated At:", template.get("updated_at", "Not Updated"))

def template_menu():

    while True:
        print("------------ Template Management ----------------")
        speak("Template Management")
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