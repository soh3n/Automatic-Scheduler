import json
from datetime import datetime

# Load labels from the external file
with open("labels.json", "r") as file:
    labels = json.load(file)

# Function to generate email content based on label data
def generate_email_content(label):
    # Basic subject based on category and event type
    subject = f"{label['Category']} - {label['Event Type']} Notification"
    # Email body template
    body = (
        f"Subject: {subject}\n"
        f"Date/Time: {label.get('Date / Time', 'N/A')}\n\n"
        f"Hello,\n\n"
        f"This is a {label['Priority Level']} priority {label['Event Type']} related to {label['Category']}. "
        f"It is scheduled to take place as a {label['Type']}.\n\n"
        f"{'Please take action as necessary.' if label['Action Required'] == 'Yes' else 'No immediate action required.'}\n\n"
        f"Best regards,\nAutomated Notification System\n"
    )
    return subject, body

# List to hold generated emails
emails = []

# Generate emails based on each label
for label in labels:
    subject, body = generate_email_content(label)
    email = {
        "subject": subject,
        "body": body,
        "spam": label["Spam"],
        "time_sensitive": label["Time Sensitive"],
        "date_time": label.get("Date / Time", None),
        "event_type": label["Event Type"],
        "category": label["Category"],
        "type": label["Type"],
        "action_required": label["Action Required"],
        "priority_level": label["Priority Level"]
    }
    emails.append(email)

# Write the emails list to a JSON file
with open("emails.json", "w") as f:
    json.dump(emails, f, indent=4)

print("Pseudo emails generated and saved to emails.json")
