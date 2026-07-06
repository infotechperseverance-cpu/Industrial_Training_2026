import csv
username = input("Enter username: ")
password = input("Enter password: ")
login_success = False
existing_user = False
with open("user.csv", "r", newline="") as file:
	 reader = csv.DictReader(file)
	 for row in reader:
		if row["username"] == username:
			existing_user = True
			if row["password"] == password:
				login_success = True
				break
if login_success:
	print("Login successful!")
elif existing_user:
	print("Invalid password")
else:
	print("user does not exist. Creating new account")
	with open('user.csv', 'a', newline='') as csvfile:
		userwriter = csv.writer(csvfile, delimiter=',')
		userwriter.writerow([username,password])
		print("user created")