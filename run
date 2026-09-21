import json
import os


def start_triage():

    #Dynamically finding folderwhere .py script is saved and anchoring that path to inbox.json
    script_directory = os.path.dirname(os.path.abspath(__file__))
    inbox_file_path = os.path.join(script_directory, "inbox.json")

    with open(inbox_file_path, 'r', encoding='utf-8') as file:
        emails=json.load(file)

    print(f"Loaded {len(emails)} emails from inbox")

    print("First 3 emails:\n\n")

    for index, email in enumerate(emails[:3]):
        print(f"\n[Email #{index + 1}]")
        print(f"From:    {email.get('from')}")
        print(f"Subject: {email.get('subject')}")
        print(f"Body:    {email.get('body')[:100]}...")

start_triage()