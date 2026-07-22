import mimetypes

class AttachmentManager:

    def add_attachment(self, email, file_path):

        if file_path == "":
            return

        try:
            with open(file_path, "rb") as file:

                file_data = file.read()
                file_name = file_path.split("\\")[-1]

                mime_type, _ = mimetypes.guess_type(file_path)

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

            print("Attachment Added Successfully.")

        except FileNotFoundError:
            print("File Not Found.")