import json
import os


def process_inbox():

    #Dynamically finding folder where .py script is saved and anchoring that path to inbox.json
    script_directory = os.path.dirname(os.path.abspath(__file__))
    inbox_file_path = os.path.join(script_directory, "inbox.json")

    with open(inbox_file_path, 'r', encoding='utf-8') as file:
        emails=json.load(file)

    print(f"Loaded {len(emails)} emails from inbox")

    final_dispositions={}

    count={"archive":0, "reply":0,"defer":0,"delegate":0,"escalate":0}

    rule_processed_count=0
    llm_required_count=0

    #Looping through emails to separate Workflow content and Agent content
    for email in emails:
        msg_id=email.get("id")
        sender=email.get("from","").lower()
        subject=email.get("subject","").lower()
        body=email.get("body","").lower()

        #ESCALATE-detection (Security risks)
        if "security" in subject or "unauthorized" in body or"password" in subject:
            final_dispositions[msg_id]={
                "disposition":"escalate",
                "reason":"Potential security risk or administrative account alert flagged for review",
                "requires_llm": True
            }
            count["escalate"]+=1
            llm_required_count+=1

        #ARCHIVE-detection (automated noise)
        elif ("no-reply" in sender or "noreply" in sender or "notifications" in sender or
              any(k in subject or k in body[:100] for k in ["storage full", "unread messages", "usage", "receipt",
                                                             "invoice", "digest", "newsletter", "shipped", "package",
                                                               "membership","bill","weekly summary","monthly summary",
                                                               "top 5"])):
            final_dispositions[msg_id]={
                "disposition":"archive",
                "reason":"Automated alerts",
                "requires_llm": False
            }
            count["archive"]+=1
            rule_processed_count+=1

        #DEFER-detection (time commitments, constraints, scheduling)
        elif any(k in subject or k in body for k in ["meeting", "deadline", "schedule", "calendar", "tomorrow", "staging"]):
            final_dispositions[msg_id] = {
                "disposition": "defer",
                "reason": "Time-sensitive operational dependency or coordination request held for context compilation.",
                "requires_llm": True
            }
            count["defer"] += 1
            llm_required_count += 1


        # DELEGATE-detection (external task handoff)
        elif any(k in body for k in ["forward to", "assign to", "cc'd", "handle this"]):
            final_dispositions[msg_id] = {
                "disposition": "delegate",
                "reason": "Operational request indicating handoff or division of labor constraints.",
                "requires_llm": True
            }
            count["delegate"] += 1
            llm_required_count += 1

        #REPLY-detection(direct interpersonal communication)
        else:
            final_dispositions[msg_id] = {
                "disposition": "reply",
                "reason": "Direct peer communication queued for standard context generation.",
                "requires_llm": True
            }
            count["reply"] += 1
            llm_required_count += 1


    print(" FIVE-TIER DISPOSITION METRICS:")
    for disp_type, ct in count.items():
        print(f"   • {disp_type.upper().ljust(10)} : {ct} messages")
    print(f" Total Accounted For    : {len(final_dispositions)} / {len(emails)}")
    print(f" Handled by Rules   : {rule_processed_count} messages")
    print(f" Pending LLM Engine  : {llm_required_count} messages")

    if len(final_dispositions) == len(emails):
        print(" Verification Check PASSED: 100% of messages have a unique disposition assigned")
    else:
        print(" Verification Check FAILED: Operational drop detected")

        #INSPECT TOP MESSAGES BY DISPOSITION
    print("\nDATA INSPECTION: TOP MESSAGES FOR REVIEW\n\n")
    
    # Grouping the actual email objects by their assigned disposition
    grouped_emails = {"escalate": [], "defer": [], "reply": [], "delegate": [], "archive": []}
    
    for email in emails:
        msg_id = email.get("id")
        disp_info = final_dispositions.get(msg_id, {})
        disp_name = disp_info.get("disposition")
        if disp_name in grouped_emails:
            grouped_emails[disp_name].append(email)
            
    # Print the top 5 (or fewer) messages for each category
    for disp_type, email_list in grouped_emails.items():
        print(f"\nCategory: {disp_type.upper()} ({len(email_list)} messages total)")
        print("-" * 50)
        
        if not email_list:
            print("   (No messages in this category)")
            continue
            
        # Slice to show up to the first 5 emails
        for index, email in enumerate(email_list[:5]):
            print(f"   [{index + 1}] ID: {email.get('id')} | From: {email.get('from')}")
            print(f"       Subject: {email.get('subject')}")



if __name__ == "__main__":

    process_inbox()

if __name__ == "__main__":

    process_inbox()
