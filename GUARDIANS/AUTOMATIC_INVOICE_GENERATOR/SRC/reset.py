import json

class InvoiceManager:
    def __init__(self):
        pass

    def reset_data(self):
        try:
            choice = input("Reset all project data (yes/no): ")

            if choice.lower() == "yes":

                with open("customer.json", "w") as file:
                    json.dump([], file, indent=4)

                with open("products.json", "w") as file:
                    json.dump([], file, indent=4)

                with open("invoices.json", "w") as file:
                    json.dump({}, file, indent=4)

                with open("temp_invoice.json", "w") as file:
                    json.dump([], file, indent=4)

                print("All project data reset successfully")

            else:
                print("Reset Cancelled")

        except Exception as e:
            print("Error:", e)


# obj = InvoiceManager()
# obj.reset_data()