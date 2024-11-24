import random
import json
from datetime import datetime, timedelta

# Updated sample email components
names = ["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Judy"]
locations = ["Room 101", "Zoom", "Google Meet", "Library", "Conference Hall", "Auditorium", "Room 202", "Cafe"]
subjects = {
    "Meeting Invitation": "Meeting with Project Team",
    "Assignment Deadline": "Assignment Due Reminder",
    "Appointment Confirmation": "Appointment Confirmation",
    "Fraud and Spam": "Congratulations, You've Won!"
}
messages = {
    "Meeting Invitation": "This is a reminder of our upcoming meeting on {date} at {time} at {location}. Please confirm your attendance.",
    "Assignment Deadline": "The deadline for your assignment is on {date} at {time}. Please ensure your work is submitted on time.",
    "Appointment Confirmation": "Your appointment is scheduled for {date} at {time} at {location}. Please arrive 15 minutes early.",
    "Fraud and Spam": "You've won a prize! To claim it, contact us by {date}."
}

# Generate a list of synthetic emails for a specific message type
def generate_emails(message_type, count=20):
    emails = []
    for _ in range(count):
        name = random.choice(names)
        location = random.choice(locations)
        date = datetime.now() + timedelta(days=random.randint(1, 30))
        time = f"{random.randint(9, 17)}:{random.choice(['00', '30'])}"
        subject = subjects[message_type]
        message = messages[message_type].format(date=date.strftime('%Y-%m-%d'), time=time, location=location)

        email = {
            "subject": subject,
            "name": name,
            "date": date.strftime('%Y-%m-%d'),
            "time": time,
            "location": location,
            "message": message
        }
        emails.append(email)
    return emails

# Generate 20 emails for each of the 4 message types
all_emails = {}
message_types = ["Meeting Invitation", "Assignment Deadline", "Appointment Confirmation", "Fraud and Spam"]
for message_type in message_types:
    all_emails[message_type] = generate_emails(message_type, count=20)

# Save the generated emails to a JSON file
with open("emails.json", "w") as json_file:
    json.dump(all_emails, json_file, indent=4)

