from google import genai


# CLASS NAME: AIEmailWriter
# WHAT IT DOES: This class connects to the Gemini AI model and generates
#               complete emails based on the topic, tone, and user details.
# INPUTS: topic, tone, details
# OUTPUT: Returns the generated email subject and body separately.

class AIEmailWriter:

    # FUNCTION NAME: __init__
    # WHAT IT DOES: Initializes the Gemini AI client using the API key.
    # INPUTS: None
    # OUTPUT: Creates a Gemini AI client object.

    def __init__(self):

        # Creating a Gemini AI client using the API key
        # This client is used to communicate with the Gemini model
        self.client = genai.Client(
            api_key="your_api"
        )


    # FUNCTION NAME: generate_email
    # WHAT IT DOES: Sends the email topic, tone, and user details to
    #               Gemini AI and generates a complete email. It then
    #               separates the generated email into subject and body.
    # INPUTS: topic, tone, details
    # OUTPUT: Returns the email subject and body.

    def generate_email(self, topic, tone, details):

        # Creating a prompt for Gemini AI
        # It includes the email topic, tone, and user details
        # so that AI can generate a complete email.

        prompt = f"""
    Write a complete email.

    Topic:
    {topic}

    Tone:
    {tone}

    Details:
    {details}

    IMPORTANT

    Return ONLY in this exact format.

    Subject: <Email Subject>

    Body:
    <Complete Email Body>

    Do not write any explanation.
    Do not use markdown.
    Do not bold anything.
    """

        # Sending the prompt to Gemini AI to generate the email
        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        # Store the generated email
        email = response.text.strip()

        # Variables to store subject and body
        subject = ""
        body = ""

        # Checking if the generated email contains a Body section
        if "Body:" in email:

            # Separating the generated email into subject and body
            parts = email.split("Body:", 1)

            subject = parts[0].replace("Subject:", "").strip()
            body = parts[1].strip()

        return subject, body