from datetime import datetime

process_name = ""
process_details = ""
workflow_steps = []
status = "Not Executed"
created_date = ""
created_time = ""


# Process Creation
def create_process():
    global process_name, process_details, created_date, created_time

    process_name = input("Enter Process Name : ")

    if process_name == "":
        print("Process Name cannot be empty.")
        return

    process_details = input("Enter Process Details : ")

    created_date = datetime.now().strftime("%Y-%m-%d")
    created_time = datetime.now().strftime("%H:%M:%S")

    print("\nProcess Created Successfully!")


# Add Workflow Steps
def add_workflow_step():
    global workflow_steps

    print("\n----- Add Workflow Steps -----")

    while True:
        step = input("Enter Workflow Step (Type 'done' to stop) : ")

        if step.lower() == "done":
            break

        workflow_steps.append(step)

    print("\nWorkflow Steps Added Successfully!")
    print("Total Workflow Steps :", len(workflow_steps))


# Execute Process
def execute_process():
    global status

    choice = input("Are you sure you want to execute the process? (yes/no): ")

    if choice.lower() != "yes":
        print("Process execution cancelled.")
        return

    status = "Executed"

    print("\n----- Process Execution -----")
    print("Process Name :", process_name)
    print("Process Details :", process_details)
    print("Process Status :", status)
    print("Created Date :", created_date)
    print("Created Time :", created_time)

    if len(workflow_steps) == 0:
        print("No Workflow Steps Found.")
    else:
        print("Workflow Steps :")
        for step in workflow_steps:
            print("-", step)

    print("\nProcess Executed Successfully!")


# Display Process Details
def display_process_details():
    print("\n----- Process Details -----")
    print("Process Name :", process_name)
    print("Process Details :", process_details)
    print("Process Status :", status)
    print("Created Date :", created_date)
    print("Created Time :", created_time)

    if len(workflow_steps) > 0:
        print("Workflow Steps :")
        for step in workflow_steps:
            print("-", step)


# Main Menu
while True:
    print("\n===== PROCESS CREATION MODULE =====")
    print("1. Create Process")
    print("2. Add Workflow Steps")
    print("3. Execute Process")
    print("4. Display Process Details")
    print("5. Exit")

    choice = input("Enter Your Choice : ")

    if choice == "1":
        create_process()

    elif choice == "2":
        add_workflow_step()

    elif choice == "3":
        execute_process()

    elif choice == "4":
        display_process_details()

    elif choice == "5":
        print("Thank You!")
        break

    else:
        print("Invalid Choice! Please Try Again.")