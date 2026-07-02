Students=[]
for i in range(10):
    Stu=[]
    print('Enter the details of Student Number ',i+1)
    Rno=int(input('Enter Roll No:'))
    Name=input('Enter Name:')
    Div=input('Enter Division:')
    Height=float(input('Enter Height in (cm)'))
    Weight=float(input('Enter Weight in (kg)'))
    Disable=input('Enter Disable (yes/no):').lower()=='yes'
    Students.append([Rno,Name,Div,Height,Weight,Disable])
    Students.append(Stu)

for Stu in Students:
    print(Stu)




