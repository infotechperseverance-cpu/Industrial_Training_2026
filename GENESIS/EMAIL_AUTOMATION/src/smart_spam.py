# =============================================================================
# FILE NAME : smart_spam.py
#
# PROJECT : EMAIL AUTOMATION SYSTEM
#
# MODULE NAME : Smart Spam Checker
#
# DESCRIPTION:
# This module checks email content before sending.
# It detects common spam words and calculates spam risk score.
#
# USED BY:
# 1. main.py
# 2. send_email.py
#
# FUNCTIONS:
# - SmartSpamChecker Class
# - check_spam_email()
#
# =============================================================================



# =============================================================================
# CLASS NAME : SmartSpamChecker
#
# PURPOSE:
# Performs spam analysis on email content.
#
# =============================================================================


class SmartSpamChecker:



    # =========================================================================
    # FUNCTION NAME : __init__
    #
    # PURPOSE:
    # Initializes spam keywords.
    #
    # =========================================================================


    def __init__(self):


        self.spam_words = [

            "free",

            "win",

            "winner",

            "offer",

            "urgent",

            "click here",

            "money",

            "prize",

            "discount",

            "limited time",

            "buy now",

            "cash",

            "claim",

            "reward",

            "guaranteed",

            "act now"

        ]



    # =========================================================================
    # FUNCTION NAME : check_spam
    #
    # PURPOSE:
    # Checks email text and returns spam report.
    #
    # INPUT:
    # Email content
    #
    # OUTPUT:
    # Dictionary containing score, status and detected words
    #
    # =========================================================================


    def check_spam(self, email_text):


        email_text = email_text.lower()


        spam_score = 0


        detected_words = []



        for word in self.spam_words:



            if word in email_text:


                spam_score += 10


                detected_words.append(word)




        # Risk calculation


        if spam_score >= 50:


            status = "HIGH RISK SPAM"



        elif spam_score >= 20:


            status = "MEDIUM RISK"



        else:


            status = "SAFE"




        result = {


            "score": spam_score,


            "status": status,


            "words": detected_words


        }



        return result






    # =========================================================================
    # FUNCTION NAME : is_spam
    #
    # PURPOSE:
    # Returns True if email is highly suspicious.
    #
    # =========================================================================


    def is_spam(self, email_text):


        result = self.check_spam(email_text)



        if result["status"] == "HIGH RISK SPAM":


            return True



        return False






# =============================================================================
# FUNCTION NAME : check_spam_email
#
# PURPOSE:
# This function is directly called from main.py
#
# Example:
#
# smart_spam.check_spam_email(text)
#
# =============================================================================



def check_spam_email(email_text):


    checker = SmartSpamChecker()



    result = checker.check_spam(email_text)



    print("\n====================================")

    print("          SPAM CHECK RESULT")

    print("====================================")



    print("Spam Score :", result["score"])


    print("Status :", result["status"])




    if len(result["words"]) > 0:



        print("\nDetected Spam Words:")



        for word in result["words"]:



            print("-", word)



    else:



        print("\nNo suspicious words detected.")




    print("====================================")





    # Return True/False for other modules


    if result["status"] == "HIGH RISK SPAM":


        return True



    return False







# =============================================================================
# TEST PROGRAM
# =============================================================================


if __name__ == "__main__":



    print("\nSMART SPAM CHECKER TEST")



    text = input("\nEnter Email Content : ")



    check_spam_email(text)