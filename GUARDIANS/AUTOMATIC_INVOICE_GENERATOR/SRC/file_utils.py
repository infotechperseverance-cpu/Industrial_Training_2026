
import os
import json

FILE_NAME="invoices.json"

#Load invoices.json file
def load_invoices():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME,"r") as file:
            try:
                return json.load(file)
            except json.JSONDecoderError:
                return {}


    return {}

#Write invoices in invoices.json file
def write_invoices(invoices):
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME,"w") as file:
            json.dump({},file)

    else:
        with open(FILE_NAME,"w") as file:
            json.dump(invoices,file,indent=4)
                
