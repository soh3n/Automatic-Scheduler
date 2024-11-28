import re
import json
import os
import ast
import random
from datetime import datetime
# from openai import OpenAI
# from dotenv import load_dotenv
# from utils.labeling_utils import re_analyze_email, gpt_label, gpt_label_eg, gpt_label_ft
from utils.evaluation_utils import evaluate_label_single, calculate_overall_metrics

pred_label=  {
    "Spam": "No",
    "Subject": "Wells Gardner Displays",
    "Sender": "Rick",
    "send_date": "1992-02-04",
    "Time_Sensitive": "Yes",
    "Start": "1992-02-18 00:00",
    "End": "",
    "Type": "Reminder",
    "Category": "Work",
    "Format": "In-person",
    "Location": "Wells Gardner",
    "Action_Required": "Yes",
    "Priority_Level": "High"
}

true_label= {
    "Spam": "No",
    "Subject": "WELLS GARDNER DISPLAYS",
    "Sender": "BERT::MEYETTE",
    "send_date": "1992-02-04",
    "Time_Sensitive": "Yes",
    "Start": "1992-02-18 00:00",
    "End": "",
    "Type": "Reminder",
    "Category": "Work",
    "Format": "In-person",
    "Location": "Wells Gardner",
    "Action_Required": "Yes",
    "Priority_Level": "High"
}

if __name__ == "__main__":
    evaluate_label_single(pred_label, true_label)