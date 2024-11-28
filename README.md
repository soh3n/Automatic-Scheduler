# Automatic-Scheduler
This is modified by Haoyuan. A dev branch.

## Background
In current era, information is exploding -- and to get useful info among all is tricky and 
challenging. Take email as an example: you receive tens, even hundreds of them per day; those 
includes promotions, appointments, casual catch-up with old friends, etc. While most of them are not
very important, and ignoring them will not effect your daily life; some, in the mean while, are very
time-sensitive -- a newly scheduled meeting, a change on your group seminar, an interview 
invitation, etc. How can you manage those information with an easier manner?

## Proposal Statement
By proposing this project, we aims at automatically catching important, and timely information;
after that, we can make them into a template-based schedule instance which can be easily (hopefully 
automatically) add to your calendar.

## Scope
What we hope to do can be sketched as:
- Identify the time-related information in emails
- Templating them into an unified form
- Categorizing them
- Is it a schedule (with a period of time); or a reminder (at one moment)

## Data
- From open dataset
  - Real Emails from: [MailEx](https://github.com/salokr/email-event-extraction?tab=readme-ov-file) (Not actually used) and [atari email archive](https://github.com/voberoi/atariemailarchive-data)
  - Spam Emails from: [Enron Spam Data](https://github.com/MWiechmann/enron_spam_data)
- Pseudo email with mannual labels
  1. anually write 30 labels First
  2. Prompt GPT to genrate emails

## Work Flow:
[./data/PAIRED_test.json]


"./data/PAIRED_test.json"
"./data/PAIRED_train.json"