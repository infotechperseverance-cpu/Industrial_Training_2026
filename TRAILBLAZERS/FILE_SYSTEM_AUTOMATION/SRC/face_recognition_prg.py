"""
==============================================================
Project Name : Face Recognition System
Purpose      : Compare images using OpenCV ORB
Database     : MySQL
Author       : Komal Mahajan
==============================================================
"""

import os
import cv2
import shutil
import mysql.connector
from datetime import datetime

class FaceRecognitionSystem:
    '''
    @Function Name : _init_
    @Description :This constructor initializes folders,database objects and creates
                  the required folders and database automatically.
    @Input Param :NONE
    @Output Param :NONE
    @Author :Komal Mahajan
    '''

    def __init__(self):
        print("\n========== MYSQL LOGIN ==========")
        self.db_user = input("Enter username:")
        self.db_password = input("Enter password:" )

        self.connection = None
        self.cursor = None
        self.database_name = "FileSystem"
        self.reference_folder = "Reference_Image"
        self.match_folder = "Matched_Images"
        self.log_folder = "Logs"
        self.create_required_folders()
        self.initialize_database()

    '''
    @Function Name : initialize_database
    @Description :This function connects with MySQL Server.It creates the FileSystem 
    database if it does not exist and also creates the Face_Recognition table.
    @Input Param :NONE
    @Output Param :NONE
    @Author :Komal Mahajan
    '''

    def initialize_database(self):
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                user=self.db_user,
                password=self.db_password
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
            self.cursor.execute(f"USE {self.database_name}")

            create_table = """
            CREATE TABLE IF NOT EXISTS Face_Recognition
            (reference_id INT AUTO_INCREMENT PRIMARY KEY,
                image_name VARCHAR(255),
                image_path TEXT,
                upload_date DATETIME,
                scan_date DATETIME,
                matched_images_count INT,
                matching_folder_path TEXT,
                match_status VARCHAR(100) )"""

            self.cursor.execute(create_table)
            self.connection.commit()
            print("\nDatabase Ready Successfully.")
            self.write_log("Database and Table Initialized.")

        except mysql.connector.Error as error:
            print("\nDatabase Error")
            print(error)

    '''
    @Function Name : create_required_folders
    @Description :This function creates all foldersrequired by the project if they
                   are not already available.
    @Input Param :NONE
    @Output Param :NONE
    @Author :Komal Mahajan'''

    def create_required_folders(self):
        folders = [self.reference_folder,self.match_folder,self.log_folder]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

        print("\nProject Folders Ready.")

    '''
    @Function Name : write_log
    @Description :This function stores every important activity performed 
    by the system into the log file with current date and time.
    @Input Param :
    message : Activity message
    @Output Param :NONE
    @Author :Komal Mahajan'''

    def write_log(self, message):
        try:
            log_path = os.path.join(self.log_folder,"face_recognition_log.txt")
            with open(log_path,"a") as file:
                file.write( f"{datetime.now()} : {message}\n")

        except Exception as error:
            print(error)

    '''
    @Function Name : upload_reference_image
    @Description :This function accepts a reference image from the user,
    validates it, copies it into the Reference_Image folderand stores its information in the Face_Recognition table.
    @Input Param :
    image_path : Complete path of the reference image
    @Output Param :
    Returns True if the image is uploaded successfully,
    otherwise returns False.
    @Author :
    Komal Mahajan
    '''
    def upload_reference_image(self, image_path):

        try:
            image_path = image_path.strip().strip('"').strip("'")
            if not os.path.exists(image_path):
                print("\nImage file does not exist.")
                return False

            extensions = (".jpg", ".jpeg", ".png", ".bmp")
            if not image_path.lower().endswith(extensions):
                print("\nOnly JPG, JPEG, PNG and BMP images are allowed.")
                return False

            image = cv2.imread(image_path)

            if image is None:
                print("\nInvalid image file.")
                return False

            image_name = os.path.basename(image_path)
            query = "SELECT reference_id FROM Face_Recognition WHERE image_name=%s"
            self.cursor.execute(query, (image_name,))
            if self.cursor.fetchone():
                print("\nReference Image Already Exists.")
                return False

            destination_path = os.path.join(self.reference_folder,image_name)
            shutil.copy2(image_path, destination_path)
            query = """INSERT INTO Face_Recognition (image_name, image_path,upload_date, scan_date, 
                        matched_images_count,matching_folder_path, match_status) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

            values = (image_name,destination_path,datetime.now(),None,0,"","Reference Uploaded")
            self.cursor.execute(query, values)
            self.connection.commit()
            self.write_log(f"Reference Image Uploaded : {image_name}")
            print("\nReference Image Uploaded Successfully.")
            return True

        except Exception as error:
            print("\nUpload Error :", error)

            self.write_log(f"Upload Error : {error}")
            return False

    '''
    @Function Name : display_reference_images
    @Description :This function displays all reference images stored in the Face_Recognition table.
    @Input Param :NONE
    @Output Param :Displays all stored records.
    @Author :Komal Mahajan '''

    def display_reference_images(self):
        try:
            query = """
                    SELECT reference_id,image_name,image_path,upload_date FROM Face_Recognition
                    ORDER BY reference_id """

            self.cursor.execute(query)
            records = self.cursor.fetchall()

            if len(records) == 0:
                print("\nNo Reference Images Found.")
                return

            print("\n==============================================")
            print("REFERENCE IMAGE DETAILS")
            print("==============================================")

            for row in records:
                print("\nReference ID :", row[0])
                print("Image Name   :", row[1])
                print("Image Path   :", row[2])
                print("Upload Date  :", row[3])
                print("------------------------------------------")

            self.write_log("Displayed all reference images." )

        except Exception as error:
            print(error)


    '''
    @Function Name : update_reference_image
    @Description :This function updates an existing reference image.It replaces the old
                  image with the new image and updates its details in the database.

    @Input Param :reference_id : Reference image ID
                  new_image_path : Path of new reference image
    @Output Param :Returns True if update is successful, otherwise returns False.
    @Author :Komal Mahajan'''

    def update_reference_image(self,reference_id,new_image_path):
        self.cursor.execute("SELECT * FROM Face_Recognition WHERE reference_id=%s",(reference_id,))

        if self.cursor.fetchone() is None:
            print("\nInvalid Reference ID.")
            return False

        try:
            if not os.path.exists(new_image_path):
                print("\nNew image not found.")
                return False

            image = cv2.imread(new_image_path)

            if image is None:
                print("\nInvalid image.")
                return False

            image_name = os.path.basename(new_image_path)
            self.cursor.execute("SELECT image_path FROM Face_Recognition WHERE reference_id=%s",(reference_id,))
            record = self.cursor.fetchone()

            if record:
                if os.path.exists(record[0]):
                    os.remove(record[0])

            destination_path = os.path.join(self.reference_folder,image_name)

            shutil.copy2(new_image_path, destination_path )
            query = """
                    UPDATE Face_Recognition
                    SET
                        image_name=%s,
                        image_path=%s,
                        upload_date=%s,
                        match_status=%s
                    WHERE
                        reference_id=%s
                    """

            values = (

                image_name,
                destination_path,
                datetime.now(),
                "Reference Updated",
                reference_id

            )

            self.cursor.execute(query, values)

            self.connection.commit()

            self.write_log(
                f"Reference Image Updated : {reference_id}"
            )

            print("\nReference Image Updated Successfully.")

            return True

        except Exception as error:

            print(error)

            self.write_log(
                f"Update Error : {error}"
            )

            return False

    '''
    @Function Name : get_reference_image

    @Description :
    This function retrieves the reference image path from the
    database using the reference ID.

    @Input Param :
    reference_id : Reference image ID
@Output Param :
    Returns image path if found otherwise None.

    @Author :
    Komal Mahajan
    '''

    def get_reference_image(self, reference_id):

        try:

            query = "SELECT image_path FROM Face_Recognition WHERE reference_id=%s"

            self.cursor.execute(query, (reference_id,))

            record = self.cursor.fetchone()

            if record:
                return record[0]

            print("\nReference Image Not Found.")

            return None

        except Exception as error:

            print(error)

            return None

    '''
    @Function Name : compare_images

    @Description :
    This function compares two images using ORB feature matching
    and returns the total number of matched key points.

    @Input Param :
    reference_path : Reference image path
    test_path : Test image path

    @Output Param :
    Returns total matched key points.

    @Author :
    Komal Mahajan
    '''

    def compare_images(self, reference_path, test_path):

        try:

            image1 = cv2.imread(reference_path, 0)
            image2 = cv2.imread(test_path, 0)

            if image1 is None or image2 is None:
                return 0

            orb = cv2.ORB_create(1000)

            kp1, des1 = orb.detectAndCompute(image1, None)
            kp2, des2 = orb.detectAndCompute(image2, None)

            if des1 is None or des2 is None:
                return 0

            matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matches = matcher.match(des1, des2)

            matches = sorted(matches, key=lambda x: x.distance)

            good_matches = []

            for match in matches:

                if match.distance < 50:
                    good_matches.append(match)

            return len(good_matches)

        except Exception as error:

            print(error)

            return 0

    '''
    @Function Name : is_match

    @Description :
    This function checks whether two images match based on
    the ORB matching score.

    @Input Param :
    reference_path : Reference image path
    test_path : Test image path

    @Output Param :
    Returns True if images match otherwise False.

    @Author :
    Komal Mahajan
    '''

    def is_match(self, reference_path, test_path):

        score = self.compare_images(reference_path, test_path)

        print(f"{os.path.basename(test_path)} -> Score : {score}")

        if score >= 80:
            return True

        return False

    '''
    @Function Name : scan_images

    @Description :
    This function scans all images inside the selected folder,
    compares them with the reference image and stores all
    matching images in the Matched_Images folder.

    @Input Param :
    reference_id : Reference Image ID
    folder_path  : Folder containing images

    @Output Param :
    NONE

    @Author :
    Komal Mahajan
    '''
    def scan_images(self, reference_id, folder_path):

        try:

            reference_path = self.get_reference_image(reference_id)
            if reference_path is None:
                return
            if not os.path.exists(reference_path):
                print("\nReference Image Missing.")
                return

            if not os.path.exists(folder_path):

                print("\nFolder does not exist.")
                return

            match_count = 0
            for file in os.listdir(self.match_folder):

                file_path = os.path.join(self.match_folder, file)

                if os.path.isfile(file_path):
                    os.remove(file_path)
            extensions = (".jpg", ".jpeg", ".png", ".bmp")

            images = []

            for file in os.listdir(folder_path):

                if file.lower().endswith(extensions):
                    images.append(file)

            if len(images) == 0:
                print("\nNo Image Files Found In Selected Folder.")

                return

            for file in images:

                image_path = os.path.join(folder_path, file)

                if self.is_match(reference_path, image_path):
                    destination = os.path.join(self.match_folder, file)

                    shutil.copy2(image_path, destination)

                    match_count += 1

            self.update_scan_record(reference_id, match_count)

            print("\nScan Completed Successfully.")
            print("Matching Images Found :", match_count)

            self.write_log(
                f"Reference ID {reference_id} : {match_count} Matching Images Found"
            )

        except Exception as error:

            print(error)



    '''
    @Function Name : update_scan_record

    @Description :
    This function updates the scan details in the
    Face_Recognition table after image matching.

    @Input Param :
    reference_id : Reference Image ID
    match_count  : Total matching images

    @Output Param :
    NONE

    @Author :
    Komal Mahajan
    '''
    def update_scan_record(self, reference_id, match_count):

        try:

            status = "Matched"

            if match_count == 0:
                status = "No Match"

            query = """
                    UPDATE Face_Recognition
                    SET
                        scan_date=%s,
                        matched_images_count=%s,
                        matching_folder_path=%s,
                        match_status=%s
                    WHERE
                        reference_id=%s
                    """

            values = (
                datetime.now(),
                match_count,
                self.match_folder,
                status,
                reference_id
            )

            self.cursor.execute(query, values)

            self.connection.commit()

        except Exception as error:

            print(error)



    '''
    @Function Name : display_scan_result

    @Description :
    This function displays the latest image
    matching details stored in the database.

    @Input Param :
    reference_id : Reference Image ID

    @Output Param :
    Displays scan details.

    @Author :
    Komal Mahajan
    '''
    def display_scan_result(self, reference_id):

        try:

            query = """
                    SELECT
                    image_name,
                    scan_date,
                    matched_images_count,
                    matching_folder_path,
                    match_status
                    FROM Face_Recognition
                    WHERE reference_id=%s
                    """

            self.cursor.execute(query, (reference_id,))

            record = self.cursor.fetchone()

            if record is None:

                print("\nRecord Not Found.")
                return

            print("\n========== SCAN RESULT ==========")
            print("Reference Image :", record[0])
            print("Scan Date       :", record[1])
            print("Matched Images  :", record[2])
            print("Matching Folder :", record[3])
            print("Status          :", record[4])

        except Exception as error:

            print(error)

        '''
        @Function Name : close_connection

        @Description :
        This function closes the MySQL cursor and
        database connection safely.

        @Input Param :
        NONE

        @Output Param :
        NONE

        @Author :
        Komal Mahajan
        '''

    '''
    @Function Name : view_reference_image

    @Description :
    This function displays the selected reference image
    using its Reference ID.

    @Input Param :
    reference_id : Reference Image ID

    @Output Param :
    Displays the reference image.

    @Author :
    Komal Mahajan
    '''

    def view_reference_image(self, reference_id):

        try:

            query = "SELECT image_name, image_path FROM Face_Recognition WHERE reference_id=%s"

            self.cursor.execute(query, (reference_id,))

            record = self.cursor.fetchone()

            if record is None:
                print("\nInvalid Reference ID.")

                return

            image = cv2.imread(record[1])

            if image is None:
                print("\nImage Not Found.")

                return

            image = cv2.resize(image, (400, 400))

            cv2.imshow(record[0], image)

            cv2.waitKey(0)

            cv2.destroyAllWindows()

        except Exception as error:

            print(error)
    def close_connection(self):

        try:

            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()

            print("\nDatabase Connection Closed.")

        except Exception as error:

            print(error)
            
def main():

    system = FaceRecognitionSystem()

    while True:

        print("\n====================================")
        print("     FACE RECOGNITION SYSTEM")
        print("====================================")
        print("1. Upload Reference Image")
        print("2. Display Reference Images")
        print("3. View Reference Image")
        print("4. Update Reference Image")
        print("5. Scan Images")
        print("6. Display Scan Result")
        print("7. Exit")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            image_path = input("Enter Reference Image Path : ")
            system.upload_reference_image(image_path)

        elif choice == "2":
            system.display_reference_images()

        elif choice == "3":
            reference_id = int(input("Enter Reference ID : "))
            system.view_reference_image(reference_id)

        elif choice == "4":
            reference_id = int(input("Enter Reference ID : "))
            new_image = input("Enter New Image Path : ")
            system.update_reference_image(reference_id, new_image)

        elif choice == "5":
            reference_id = int(input("Enter Reference ID : "))
            folder = input("Enter Folder Path : ")
            system.scan_images(reference_id, folder)

        elif choice == "6":
            reference_id = int(input("Enter Reference ID : "))
            system.display_scan_result(reference_id)

        elif choice == "7":
            system.close_connection()
            break

        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()