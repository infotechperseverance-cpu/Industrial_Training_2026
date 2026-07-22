# =============================================================================
# FILE NAME : attachment.py
#
# PROJECT : Email Automation System
#
# MODULE :
# Attachment Management System
#
# DESCRIPTION :
# This module manages email attachments.
#
# FEATURES :
# 1. Add single attachment
# 2. Add multiple attachments
# 3. Detect file type automatically
# 4. Handle invalid files
# 5. Handle file errors
#
# USED WITH:
# send_email.py
# bulk_email.py
# draft_management.py
#
# =============================================================================


import os
import mimetypes



# =============================================================================
# CLASS NAME : AttachmentManager
#
# PURPOSE :
# Handles email file attachments.
#
# =============================================================================


class AttachmentManager:


    # =========================================================================
    # FUNCTION NAME : add_attachment
    #
    # PURPOSE :
    # Adds one file attachment to email object.
    #
    # INPUT :
    # email object
    # file path
    #
    # OUTPUT :
    # Adds attachment
    #
    # =========================================================================


    def add_attachment(self, email, file_path):


        if file_path is None or file_path.strip() == "":


            print("No Attachment Selected.")

            return False



        if not os.path.exists(file_path):


            print("File Not Found.")

            return False



        try:



            with open(file_path, "rb") as file:



                file_data = file.read()



            file_name = os.path.basename(file_path)



            mime_type, encoding = mimetypes.guess_type(file_path)



            if mime_type:



                maintype, subtype = mime_type.split("/")



            else:



                maintype = "application"

                subtype = "octet-stream"




            email.add_attachment(


                file_data,


                maintype=maintype,


                subtype=subtype,


                filename=file_name


            )



            print(

                "Attachment Added Successfully:",

                file_name

            )



            return True




        except PermissionError:



            print("Permission Denied. Cannot Read File.")

            return False



        except Exception as e:



            print("Attachment Error :", e)

            return False





    # =========================================================================
    # FUNCTION NAME : add_multiple_attachments
    #
    # PURPOSE :
    # Adds multiple files to email.
    #
    # INPUT :
    # email object
    # list of file paths
    #
    # OUTPUT :
    # Adds multiple attachments
    #
    # =========================================================================



    def add_multiple_attachments(self, email, file_paths):



        if not file_paths:



            print("No Attachments Provided.")

            return False




        success = 0



        for file_path in file_paths:



            result = self.add_attachment(

                email,

                file_path

            )



            if result:



                success += 1




        print(

            f"{success} Attachment(s) Added."

        )



        return success > 0




# =============================================================================
# TEST PROGRAM
# =============================================================================


if __name__ == "__main__":



    manager = AttachmentManager()



    print(

        "Attachment Manager Module Loaded Successfully."

    )