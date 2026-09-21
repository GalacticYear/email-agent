import json
import os


def process_inbox():

    #Dynamically finding folder where .py script is saved and anchoring that path to inbox.json
    script_directory = os.path.dirname(os.path.abspath(__file__))
    inbox_file_path = os.path.join(script_directory, "inbox.json")

    with open(inbox_file_path, 'r', encoding='utf-8') as file:
        emails=json.load(file)

    print(f"Loaded {len(emails)} emails from inbox")

    noise_box=[]
    action_box=[]

    #Looping through emails to separate Workflow content and Agent content
    for email in emails:
        sender=email.get("from","").lower()
        subject=email.get("subject","").lower()

    #Checking for automated messages
    is_automated ="no-reply" in sender or "noreply" in sender

    #Check for newsletters or receipts
    noise_keywords=["storage full","receipt","invoice","weekly digest","newsletter","digest"]
    has_noise_subject=any(keyword in subject for keyword in noise_keywords)

    if is_automated or has_noise_subject:
      noise_box.append(email)
    else:
     action_box.append(email)

    print(f"Noise (Workflow Tier): {len(noise_box)} emails filtered locally.")
    print(f"Content (AI/Agent Tier): {len(action_box)} emails remaining.")

    if len(action_box) > 0:
        first_real = action_box[0]
        print("Next Up for Triage Evaluation:")
        print(f"From:    {first_real.get('from')}")
        print(f"Subject: {first_real.get('subject')}")
        print(f"Body:    {first_real.get('body')[:120]}...")

process_inbox()
