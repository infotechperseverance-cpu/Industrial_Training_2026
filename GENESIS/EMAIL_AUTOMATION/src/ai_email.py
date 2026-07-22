# =============================================================================
# FILE NAME : ai_email.py
#
# MODULE NAME : AI Email Generator
#
# DESCRIPTION:
# This module generates professional emails using Google Gemini AI.
#
# FEATURES:
# 1. Generate email subject
# 2. Generate email body
# 3. Supports different tones
# 4. Returns generated email to main program
#
# IMPORTANT:
# This file does NOT import draft_management.py.
# Draft saving is handled by main.py.
#
# =============================================================================


# Gemini AI Library
from google import genai



# =============================================================================
# CLASS NAME : AIEmailWriter
#
# PURPOSE:
# Handles communication with Gemini AI model.
# =============================================================================


class AIEmailWriter:



    # =========================================================================
    # FUNCTION NAME : __init__
    #
    # WHAT IT DOES:
    # Creates Gemini AI client.
    #
    # INPUT:
    # None
    #
    # OUTPUT:
    # Gemini client object
    # =========================================================================


    def __init__(self):


        try:


            self.client = genai.Client(

                api_key="YOUR_API_KEY"

            )


        except Exception as e:


            print(
                "\nAI Initialization Error :",
                e
            )

            self.client = None





    # =========================================================================
    # FUNCTION NAME : generate_email
    #
    # WHAT IT DOES:
    # Sends user requirements to Gemini AI
    # and generates complete email.
    #
    # INPUT:
    # topic
    # tone
    # details
    #
    # OUTPUT:
    # Returns subject and body
    #
    # =========================================================================



    def generate_email(
            self,
            topic,
            tone,
            details
        ):



        if self.client is None:


            return (
                "Error",
                "AI service is not available"
            )




        prompt = f"""


            You are an expert email writer.


            Create a complete professional email.


            Email Topic:
            {topic}


            Email Tone:
            {tone}


            Additional Details:
            {details}



            Follow this exact format:


            Subject:
                Only email subject>


            Body:
                <Complete email body>



            Rules:

            1. Do not add explanation.
            2. Do not use markdown.
            3. Do not use bullet points.
            4. Write only email content.
            
        """



        try:



            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            email_text = response.text.strip()


            subject = ""

            body = ""




            # ---------------------------------------------------------
            # Separate Subject and Body
            # ---------------------------------------------------------


            if "Body:" in email_text:



                parts = email_text.split(

                    "Body:",

                    1

                )



                subject = parts[0].replace(

                    "Subject:",

                    ""

                ).strip()



                body = parts[1].strip()




            else:



                # If AI does not follow format

                subject = "Generated Email"

                body = email_text





            return subject, body





        except Exception as e:



            print(

                "\nAI Generation Error :",

                e

            )


            return (

                "Error",

                "Unable to generate email"

            )





# =============================================================================
# TEST PROGRAM
# =============================================================================


if __name__ == "__main__":



    writer = AIEmailWriter()



    topic = input(

        "Enter Email Topic : "

    )



    tone = input(

        "Enter Email Tone : "

    )



    details = input(

        "Enter Email Details : "

    )




    subject, body = writer.generate_email(

        topic,

        tone,

        details

    )



    print("\n================================")

    print("GENERATED EMAIL")

    print("================================")



    print("\nSubject:")

    print(subject)



    print("\nBody:")

    print(body)