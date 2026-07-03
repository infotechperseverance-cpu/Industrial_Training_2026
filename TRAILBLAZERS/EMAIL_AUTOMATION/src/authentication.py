import csv
import os

MAX_ATTEMPTS = 3


def authenticate_user():

    attempts = 0

    while attempts < MAX_ATTEMPTS:

        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        # Input Validation
        if not username or not password:

            print("Username and Password cannot be empty.\n")
            continue

        try:

            # Check if CSV exists
            if not os.path.exists("users.csv"):
                raise FileNotFoundError

            with open(
                    "users.csv",
                    "r",
                    newline="",
                    encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                # Empty CSV
                if reader.fieldnames is None:
                    raise ValueError("CSV file is empty.")

                # Required Columns
                if (
                        "username" not in reader.fieldnames
                        or
                        "password" not in reader.fieldnames
                ):
                    raise ValueError(
                        "Required columns are missing."
                    )

                # Verify Credentials
                for row in reader:

                    if (
                            row["username"].strip() == username
                            and
                            row["password"].strip() == password
                    ):

                        print("\nLogin Successful.")

                        return True

            attempts += 1

            remaining = MAX_ATTEMPTS - attempts

            print("\nInvalid Username or Password.")

            if remaining > 0:

                print(
                    f"Attempts Remaining : {remaining}\n"
                )

        except FileNotFoundError:

            print("users.csv not found.")

            return False

        except PermissionError:

            print("Permission Denied.")

            return False

        except csv.Error as e:

            print("CSV Error :", e)

            return False

        except ValueError as e:

            print(e)

            return False

        except KeyError as e:

            print(f"Missing Column : {e}")

            return False

        except Exception as e:

            print("Unexpected Error :", e)

            return False

    print("\nMaximum Login Attempts Exceeded.")

    print("Access Denied.")

    return False