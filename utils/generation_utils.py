import os
from openai import OpenAI
from dotenv import load_dotenv
import random
import json
from datetime import datetime, timedelta
from utils.gpt_utils import gpt_completion

# # Load the environment variables from the .env file
# # In this .env, it contains openai's API Key.
# load_dotenv()
# # Load the key to call the client.
# client = OpenAI()
# model_name="gpt-4o-mini"

# def get_completion(sys_prompt, prompt, temperature=0.7, model=model_name):
#     '''
#     prompt: 
#     model: 
#     '''
#     messages = [
#         {"role": "system", "content": sys_prompt},
#         {"role": "user", "content": prompt}
#         ]
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#     )
#     # 调用 OpenAI 的 ChatCompletion 接口
#     # return response.choices[0].message["content"]
#     return response.choices[0].message.content

def label_to_prompt(entry):
    email_info = f"""
    You will write this email about {entry['Category']} as {entry['Sender']}. \
    The subject of the email is: "{entry['Subject']}"; \
    Is this email time-sensitive? {entry['Time_Sensitive']}; \
    (Don't mention time-sensitivity explicitly); \
    The session will start at {entry['Start']} and end at {entry['End']}. \
    (If the timestamp is given, make sure to include the date and time in the email in a natural way.) \
    This is a {entry['Format']} item held in {entry['Location']}. \
    Do you expect any kind of action (like reply, submission or others)? {entry['Action_Required']}. \
    (Ensure the email requests the recipients to take action if required (e.g., reply, confirm attendance, or ask questions).) \
    The urgency of this email is {entry['Priority_Level']}.
    """
    return email_info

pseudo_label0 = {
    'Spam': 'No',
    'Subject': 'Briefint session changed to 9:30 this morning',
    'Sender': "Mia O'Connor",
    'send_date': '2024-11-11',
    'Time_Sensitive': 'Yes',
    'Start': '2024-11-11 09:30',
    'End': '2024-11-11 10:00',
    'Type': 'Event',
    'Category': 'Work',
    'Format': 'Online',
    'Location': 'Microsoft Teams',
    'Action_Required': 'Yes',
    'Priority_Level': 'Urgent'
 }
eg_email_prompt0 = label_to_prompt(pseudo_label0)
eg_email0 = f"""
From:	Mia O’Connor           2024-11-11
Subject: Briefing Session Changed to 9:30 This Morning

Dear Team,

Please be informed that the briefing session scheduled for today has been rescheduled. The session will now take place online via Microsoft Teams from 9:30 AM to 10:00 AM on Monday, November 11, 2024.
To ensure everything runs smoothly, kindly confirm your attendance or reach out if you have any questions or concerns about accessing the session.
Thank you for your prompt attention to this update.

Best regards,
Mia O’Connor
"""

pseudo_label1 = {
    'Spam': 'No',
    'Subject': 'Coffee Catch-Up with Hugo on November 16th!',
    'Sender': 'Hugo Dupont',
    'Time_Sensitive': 'Yes',
    'send_date': '2024-11-13',
    'Start': '2024-11-16 09:00',
    'End': '2024-11-16 10:45',
    'Type': 'Event',
    'Category': 'Leisure',
    'Format': 'In-person',
    'Location': 'Starbucks in Student Union',
    'Action_Required': 'No',
    'Priority_Level': 'Low'
 }

eg_email_prompt1 = label_to_prompt(pseudo_label1)
eg_email1 = f"""
From:	Hugo Dupont           2024-11-13
Subject: Coffee Catch-Up with Hugo on November 16th!

Hi,

I hope this message finds you well! I’d love to invite you to a coffee catch-up on Saturday, November 16, 2024, from 9:00 AM to 10:45 AM. We’ll meet in person at Starbucks in the Student Union
This is a relaxed and informal gathering—feel free to drop by and enjoy a chat over coffee. No RSVP is required; just bring your great vibes and let’s have a wonderful time!
Looking forward to seeing you there.

Warm regards,
Hugo Dupont
"""

