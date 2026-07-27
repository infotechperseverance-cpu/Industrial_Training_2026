# =============================================================================
# FILE NAME : smart_spam.py
# PROJECT : EMAIL AUTOMATION SYSTEM
# MODULE NAME : Smart Spam Checker
# DESCRIPTION: Checks email content before sending.
#              Detects common spam words and calculates spam risk score.
# USED BY: 1. main.py, 2. send_email.py
# FUNCTIONS: SmartSpamChecker Class, check_spam_email()
# =============================================================================


class SmartSpamChecker:

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

    def check_spam(self, email_text):
        email_text = email_text.lower()
        spam_score = 0
        detected_words = []

        for word in self.spam_words:
            if word in email_text:
                spam_score += 10
                detected_words.append(word)

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

    def is_spam(self, email_text):
        result = self.check_spam(email_text)
        if result["status"] == "HIGH RISK SPAM":
            return True
        return False


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

    if result["status"] == "HIGH RISK SPAM":
        return True
    return False


if __name__ == "__main__":
    print("\nSMART SPAM CHECKER TEST")
    text = input("\nEnter Email Content : ")
    check_spam_email(text)
