import pathlib
import re
''' this module give final name of file if any duplication but name only, not create file
 this file duplication function: which takes two parameter file_path,filename
 this module check name file first then creatd new file is not follow ,
 this module required filename with extension, if incase any incorect path it written none'''

max_Attempts = 3

def validate_filename(filename):

    if filename is None or filename.strip() == "":
        print("Filename is required")
        return False

    pattern = (
        r"^"
        r"([^\\/:*?\"<>|.]+)"  # Group 1: Name (blocks OS special chars and dots)
        r"\."                  # The single structural dot
        r"("                   # Group 2: Allowed real-world extensions
        r"pdf|docx|xlsx|ppt|pptx|txt|csv|json|xml|"   # Documents & Data
        r"html|css|js|ts|py|c|cpp|h|hpp|java|sh|"  # Code & Web
        r"png|jpg|jpeg|gif|svg|webp|ico|"          # Images
        r"mp3|wav|mp4|mkv|mov|avi|"                # Media
        r"zip|rar|tar|gz|7z|exe"                   # Archives & Systems
        r")$"
    )

    if re.fullmatch(pattern, filename):
        return True

    return False


#Automatic sequence with name change if user not change
def automatic_name(filename):
    print("Automatic rename file name with sequence")

    try:
        if "." in filename:
            index = filename.find(".")

            text1 = filename[0:index]
            text2 = filename[index:]

            i = len(text1)- 1

            while i >= 0 and text1[i].isdigit():
                i -= 1

            if i != len(text1) - 1:
                num = int(text1[i + 1:]) + 1
                filename = text1[:i + 1] + str(num) + text2
                print("Automatic rename file name as", filename)
                return filename

            filename = text1 + "_1" + text2
            print("Automatic rename file name as", filename)
            return filename

        else:
            i = len(filename) - 1

            while i >= 0 and filename[i].isdigit():
                i -= 1

            if i != len(filename) - 1:
                num = int(filename[i + 1:]) + 1
                filename = filename[:i + 1] + str(num)
                print("Automatic rename file name as", filename)
                return filename

            filename = filename + "_1"
            print("Automatic rename file name as", filename)
            return filename
    except:
       print("Something went wrong")
       return ''
# duplication think function
def duplication_files_detection(folder_path, filename):
    try:
        if validate_filename(filename)== False:
            print("invalid filename provide by user ")
            return ''

        if folder_path is None or filename is None:
            return ''
        folder_path = str(folder_path)
        folder_path = folder_path.replace("\\", "/")
        folder = pathlib.Path(str(folder_path))

        if not folder.exists():
            print("Wrong path")
            return ''

        if not folder.is_dir():
            print("Not a folder")
            return ''

        if not any(folder.iterdir()):
            print("Empty folder")
            return ''
        for file in folder.iterdir():
            if not file.is_file():
                continue
            if filename.strip() == file.name:
                print(f"{file} is Duplicated")
                c = 0
                while True:
                    try:
                        c += 1
                        if c > max_Attempts:
                            print("Too many attempts")
                            fname = automatic_name(filename)
                            return fname
                        choice = input("Do you want rename file name(yes/no) ")

                        if choice.lower() == "yes":
                            fname = input("Enter file name with extension: ")
                            if validate_filename(fname) == False:
                                continue

                            
                            duplicate = False

                            for f in folder.iterdir():
                                if not f.is_file():
                                    continue
                                if fname.strip() == f.name:

                                    duplicate = True
                                    break
                            if duplicate == True:
                                print("File name already exists")
                                
                                continue

                            return fname
                        elif choice.lower() == "no":

                            while True:
                                filename = automatic_name(filename)

                                duplicate = False
                                for f in folder.iterdir():
                                    if not f.is_file():
                                        continue

                                    if filename == f.name:
                                        duplicate = True
                                        break

                                if duplicate == False:
                                    return filename
                        else:
                            print("Wrong input")

                    except ValueError:
                        print("Wrong input")
                    except TypeError:
                        print("Wrong input")
                    except KeyboardInterrupt:
                        print("User keyboard interrupt")
                    except EOFError:
                        print("EOF error")
                    except:
                        print("Something went wrong")

    except:
        print("Something went wrong")  
    return filename      

####################################END##############################