true_label0 = {
    "Spam": "No",
    "Subject": "Walkabout Friday -- 1/10/92 -- 3:30-5:00",
    "Sender": "GAWD RAY",
    "send_date": "1992-01-06",
    "Time_Sensitive": "Yes",
    "Start": "1992-01-10 15:30",
    "End": "1992-01-10 17:00",
    "Type": "Event",
    "Category": "Work",
    "Format": "In-Person",
    "Location": "Alpha, Nu, Omega Labs",
    "Action_Required": "No",
    "Priority_Level": "Medium"
}
true_label_prompt0 = label_to_prompt(true_label0)
true_email0 = f"""
From:	GAWD::RAY           6-JAN-1992 09:20:55.68
Subj:	Walkabout Friday -- 1/10/92 -- 3:30-5:00

     Dennis Harper and the Moto Mania team will be hosting this week's 
Walkabout Friday. 
 
     The festivities will begin at 3:30 in the Alpha, Nu, and
Omega labs in Engineering. Please come by the labs, sample the
munchies, play the games, and give your feedback (positive and
negative).

                       Friday, Jan. 10, 1992
                        3:30 - 5:00 p.m.
                      Alpha, Nu, Omega Labs
"""

true_label1 = {
    "Spam": "No",
    "Subject": "New telephone system/New area code",
    "Sender": "KIM ESTRADA",
    "send_date": "1992-01-24",
    "Time_Sensitive": "Yes",
    "Start": "1992-01-27 00:00",
    "End": "1992-04-17 23:59",
    "Type": "Update",
    "Category": "Work",
    "Format": "Email",
    "Location": "N/A",
    "Action_Required": "Yes",
    "Priority_Level": "High"
}

true_label_prompt1 = label_to_prompt(true_label1)
true_email1= f"""
From:	KIM::ESTRADA      24-JAN-1992 09:14:09.80
Subj:	New telephone system/New area code.


The installation of the new telephone system has been delayed until 
04/17/92, due to additional preparations that need to be made before 
the system can be installed.

Effective January 27, 1992 calls dialed to the oakland/east bay area 
must include the 510 area code. Calls dialed without the 510 area code 
will not be complete, and callers will reach a recorded announcement 
with a reminder to dial  (510) before the 7 digit telephone number.
"""

def generate_prompt(label):
    email_prompt = label_to_prompt(label)
    system_prompt = f"""
    You are a professional email writer with expertise in crafting clear, concise,\
    and engaging emails for different purposes. You can write formal business emails, \
    friendly personal emails, academic based emails, and much more. \
    Your tone, structure, and content adapt based on the context and audience. \
    Be as nature as possible.
    """

    # task_prompt = f"""
    # Your task is to write an email based on a brief conclusion message. Here is an example: \
    # Email Conclusion: {eg_email_prompt0} \
    # Email: {eg_email0}; \
    # Email Conclusion: {eg_email_prompt1} \
    # Email: {eg_email1}
    # Email Conclusion: {true_label_prompt0} \
    # Email: {true_email0}; \
    # Email Conclusion: {true_label_prompt1} \
    # Email: {true_email1}
    # Email Conclusion: {email_prompt} \
    # Email: 
    # """
    task_prompt = f"""
    Your task is to write an email based on a brief conclusion message. Here is some examples: \
    Email Conclusion: {eg_email_prompt0} \
    Email: {eg_email0}; \
    Email Conclusion: {eg_email_prompt1} \
    Email: {eg_email1}
    Email Conclusion: {true_label_prompt0} \
    Email: {true_email0}; \
    Email Conclusion: {true_label_prompt1} \
    Email: {true_email1}
    Email Conclusion: {email_prompt} \
    Email: 
    """

    return system_prompt, task_prompt

# def label2email(label, client, temperature=0.7, model="gpt-4o-mini"):
#     '''
#     prompt: 
#     model: 
#     '''
#     sys_prompt, prompt = generate_prompt(label)
#     messages = [
#         {"role": "system", "content": sys_prompt},
#         {"role": "user", "content": prompt}
#         ]
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#     )
#     # 调用 OpenAI 的 ChatCompletion 接口
#     # return response.choices[0].message["content"]
#     return response.choices[0].message.content

def label2email(label, client, temperature=0.7, model="gpt-4o-mini"):
    '''
    prompt: 
    model: 
    '''
    sys_prompt, prompt = generate_prompt(label)
    return gpt_completion(client, sys_prompt, prompt, temperature, model)