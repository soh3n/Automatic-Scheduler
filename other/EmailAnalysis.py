import re

def analyze_email(email: str) -> dict:
    # Analyze the email and generate labels based on its content.
    # Initialize all fields to "N/A"
    label = {
        "Spam": "N/A", # "Yes" / "No"
        "Subject": "N/A",
        "Sender": "N/A",
        "send_date": "N/A",
        "Time_Sensitive": "N/A", # "Yes" / "No"
        "Start": "N/A",
        "End": "N/A",
        "Type": "N/A", # "Event" / "Reminder" / "N/A"
        "Category": "N/A", # "Work" / "Study" / "Leisure"
        "Format": "N/A", # "Online" / "In-person"
        "Location": "N/A",
        "Action_Required": "N/A", # "Yes" / "No"
        "Priority_Level": "N/A" # "Low" / "Medium" / "High" / "Urgent"
    }

    # Determine if the email is spam
    spam_keywords = r"promo|deal|discount|offer|win|prize|cash|free|risk-free|congratulations"
    if re.search(spam_keywords, email, re.IGNORECASE):
        label["Spam"] = "Yes"
    else:
        label["Spam"] = "No"

    # Extract subject
    subject_match = re.search(r"Subj:\s*(.+)", email) # Regex Function
    if subject_match:
        label["Subject"] = subject_match.group(1).strip()

    # Extract sender
    sender_match = re.search(r"From:\s*([\w@:.$\-]+)", email)
    if sender_match:
        label["Sender"] = sender_match.group(1).strip()

    # Extract send date
    date_match = re.search(r"(\d{1,2}-[A-Z]{3}-\d{4})", email)
    if date_match:
        label["send_date"] = date_match.group(1)

    # Determine if the email is time-sensitive
    time_sensitive_keywords = r"by|deadline|urgent|immediately|due|ASAP"
    if re.search(time_sensitive_keywords, email, re.IGNORECASE):
        label["Time_Sensitive"] = "Yes"
    else:
        label["Time_Sensitive"] = "No"

    # Extract start time
    time_match = re.search(r"(\d{1,2}:\d{2} (AM|PM))", email)
    if time_match:
        label["Start"] = time_match.group(1)

    # Extract end time
    end_match = re.search(r"until (\d{1,2}:\d{2} (AM|PM))", email)
    if end_match:
        label["End"] = end_match.group(1)

    # Determine type of the email
    type_keywords_reminder = r"reminder|don't forget|alert|due soon|deadline|urgent|asap"
    type_keywords_event = r"event|meeting|conference|invitation|party|training|workshop"
    if re.search(type_keywords_reminder, email, re.IGNORECASE):
        label["Type"] = "Reminder"
    elif re.search(type_keywords_event, email, re.IGNORECASE):
        label["Type"] = "Event"

    # Determine category
    category_keywords_work = r"work|team|office|client|colleague|workplace|report|job|business"
    category_keywords_leisure = r"leisure|social|fun|vacation|hobby|movie|recreation|festival|valentine|flowers"
    category_keywords_study = r"study|education|lecture|assignment|exam|course|university|research"
    if re.search(category_keywords_work, email, re.IGNORECASE):
        label["Category"] = "Work"
    elif re.search(category_keywords_leisure, email, re.IGNORECASE):
        label["Category"] = "Leisure"
    elif re.search(category_keywords_study, email, re.IGNORECASE):
        label["Category"] = "Study"

    # Determine format
    format_keywords_online = r"online|virtual|webinar|zoom|remote|call"
    format_keywords_in_person = r"in-person|lobby|conference room|office|on-site"
    if re.search(format_keywords_online, email, re.IGNORECASE):
        label["Format"] = "Online"
    elif re.search(format_keywords_in_person, email, re.IGNORECASE):
        label["Format"] = "In-person"

    # Extract location
    location_match = re.search(
        r"(Main Lobby|Room|Office|Center|Building|Park)", email, re.IGNORECASE)
    if location_match:
        label["Location"] = location_match.group(1).strip().title()

    # Determine if action is required
    action_required_keywords = r"contact|respond|order|register|RSVP|confirm|subscribe|submit|apply|reserve"
    if re.search(action_required_keywords, email, re.IGNORECASE):
        label["Action_Required"] = "Yes"
    else:
        label["Action_Required"] = "No"

    # Determine priority level
    if re.search(r"urgent|important|asap|deadline|reminder", email, re.IGNORECASE):
        label["Priority_Level"] = "Urgent"
    elif re.search(r"high", email, re.IGNORECASE):
        label["Priority_Level"] = "High"
    elif re.search(r"medium", email, re.IGNORECASE):
        label["Priority_Level"] = "Medium"
    elif re.search(r"low", email, re.IGNORECASE):
        label["Priority_Level"] = "Low"

    return label


def test_emails(emails: list):
    """
    Test the labeling function against provided email-label pairs.
    """
    for i, email_data in enumerate(emails, 1):
        email_content = email_data["email"]
        expected_label = {k: v if v else "N/A" for k, v in email_data["expected_label"].items()}
        actual_label = analyze_email(email_content)

        print(f"Test Case {i}:")
        print(f"Email Content:\n{email_content}")
        print(f"Expected Label: {expected_label}")
        print(f"Actual Label:   {actual_label}")
        print(f"Pass:           {actual_label == expected_label}")
        print("-" * 50)


# Example email-label pairs
emails_to_test = [
    {
        "email": """\
From: BERT::FRANCES       7-FEB-1992 16:32:15.78
To: @SYS$MAIL:JUNK
Subj: THE FLOWERMAN

JUST A REMINDER THAT THE VALENTINE FLOWERS HAVE TO BE ORDERED BY 
TUESDAY FEB.11TH. PLEASE CONTACT FRANCES OR SHELLEY AT THE RECEPTIONIST
DESK IN THE MAIN LOBBY.

FRANCES

""",
        "expected_label": {
            "Spam": "No",
            "Subject": "THE FLOWERMAN",
            "Sender": "BERT::FRANCES",
            "send_date": "7-FEB-1992",
            "Time_Sensitive": "Yes",
            "Start": "N/A",
            "End": "N/A",
            "Type": "Reminder",
            "Category": "Leisure",
            "Format": "In-person",
            "Location": "Main Lobby",
            "Action_Required": "Yes",
            "Priority_Level": "Urgent"
        }
    },
    {
        "email": """\
From: PROMO::DEALS       15-MAR-2023 12:00:00.00
To: @SYS$MAIL:JUNK
Subj: AMAZING DISCOUNTS

LIMITED TIME OFFER! GET UP TO 70% OFF ON SELECTED ITEMS. ACT NOW!

PROMOTIONS TEAM

""",
        "expected_label": {
            "Spam": "Yes",
            "Subject": "AMAZING DISCOUNTS",
            "Sender": "PROMO::DEALS",
            "send_date": "15-MAR-2023",
            "Time_Sensitive": "Yes",
            "Start": "N/A",
            "End": "N/A",
            "Type": "N/A",
            "Category": "Leisure",
            "Format": "Online",
            "Location": "N/A",
            "Action_Required": "Yes",
            "Priority_Level": "Urgent"
        }
    }
]

# Run tests
test_emails(emails_to_test)
