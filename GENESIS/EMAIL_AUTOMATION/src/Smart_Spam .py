# FR-11: Smart Spam Checker

spam_words = [
    "free", "winner", "win", "lottery", "prize",
    "money", "cash", "urgent", "offer", "click",
    "buy now", "limited", "discount", "guaranteed"
]

def spam_checker(email_text):
    email = email_text.lower()

    found_words = []

    for word in spam_words:
        if word in email:
            found_words.append(word)

    spam_count = len(found_words)

    # Quality Score
    score = 100 - (spam_count * 10)

    if score < 0:
        score = 0

    print("\n========== SMART SPAM CHECKER ==========")
    print("Spam Words Found :", found_words)

    print("Quality Score    :", score, "/100")

    if spam_count == 0:
        print("Status           : Safe Email")
    elif spam_count <= 3:
        print("Status           : Medium Risk")
    else:
        print("Status           : Spam Email")
    print("========================================")


# Main Program

email = input("Enter Email Content:\n")

spam_checker(email)