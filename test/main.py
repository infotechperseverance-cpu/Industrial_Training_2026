from classes import person
from classes import student
from classes import Teacher
from classes import checkprime
import os
import csv

personlist = []
try:
 if os.path.exists("persondetails.csv"):
    with open("persondetails.csv",newline='') as personfile:
        preader = csv.reader(personfile,delimiter=',')

        for row in preader:
            if len(row)>=9:
              p1 = person(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
              personlist.append(p1)
 while True:      
  try:   
   n = int(input("enter the number of persons:"))
   if n > 0:
      break
   else:
      print("enter natural number")
  except:
      print("inavalid input: enter please digit")

 for i in range(1,1+n):
    p1 = person("","","","","","","","","")
    p1.getdetails()
    personlist.append(p1)

 with open("persondetails.csv",'w',newline='') as personfile:
    pwriter = csv.writer(personfile,delimiter=',')

    for i in personlist:
        pwriter.writerow(i.getproprtylist())

 print("person details : ")
 for i in personlist:
      i.displaydetails()
      
 age = input("if you want to print the all details of person enter y or n")
 if age == 'y':
   age = int(input("enter your age :"))
   if age > 18 :
    password = input("enter password to print all details of student: ")
    if password == "person345":
     print("All person details : ")
     for i in personlist:
      i.alldisplay_details()
      print("Age: ",i.calculate_age())
      print("BMI: ",i.calculate_bmi())
      print("disability: ",i.has_disability())

 try:   
   folder = input("you want to create folder of each person just yes :")
 except:
     print("inavalid input: enter please yes or no")

 if folder == "yes":
    for i in personlist:
        foldername = i.name

        if not os.path.exists(foldername):
            os.makedirs(foldername, exist_ok=True)
            
        filename = os.path.join(foldername,foldername+".csv")

        with open(filename,'w') as file:  
            filewriter = csv.writer(file,delimiter=',')  
            
            filewriter.writerow(i.getproprtylist())
         
        print("succssfully created folder and file of student is :",i.name)
     

 studentlist = []

 if os.path.exists("studentsdetails.csv"):
    with open("studentsdetails.csv",newline='') as studentfile:
        studentreader = csv.reader(studentfile,delimiter=',')

        for row in studentreader:
            if len(row)>=11:
              s1 = student(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
              studentlist.append(s1)
        
 while True :  
  try:   
   n = int(input("enter the number of persons:"))
   if n > 0:
     break
   else:
      print("enter natural number")
  except:
      print("inavalid input: enter please digit")


 for i in range(1,1+n):
    s1 = student("","","","","","","","","","","")
    s1.getdetails()
    s1.getstudentdetails()
    studentlist.append(s1)

 with open("studentsdetails.csv",'w',newline='') as studentfile:
    studentwriter = csv.writer(studentfile,delimiter=',')

    for i in studentlist:
        studentwriter.writerow(i.getproprtylist())

 print("All students details : ")
 for i in studentlist:
    i.display_details()
    i.studentdetails()
 try: 
  sgender = input("if you want sepreate girls and boys enter yes : ")
 except:
      print("inavalid input: enter please yes or no")

 if sgender == "yes":
    with open("girlstudent.csv",'w',newline='') as girlfile ,\
         open("boystudentes.csv",'w',newline='') as boyfile:

         girlwrite = csv.writer(girlfile,delimiter=',')
         boywrite= csv.writer(boyfile,delimiter=',')

         for i in studentlist:
            if i.gender == "f":
                  girlwrite.writerow(i.getproprtylist())
                            
            else:
                  boywrite.writerow(i.getproprtylist())

         print("add data in file is succsefully")          

 try:                 
   rollnoprime= input("you want to create seprate file of prime roll number enter yes : ")   
 except:
      print("inavalid input: enter please yes or no")

 if rollnoprime =="yes":
    with open("primerollno.csv",'w',newline="") as primefile:
        primewrite = csv.writer(primefile,delimiter=',')

        for i in studentlist:
           if checkprime(int(i.rollno)):
                primewrite.writerow(i.getproprtylist())

        print("data add succssefully")  

 try: 
  folder = input("you want to create folder of each student just yes :")
 except:
      print("inavalid input: enter please yes or no")

 if folder == "yes":
    for i in studentlist:
        foldername = i.name

        if not os.path.exists(foldername):
            os.makedirs(foldername, exist_ok=True)
            
        filename = os.path.join(foldername,foldername+".csv")

        with open(filename,'w') as file:  
            filewriter = csv.writer(file,delimiter=',')  
            
            filewriter.writerow(i.getproprtylist())
         
        print("succssfully created folder and file of student is :",i.name)

 teacherlist = []

 if os.path.exists("teacherdetails.csv"):
    with open("teacherdetails.csv",newline='') as teacherfile:
        treader = csv.reader(teacherfile,delimiter=',')

        for row in treader:
            if len(row)>=13:
              t1 = Teacher(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
              personlist.append(t1)

 while True :  
  try:   
   n = int(input("enter the number of persons:"))
   if n > 0:
     break
   else:
      print("enter natural number")
  except:
      print("inavalid input: enter please digit")

 for i in range(1,1+n):
    t1 = Teacher("","","","","","","","","","","","")
    t1.getdetails()
    t1.getteacherdetails()
    teacherlist.append(t1)

 with open("teacherdetails.csv",'w',newline='') as teacherfile:
    twriter = csv.writer(teacherfile,delimiter=',')

    for i in teacherlist:
        twriter.writerow(i.getproprtylist())

 print("All students details : ")
 for i in teacherlist:
    i.display_details()
    i.teacherdetails()
    print("Age: ",i.calculate_age())
    print("BMI: ",i.calculate_bmi())
    print("disability: ",i.has_disability())
   
 try:  
  folder = input("you want to create folder of each teacher just yes :")
 except:
    print("inavalid input: enter please yes or no")

 if folder == "yes":
    for i in teacherlist:
        foldername = i.subject

        if not os.path.exists(foldername):
            os.makedirs(foldername, exist_ok=True)
            
        filename = os.path.join(foldername,foldername+".csv")

        with open(filename,'w') as file:  
            filewriter = csv.writer(file,delimiter=',')  
            
            filewriter.writerow(i.getproprtylist())
         
        print("succssfully created folder and file of student is :",i.name)

except Exception as e:
    print(e)

