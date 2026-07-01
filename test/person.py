from email_validator import validate_email
#this is person classs

'''this is a class implemetsation for a class named person
this class can be rsused by any class which stores indivisual information'''
class Person:
    ''' this is a constructor'''
    def __init__(self, aName = "a", aAdhar_id = 0,  aDOB = "",  aBlood_group="", aHeight=0.0, aWeight=0.0, aEmail="" , aDisability=""):
        print("Inside Base constructor")
        self.Name = aName
        self.Adhar_id = aAdhar_id
        self.DOB = aDOB
        self.Blood_group = aBlood_group
        self.Height = aHeight
        self.Weight = aWeight
        self.Email = aEmail
        self.Disability = aDisability
    
    ''' this method validates the email and upon succesfull validation it updates
    indivisual persons email address'''
    def updateEmail(self, aEmail):
        try:
            email_info = validate_email(aEmail, check_deliverability=True)
            normalized_email = email_info.normalized
            print(f"Success! Normalized email: {normalized_email}")
            self.email = aEmail;
            return True;
        except :
            # Returns user-friendly, descriptive English errors
            print(f"Invalid email:")
        return False
        
class Teacher(Person):
    def __init__(self):
         super().__init__("Akshay")
         print("Inside derived constructor")
         self.__teacher_id = ""
         self.salary = ""
         self.subject = ""

    def updateAsalary():
         pass

class Master(Teacher):        
    def __init__(self):
        super().__init__()
        print("Inside Master")

m1 = Master()