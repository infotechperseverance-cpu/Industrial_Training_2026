import os
def mk():
    print("enter folder name: ")
    s=input()
    l=s.split(",")
    for x in l:
        x=x.strip()
        if not os.path.exists(x):
            os.mkdir(x)
            print(x,"created")
        else:
            print(x,"already exists")

mk()