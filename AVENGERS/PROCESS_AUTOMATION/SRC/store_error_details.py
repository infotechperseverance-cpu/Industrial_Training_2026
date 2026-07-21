from logger import write_log

write_log("Process Start", "Success")

try:
    f = open("data.txt", "r")
    write_log("Read File", "Success")
except:
    write_log("Read File", "Failure", "File not found")

try:
    salary = int("abc")
    write_log("Input Salary", "Success")
except:
    write_log("Input Salary", "Failure", "Invalid Number")

write_log("Process End", "Success")
print("Done! Check logs.db file")